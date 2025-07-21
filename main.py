import os
import subprocess
from helper import clear_console, run_ffmpeg, download_dji_lut_if_needed


def main_menu():
    while True:
        clear_console()
        print("== Video Conversion Tool ==")
        print("===========================")
        print("1) Convert DJI Osmo Pocket 3 D-Log-M to Rec.709")
        print("2) Batch Convert DJI Osmo Pocket 3 D-Log-M to Rec.709")
        print("3) Convert General Video (with your own LUT)")
        print("4) Batch Convert General Videos (with your own LUT)")
        print("0) Exit")
        print("===========================")

        choice = input("Select an option (0–4): ").strip()

        if choice == "1":
            lut_path = download_dji_lut_if_needed()
            if lut_path:
                print("\n== Convert DJI D-Log-M Video to Rec.709 ==")
                convert_single_video(lut_path)
        elif choice == "2":
            lut_path = download_dji_lut_if_needed()
            if lut_path:
                print("\n== Batch Convert DJI D-Log-M Videos to Rec.709 ==")
                convert_batch_videos(lut_path)
        elif choice == "3":
            lut_path = input("Enter path to your LUT (.cube) file: ").strip('"')
            if not os.path.isfile(lut_path):
                print("Invalid LUT file.")
            else:
                print("\n== Convert General Video with custom LUT ==")
                convert_single_video(lut_path)
        elif choice == "4":
            lut_path = input("Enter path to your LUT (.cube) file: ").strip('"')
            if not os.path.isfile(lut_path):
                print("Invalid LUT file.")
            else:
                print("\n== Batch Convert General Videos with custom LUT ==")
                convert_batch_videos(lut_path)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid option.")
            input("Press Enter to try again...")


# === Functions ===
def convert_single_video(lut_path):
    # Step 1: Ask user for input video
    input_path = input("Enter full path to the video: ").strip('"')
    if not os.path.isfile(input_path):
        print("Error: Video file not found.")
        input("Press Enter to return to the menu...")
        return

    input_dir = os.path.dirname(input_path)
    filename = os.path.basename(input_path)

    # Step 2: Ask for output location
    print("\nWhere should the converted video be saved?")
    print("1) In the same folder (prefix: converted_)")
    print("2) In a subfolder named 'converted' in the same folder")
    print("3) Specify a custom output folder")
    choice = input("Choose 1, 2, or 3: ").strip()

    if choice == "1":
        output_path = os.path.join(input_dir, f"converted_{filename}")
    elif choice == "2":
        output_dir = os.path.join(input_dir, "converted")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename)
    elif choice == "3":
        output_dir = input("Enter full path to custom output folder: ").strip('"')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename)
    else:
        print("Invalid selection.")
        input("Press Enter to return to the menu...")
        return

    # Step 3: Skip if output already exists
    if os.path.exists(output_path):
        print("Output file already exists. Skipping.")
        input("Press Enter to return to the menu...")
        return

    # Step 4: Convert using shared run_ffmpeg() function
    try:
        print(f"\nConverting: {filename}")
        run_ffmpeg(input_path, output_path, lut_path)
        print(f"\nConversion successful! Output saved to:\n{output_path}")
    except subprocess.CalledProcessError as e:
        print(f"\nFFmpeg error: {e}")

    input("\nPress Enter to return to the menu...")


def convert_batch_videos(lut_path):
    # Step 1: Ask user for input folder
    input_dir = input("Enter path to folder containing the videos: ").strip('"')
    if not os.path.isdir(input_dir):
        print("Error: Folder not found.")
        input("Press Enter to return to the menu...")
        return

    # Step 2: Output location mode
    print("\nWhere should the converted files be saved?")
    print("1) In the original folder, with prefix 'converted_'")
    print("2) In a subfolder named 'converted' inside the original folder")
    print("3) Specify a custom output folder")
    choice = input("Choose 1, 2 or 3: ").strip()

    if choice == "1":
        output_mode = "prefix"
        output_dir = input_dir
    elif choice == "2":
        output_mode = "subfolder"
        output_dir = os.path.join(input_dir, "converted")
        os.makedirs(output_dir, exist_ok=True)
    elif choice == "3":
        output_mode = "custom"
        output_dir = input("Enter full path to output folder: ").strip('"')
        os.makedirs(output_dir, exist_ok=True)
    else:
        print("Invalid selection.")
        input("Press Enter to return to the menu...")
        return

    # Step 3: Find input files
    video_files = [
        f for f in os.listdir(input_dir)
        if f.lower().endswith(('.mp4', '.mov', '.mkv'))
    ]

    if not video_files:
        print("No video files (.mp4, .mov, .mkv) found in the folder.")
        input("Press Enter to return to the menu...")
        return

    print(f"\nFound {len(video_files)} video(s). Starting conversion...\n")

    # Step 4: Process each video
    for filename in video_files:
        input_path = os.path.join(input_dir, filename)

        if output_mode == "prefix":
            output_path = os.path.join(output_dir, f"converted_{filename}")
        else:
            output_path = os.path.join(output_dir, filename)

        if os.path.exists(output_path):
            print(f"Skipping (already exists): {filename}")
            continue

        try:
            print(f"Converting: {filename}")
            run_ffmpeg(input_path, output_path, lut_path)
        except subprocess.CalledProcessError as e:
            print(f"Error converting {filename}: {e}")

    print("\n✅ Batch conversion complete.")
    input("Press Enter to return to the menu...")





# === Entry Point ===
if __name__ == "__main__":
    main_menu()
