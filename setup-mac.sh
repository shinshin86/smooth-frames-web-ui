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

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null
then
    echo "ffmpeg is not installed. Please install ffmpeg (supports OpenH264)."
    echo "==================================================================="
    echo "curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/shinshin86/setup-mac-ffmpeg-with-openh264-ciscobinary/main/setup-mac-openh264.sh | bash"
    exit 1
fi

# Check if ffmpeg supports OpenH264
if ffmpeg -codecs 2>&1 | grep -q "openh264"
then
    echo "ffmpeg supports OpenH264."
else
    echo "ffmpeg does not support OpenH264."
    echo "First uninstall FFmpeg, then please run the specific command to configure ffmpeg to support OpenH264."
    echo "====================================================================================================="
    echo "curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/shinshin86/setup-mac-ffmpeg-with-openh264-ciscobinary/main/setup-mac-openh264.sh | bash"
    exit 1
fi

echo "setup script is complete"
echo "========================"
echo -e "Start web ui with this command: \033[36mpython launch.py\033[0m"