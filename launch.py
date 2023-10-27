import math
import subprocess
import os
import concurrent.futures
import shutil
import tempfile
import argparse
import cv2
from dotenv import load_dotenv
import gradio as gr
import ffmpeg
import time

FRAMES_FOLDER = "temp_frames"
OUTPUT_FRAMES_FOLDER = "temp_output_frames"

load_dotenv()
rife_ncnn_vulkan_path = os.getenv("RIFE_NCNN_VULKAN_PATH")

parser = argparse.ArgumentParser(description="Launch the smooth-frames-web-ui on Gradio Interface")
parser.add_argument("--share", action="store_true", help="Enable sharing the app")
args = parser.parse_args()

codec_mapping = {
    "OpenH264": "openh264",
    "VP9": "vp09"
}


def get_fps(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return fps


def smart_roundup(number, base=10):
    """If the first digit of number is non-zero, carry forward to base."""
    return number if number % base == 0 else math.ceil(number / base) * base


def interpolate_frames(prev_frame, next_frame, interp_factor):
    interpolated_frames = []
    for i in range(1, interp_factor):
        alpha = i / interp_factor
        beta = 1.0 - alpha
        interpolated_frame = cv2.addWeighted(prev_frame, beta, next_frame, alpha, 0)
        interpolated_frames.append(interpolated_frame)
    return interpolated_frames


def generate_intermediate_frame(img_path1, img_path2, output_path):
    cmd = [rife_ncnn_vulkan_path, "-0", img_path1, "-1", img_path2, "-o", output_path]
    subprocess.run(cmd)
    return output_path


def generate_intermediate_frames_with_dir(input_dir, output_path):
    cmd = [rife_ncnn_vulkan_path, "-v", "-i", input_dir, "-o", output_path]
    subprocess.run(cmd)
    return output_path


def extract_frames_from_video(video_path, output_folder, target_fps=60/2):
    orig_fps = smart_roundup(get_fps(video_path))
    interp_factor = math.ceil(target_fps / orig_fps)  # Rounding up to ensure >= target_fps

    cap = cv2.VideoCapture(video_path)
    frames = []
    count = 0
    ret, prev_frame = cap.read()
    if not ret:
        cap.release()
        return frames
    
    prev_frame_path = os.path.join(output_folder, f"frame_{count:07}.png")
    cv2.imwrite(prev_frame_path, prev_frame)
    frames.append(prev_frame_path)
    count += 1

    futures = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        while True:
            ret, next_frame = cap.read()
            if not ret:
                break

            if orig_fps < target_fps:
                for i in range(1, interp_factor):
                    count += 2
                    next_frame_path = os.path.join(output_folder, f"frame_{count+1:07}.png")
                    cv2.imwrite(next_frame_path, next_frame)
                    frames.append(next_frame_path)
            
                    output_frame_path = os.path.join(output_folder, f"frame_{count:07}.png")
                    

                    future = executor.submit(
                        generate_intermediate_frame,
                        prev_frame_path,
                        next_frame_path,
                        output_frame_path,
                    )
                    futures.append(future)

                    frames.append(output_frame_path)

                    prev_frame_path = next_frame_path  # Set the path of the current frame for the next iteration
                    next_frame_path = os.path.join(output_folder, f"frame_{count:07}.png")
            else:
                count += 1
                next_frame_path = os.path.join(output_folder, f"frame_{count:07}.png")
                cv2.imwrite(next_frame_path, next_frame)
                frames.append(next_frame_path)
                

    concurrent.futures.wait(futures)

    cap.release()
    return frames


def generate_video_from_images(image_dir, codec):
    if codec == "openh264":
        vcodec = 'libopenh264'
        output_video_name = "output.mp4"
        pix_fmt = 'yuv420p'
    elif codec == "vp09":
        vcodec = 'libvpx-vp9'
        output_video_name = "output.webm"
        pix_fmt = 'yuva420p'
    else:
        raise ValueError("Invalid codec specified")

    # Ensure the directory is valid
    if not os.path.exists(image_dir):
        raise ValueError("The image directory does not exist")

    image_pattern = os.path.join(image_dir, '%08d.png')

    # Obtain the dimensions of the first image
    probe = ffmpeg.probe(image_pattern % 1)
    video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
    width = int(video_info['width'])
    height = int(video_info['height'])

    try:
        (
            ffmpeg
            .input(image_pattern, framerate=60)
            .output(output_video_name, vcodec=vcodec, pix_fmt=pix_fmt, s=f'{width}x{height}', video_bitrate='5000k')
            .global_args("-y")
            .run()
        )
    except ffmpeg._run.Error as e:
        print(f'ffmpeg stderr:\n{e.stderr.decode()}')
        raise e

    return output_video_name


def is_valid_frame_filename(filename):
    if not filename.endswith('.png'):
        return False
        
    return True


def interpolate_and_create_video(video_path, codec):
    extract_frames_from_video(video_path, FRAMES_FOLDER)

    generate_intermediate_frames_with_dir(FRAMES_FOLDER, OUTPUT_FRAMES_FOLDER)

    return generate_video_from_images(OUTPUT_FRAMES_FOLDER, codec)


def delete_all_files_in_dir(dir_path):
    if not os.path.exists(dir_path):
        print(f"The path {dir_path} does not exist.")
        return
    
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except OSError as e:
                print(f"Error: {file_path} : {e.strerror}")


def process_video(input_video, codec_choice, output_video):
    start_time = time.time()

    if not os.path.exists(rife_ncnn_vulkan_path):
        raise FileNotFoundError(f"RIFE ncnn Vulkan at path {rife_ncnn_vulkan_path} does not exist. Check your configuration.")

    if not os.path.exists(FRAMES_FOLDER):
        os.makedirs(FRAMES_FOLDER)
    if not os.path.exists(OUTPUT_FRAMES_FOLDER):
        os.makedirs(OUTPUT_FRAMES_FOLDER)

    codec = codec_mapping.get(codec_choice, "vp9")

    temp_dir = tempfile.mkdtemp()
    _, file_extension = os.path.splitext(input_video.name)
    temp_file_path = os.path.join(temp_dir, "input_video" + file_extension)
    shutil.copy2(input_video.name, temp_file_path)
    
    output_video = interpolate_and_create_video(temp_file_path, codec)

    # clean
    delete_all_files_in_dir('temp_frames')
    delete_all_files_in_dir('temp_output_frames')
    shutil.rmtree(temp_dir)

    end_time = time.time()
    print(f"Execution time: {end_time - start_time} second")
    return output_video


# gradio
input_video = gr.File(label="Upload a video")
output_video = gr.Video(label="Processed video")
codec_choice = gr.Dropdown(choices=["OpenH264", "VP9"], value="OpenH264", label="Select a Codec")
gr.Interface(fn=process_video, inputs=[input_video, codec_choice], outputs=output_video).launch(share=args.share)