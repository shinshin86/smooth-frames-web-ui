#!/bin/bash

# Setup rye
if ! command -v rye &> /dev/null; then
    # install rye: https://rye-up.com/
    curl -sSf https://rye-up.com/get | bash
else
    echo "'rye' command is already installed."
fi

# Setup .env file
if [ ! -f .env ]; then
    echo "RIFE_NCNN_VULKAN_PATH=./rife-ncnn-vulkan/rife-ncnn-vulkan" > .env
    echo ".env file has been created."
else
    echo ".env file already exists. No changes were made."
fi

# Setup rife-ncnn-vulkan
if [ ! -d rife-ncnn-vulkan ]; then
    curl -LO https://github.com/nihui/rife-ncnn-vulkan/releases/download/20221029/rife-ncnn-vulkan-20221029-macos.zip
    unzip rife-ncnn-vulkan-20221029-macos.zip
    xattr -c rife-ncnn-vulkan
    echo "rife-ncnn-vulkan has been downloaded, unzipped, and processed."
else
    echo "rife-ncnn-vulkan directory already exists."
fi

echo "setup script is complete"
echo "========================"
echo -e "Start web ui with this command: \033[36mpython launch.py\033[0m"