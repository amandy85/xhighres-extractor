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
    """Create configured Chrome WebDriver"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-features=TranslateUI")
    chrome_options.add_argument("--disable-ipc-flooding-protection")
    chrome_options.add_argument("--remote-debugging-port=9222")
    
    try:
        # Use system ChromeDriver (installed in Docker)
        service = Service('/usr/local/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)
        logging.info("Chrome driver created successfully")
        return driver
    except Exception as e:
        logging.error(f"Failed to create Chrome driver: {str(e)}")
        raise

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
                
                try:
                    driver = create_driver()
                    logging.info(f"Processing URL: {url}")
                    
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
                    
                    logging.info(f"Found {len(images)} images with xhighres attribute")
                    
                except Exception as e:
                    error = f"Error processing URL: {str(e)}"
                    logging.error(error)
                finally:
                    try:
                        driver.quit()
                    except:
                        pass
            
            elif 'file' in request.files:
                file = request.files['file']
                if file.filename != '' and file.filename.endswith(('.html', '.htm')):
                    source = f"File: {file.filename}"
                    try:
                        content = file.read().decode('utf-8')
                        soup = BeautifulSoup(content, 'html.parser')
                        for i, img in enumerate(soup.find_all('img')):
                            if img.get('xhighres'):
                                images.append({
                                    'index': i+1,
                                    'url': img['xhighres']
                                })
                        
                        logging.info(f"Found {len(images)} images with xhighres attribute in uploaded file")
                        
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
            logging.error(f"Unexpected error: {str(e)}")
            return render_template('index.html', 
                                  error=f"Unexpected error: {str(e)}")
    
    # GET request - show empty form
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        # Quick Chrome test
        driver = create_driver()
        driver.quit()
        chrome_status = "working"
    except:
        chrome_status = "failed"
    
    return {
        'status': 'healthy', 
        'chrome_status': chrome_status,
        'chromedriver_path': '/usr/local/bin/chromedriver'
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))