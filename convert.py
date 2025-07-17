import os
import subprocess
import urllib.request
from pathlib import Path

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    while True:
        clear_console()
        print("Video Conversion Tool")
        print("========================")
        print("1) Convert DJI Osmo Pocket 3 D-Log-M to Rec.709")
        print("2) Batch Convert DJI Osmo Pocket 3 D-Log-M to Rec.709")
        print("3) Convert General Video")
        print("4) Batch Convert General Videos")
        print("0) Exit")
        print("========================")

        choice = input("Select an option (0–4): ").strip()

        if choice == "1":
            convert_dji_single()
        elif choice == "2":
            convert_dji_batch()
        elif choice == "3":
            convert_general_single()
        elif choice == "4":
            convert_general_batch()
        elif choice == "0":
            print("Exiting program...")
            break
        else:
            print("Invalid input. Please try again.")
            input("Press Enter to continue...")

# === Functions ===
def convert_dji_single():
    print("\n[Convert DJI D-Log-M video to Rec.709]")

    # Step 1: Ensure LUT exists
    lut_local_path = download_dji_lut_if_needed()
    if lut_local_path is None:
        input("Press Enter to return to the menu...")
        return

    # Step 2: Ask for input file
    input_path = input("\nEnter full path to the DJI D-Log-M video: ").strip().strip('"')
    if not os.path.isfile(input_path):
        print("Error: Video file not found.")
        input("Press Enter to return to the menu...")
        return

    original_filename = os.path.basename(input_path)
    input_dir = os.path.dirname(input_path)

    # Step 3: Output options
    print("\nWhere should the converted file be saved?")
    print("1) In the same folder as the original file (prefix: converted_)")
    print("2) In a subfolder named 'converted' in the original folder")
    print("3) Specify a custom output folder")
    choice = input("Choose 1, 2 or 3: ").strip()

    if choice == "1":
        output_path = os.path.join(input_dir, f"converted_{original_filename}")
    elif choice == "2":
        output_dir = os.path.join(input_dir, "converted")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, original_filename)
    elif choice == "3":
        output_dir = input("Enter full output folder path: ").strip().strip('"')
        if not os.path.isdir(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                print(f"Error creating output folder: {e}")
                input("Press Enter to return to the menu...")
                return
        output_path = os.path.join(output_dir, original_filename)
    else:
        print("Invalid selection.")
        input("Press Enter to return to the menu...")
        return

    # Step 4: Convert
    lut_ffmpeg_path = to_ffmpeg_lut_path(lut_local_path)
    print("\nStarting FFmpeg conversion...")

    command = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-vf", f"lut3d={lut_ffmpeg_path}",
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "slow",
        "-c:a", "copy",
        output_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"\nConversion successful. Output saved to: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"\nFFmpeg returned an error: {e}")

    input("\nPress Enter to return to the menu...")


def convert_dji_batch():
    print("\n[Batch convert DJI D-Log-M videos to Rec.709]")

    # Step 1: Download DJI LUT
    lut_local_path = download_dji_lut_if_needed()
    if lut_local_path is None:
        input("Press Enter to return to the menu...")
        return

    # Step 2: Ask for input folder
    input_dir = input("\nEnter path to folder containing DJI D-Log-M videos: ").strip().strip('"')
    if not os.path.isdir(input_dir):
        print("Error: Folder not found.")
        input("Press Enter to return to the menu...")
        return

    # Step 3: Choose output mode
    print("\nWhere should the converted files be saved?")
    print("1) In the original folder, with prefix 'converted_'")
    print("2) In a subfolder named 'converted' inside the original folder")
    print("3) Specify a custom output folder")
    choice = input("Choose 1, 2 or 3: ").strip()

    if choice == "1":
        output_dir = input_dir
    elif choice == "2":
        output_dir = os.path.join(input_dir, "converted")
        os.makedirs(output_dir, exist_ok=True)
    elif choice == "3":
        output_dir = input("Enter full path to output folder: ").strip().strip('"')
        if not os.path.isdir(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                print(f"Error creating output folder: {e}")
                input("Press Enter to return to the menu...")
                return
    else:
        print("Invalid selection.")
        input("Press Enter to return to the menu...")
        return

    # Step 4: Find and convert videos
    lut_ffmpeg_path = to_ffmpeg_lut_path(lut_local_path)
    video_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".mp4")]

    if not video_files:
        print("No .mp4 files found in the folder.")
        input("Press Enter to return to the menu...")
        return

    print(f"\nFound {len(video_files)} video(s). Starting batch conversion...\n")

    for filename in video_files:
        input_path = os.path.join(input_dir, filename)

        if choice == "1":
            output_path = os.path.join(output_dir, f"converted_{filename}")
        else:
            output_path = os.path.join(output_dir, filename)

        if os.path.exists(output_path):
            print(f"Skipping (already exists): {filename}")
            continue

        print(f"Converting: {filename}")
        command = [
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-vf", f"lut3d={lut_ffmpeg_path}",
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "slow",
            "-c:a", "copy",
            output_path
        ]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error converting {filename}: {e}")

    print("\nBatch conversion complete.")
    input("Press Enter to return to the menu...")



def convert_general_single():
    print("\n[Convert general video using custom LUT]")

    # Step 1: Ask for LUT path
    lut_local_path = input("Enter full path to your .cube LUT file: ").strip().strip('"')
    if not os.path.isfile(lut_local_path):
        print("Error: LUT file not found.")
        input("Press Enter to return to the menu...")
        return

    # Step 2: Ask for input video file
    input_path = input("\nEnter full path to the input video file: ").strip().strip('"')
    if not os.path.isfile(input_path):
        print("Error: Video file not found.")
        input("Press Enter to return to the menu...")
        return

    # Step 3: Choose output location
    print("\nWhere should the converted file be saved?")
    print("1) In the same folder as the original file (prefix: converted_)")
    print("2) Specify a custom output path")
    choice = input("Choose 1 or 2: ").strip()

    original_filename = os.path.basename(input_path)
    if choice == "1":
        output_path = os.path.join(os.path.dirname(input_path), f"converted_{original_filename}")
    elif choice == "2":
        output_path = input("Enter full output path including .mp4 extension: ").strip().strip('"')
    else:
        print("Invalid selection.")
        input("Press Enter to return to the menu...")
        return

    # Step 4: Run FFmpeg with specified LUT
    lut_ffmpeg_path = to_ffmpeg_lut_path(lut_local_path)

    print("\nStarting FFmpeg conversion...")

    command = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-vf", f"lut3d={lut_ffmpeg_path}",
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "slow",
        "-c:a", "copy",
        output_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"\nConversion successful. Output saved to: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"\nFFmpeg returned an error: {e}")

    input("\nPress Enter to return to the menu...")




def convert_general_batch():
    print("\n[Batch convert general videos using custom LUT]")

    # Step 1: Ask for LUT path
    lut_local_path = input("Enter full path to your .cube LUT file: ").strip().strip('"')
    if not os.path.isfile(lut_local_path):
        print("Error: LUT file not found.")
        input("Press Enter to return to the menu...")
        return

    # Step 2: Ask for input folder
    input_dir = input("\nEnter path to folder containing video files: ").strip().strip('"')
    if not os.path.isdir(input_dir):
        print("Error: Folder not found.")
        input("Press Enter to return to the menu...")
        return

    # Step 3: Choose output mode
    print("\nWhere should the converted files be saved?")
    print("1) In the original folder, with prefix 'converted_'")
    print("2) In a subfolder named 'converted' inside the original folder")
    print("3) Specify a custom output folder")
    choice = input("Choose 1, 2 or 3: ").strip()

    if choice == "1":
        output_dir = input_dir
    elif choice == "2":
        output_dir = os.path.join(input_dir, "converted")
        os.makedirs(output_dir, exist_ok=True)
    elif choice == "3":
        output_dir = input("Enter full path to output folder: ").strip().strip('"')
        if not os.path.isdir(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                print(f"Error creating output folder: {e}")
                input("Press Enter to return to the menu...")
                return
    else:
        print("Invalid selection.")
        input("Press Enter to return to the menu...")
        return

    # Step 4: Find and convert all .mp4 files
    lut_ffmpeg_path = to_ffmpeg_lut_path(lut_local_path)
    video_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".mp4")]

    if not video_files:
        print("No .mp4 files found in the folder.")
        input("Press Enter to return to the menu...")
        return

    print(f"\nFound {len(video_files)} video(s). Starting batch conversion...\n")

    for filename in video_files:
        input_path = os.path.join(input_dir, filename)

        if choice == "1":
            output_path = os.path.join(output_dir, f"converted_{filename}")
        else:
            output_path = os.path.join(output_dir, filename)

        if os.path.exists(output_path):
            print(f"Skipping (already exists): {filename}")
            continue

        print(f"Converting: {filename}")
        command = [
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-vf", f"lut3d={lut_ffmpeg_path}",
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "slow",
            "-c:a", "copy",
            output_path
        ]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error converting {filename}: {e}")

    print("\nBatch conversion complete.")
    input("Press Enter to return to the menu...")

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


# === Entry Point ===
if __name__ == "__main__":
    main_menu()
