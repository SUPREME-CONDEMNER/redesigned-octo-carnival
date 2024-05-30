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
        driver.get("https://accounts.google.com/signup")

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
