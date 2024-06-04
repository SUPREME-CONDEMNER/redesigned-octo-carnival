import base64
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.proxy import Proxy, ProxyType

# Proxy details
proxy_ip = '38.154.227.167'
proxy_port = '5868'
proxy_username = 'irinbkag'
proxy_password = '59cpz5symen8'

# User Agent
user_agent = 'Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-G935FQ Build/MMB29M) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/53.0.2529.326 Mobile Safari/603.8'

# Proxy setup
proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = f'{proxy_ip}:{proxy_port}'
proxy.ssl_proxy = f'{proxy_ip}:{proxy_port}'

# Add proxy to capabilities
capabilities = DesiredCapabilities.CHROME.copy()
proxy.add_to_capabilities(capabilities)

# Chrome options setup
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

# Create a service object to manage the driver
service = Service(ChromeDriverManager().install())

# Initialize the Chrome WebDriver with options and capabilities
driver = webdriver.Chrome(service=service, options=chrome_options, desired_capabilities=capabilities)

# Set up basic auth for the proxy
driver.execute_cdp_cmd('Network.enable', {})
driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {
    'headers': {
        'Proxy-Authorization': 'Basic ' + base64.b64encode(f'{proxy_username}:{proxy_password}'.encode()).decode()
    }
})

# Navigate to a website to check the setup
driver.get('https://www.example.com')

# Close the browser when done
# driver.quit()
