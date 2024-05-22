import os
import subprocess
import json

def install_google_chrome():
    # Download Google Chrome
    subprocess.run(['wget', 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'])
    
    # Install the downloaded package
    subprocess.run(['sudo', 'dpkg', '-i', 'google-chrome-stable_current_amd64.deb'])
    
    # Fix any dependency issues
    subprocess.run(['sudo', 'apt-get', 'install', '-f', '-y'])

def create_policy_directory():
    # Create the directory for Chrome policies if it doesn't exist
    policy_dir = '/etc/opt/chrome/policies/managed'
    os.makedirs(policy_dir, exist_ok=True)
    return policy_dir

def write_policy_file(policy_dir, extensions):
    # Define the policy JSON file path
    policy_file_path = os.path.join(policy_dir, 'managed_extensions_policy.json')
    
    # Create the policy content
    policy_content = {
        "ExtensionInstallForcelist": extensions
    }
    
    # Write the JSON policy content to the file
    with open(policy_file_path, 'w') as policy_file:
        json.dump(policy_content, policy_file, indent=4)
    
    return policy_file_path

def launch_chrome_with_profiles(profiles):
    # Launch Chrome with each specified profile
    for profile in profiles:
        subprocess.run(['google-chrome', f'--profile-directory={profile}'])

def main():
    # Define the extensions to be installed (extension_id;update_url)
    extensions = [
        "jinjaccalgkegednnccohejagnlnfdag;https://clients2.google.com/service/update2/crx",
        "aapbdbdomjkkjkaonfhkkikfgjllcleb;https://clients2.google.com/service/update2/crx",
        "dhmfcfohejndhhhdabdiopbnhhabjafm;https://clients2.google.com/service/update2/crx",
        "another_extension_id;https://clients2.google.com/service/update2/crx"
    ]
    
    # Define the profiles to launch Chrome with
    profiles = ["Profile 1", "Profile 2"]

    # Install Google Chrome
    install_google_chrome()
    
    # Create the policy directory
    policy_dir = create_policy_directory()
    
    # Write the policy file
    policy_file_path = write_policy_file(policy_dir, extensions)
    print(f'Policy file created at: {policy_file_path}')
    
    # Launch Chrome with specified profiles
    launch_chrome_with_profiles(profiles)
    
if __name__ == "__main__":
    main()
