# smooth-frames-web-ui

Web UI tool for smoothing videos using [RIFE ncnn Vulkan](https://github.com/nihui/rife-ncnn-vulkan).

## Usage

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

Finally, run the following command to launch Gradio's Web UI.

```
python launch.py
```

Access to `localhost:7860`.

![gradion web ui](./demo/gradio_webui_image.png)



## Special thanks

I came up with this program after learning about [RIFE ncnn Vulkan](https://github.com/nihui/rife-ncnn-vulkan).
