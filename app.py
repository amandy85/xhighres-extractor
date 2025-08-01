from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin
import time
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

def setup_selenium():
    """Configure and return a headless Chrome browser"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

def extract_urls(html_content, base_url=None):
    """Extract xhighres URLs from HTML, making relative URLs absolute"""
    soup = BeautifulSoup(html_content, 'html.parser')
    images = soup.find_all('img', attrs={'xhighres': True})
    
    urls = []
    for img in images:
        url = img['xhighres']
        if base_url and not url.startswith(('http://', 'https://')):
            url = urljoin(base_url, url)
        urls.append(url)
    
    return urls

@app.route('/', methods=['GET', 'POST'])
def index():
    images = []  # List of {'url': '', 'index': int}
    error = None
    source = None

    if request.method == 'POST':
        # URL Processing
        if 'url' in request.form and request.form['url'].strip():
            url = request.form['url'].strip()
            source = f"URL: {url}"
            
            try:
                driver = setup_selenium()
                driver.get(url)
                time.sleep(2)  # Allow JavaScript to execute
                
                html = driver.page_source
                urls = extract_urls(html, base_url=url)
                
                images = [{'url': u, 'index': i+1} for i, u in enumerate(urls)]
                driver.quit()
                
            except Exception as e:
                error = f"Failed to process URL: {str(e)}"
                if 'driver' in locals():
                    driver.quit()

        # File Processing
        elif 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                source = f"File: {file.filename}"
                
                try:
                    if not file.filename.lower().endswith(('.html', '.htm')):
                        raise ValueError("Only HTML files are accepted")
                    
                    html = file.read().decode('utf-8')
                    urls = extract_urls(html)
                    images = [{'url': u, 'index': i+1} for i, u in enumerate(urls)]
                    
                except Exception as e:
                    error = f"Failed to process file: {str(e)}"

    return render_template(
        'index.html',
        images=images,
        error=error,
        source=source,
        count=len(images)
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)