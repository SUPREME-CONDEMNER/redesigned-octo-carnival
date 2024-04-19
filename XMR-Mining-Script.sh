#!/bin/bash
MINER_NAME="KNIGHT"
WALLET_ADDRESS="49vjbP4YDANKk1WVYHqvJUfeBasMCpubaSC6FiQX6YxwCmP2FHkF3jgFdLhPCpMUy2fdoo5qGh3rn7DxnrNTRTdR8R84LYM"
POOL_ADDRESS="gulf.moneroocean.stream"
POOL_PORT="10128"

# Install dependencies (if not already installed)
sudo apt-get update
sudo apt-get install -y git build-essential cmake libuv1-dev libssl-dev libhwloc-dev

# Clone XMRig repository
git clone https://github.com/xmrig/xmrig.git

# Build XMRig
mkdir build
cd build
cmake ..
make -j$(nproc)

# Create config file
echo '{
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
  ]
}' > config.json

# Run XMRig
./xmrig
