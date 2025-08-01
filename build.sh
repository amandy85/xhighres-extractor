# Install Chrome first
sudo dpkg -i google-chrome-stable_current_amd64.deb || sudo apt-get install -fy

# Get installed Chrome version (output: "Google Chrome 138.0.7080.0")
CHROME_VERSION=$(google-chrome --version)

# Extract the major version number (e.g., 138)
CHROME_MAJOR=${CHROME_VERSION#* }  # Remove "Google Chrome"
CHROME_MAJOR=${CHROME_MAJOR%%.*}   # Take only first number

# Fetch matching ChromeDriver version
CHROMEDRIVER_VERSION=$(wget -qO- "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_MAJOR")
wget "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"