#!/bin/bash

# Define a list of packages to install
PACKAGES=("autotools-dev" "automake" "libtool" "libleptonica-dev" "zlib1g" "zlib1g-dev")


# Function to install JBIG2 encoder
install_jbig2enc() {
    echo "Installing JBIG2 encoder..."
    git clone https://github.com/agl/jbig2enc
    cd jbig2enc || exit
    ./autogen.sh
    ./configure && make
    sudo make install
    cd ..
    rm -rf jbig2enc  # Clean up intermediate files
    echo "JBIG2 encoder installed successfully."
}


# Update and upgrade the system
sudo apt-get update && sudo apt-get upgrade -y

# Variable to track installation status
INSTALL_FAILED=0

# Install packages
for pkg in "${PACKAGES[@]}"; do
    echo "Attempting to install $pkg..."
    if ! sudo apt-get install -y "$pkg"; then
        echo "Error: Failed to install $pkg. It may not be available or another error occurred." >&2
        INSTALL_FAILED=1
    fi
done

# Check if any installation failed
if [ $INSTALL_FAILED -eq 1 ]; then
    echo "One or more packages failed to install." >&2
else
    echo "All packages installed successfully."
fi


# Install JBIG2 encoder
install_jbig2enc


# Clean up
sudo apt-get autoremove -y
sudo apt-get autoclean -y

echo "System update and package installation process complete."
