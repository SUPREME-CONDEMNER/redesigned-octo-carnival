from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def install_tampermonkey_selenium(profile_dir):
    print("Installing Tampermonkey extension using Selenium...")
    tampermonkey_url = "https://chrome.google.com/webstore/detail/dhdgffkkebhmkfjojejmpbldmpobfkfo"

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument(f"--user-data-dir={profile_dir}")

    # Specify the correct path to ChromeDriver executable
    chrome_driver_path = "./chromedriver"

    # Start Chrome with Selenium
    chrome_service = Service(chrome_driver_path)
    chrome_service.start()
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    # Install Tampermonkey extension
    driver.get(tampermonkey_url)
    driver.find_element_by_id("detailsInstall").click()

    # Clean up
    driver.quit()
    chrome_service.stop()

if __name__ == "__main__":
    install_tampermonkey_selenium("/path/to/profile_dir")
