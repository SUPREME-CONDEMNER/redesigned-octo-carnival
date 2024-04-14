#!/bin/bash

# Function to handle jump to labels
function goto {
    label=$1
    cd
    cmd=$(sed -n "/^:[[:blank:]][[:blank:]]*${label}/{:a;n;p;ba};" $0 | grep -v ':$')
    eval "$cmd"
    exit
}

# Download ngrok and make it executable
clear
rm -rf ngrok ngrok.zip ng.sh > /dev/null 2>&1
echo "======================="
echo "Downloading ngrok..."
echo "======================="
wget -O ngrok.tgz https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz > /dev/null 2>&1
tar -xvzf ngrok.tgz > /dev/null 2>&1
chmod +x ngrok

# Prompt user for Ngrok Authtoken
clear
echo "Go to: https://dashboard.ngrok.com/get-started/your-authtoken"
read -p "Paste Ngrok Authtoken: " CRP
./ngrok config add-authtoken $CRP 

# Choose Ngrok region
clear
echo "Repo: https://github.com/kmille36/Docker-Ubuntu-Desktop-NoMachine"
echo "======================="
echo "choose ngrok region (for better connection)."
echo "======================="
echo "us - United States (Ohio)"
echo "eu - Europe (Frankfurt)"
echo "ap - Asia/Pacific (Singapore)"
echo "au - Australia (Sydney)"
echo "sa - South America (Sao Paulo)"
echo "jp - Japan (Tokyo)"
echo "in - India (Mumbai)"
read -p "choose ngrok region: " CRP
./ngrok tcp --region $CRP 4000 &>/dev/null &
sleep 1

# Check Ngrok connection
if curl --silent --show-error http://127.0.0.1:4040/api/tunnels  > /dev/null 2>&1; then
    echo OK
else
    echo "Ngrok Error! Please try again!"
    sleep 1
    goto ngrok
fi

# Run Docker container for NoMachine
docker run --rm -d --network host --privileged --name nomachine-xfce4 -e PASSWORD=123456 -e USER=user --cap-add=SYS_PTRACE --shm-size=1g thuonghai2711/nomachine-ubuntu-desktop:windows10

# Display NoMachine information
clear
echo "NoMachine: https://www.nomachine.com/download"
echo Done! NoMachine Information:
echo IP Address:
curl --silent --show-error http://127.0.0.1:4040/api/tunnels | sed -nE 's/.*public_url":"tcp:..([^"]*).*/\1/p' 
echo User: user
echo Passwd: 123456
echo "VM can't connect? Restart Cloud Shell then Re-run script."

# Timer
seq 1 43200 | while read i; do
    echo -en "\r Running .     $i s /43200 s"
    sleep 0.1
    echo -en "\r Running ..    $i s /43200 s"
    sleep 0.1
    echo -en "\r Running ...   $i s /43200 s"
    sleep 0.1
    echo -en "\r Running ....  $i s /43200 s"
    sleep 0.1
    echo -en "\r Running ..... $i s /43200 s"
    sleep 0.1
    echo -en "\r Running     . $i s /43200 s"
    sleep 0.1
    echo -en "\r Running  .... $i s /43200 s"
    sleep 0.1
    echo -en "\r Running   ... $i s /43200 s"
    sleep 0.1
    echo -en "\r Running    .. $i s /43200 s"
    sleep 0.1
    echo -en "\r Running     . $i s /43200 s"
    sleep 0.1
done
