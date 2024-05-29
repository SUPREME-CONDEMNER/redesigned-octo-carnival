import os
import subprocess
import sys
import urllib.request

def ensure_chrome_driver_installed():
    if not is_tool_installed("chromedriver"):
        subprocess.check_call([sys.executable, "-m", "pip", "install", "chromedriver-autoinstaller"])
        import chromedriver_autoinstaller
        chromedriver_autoinstaller.install()
        print("Chrome WebDriver installed.")
    else:
        print("Chrome WebDriver is already installed.")

def ensure_policy_directory_exists():
    policy_dir = "/etc/opt/chrome/policies/managed"
    if not os.path.exists(policy_dir):
        os.makedirs(policy_dir)
        print(f"Created directory {policy_dir}")
    else:
        print(f"Directory {policy_dir} already exists")

def ensure_policy_file_exists():
    policy_file_path = "/etc/opt/chrome/policies/managed/managed_extensions_policy.json"
    policy_content = {
        "ExtensionInstallForcelist": [
            "jinjaccalgkegednnccohejagnlnfdag;https://clients2.google.com/service/update2/crx"
        ]
    }
    import json
    if not os.path.isfile(policy_file_path):
        with open(policy_file_path, 'w') as policy_file:
            json.dump(policy_content, policy_file, indent=2)
        print(f"Created policy file {policy_file_path}")
    else:
        print(f"Policy file {policy_file_path} already exists")

def main():
    ensure_chrome_driver_installed()
    ensure_policy_directory_exists()
    ensure_policy_file_exists()

if __name__ == "__main__":
    main()
