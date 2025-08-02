from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import logging
import time
from bs4 import BeautifulSoup

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def create_driver():
    """Create configured Chrome WebDriver for Render"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Render-specific paths
    chrome_bin = "/opt/render/project/.render/chrome/opt/google/chrome/chrome"
    chromedriver_bin = "/opt/render/project/.render/drivers/chromedriver"
    
    if os.path.exists(chrome_bin):
        chrome_options.binary_location = chrome_bin
    
    service = Service(executable_path=chromedriver_bin)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)
    return driver

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main page with form for image extraction"""
    if request.method == 'POST':
        try:
            source = ""
            images = []
            error = None
            
            if request.form.get('url'):
                url = request.form['url']
                source = f"URL: {url}"
                driver = create_driver()
                try:
                    driver.get(url)
                    time.sleep(3)  # Wait for JS execution
                    
                    # Extract images with xhighres attributes
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    for i, img in enumerate(soup.find_all('img')):
                        if img.get('xhighres'):
                            images.append({
                                'index': i+1,
                                'url': img['xhighres']
                            })
                except Exception as e:
                    error = f"Error processing URL: {str(e)}"
                    logging.error(error)
                finally:
                    driver.quit()
            
            elif 'file' in request.files:
                file = request.files['file']
                if file.filename != '' and file.filename.endswith(('.html', '.htm')):
                    source = f"File: {file.filename}"
                    try:
                        soup = BeautifulSoup(file.read().decode('utf-8'), 'html.parser')
                        for i, img in enumerate(soup.find_all('img')):
                            if img.get('xhighres'):
                                images.append({
                                    'index': i+1,
                                    'url': img['xhighres']
                                })
                    except Exception as e:
                        error = f"Error processing file: {str(e)}"
                        logging.error(error)
                else:
                    error = "Invalid file format. Please upload an HTML file."
            
            return render_template('index.html', 
                                  source=source, 
                                  images=images, 
                                  count=len(images),
                                  error=error)
            
        except Exception as e:
            return render_template('index.html', 
                                  error=str(e))
    
    # GET request - show empty form
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))