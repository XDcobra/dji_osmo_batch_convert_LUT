import os
import subprocess

def get_video_fps(path):
    """Extract FPS from a video file using ffprobe."""
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=r_frame_rate",
                "-of", "default=noprint_wrappers=1:nokey=1",
                path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        fps_str = result.stdout.strip()
        if '/' in fps_str:
            num, denom = map(int, fps_str.split('/'))
            return round(num / denom, 3) if denom != 0 else None
        else:
            return float(fps_str)
    except Exception as e:
        print(f"Error extracting FPS from {path}: {e}")
        return None

# === Paths (edit as needed) ===
input_dir = r"C:\Users\User\OneDrive\Videos\Lyson"
output_dir = os.path.join(input_dir, "converted")
lut_path = r"C\\:/Users/User/OneDrive/Videos/Lyson/DJI_DLogM_to_REC709.cube"

# === Create output folder if it doesn't exist ===
os.makedirs(output_dir, exist_ok=True)

# === Supported video file extensions ===
valid_extensions = (".mp4", ".mov", ".mkv", ".avi", ".mxf", ".webm")

# === Convert all supported video files in the input folder ===
for filename in os.listdir(input_dir):
    if filename.lower().endswith(valid_extensions):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        if os.path.exists(output_path):
            print(f"Skipping already converted video: {filename}")
            continue

        print(f"Converting: {filename}")

        # Automatically detect original FPS
        fps = get_video_fps(input_path)
        if fps is None:
            print(f"Could not determine FPS for {filename}, skipping.")
            continue

        print(f"Detected FPS: {fps}")

        # FFmpeg command to apply LUT and convert video with stable playback settings
        command = [
            "ffmpeg",
            "-y",
            "-fflags", "+genpts",
            "-i", input_path,
            "-vf", f"lut3d={lut_path}",
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

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while converting {filename}: {e}")

print("\nAll videos were converted successfully.")
