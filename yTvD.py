from tkinter import *
from tkinter.ttk import Progressbar
from pytube import YouTube
from tqdm import tqdm
import threading

def download ():
    try:
        # Get the URL from the entry widget
        video_url = url_entry.get()

        # Create YouTube object
        yt = YouTube(video_url)

        # Get all available video streams
        streams = yt.streams.filter(progressive=True)

        # Get the selected resolution from the dropdown menu
        selected_res = resolution_var.get()

        # Find the first stream with the selected resolution
        stream = None
        for s in streams:
            if s.resolution == selected_res:
                stream = s
                break
# Check if stream is not None before accessing its attributes
        if stream is not None:
            # Get video title and file extension
            title = yt.title
            extension = stream.subtype

            # Build the filename
            filename = f"{title}.{extension}"

            # Create the downloads folder if it doesn't exist
            import os
            if not os.path.exists("downloads"):
                os.makedirs("downloads")

            # Disable the download button while downloading
            download_button.config(state=DISABLED)

            # Create a separate thread for downloading
            download_thread = threading.Thread(target=download_video, args=(stream, filename))
            download_thread.start()
        else:
            # Display an error message if no stream was found
            status_label.config(text=f"No video stream found with resolution {selected_res}.")    
    except Exception as e:
        # Display an error message if any exception occurs
        status_label.config(text="An error occurred during download.")
        print("Error:", str(e))
def download_video(stream, filename):
    try:
        # Create the progress bar
        progress_bar.config(maximum=100, value=0)
        progress_bar.pack(padx=10, pady=10)

        # Download the video
        status_label.config(text="Downloading...")
        stream.download(output_path="downloads", filename=filename)
        status_label.config(text="Video download completed!")
        progress_bar.pack_forget()

        # Enable the download button after completion
        download_button.config(state=NORMAL)
    
    except Exception as e:
        # Display an error message if any exception occurs
        status_label.config(text="An error occurred during download.")
        print ("Error:", str(e))

# Create the GUI window
window = Tk ()
window.title("YouTube Video Downloader")

# Create the URL entry widget
url_entry = Entry (window, width=50)
url_entry.pack(padx=10, pady=10)

# Create the resolution dropdown menu
resolutions = ["240p", "360p", "480p", "720p", "1080p"]
resolution_var = StringVar(window)
resolution_var.set(resolutions [0])
resolution_menu = OptionMenu(window, resolution_var, *resolutions)
resolution_menu.pack(padx=10, pady=10)

# Create the download button
download_button = Button (window, text="Download", command=download)
download_button.pack(padx=10, pady=10)

# Create the status label
status_label = Label (window, text="")
status_label.pack(padx=10, pady=10)
# Create the progress bar
progress_bar = Progressbar(window, orient=HORIZONTAL, length=200)
# Start the GUI loop
window.mainloop()