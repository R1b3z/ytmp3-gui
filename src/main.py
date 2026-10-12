#!/usr/bin/env python3
import argparse
from pathlib import Path
from time import sleep
import threading
import json

import yt_dlp
import customtkinter


version = "v0.2.0"
height = 720
width = height * (16 / 9)

video = False

class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("YTmp3")
        #self.geometry("1080x540")
        self.minsize(width, height)
        self.maxsize(width, height)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  

        self._build_topbar()
        self._build_center()
        self._build_footer()



    def _build_topbar(self):

        bar = customtkinter.CTkFrame(self, fg_color="transparent")
        bar.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        bar.grid_columnconfigure(1, weight=1)


        self.version_label = customtkinter.CTkLabel(bar, text=version, font=customtkinter.CTkFont(size=13, weight="bold"))
        self.version_label.grid(row=0, column=0, sticky="w")

        sw = customtkinter.CTkFrame(bar, fg_color="transparent")
        sw.grid(row=0, column=2, sticky="e")

        self.switch_label = customtkinter.CTkLabel(sw, text="Video", font=customtkinter.CTkFont(size=13))
        self.switch_label.grid(row=0, column=0, padx=(0, 8))


        self.switch_var = customtkinter.StringVar(value="Audio")
        self.switch = customtkinter.CTkSwitch(sw, text="Audio", font=customtkinter.CTkFont(size=13), command=self.switch_event, variable=self.switch_var, onvalue="Audio", offvalue="Video")
        self.switch.grid(row=0, column=1)


        

    def _build_center(self):

        center = customtkinter.CTkFrame(self, fg_color="transparent")
        center.grid(row=1, column=0)


        center.grid_columnconfigure(0, weight=1, uniform="side")
        center.grid_columnconfigure((1, 2), weight=0, minsize=200)
        center.grid_columnconfigure(3, weight=1, uniform="side")


        self.subtitle = customtkinter.CTkLabel(center, 
            text=f"Youtube converter to mp3", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.subtitle.grid(row=0, column=1, columnspan=2, pady=(0, 20))


        self.entry = customtkinter.CTkEntry(center, width=500, height=35, border_width=0)
        self.entry.grid(row=1, column=1, columnspan=2, sticky="ew")


        self.optionmenu_var = customtkinter.StringVar(value="mp3")
        self.optionmenu = customtkinter.CTkOptionMenu(
            center, width=90, height=35,values=["mp3", "m4a"], command=self.optionmenu_callback, variable=self.optionmenu_var, 
            fg_color="#4A3022",
            button_color="#684634",
            button_hover_color="#845B43",
            dropdown_fg_color="#2C1D16",
            dropdown_hover_color="#684634"
        )
        self.optionmenu.grid(row=1, column=3, padx=(40, 0), sticky="w")


        self.button = customtkinter.CTkButton(center, 
            text="Download", command=self.button_callback, font=customtkinter.CTkFont(size=16), fg_color="#4A3022", hover_color="#5A3E2B")
        self.button.grid(row=2, column=1, columnspan=2, pady=20)


        self.progress = customtkinter.CTkProgressBar(center, width=200, mode="indeterminate", progress_color="#4A3022")
        self.progress.grid(row=3, column=1, columnspan=2, pady=25, padx=100, sticky="ew")
        self.progress.grid_remove()


        self.feedback_label = customtkinter.CTkLabel(center, text="", font=customtkinter.CTkFont(size=16))
        self.feedback_label.grid(row=4, column=0, columnspan=4, pady=(10, 0))


        
    def _build_footer(self):

        self.copyright_label = customtkinter.CTkLabel(self, text="© 2026 by @R1b3z", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.copyright_label.grid(row=2, column=0, pady=(0,8))



    def switch_event(self):
        print("switch toggled, current value:", self.switch_var.get())

        if self.switch_var.get() == "Audio":
            self.optionmenu.configure(values=["mp3", "m4a"])
            self.optionmenu_var.set("mp3")
            self.subtitle.configure(text=f"Youtube converter to mp3")
            self.styles(self.switch_var.get(), self.optionmenu_var.get())
            if self.optionmenu_var.get() == "mp3":
                self.optionmenu_callback("mp3")
            else:
                self.optionmenu_callback("m4a")
        else:
            self.optionmenu.configure(values=["mp4", "mkv"])
            self.optionmenu_var.set("mp4")
            self.subtitle.configure(text=f"Youtube video download")
            self.styles(self.switch_var.get(), self.optionmenu_var.get())
            if self.optionmenu_var.get() == "mp4":
                self.optionmenu_callback("mp4")
            else:
                self.optionmenu_callback("mkv")



    def optionmenu_callback(self, choice):
        print("optionmenu dropdown clicked", choice)

        self.subtitle.configure(text=f"Youtube converter to {choice}")

        self.styles(self.switch_var.get(), choice)
            
        

    def button_callback(self):
        url = self.entry.get()
        if url == "" or not url.startswith("https://www.youtube.com/watch?v="):
            print("Please enter a valid YouTube URL.")
            self.feedback_label.configure(text="Please enter a valid YouTube URL.")
            return

        self.button.configure(state="disabled")  # Disable the button to prevent multiple clicks
        self.optionmenu.configure(state="disabled")  # Disable the option menu to prevent changes during download
        self.switch.configure(state="disabled")  # Disable the switch to prevent changes during download

        self.feedback_label.configure(text=f"Starting process...")

        codec = self.optionmenu.get()

        thread = threading.Thread(target=self.download_thread, args=(url, codec))
        thread.start()

        self.progress.grid()  # Show the progress bar
        #self.progress.indeterminate_speed = 0.5  # Set the speed of the indeterminate animation
        self.progress.start()


        
    def download_thread(self, url, codec):


        self.feedback_label.configure(text=f"Download started...")
        print(f"Download of {url} started...")

        sleep(1)  # Simulate a delay for demonstration purposes

        if self.switch_var.get() == "Audio":
            output = download_yt_mp3(url, codec)
        else:
            output = download_yt_video(url, codec)


        self.after(0, self.download_done, output)



    def download_done(self, output):

        self.progress.stop()
        self.progress.grid_remove()

        self.button.configure(state="normal")
        self.optionmenu.configure(state="normal")
        self.switch.configure(state="normal")

        if output == "Fail":
            self.feedback_label.configure(text="Download failed. Please check the URL and try again.")
        else:
            self.feedback_label.configure(text=f"Download completed successfully and saved in:\n\n{output}")



    def styles(self, switch, menu):
        if switch == "Video" and menu == "mp4":
            self.button.configure(fg_color="#36A761", hover_color="#4CE788")
            self.optionmenu.configure(fg_color="#36A761",
                                button_color="#1F6138",
                                button_hover_color="#309456",
                                dropdown_fg_color="#0E5F2D",
                                dropdown_hover_color="#149646")
            self.progress.configure(progress_color="#36A761")
        elif switch == "Video" and menu == "mkv":
            self.button.configure(fg_color="#A79236", hover_color="#E0C54C")
            self.optionmenu.configure(fg_color="#A79236",
                                button_color="#61551F",
                                button_hover_color="#A79236",
                                dropdown_fg_color="#5F5111",
                                dropdown_hover_color="#9C851D")
            self.progress.configure(progress_color="#A79236")
        elif switch == "Audio" and menu == "m4a":
            self.button.configure(fg_color="#3730A3", hover_color="#4F46E5")
            self.optionmenu.configure(fg_color="#3730A3",
                                button_color="#4F46E5",
                                button_hover_color="#6366F1",
                                dropdown_fg_color="#1E1B4B",
                                dropdown_hover_color="#4F46E5")
            self.progress.configure(progress_color="#3730A3")
        elif switch == "Audio" and menu == "mp3":
            self.button.configure(fg_color="#4A3022", hover_color="#5A3E2B")
            self.optionmenu.configure(fg_color="#4A3022",
                                button_color="#684634",
                                button_hover_color="#845B43",
                                dropdown_fg_color="#2C1D16",
                                dropdown_hover_color="#684634")
            self.progress.configure(progress_color="#4A3022")




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


def download_yt_video(url: str, codec, output_dir: str = "./downloads"):
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "merge_output_format": codec,
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

    print(f"Window is {width} x {height}")
    

    parser = argparse.ArgumentParser(description="Script to Download audio from YouTube (MP3).")
    #parser.add_argument("url", type=str, help="YouTube url")
    parser.add_argument("-o", "--output", type=str, default="./downloads", help="Download destination (default: ./downloads)")

    args = parser.parse_args()
    app.mainloop()

