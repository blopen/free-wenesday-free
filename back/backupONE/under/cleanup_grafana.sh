# Check if Grafana is installed
if ! dpkg -s grafana &>/dev/null; then
  echo "Grafana is not installed. Installing..."
  # Install Grafana
  sudo apt-get install -y grafana
else
  echo "Grafana is already installed."
fi

# Check if the config directory exists
if [ ! -d "/usr/local/etc/grafana" ]; then
  echo "Creating config directory..."
  # Create the config directory
  sudo mkdir -p /usr/local/etc/grafana
else
  echo "Config directory already exists."
fi

# Check if the grafana.ini file exists
if [ ! -f "/usr/local/etc/grafana/grafana.ini" ]; then
  echo "Creating grafana.ini file..."
  # Create the grafana.ini file
  sudo touch /usr/local/etc/grafana/grafana.ini
else
  echo "grafana.ini file already exists."
fi

# Start the Grafana server
sudo grafana-server --config /usr/local/etc/grafana/grafana.ini

