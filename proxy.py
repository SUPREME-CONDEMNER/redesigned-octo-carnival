import requests
import socket
import socks

# Function to check if an HTTP proxy is accessible without authentication for all websites
def check_http_proxy(proxy, urls):
    try:
        proxies = {
            "http": f"http://{proxy}"
        }
        for url in urls:
            response = requests.get(url, proxies=proxies, timeout=5)
            if response.status_code != 200:
                return False
        return True
    except requests.exceptions.RequestException:
        return False

# Function to check if an HTTPS proxy is accessible without authentication for all websites
def check_https_proxy(proxy, urls):
    try:
        proxies = {
            "https": f"https://{proxy}"
        }
        for url in urls:
            response = requests.get(url, proxies=proxies, timeout=5)
            if response.status_code != 200:
                return False
        return True
    except requests.exceptions.RequestException:
        return False

# Function to check if a SOCKS5 proxy is accessible without authentication for all websites
def check_socks5_proxy(proxy, urls):
    try:
        ip, port = proxy.split(":")
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, int(port))
        socket.socket = socks.socksocket
        for url in urls:
            host, port = url.split(":")
            s = socket.socket()
            s.settimeout(5)
            s.connect((host, int(port)))
            s.sendall(b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
            response = s.recv(4096)
            if b"200 OK" not in response:
                return False
        return True
    except (socket.error, socks.ProxyError, socks.GeneralProxyError):
        return False

# URL of the text file containing proxies
proxies_url = "https://raw.githubusercontent.com/SUPREME-CONDEMNER/redesigned-octo-carnival/main/proxs-ru.txt"

# Fetch proxies from URL
response = requests.get(proxies_url)
if response.status_code == 200:
    proxies = response.text.splitlines()
else:
    print("Failed to fetch proxy list")
    proxies = []

# List of websites to check
websites_http = [
    "http://www.google.com",
    "http://accounts.google.com/signup"
]

websites_https = [
    "https://www.google.com",
    "https://accounts.google.com/signup"
]

# Prepare sets to ensure uniqueness
unique_proxies = set()
http_proxies = set()
https_proxies = set()
socks5_proxies = set()

# Check each proxy
for proxy in proxies:
    proxy = proxy.strip()
    if proxy in unique_proxies:
        continue
    unique_proxies.add(proxy)
    
    if proxy.startswith("http://"):
        proxy = proxy[len("http://"):]
        if check_http_proxy(proxy, websites_http):
            http_proxies.add(proxy)
    elif proxy.startswith("https://"):
        proxy = proxy[len("https://"):]
        if check_https_proxy(proxy, websites_https):
            https_proxies.add(proxy)
    else:
        # Assume SOCKS5 if not HTTP/HTTPS
        if check_socks5_proxy(proxy, websites_http):
            socks5_proxies.add(proxy)

# Write accessible proxies to respective files
with open("http.txt", "w") as file:
    for proxy in http_proxies:
        file.write(f"{proxy}\n")

with open("https.txt", "w") as file:
    for proxy in https_proxies:
        file.write(f"{proxy}\n")

with open("socks5.txt", "w") as file:
    for proxy in socks5_proxies:
        file.write(f"{proxy}\n")

print("Accessible proxies without authentication have been saved to http.txt, https.txt, and socks5.txt")
