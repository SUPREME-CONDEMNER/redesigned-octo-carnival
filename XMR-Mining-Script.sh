#!/bin/bash

# Set variables
MINER_NAME="KNIGHT"
WALLET_ADDRESS="49vjbP4YDANKk1WVYHqvJUfeBasMCpubaSC6FiQX6YxwCmP2FHkF3jgFdLhPCpMUy2fdoo5qGh3rn7DxnrNTRTdR8R84LYM"
POOL_ADDRESS="gulf.moneroocean.stream"
POOL_PORT="10128"

# Update system packages
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y git build-essential cmake libuv1-dev libssl-dev libhwloc-dev

# Clone the Monero miner repository
git clone https://github.com/xmrig/xmrig.git

# Enter the xmrig directory
cd xmrig

# Build the miner
mkdir build && cd build
cmake ..
make -j$(nproc)

# Create the config file
cat << EOF > config.json
{
    "autosave": true,
    "donate-level": 0,
    "cpu": true,
    "opencl": false,
    "cuda": false,
    "pools": [
        {
            "url": "$POOL_ADDRESS:$POOL_PORT",
            "user": "$WALLET_ADDRESS.$MINER_NAME",
            "pass": "x",
            "keepalive": true,
            "nicehash": false
        }
    ],
    "print-time": 60,
    "http": {
        "enabled": false,
        "host": "127.0.0.1",
        "port": 0,
        "access-token": null,
        "restricted": true
    }
}
EOF

# Run the miner
./xmrig

# Ensure the script is executable
chmod +x start_mining.sh

# Start mining
./start_mining.sh
