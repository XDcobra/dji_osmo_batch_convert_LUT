# DJI & General Video LUT Converter (including batch conversion)

A Python-based command-line tool for converting single or batch video files (DJI D-Log-M or general formats) to Rec.709 or other color spaces using 3D LUTs (`.cube`).


## Features

- Interactive CLI menu
- Converts DJI Osmo Pocket 3 D-Log-M footage to Rec.709
- Supports `.mp4`, `.mov`, `.mkv`, `.avi`, `.mxf`, `.webm`
- Automatically downloads the DJI LUT if not already present
- Supports custom LUTs for general videos
- Batch and single-file conversion
- Flexible output options:
  - Same folder with prefix
  - Subfolder `converted/`
  - Custom output path

## Requirements

- Python 3.7+
- FFmpeg (must be accessible via system PATH)

## Installation

1. Clone this repository:

```
git clone https://github.com/XDcobra/dji_osmo_batch_convert_LUT.git
cd dji_osmo_batch_convert_LUT
```

2. Install dependencies (optional – standard library is enough):

```
pip install -r requirements.txt
```

3. Ensure FFmpeg is installed and added to your PATH:

```
ffmpeg -version
```

## Usage

Simply run the main script:

```
python main.py
```

You will be prompted with an interactive menu:

```
1) Convert DJI Osmo Pocket 3 D-Log-M to Rec.709
2) Batch Convert DJI Osmo Pocket 3 D-Log-M to Rec.709
3) Convert General Video (with custom LUT)
4) Batch Convert General Videos (with custom LUT)
0) Exit
```

Follow the prompts to select input files/folders, LUTs, and output options.

## Example: Convert DJI D-Log-M video

- Choose option `1`
- The DJI LUT will be downloaded automatically if missing
- Select a video file
- Choose output location
- Done – FFmpeg will convert your file to Rec.709

## To-Do's for the future

- [ ] Drag & drop support
- [ ] GUI version (e.g. with PyQt)
- [ ] Support for `.mov` to `.mp4` conversion
- [ ] Option to adjust FFmpeg parameters (e.g. CRF, codec)

## License

MIT License

## Credits

- DJI Osmo Pocket 3 LUT: [DJI Official Download](https://www.dji.com)
- Powered by [FFmpeg](https://ffmpeg.org)
