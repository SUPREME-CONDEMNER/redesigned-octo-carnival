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
echo -e "\e[93m               Installation Started               "
sleep 3

# Install Libraries
clear
echo -e "\e[93m               Importing Libraries                "
add-apt-repository -y ppa:jonathonf/gcc-7.1 > /dev/null 2>&1
apt-get update > /dev/null 2>&1
apt-get install -y libmicrohttpd-dev > /dev/null 2>&1

# Install XMRIG Binary
clear
echo -e "\e[93m             Installing XMRIG Binary              "
cd /tmp
wget --quiet https://github.com/xmrig/xmrig/releases/download/v6.12.1/xmrig-6.12.1-linux-x64.tar.gz
tar -xf xmrig-6.12.1-linux-x64.tar.gz
mv xmrig-6.12.1/xmrig /usr/local/bin/xmrig
chmod +x /usr/local/bin/xmrig

# Setting Up Config
clear
echo -e "\e[93m                Setting Up Config                 "
cd /etc
cat <<EOF > config.json
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
echo -e "\e[93m                 Starting Miner                   "
xmrig -c /etc/config.json
