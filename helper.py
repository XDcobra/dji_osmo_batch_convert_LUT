import os
import subprocess
import json
import urllib.request

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_ffmpeg(input_path, output_path, lut_path):
    fps = get_video_fps(input_path)
    lut_ffmpeg_path = to_ffmpeg_lut_path(lut_path)

    command = [
            "ffmpeg",
            "-y",
            "-fflags", "+genpts",
            "-i", input_path,
            "-vf", f"lut3d={lut_ffmpeg_path}",
            "-r", str(fps),
            "-vsync", "cfr",
            "-c:v", "libx264",
            "-crf", "20",
            "-preset", "medium",
            "-pix_fmt", "yuv420p",
            "-profile:v", "high",
            "-level", "4.1",
            "-c:a", "copy",
            output_path
        ]

    subprocess.run(command, check=True)

def to_ffmpeg_lut_path(path):
    drive, rest = os.path.splitdrive(path)
    ffmpeg_path = drive.replace(':', '\\\\:') + rest.replace('\\', '/')
    return ffmpeg_path

def download_dji_lut_if_needed():
    lut_filename = "DJI_DLogM_to_Rec709.cube"
    lut_path = os.path.join(os.getcwd(), lut_filename)

    if os.path.isfile(lut_path):
        print(f"LUT already exists at: {lut_path}")
    else:
        print("LUT not found, downloading...")
        lut_url = "https://www-dl.djicdn.com/5e45168b46b342d5b88f72c458ba6e79/OP3%20LUT%E6%96%87%E4%BB%B6%E7%89%B9%E6%AE%8A%E5%A4%84%E7%90%86/DJI%20OSMO%20Pocket%203%20D-Log%20M%20to%20Rec.709%20V1.cube"
        try:
            urllib.request.urlretrieve(lut_url, lut_path)
            print(f"LUT successfully downloaded to: {lut_path}")
        except Exception as e:
            print(f"Error downloading LUT: {e}")
            return None

    return lut_path

def get_video_fps(video_path):
    """Uses ffprobe to get the original video's frame rate"""
    try:
        result = subprocess.run([
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=r_frame_rate",
            "-of", "json",
            video_path
        ], capture_output=True, text=True, check=True)

        data = json.loads(result.stdout)
        fps_str = data["streams"][0]["r_frame_rate"]
        num, den = map(int, fps_str.split('/'))
        return round(num / den, 2)

    except Exception as e:
        print(f"Warning: Unable to detect FPS, defaulting to 30. Error: {e}")
        return 30.0
    
