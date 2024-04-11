#!/bin/bash

# Fixed Data
ALGO="RANDOMXMONERO"
POOL_URL_AND_PORT="pool.supportxmr.com:3333"
WALLET_ADDRESS="49vjbP4YDANKk1WVYHqvJUfeBasMCpubaSC6FiQX6YxwCmP2FHkF3jgFdLhPCpMUy2fdoo5qGh3rn7DxnrNTRTdR8R84LYM"
WORKER_NAME="SupportXMR"
CPU_USAGE="100%"
THREAD_USAGE="all" # or "100%"
DONATION_LEVEL=0

# Installation Process
clear
echo -e "\e[93mInstallation Started\e[0m"
sleep 3

# Install Libraries
clear
echo -e "\e[93mImporting Libraries\e[0m"
sudo apt-get update > /dev/null 2>&1
sudo apt-get install -y libmicrohttpd-dev > /dev/null 2>&1

# Fetching Latest XMRig Version
clear
echo -e "\e[93mFetching Latest XMRig\e[0m"
latest_version=$(curl -s "https://api.github.com/repos/xmrig/xmrig/releases/latest" | grep -oP '"tag_name": "\K(.*)(?=")')
download_url="https://github.com/xmrig/xmrig/releases/download/${latest_version}/xmrig-${latest_version}-linux-x64.tar.gz"

# Install XMRIG Binary
clear
echo -e "\e[93mInstalling XMRIG Binary\e[0m"
sudo mkdir -p /usr/local/bin/xmrig
cd /usr/local/bin/xmrig || exit
sudo wget --quiet "$download_url"
sudo tar -xf "xmrig-${latest_version}-linux-x64.tar.gz" --strip-components=1
sudo chmod +x xmrig

# Setting Up Config
clear
echo -e "\e[93mSetting Up Config\e[0m"
cat <<EOF | sudo tee /etc/xmrig.conf > /dev/null
{
    "algo": "${ALGO}",
    "url": "${POOL_URL_AND_PORT}",
    "user": "${WALLET_ADDRESS}.${WORKER_NAME}",
    "cpu": "${CPU_USAGE}",
    "threads": "${THREAD_USAGE}",
    "donate-level": ${DONATION_LEVEL},
    "log-file": null,
    "print-time": 60,
    "cpu-priority": null,
    "background": true
}
EOF

# Starting Miner
clear
echo -e "\e[93mStarting Miner\e[0m"
sudo xmrig -c /etc/xmrig.conf
