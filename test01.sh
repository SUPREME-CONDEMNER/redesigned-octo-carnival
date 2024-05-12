#!/bin/bash

# Define the base directory for Chrome profiles
BASE_DIR="$HOME/chrome-profiles"

# Loop through each profile directory
for i in {1..5}; do
    PROFILE_DIR="$BASE_DIR/profile$i"

    # Install Violentmonkey extension
    curl -L -o "$PROFILE_DIR/violentmonkey.zip" "https://github.com/violentmonkey/violentmonkey/releases/latest/download/violentmonkey.zip"
    unzip -q "$PROFILE_DIR/violentmonkey.zip" -d "$PROFILE_DIR"
    google-chrome --user-data-dir="$PROFILE_DIR" --load-extension="$PROFILE_DIR/violentmonkey" &

    # Install userscripts using Violentmonkey API
    sleep 5  # Wait for Chrome to start
    cat <<EOF | google-chrome --user-data-dir="$PROFILE_DIR" --new-window --no-first-run --no-default-browser-check "https://violentmonkey.github.io/get-it/"
{
  "install_from_url": [
    "https://example.com/userscript1.user.js",
    "https://example.com/userscript2.user.js"
  ]
}
EOF
done
