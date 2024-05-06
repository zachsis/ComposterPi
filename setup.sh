#!/bin/bash

echo '[+] Updating system'
sudo apt-get update && sudo apt-get upgrade

echo '[+] Downloading Grafana Binaries'
wget https://dl.grafana.com/oss/release/grafana-10.4.2.linux-armv7.tar.gz

echo '[+] Uncompressing'
tar -xzvf grafana-10.4.2.linux-armv7.tar.gz 
mv grafana-v10.4.2/ /usr/local/bin/grafana

echo '[+] Downloading Prometheus Binaries'
wget https://github.com/prometheus/prometheus/releases/download/v2.52.0-rc.0/prometheus-2.52.0-rc.0.linux-armv7.tar.gz

echo '[+] Uncompressing'
tar -xzvf prometheus-2.52.0-rc.0.linux-armv7.tar.gz
mv prometheus-2.52.0-rc.0.linux-armv7 /usr/local/bin/prometheus

echo '[+] Copying prometheus configs'
cp -pv prometheus.yml /usr/local/bin/prometheus/prometheus.yml


echo '[+] creating virtual environment'

# Check if the venv folder exists
if [ ! -d "./venv" ]; then
    echo "Creating virtual environment..."
    # Run the command to create a virtual environment
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

source venv/bin/activate
pip install -r requirements.txt

sudo cp composter.service /etc/systemd/system/.
sudo cp prometheus.service /etc/systemd/system/.
sudo cp grafana.service /etc/systemd/system/.
sudo systemctl daemon-reload
sudo systemctl enable prometheus
sudo systemctl start prometheus
sudo systemctl enable grafana
sudo systemctl start grafana
sudo systemctl enable composter
sudo systemctl start composter

echo "[+] Prometheus is running on http://$(ip -o -4 addr show wlan0 | awk '{print $4}' | cut -d'/' -f1):9090"
echo "[+] Grafana Dashboard can be accessed at is running on http://$(ip -o -4 addr show wlan0 | awk '{print $4}' | cut -d'/' -f1):3000"
echo "[!] Initial Setup Complete. Please follow the remaining instructions in the README.md file to create your compost temperature dashboard"

