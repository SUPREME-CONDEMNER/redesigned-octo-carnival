import os
import platform
import subprocess
import sys
import shutil
import zipfile
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def install_chrome():
    print("Installing Google Chrome...")
    if platform.system() == 'Linux':
        subprocess.check_call(["wget", "-q", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"])
        subprocess.check_call(["sudo", "dpkg", "-i", "google-chrome-stable_current_amd64.deb"])
        subprocess.check_call(["sudo", "apt-get", "-y", "update"])
        subprocess.check_call(["sudo", "apt-get", "-y", "install", "--fix-broken"])
    elif platform.system() == 'Darwin':  # macOS
        subprocess.check_call(["brew", "install", "google-chrome"])
    else:
        print("Unsupported operating system.")
        sys.exit(1)

def create_chrome_profile(profile_dir):
    print("Creating new Chrome profile...")
    os.makedirs(profile_dir, exist_ok=True)
    return profile_dir

def install_tampermonkey(profile_dir):
    print("Installing Tampermonkey extension...")
    tampermonkey_url = "https://chrome.google.com/webstore/detail/dhdgffkkebhmkfjojejmpbldmpobfkfo"  # Tampermonkey Chrome Web Store URL
    subprocess.check_call(["google-chrome", "--no-first-run", "--no-default-browser-check", "--user-data-dir=" + profile_dir, "--install-extension=" + tampermonkey_url])

def install_userscript(profile_dir):
    print("Installing userscript...")
    userscript_url = "https://gist.github.com/origamiofficial/2557dd47fb0aaf08e3c298a236bfa14d/raw/6673c45ca583410d8e7a4639b6fcd954aabf67da/Recaptcha%2520Solver%2520(Automatically%2520solves%2520Recaptcha%2520in%2520browser).user.js"
    userscript_path = os.path.join(profile_dir, "Extensions", "kebgndikjjkabgoccdakhmlahpbghcfp", "0.1.0_0", "user.js")
    subprocess.check_call(["curl", "-o", userscript_path, userscript_url])

def install_selenium_and_webdriver():
    # Install Chrome
    install_chrome()

    # Get the current directory
    current_dir = Path(__file__).parent.resolve()

    # Install Selenium using pip
    print("Installing Selenium...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "selenium"])

    # Download the latest ChromeDriver
    chromedriver_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    response = subprocess.check_output(["curl", "-s", chromedriver_url])
    latest_version = response.decode().strip()

    # Download ChromeDriver
    chromedriver_url = f"https://chromedriver.storage.googleapis.com/{latest_version}/chromedriver_linux64.zip"
    chromedriver_zip = current_dir / "chromedriver.zip"
    print("Downloading ChromeDriver...")
    subprocess.check_call(["curl", "-s", "-o", str(chromedriver_zip), chromedriver_url])

    # Unzip ChromeDriver
    print("Unzipping ChromeDriver...")
    with zipfile.ZipFile(chromedriver_zip, 'r') as zip_ref:
        zip_ref.extractall(str(current_dir))

    # Make ChromeDriver executable
    chromedriver_path = current_dir / "chromedriver"
    os.chmod(str(chromedriver_path), 0o755)

    # Clean up
    chromedriver_zip.unlink()

    print("ChromeDriver installation completed.")

    # Create a new Chrome profile
    profile_dir = create_chrome_profile(os.path.join(current_dir, "chrome_profile"))

    # Set Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # This line enables headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize Chrome WebDriver with headless mode
    driver = webdriver.Chrome(options=chrome_options)

    # Install Tampermonkey extension
    install_tampermonkey(profile_dir)

    # Install userscript with Tampermonkey
    install_userscript(profile_dir)

if __name__ == "__main__":
    install_selenium_and_webdriver()
