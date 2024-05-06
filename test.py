import os
import platform
import subprocess
import sys
import shutil
import zipfile
from pathlib import Path

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

    # Install Tampermonkey extension
    install_tampermonkey(profile_dir)

    # Install userscript with Tampermonkey
    install_userscript(profile_dir)

if __name__ == "__main__":
    install_selenium_and_webdriver()






import os
import traceback
import requests
import random
import time

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import string

def random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def getUserAgents(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            user_agents = response.text.split('\n')
            return user_agents
        else:
            print("Could not fetch user agents. Using default user agent.")
            return []
    except requests.RequestException as e:
        print("Error fetching user agents:", e)
        return []

def createGmailAccount(driver, wait):
    try:
        driver.get("https://www.gmail.com")

        create_account_button = wait.until(EC.presence_of_element_located((By.XPATH, "//a[text()='Create account']")))
        create_account_button.click()

        time.sleep(5)

        first_name_text = random_string(8)
        last_name_text = random_string(10)
        username_text = random_string(10) + "12345"
        password_text = f"DARKness2006!!!!!{username_text}@gmail.com"  # Constant password with username

        first_name = wait.until(EC.element_to_be_clickable((By.ID, "firstName")))
        first_name.send_keys(first_name_text)

        last_name = driver.find_element(By.ID, "lastName")
        last_name.send_keys(last_name_text)

        username = driver.find_element(By.ID, "username")
        username.send_keys(username_text)

        password = driver.find_element(By.NAME, "Passwd")
        password.send_keys(password_text)

        confirm_password = driver.find_element(By.NAME, "ConfirmPasswd")
        confirm_password.send_keys(password_text)

        next_button = driver.find_element(By.XPATH, "//div[@id='accountDetailsNext']/div/button")
        next_button.click()

        wait.until(EC.presence_of_element_located((By.ID, "phoneNumberId")))

        return f"{username_text}@gmail.com"

    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()
        return None

def saveToTextFile(gmail_address, file_path):
    try:
        with open(file_path, "a") as file:
            file.write(f"{gmail_address}\n")
        return True
    except Exception as e:
        print("Error saving to file:", e)
        return False

def createMultipleAccounts(driver, wait, user_agents):
    gmail_count = 0
    file_number = 0
    max_gmails = 100
    gmails_per_file = 10
    max_files = max_gmails // gmails_per_file

    for user_agent in user_agents:
        options = Options()
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 50)

        for _ in range(max_gmails):
            gmail_address = createGmailAccount(driver, wait)
            if gmail_address:
                gmail_count += 1
                if gmail_count % gmails_per_file == 0:
                    file_number += 1
                if file_number > max_files:
                    break











                file_name = f"b-{str(file_number).zfill(2)}.txt"












                file_path = os.path.abspath(file_name)
                if not saveToTextFile(gmail_address, file_path):
                    print("Failed to save to file.")
                    break

def main():
    userAgentsUrl = "https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt"
    user_agents = getUserAgents(userAgentsUrl)

    if user_agents:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run browser in background
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 10)
        createMultipleAccounts(driver, wait, user_agents)
        driver.quit()
    else:
        print("No user agents fetched.")

if __name__ == "__main__":
    main()







import requests
import base64
import time

def authenticate_github(email, password):
    # Authenticate with GitHub using email and password
    try_count = 0
    while try_count < 3:  # Retry up to 3 times
        try:
            response = requests.post(
                "https://api.github.com/authorizations",
                auth=(email, password),
                json={"scopes": ["repo"], "note": "Script access"}
            )
            if response.status_code == 201:
                token = response.json()["token"]
                return token
            else:
                print("Failed to authenticate with GitHub. Retrying...")
        except requests.RequestException as e:
            print(f"Error during authentication: {e}. Retrying...")
        try_count += 1
        time.sleep(3)  # Wait for 3 seconds before retrying
    print("Failed to authenticate with GitHub after multiple attempts.")
    return None

def upload_file(token, repo_owner, repo_name, file_path, folder_name):
    # Upload a file to the repository
    try_count = 0
    while try_count < 3:  # Retry up to 3 times
        try:
            headers = {"Authorization": f"token {token}"}
            with open(file_path, "rb") as file:
                content = base64.b64encode(file.read()).decode()
            data = {
                "message": "Upload file",
                "content": content,
                "branch": "main"
            }
            response = requests.put(
                f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{folder_name}/{file_path.name}",
                headers=headers,
                json=data
            )
            if response.status_code == 201:
                print(f"File '{file_path.name}' uploaded successfully.")
                return True
            else:
                print(f"Failed to upload file '{file_path.name}'. Retrying...")
        except requests.RequestException as e:
            print(f"Error during file upload: {e}. Retrying...")
        try_count += 1
        time.sleep(3)  # Wait for 3 seconds before retrying
    print("Failed to upload file after multiple attempts.")
    return False




def main():
    # Your GitHub credentials
    email = "data-receiver@omail.edu.pl"
    password = "data-receiver@omail.edu.pl"

    # Authenticate with GitHub
    token = authenticate_github(email, password)
    if token:
        # Repository information
        repo_owner = "Data-Receiver"
        repo_name = "Data"
        folder_name = "Gmails"




        # Upload files to the existing folder
        for i in range(1, 11):
            file_path = f"b-{str(i).zfill(2)}.txt"  # Assuming file names follow the pattern b-01.txt, b-02.txt, ..., b-10.txt
            if not upload_file(token, repo_owner, repo_name, file_path, folder_name):
                print(f"Failed to upload file '{file_path}'. Exiting...")
                break
    else:
        print("Authentication failed. Please check your credentials.")

if __name__ == "__main__":
    main()
