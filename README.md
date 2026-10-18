<div align="center">
  
# YTmp3 

![Python package](https://github.com/R1b3z/ytmp3-gui/actions/workflows/python-package.yml/badge.svg)
![Release](https://img.shields.io/github/v/release/R1b3z/ytmp3-gui?include_prereleases)
![Last commit](https://img.shields.io/github/last-commit/R1b3z/ytmp3-gui)
![Python](https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/github/license/R1b3z/ytmp3-gui)


<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&pause=1000&color=6DBCC9&center=true&vCenter=true&width=800&lines=GUI+Application;Extract+Audio+of+YouTube+%7C+MP3+or+M4A;Save+Video+as+MKV+or+MP4" alt="Typing SVG" />

</div>

## App

![Screenshot](docs/screenshot.png)

## What the program uses

- **Python 3** to execute the application.
- **CustomTkinter** to create the graphical interface.
- **yt-dlp** to obtain the video audio.
- **FFmpeg** to convert the audio into MP3. FFmpeg needs to be installed and available in `PATH`.

## How it works

Introducing a YouTube URL in the textbox and clicking the button triggers the app to start the process in the background, it then creates a `downloads` folder in the current directory if there isn't already one, presents the location/filename in the screen and saves the converted file in the `downloads` folder.

The application only accepts URL's in the following format: `https://www.youtube.com/watch?v=...` and processes one video at a time.

It uses threads to fetch and convert the video seperately from the main thread so the UI is rendering without being interrupted.

## Requirements

- Windows/Linux
- Python 3 installed and available in `PATH`
- FFmpeg installed and available in `PATH`
- Internet connection

## Installation

Install the Python dependencies with:

```bash
python -m pip install yt-dlp customtkinter
```

Install FFmpeg separately, following the instructions for your system, and confirm the command `ffmpeg` is available in `PATH`.

## Executing

For windows, I created a .bat so the app can be start just by running `ytmp3.bat`. Alternatively, execute the following in the project directory:

```bash
python main.py
```

## Structure

- `main.py` — graphical interface and transfer/conversion logic.
- `ytmp3.bat` — shortcut to start the app on Windows.
- `downloads/` — destination folder for the MP3 files.

## App

- ### UI Feedback

<img width="1080" height="610" alt="ytmp3-v0 2 0-feedback" src="https://github.com/user-attachments/assets/a1b3eccf-df4a-4233-9301-1ca27fd06045" />

- ### Workflow

<img width="1080" height="530" alt="ytmp3-workflow" src="https://github.com/user-attachments/assets/df5d9074-b3eb-4a62-a8ec-156ea6874864" />



## Note

Only use the app with contents that you have the right to download and respect YouTube terms of service and applicable copyrights.
