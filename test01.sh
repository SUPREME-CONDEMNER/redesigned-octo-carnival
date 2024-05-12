#!/bin/bash

# Define the Chrome extension URL
extension_url="https://chrome.google.com/webstore/detail/violentmonkey/jinjaccalgkegednnccohejagnlnfdag"

# Loop through each user profile and install the extension
for i in {1..10}
do
    profile_path="/home/user$i/.config/google-chrome/Default/Extensions"
    profile_user="user$i"
    sudo -u $profile_user mkdir -p $profile_path
    sudo -u $profile_user wget -O /tmp/violentmonkey.zip $extension_url
    sudo -u $profile_user unzip /tmp/violentmonkey.zip -d $profile_path
    sudo -u $profile_user rm /tmp/violentmonkey.zip
    echo "Violentmonkey extension installed for user$i."
done
