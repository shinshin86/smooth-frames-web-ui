# smooth-frames-web-ui

Web UI tool for smoothing videos using [RIFE ncnn Vulkan](https://github.com/nihui/rife-ncnn-vulkan).

## Demo

### Input video

https://github.com/shinshin86/smooth-frames-web-ui/assets/8216064/69aee72c-bff7-434f-b462-71afe108b524

### Output video

https://github.com/shinshin86/smooth-frames-web-ui/assets/8216064/05a8abe9-8abe-46a3-b716-38d8e4a1d56b

## Setup

### Setup script (macOS)
You can run this shell script to perform all setups at once.  
This project uses [rye](https://github.com/mitsuhiko/rye) as the Python project management tool.  
Note that running the setup script will install rye on your machine!  
(Note that if it is already installed, the installation process will be skipped.)

**What is executed**

1. Install `rye`
2. Creating .env files
3. Download `RIFE ncnn Vulkan`
4. TODO: Not yet, See [Manual](#manual-windows-or-macos-or-linux) -> ~~Install `ffmpeg (supports OpenH264)`~~

```
bash setup-mac.sh
```

### Manual (Windows or macOS or Linux)

First you need to install [RIFE ncnn Vulkan](https://github.com/nihui/rife-ncnn-vulkan) in your environment.  
Release binaries for each OS are available in [GitHub releases](https://github.com/nihui/rife-ncnn-vulkan/releases), so please download them.

Next, put the path to RIFE ncnn Vulkan in your `.env` file.

Copy the `.env_sample` with the name `.env`.
Then specify the path.

```
cp .env_sample .env
```

Example setting `.env`:

```
RIFE_NCNN_VULKAN_PATH =./rife-ncnn-vulkan/rife-ncnn-vulkan
```

Then install the Python dependencies.  
This project uses [rye](https://github.com/mitsuhiko/rye).

```
rye sync
```

This program requires that `FFmpeg` be installed in the execution environment. In addition, `OpenH264` must be supported by FFmpeg in order to export in H.264.

Here is the installation command assuming macOS.

```
curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/shinshin86/setup-mac-ffmpeg-with-openh264-ciscobinary/main/setup-mac-openh264.sh | bash
```

## Usage

Run the following command to launch Gradio's Web UI.

```
python launch.py
```

Access to `localhost:7860`.

![gradion web ui](./demo/gradio_webui_image.png)

### About codecs

On the Web UI, previews can only be displayed in webm format (with the codecs currently available for selection).  
Therefore, the default is to export files in webm (VP9 codec).  
However, mp4 (MPEG4-V codec) has a smaller file size after conversion.  
You can change these codecs in the drop-down list.

## Google Colab

**Does not work as expected on Google Colab  
See this issue for details.**  
https://github.com/shinshin86/smooth-frames-web-ui/issues/1

To use on Google Colab, execute the following command

```
!apt-get install -y libvulkan-dev

!git clone https://github.com/shinshin86/smooth-frames-web-ui.git
%cd smooth-frames-web-ui

!wget https://github.com/nihui/rife-ncnn-vulkan/releases/download/20221029/rife-ncnn-vulkan-20221029-ubuntu.zip
!unzip rife-ncnn-vulkan-20221029-ubuntu

!echo "RIFE_NCNN_VULKAN_PATH =./rife-ncnn-vulkan-20221029-ubuntu/rife-ncnn-vulkan" > .env

!pip install gradio python-dotenv

!python launch.py --share
```

## Special thanks

I came up with this program after learning about [RIFE ncnn Vulkan](https://github.com/nihui/rife-ncnn-vulkan).
