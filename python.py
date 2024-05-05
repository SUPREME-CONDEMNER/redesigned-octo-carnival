import os

def create_python_files():
    # Define constants
    constants = ['b', 'c', 'd']

    # Start with b
    current_constant_index = 0
    current_first_digit = 0
    current_second_digit = 0
    current_third_digit = 0

    # Loop until reaching d-10-10-10
    while current_constant_index < len(constants):
        # Generate file name
        if constants[current_constant_index] == 'b':
            file_name = f"{constants[current_constant_index]}-{str(current_first_digit).zfill(2)}.py"
        elif constants[current_constant_index] == 'c':
            file_name = f"{constants[current_constant_index]}-{str(current_first_digit).zfill(2)}-{str(current_second_digit).zfill(2)}.py"
        else:
            file_name = f"{constants[current_constant_index]}-{str(current_first_digit).zfill(2)}-{str(current_second_digit).zfill(2)}-{str(current_third_digit).zfill(2)}.py"

        # Create Python file
        with open(file_name, 'w') as file:
            # Write the Python code into the file
            file.write("""















import os
import platform
import subprocess
import sys
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
    subprocess.check_call(["unzip", "-o", str(chromedriver_zip), "-d", str(current_dir)])

    # Make ChromeDriver executable
    chromedriver_path = current_dir / "chromedriver"
    os.chmod(str(chromedriver_path), 0o755)

    # Clean up
    chromedriver_zip.unlink()

    print("ChromeDriver installation completed.")

if __name__ == "__main__":
    install_selenium_and_webdriver()






import os
import shutil
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def download_tampermonkey():
    subprocess.run(["wget", "https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo"])

def install_tampermonkey(profile_dir):
    extension_path = os.path.join(profile_dir, "Extensions")
    os.makedirs(extension_path, exist_ok=True)
    shutil.move("dhdgffkkebhmkfjojejmpbldmpobfkfo", extension_path)

def install_userscript(profile_dir):
    userscript_url = "https://gist.github.com/origamiofficial/2557dd47fb0aaf08e3c298a236bfa14d/raw/6673c45ca583410d8e7a4639b6fcd954aabf67da/Recaptcha%2520Solver%2520(Automatically%2520solves%2520Recaptcha%2520in%2520browser).user.js"
    with open("Recaptcha_Solver.user.js", "w") as file:
        subprocess.run(["wget", "-O", "-", userscript_url], stdout=file)
    userscript_path = os.path.join(profile_dir, "Extensions")
    shutil.move("Recaptcha_Solver.user.js", userscript_path)

def create_profiles(num_profiles):
    profiles = []
    for i in range(num_profiles):
        profile_dir = f"chrome_profile_{i+1}"
        os.makedirs(profile_dir, exist_ok=True)
        profiles.append(profile_dir)
    return profiles

def sign_in_gmail(driver, email, password):
    driver.get("https://www.gmail.com")
    driver.find_element_by_id("identifierId").send_keys(email)
    driver.find_element_by_id("identifierNext").click()
    time.sleep(2)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_id("passwordNext").click()
    time.sleep(5)  # Wait for login

def open_google_cloud_console(driver):
    driver.get("https://shell.cloud.google.com/")
    time.sleep(10)  # Wait for the page to load
    
    # Handle pop-up window
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#mat-checkbox-1 > label > span.mat-checkbox-inner-container"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#mat-dialog-0 > dialog-overlay > div.mat-dialog-actions.actions.overlay-actions.gmat-button > modal-action > button > span.mat-button-wrapper"))).click()
    except:
        pass
    









def run_scripts_in_cloud_console(profile_dir):
    script_url = "https://raw.githubusercontent.com/SUPREME-CONDEMNER/Test/main/Main/Scripts/"
    for i in range(1, 11):
        script_name = f"b-{str(i).zfill(2)}.py"
        subprocess.run(["wget", "-O", "-", f"{script_url}{script_name}", "|", "python3", "-"], cwd=profile_dir)








def main():
    download_tampermonkey()
    







    num_profiles = 10
    profiles = create_profiles(num_profiles)
    








    gmail_file_url = "https://raw.githubusercontent.com/SUPREME-CONDEMNER/Test/main/Main/Gmails/a.txt"
    with open("a.txt", "r") as file:
        gmail_accounts = file.read().splitlines()

    chrome_options = Options()
    for profile_dir in profiles:
        chrome_options.add_argument(f"--user-data-dir={os.path.abspath(profile_dir)}")
    
    for profile_dir in profiles:
        install_tampermonkey(profile_dir)
        install_userscript(profile_dir)
        driver = webdriver.Chrome(options=chrome_options)
        for gmail_account in gmail_accounts:
            username_text = gmail_account.split("@")[0]
            password_text = f"DARKness2006!!!!!{username_text}@gmail.com"
            sign_in_gmail(driver, gmail_account, password_text)
            open_google_cloud_console(driver)
            driver.close()

    # Close all profiles except the ones where Google Cloud Console is opened
    for profile_dir in profiles:
        if os.path.exists(os.path.join(profile_dir, "Preferences")):
            shutil.rmtree(profile_dir)

    # Run scripts in Google Cloud Console
    for profile_dir in profiles:
        run_scripts_in_cloud_console(profile_dir)

if __name__ == "__main__":
    main()
















""")
            # Adjust script_name based on file name
            if 'b' in file_name:
                script_prefix = 'c'
            elif 'c' in file_name:
                script_prefix = 'd'
            else:
                script_prefix = 'e'  # Default or handle other cases as needed
            
            # Write script_name with adjusted prefix
            script_name = f"{script_prefix}-{file_name.split('-')[1]}-{str(current_first_digit).zfill(2)}.py"
            file.write(f"script_name = '{script_name}'\n")

        # Increment digits
        if constants[current_constant_index] == 'd':
            current_third_digit += 1
            if current_third_digit > 10:
                current_third_digit = 1
                current_second_digit += 1
                if current_second_digit > 10:
                    current_second_digit = 1
                    current_first_digit += 1
                    if current_first_digit > 10:
                        current_first_digit = 1
                        current_constant_index += 1
        elif constants[current_constant_index] == 'c':
            current_second_digit += 1
            if current_second_digit > 10:
                current_second_digit = 1
                current_first_digit += 1
                if current_first_digit > 10:
                    current_first_digit = 1
                    current_constant_index += 1
        else:
            current_first_digit += 1
            if current_first_digit > 10:
                current_first_digit = 1
                current_constant_index += 1

# Run the function to create Python files
create_python_files()

