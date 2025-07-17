import os
import subprocess

# === paths === (please change these to your needed paths)
input_dir = r"C:\Users\User\OneDrive\Videos\Lyson"
output_dir = os.path.join(input_dir, "converted")
lut_path = r"C\\:/Users/User/OneDrive/Videos/Lyson/DJI_DLogM_to_REC709.cube"

# === Create output dir in the same directory as the videos ===
os.makedirs(output_dir, exist_ok=True)

# === convert4 all MP4-Files ===
for filename in os.listdir(input_dir):
    if filename.lower().endswith(".mp4"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f"converted_{filename}")

        if os.path.exists(output_path):
            print(f"⏭️  Skip already converted video: {filename}")
            continue

        print(f"🎬 Convert: {filename}")

        command = [
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-vf", f"lut3d={lut_path}",
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "slow",
            "-c:a", "copy",
            output_path
        ]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error while converting {filename}: {e}")

print("\n✅ All Videos were converted successfully!")
