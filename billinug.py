import pygame
import os
import sys
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk  # For handling images

# Initialize Pygame mixer
pygame.mixer.init()

# Create the main window
root = Tk()
root.title("නෝවගෙ සින්දු 🎵")
root.geometry("800x500")
root.config(bg="#212121")  # Dark background

# Global Variables
current_music = None
playlist = []
current_index = 0

# Load icons
def load_icon(path, size=(30, 30)):
    if getattr(sys, 'frozen', False):
        # If running as a PyInstaller bundle, use the bundle's directory
        base_path = sys._MEIPASS
        img = Image.open(os.path.join(base_path, path)).resize(size)
    else:
        img = Image.open(path).resize(size)
    return ImageTk.PhotoImage(img)


play_icon = load_icon("play.png")
pause_icon = load_icon("pause.png")
next_icon = load_icon("next.png")
prev_icon = load_icon("prev.png")
stop_icon = load_icon("stop.png")

# Functions
def load_music():
    files = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg *.flac")])
    if files:
        playlist.extend(files)
        update_playlist()

def update_playlist():
    playlist_box.delete(0, END)
    for song in playlist:
        playlist_box.insert(END, os.path.basename(song))

def play_music():
    global current_index
    if playlist:
        song = playlist[current_index]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        song_label.config(text=f"Playing: {os.path.basename(song)}")

def pause_music():
    pygame.mixer.music.pause()

def resume_music():
    pygame.mixer.music.unpause()

def stop_music():
    pygame.mixer.music.stop()
    song_label.config(text="Music Stopped")

def next_song():
    global current_index
    if current_index < len(playlist) - 1:
        current_index += 1
        play_music()

def previous_song():
    global current_index
    if current_index > 0:
        current_index -= 1
        play_music()

def select_song(event):
    global current_index
    current_index = playlist_box.curselection()[0]
    play_music()

# GUI Components
# Playlist Frame
playlist_frame = Frame(root, bg="#333")
playlist_frame.pack(side=LEFT, fill=Y, padx=10, pady=10)

playlist_box = Listbox(playlist_frame, bg="#424242", fg="white", font=("Helvetica", 14), selectbackground="#616161")
playlist_box.pack(side=LEFT, fill=BOTH, expand=True)
playlist_box.bind("<<ListboxSelect>>", select_song)

# Main Section
main_frame = Frame(root, bg="#212121")
main_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=20, pady=20)

song_label = Label(main_frame, text="No song loaded", font=("Helvetica", 18), bg="#212121", fg="white")
song_label.pack(pady=30)

# Control Buttons at the Bottom
button_frame = Frame(main_frame, bg="#212121")
button_frame.pack(side=BOTTOM, pady=30)

prev_button = Button(button_frame, image=prev_icon, command=previous_song, bg="#424242", bd=0, activebackground="#616161")
prev_button.grid(row=0, column=0, padx=10)

play_button = Button(button_frame, image=play_icon, command=play_music, bg="#424242", bd=0, activebackground="#616161")
play_button.grid(row=0, column=1, padx=10)

pause_button = Button(button_frame, image=pause_icon, command=pause_music, bg="#424242", bd=0, activebackground="#616161")
pause_button.grid(row=0, column=2, padx=10)

stop_button = Button(button_frame, image=stop_icon, command=stop_music, bg="#424242", bd=0, activebackground="#616161")
stop_button.grid(row=0, column=3, padx=10)

next_button = Button(button_frame, image=next_icon, command=next_song, bg="#424242", bd=0, activebackground="#616161")
next_button.grid(row=0, column=4, padx=10)

# Load Music Button
load_button = ttk.Button(main_frame, text="Load Songs", command=load_music, width=20)
load_button.pack(side=BOTTOM, pady=10)

# Run the main event loop
root.mainloop()
