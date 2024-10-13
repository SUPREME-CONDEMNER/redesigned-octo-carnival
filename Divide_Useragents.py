import requests

# URL of the text file containing user agents
url = "https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt"

# Fetch the content from the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    user_agents = response.text.splitlines()  # Split the content into lines
else:
    print("Failed to retrieve the file")
    exit()

# Total number of user agents
total_user_agents = len(user_agents)

# Number of files to create
num_files = 10

# Number of user agents per file
agents_per_file = total_user_agents // num_files

# Create 10 files and write 100 user agents in each
for i in range(num_files):
    start = i * agents_per_file
    end = start + agents_per_file
    file_name = f'user_agents_part_{i+1}.txt'
    
    with open(file_name, 'w') as f:
        f.write('\n'.join(user_agents[start:end]))

print("User agents have been split into 10 files.")
