from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import logging
import time
from bs4 import BeautifulSoup

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def create_driver():
    """Create configured Chrome WebDriver"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # For Render deployment
    if os.path.exists("/app/chrome/opt/google/chrome/google-chrome"):
        chrome_options.binary_location = "/app/chrome/opt/google/chrome/google-chrome"
    
    service = Service(ChromeDriverManager().install())
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
            
            # Process URL input
            if request.form.get('url'):
                url = request.form['url']
                source = f"URL: {url}"
                driver = create_driver()
                try:
                    driver.get(url)
                    time.sleep(3)  # Wait for JS execution
                    
                    # Extract images with BeautifulSoup
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    img_tags = soup.find_all('img')
                    
                    # Filter images with xhighres attributes
                    for i, img in enumerate(img_tags):
                        if img.get('xhighres'):
                            images.append({
                                'index': i+1,
                                'url': img['xhighres']
                            })
                        elif img.get('src'):
                            images.append({
                                'index': i+1,
                                'url': img['src']
                            })
                except Exception as e:
                    error = f"Error processing URL: {str(e)}"
                    logging.error(error)
                finally:
                    if driver:
                        driver.quit()
            
            # Process file upload
            elif 'file' in request.files:
                file = request.files['file']
                if file.filename != '' and file.filename.endswith(('.html', '.htm')):
                    source = f"File: {file.filename}"
                    try:
                        soup = BeautifulSoup(file.read().decode('utf-8'), 'html.parser')
                        img_tags = soup.find_all('img')
                        
                        # Extract images with xhighres attributes
                        for i, img in enumerate(img_tags):
                            if img.get('xhighres'):
                                images.append({
                                    'index': i+1,
                                    'url': img['xhighres']
                                })
                            elif img.get('src'):
                                images.append({
                                    'index': i+1,
                                    'url': img['src']
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