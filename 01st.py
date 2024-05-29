import os
import subprocess
import json

def run_command(command):
    """Run a shell command."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception(f"Command failed with error: {stderr.decode().strip()}")
    return stdout.decode().strip()

# 1. Download and install Google Chrome
print("Downloading and installing Google Chrome...")
run_command("wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/google-chrome-stable_current_amd64.deb")
run_command("sudo dpkg -i /tmp/google-chrome-stable_current_amd64.deb || sudo apt-get -f install -y")

# 2. Install Selenium and Chrome WebDriver
print("Installing Selenium and Chrome WebDriver...")
run_command("pip install selenium")
run_command("sudo apt-get install -y chromium-chromedriver")

# 3. Create the Chrome policies directory
policy_dir = "/etc/opt/chrome/policies/managed"
print(f"Creating directory {policy_dir}...")
run_command(f"sudo mkdir -p {policy_dir}")

# 4. Create managed_policies.json file
policy_file_path = os.path.join(policy_dir, "managed_policies.json")
policy_content = {
    "PrivacySandboxSettingsEnabled": False,
    "ExtensionInstallForcelist": [
        "jinjaccalgkegednnccohejagnlnfdag;https://clients2.google.com/service/update2/crx"
    ]
}
print(f"Creating policy file at {policy_file_path} with content:\n{json.dumps(policy_content, indent=4)}")
with open("/tmp/managed_policies.json", 'w') as policy_file:
    json.dump(policy_content, policy_file, indent=4)

# Move the policy file to the correct location with appropriate permissions
run_command(f"sudo mv /tmp/managed_policies.json {policy_file_path}")
run_command(f"sudo chmod 644 {policy_file_path}")

print("Setup completed successfully.")
