import subprocess
import time
import os

# Function to download and extract xmrig if not already done
def setup_xmrig():
    if not os.path.exists("xmrig-6.12.2-linux-x64.tar.gz"):
        subprocess.run("wget https://github.com/xmrig/xmrig/releases/download/v6.12.2/xmrig-6.12.2-linux-x64.tar.gz", shell=True)
    if not os.path.exists("xmrig-6.12.2"):
        subprocess.run("tar -zxvf xmrig-6.12.2-linux-x64.tar.gz", shell=True)

# Function to start mining
def start_mining():
    command = "./xmrig-6.12.2/xmrig -o rx.unmineable.com:3333 -a rx -k -t 2 -u DOGE:DFwWFuKENgq3pd3zrnzafTMXcWLLmERZ6x"
    subprocess.Popen(command, shell=True)

# Function to monitor mining
def monitor_mining():
    while True:
        process = subprocess.Popen("pgrep xmrig", shell=True, stdout=subprocess.PIPE)
        output, _ = process.communicate()
        if output:
            print("Mining is running.")
        else:
            print("Mining stopped. Restarting...")
            start_mining()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    setup_xmrig()
    start_mining()
    monitor_mining()
