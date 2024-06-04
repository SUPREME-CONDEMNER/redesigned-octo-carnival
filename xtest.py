import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Proxy details
proxy_ip = '38.154.227.167'
proxy_port = '5868'
proxy_username = 'irinbkag'
proxy_password = '59cpz5symen8'

# User Agent
user_agent = 'Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-G935FQ Build/MMB29M) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/53.0.2529.326 Mobile Safari/603.8'

# Chrome options setup
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

# Proxy setup
chrome_options.add_argument(f'--proxy-server={proxy_ip}:{proxy_port}')
chrome_options.add_argument(f'--proxy-auth={proxy_username}:{proxy_password}')

# Create a service object to manage the driver
service = Service(ChromeDriverManager().install())

# Initialize the Chrome WebDriver with options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to a website to check the setup
driver.get('https://accounts.google.com//signup')

# Close the browser when done
