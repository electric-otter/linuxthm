sudo -i

# Go to Downloads directory
cd ~/Downloads

# Create a virtual environment named 'linuxthm'
sudo python3 -m venv linuxthm

# Activate the virtual environment
sudo source linuxthm/bin/activate

# (Assuming you've extracted a folder named linuxthm-main already)
cd linuxthm-main

# Display a message
echo "Installing LinuxTHeMe"

# Install dearpygui in the virtual environment
pip install dearpygui
