#!/usr/bin/env python3
import argparse
from pathlib import Path
from time import sleep
import threading
import json

import yt_dlp
import customtkinter


version = "v0.1.1"


class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("YTmp3")
        self.geometry("1080x540")

        for i in range(3):
            self.grid_columnconfigure(i, weight=1, minsize=270)
        
        self.grid_rowconfigure(0, weight=0)


        self.subtitle = customtkinter.CTkLabel(self, text=f"Youtube converter to mp3", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.subtitle.grid(row=1, column=1, columnspan=2, padx=20, pady=25)


        self.entry = customtkinter.CTkEntry(self, width=500, height=35, border_width=0)
        self.entry.grid(row=2, column=1, columnspan=2, padx=20, pady=25)


        self.button = customtkinter.CTkButton(self, text="Download", command=self.button_callback, font=customtkinter.CTkFont(size=16), fg_color="#4A3022", hover_color="#5A3E2B")
        self.button.grid(row=3, column=1, columnspan=2, padx=125, pady=25, sticky="ew")


        self.optionmenu_var = customtkinter.StringVar(value="mp3")
        self.optionmenu = customtkinter.CTkOptionMenu(
            self, values=["mp3", "m4a"], command=self.optionmenu_callback, variable=self.optionmenu_var, 
            fg_color="#4A3022",
            button_color="#684634",
            button_hover_color="#845B43",
            dropdown_fg_color="#2C1D16",
            dropdown_hover_color="#684634"
        )

        self.optionmenu.grid(row=3, column=3, padx=(25, 400), pady=25, sticky="w")


        self.feedback_label = customtkinter.CTkLabel(self, text="", font=customtkinter.CTkFont(size=16))
        self.feedback_label.grid(row=4, column=1, columnspan=2, padx=25, pady=25)


        self.version_label = customtkinter.CTkLabel(self, text=version, font=customtkinter.CTkFont(size=13, weight="bold"))
        self.version_label.grid(row=0, column=0, columnspan=1, padx=(10, 10), pady=10, sticky="w")




    def optionmenu_callback(self, choice):
        print("optionmenu dropdown clicked", choice)

        self.subtitle.configure(text=f"Youtube converter to {choice}")

        if choice == "m4a":
            self.button.configure(fg_color="#3730A3", hover_color="#4F46E5")
            self.optionmenu.configure(fg_color="#3730A3",
                                button_color="#4F46E5",
                                button_hover_color="#6366F1",
                                dropdown_fg_color="#1E1B4B",
                                dropdown_hover_color="#4F46E5")
        else:
            self.button.configure(fg_color="#4A3022", hover_color="#5A3E2B")
            self.optionmenu.configure(fg_color="#4A3022",
                                button_color="#684634",
                                button_hover_color="#845B43",
                                dropdown_fg_color="#2C1D16",
                                dropdown_hover_color="#684634")

        

    def button_callback(self):
        url = self.entry.get()
        if url == "" or not url.startswith("https://www.youtube.com/watch?v="):
            print("Please enter a valid YouTube URL.")
            self.feedback_label.configure(text="Please enter a valid YouTube URL.")
            return

        self.button.configure(state="disabled")  # Disable the button to prevent multiple clicks
        self.feedback_label.configure(text=f"Starting process...")

        codec = self.optionmenu.get()

        thread = threading.Thread(target=self.download_thread, args=(url, codec))
        thread.start()

        self.progress_bar = customtkinter.CTkProgressBar(self, width=250, height=10)
        self.progress_bar.grid(row=5, column=1, columnspan=2, padx=25, pady=25)
        self.progress_bar.configure(mode="indeterminate")  # Set the progress bar to indeterminate mode
        self.progress_bar.indeterminate_speed = 0.5  # Set the speed of the indeterminate animation

        self.progress_bar.start()


        
    def download_thread(self, url, codec):


        self.feedback_label.configure(text=f"Download started...")
        print(f"Download of {url} started...")


        sleep(5)  # Simulate a delay for demonstration purposes


        output = download_yt_mp3(url, codec)

        if output == "Fail":
            self.feedback_label.configure(text=f"Download failed. Please check the URL and try again.")
        else:
            self.feedback_label.configure(text=f"Download completed successfully and saved in:\n\n {output}")

            self.progress_bar.stop()
            self.progress_bar.destroy()

            self.button.configure(state="normal")  # Re-enable the button after download is complete




def download_yt_mp3(url: str, codec, output_dir: str = "./downloads"):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": codec,
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


    if success := ydl.prepare_filename(ydl.extract_info(url, download=False)):
        return Path(success).with_suffix(f".{codec}")
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