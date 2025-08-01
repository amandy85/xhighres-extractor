from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def create_driver():
    # Automatic driver management
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    
    # Recommended Render-compatible options
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    return webdriver.Chrome(service=service, options=options)

# Usage example
driver = create_driver()