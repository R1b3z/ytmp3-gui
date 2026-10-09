#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
import sys
from time import sleep
import threading

import yt_dlp
import customtkinter


class MyCheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.checkbox_1 = customtkinter.CTkCheckBox(self, text="checkbox 1")
        self.checkbox_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("YTmp3")
        self.geometry("1080x540")
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=0)

        self.subtitle = customtkinter.CTkLabel(self, text="Youtube converter to MP3", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.subtitle.grid(row=1, column=0, padx=25, pady=25, sticky="ew")


        self.entry = customtkinter.CTkEntry(self, width=350, height=35, border_width=0)
        self.entry.grid(row=2, column=0, columnspan=1, padx=250, pady=25, sticky="ew")


        self.button = customtkinter.CTkButton(self, text="Clica-mos", command=self.button_callback, font=customtkinter.CTkFont(size=16))
        self.button.grid(row=3, column=0, padx=460, pady=25, sticky="ew")


        self.feedback_label = customtkinter.CTkLabel(self, text="", font=customtkinter.CTkFont(size=16))
        self.feedback_label.grid(row=4, column=0, padx=250, pady=25, sticky="ew")



        self.version_label = customtkinter.CTkLabel(self, text="v0.1", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.version_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")



    def button_callback(self):
        url = self.entry.get()
        if url == "" or not url.startswith("https://www.youtube.com/watch?v="):
            print("Please enter a valid YouTube URL.")
            self.feedback_label.configure(text="Please enter a valid YouTube URL.")
            return

        self.button.configure(state="disabled")  # Disable the button to prevent multiple clicks
        self.feedback_label.configure(text=f"Starting process...")

        thread = threading.Thread(target=self.download_thread, args=(url,))
        thread.start()

        self.progress_bar = customtkinter.CTkProgressBar(self, width=250, height=10)
        self.progress_bar.grid(row=5, column=0, padx=25, pady=25)
        self.progress_bar.configure(mode="indeterminate")  # Set the progress bar to indeterminate mode
        self.progress_bar.indeterminate_speed = 0.5  # Set the speed of the indeterminate animation

        self.progress_bar.start()

        
    def download_thread(self, url):


        self.feedback_label.configure(text=f"Download started...")
        print(f"Download of {url} started...")


        sleep(5)  # Simulate a delay for demonstration purposes


        output = download_yt_mp3(url)

        if output == "Fail":
            self.feedback_label.configure(text=f"Download failed. Please check the URL and try again.")
        else:
            self.feedback_label.configure(text=f"Download completed successfully,\n saved in {output}")

            self.progress_bar.stop()
            self.progress_bar.destroy()

            self.button.configure(state="normal")  # Re-enable the button after download is complete




def download_yt_mp3(url: str, output_dir: str = "./downloads"):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


    if success := ydl.prepare_filename(ydl.extract_info(url, download=False)):
        return Path(success).with_suffix(".mp3")
    else:
        return "Fail"



if __name__ == "__main__":


    app = App()

    parser = argparse.ArgumentParser(description="Script to Download audio from YouTube (MP3).")
    #parser.add_argument("url", type=str, help="YouTube url")
    parser.add_argument("-o", "--output", type=str, default="./downloads", help="Download destination (default: ./downloads)")

    args = parser.parse_args()
    app.mainloop()


   #print(f"Download of {args.url} started...")
   #download_yt_mp3(args.url, args.output)