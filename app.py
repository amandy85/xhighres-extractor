from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
import logging
from werkzeug.middleware.proxy_fix import ProxyFix

# Initialize Flask app
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_driver():
    """Create and configure Chrome WebDriver"""
    try:
        # Configure Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Set binary location if in production
        if os.path.exists("/app/chrome/opt/google/chrome/google-chrome"):
            chrome_options.binary_location = "/app/chrome/opt/google/chrome/google-chrome"
        
        # Initialize service and driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Configure timeouts
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)
        
        return driver
    except Exception as e:
        logger.error(f"Driver creation failed: {str(e)}")
        raise

@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "xhighres-extractor",
        "version": "1.0.0"
    })

@app.route('/extract', methods=['POST'])
def extract_content():
    """Main extraction endpoint"""
    try:
        # Validate input
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({"error": "Missing URL parameter"}), 400
        
        # Process request
        driver = create_driver()
        try:
            driver.get(data['url'])
            
            # Example extraction logic - customize for your needs
            title = driver.title
            images = [img.get_attribute('src') for img in driver.find_elements(By.TAG_NAME, 'img')]
            
            return jsonify({
                "status": "success",
                "url": data['url'],
                "title": title,
                "image_count": len(images),
                "images": images[:5]  # Return first 5 images as example
            })
        finally:
            driver.quit()
    except Exception as e:
        logger.error(f"Extraction failed: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))