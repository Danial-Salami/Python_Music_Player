import tkinter as tk
from tkinter import messagebox
import pygame
import os
import random
from tkinter import ttk
from ttkthemes import themed_tk as tkk
from PIL import Image, ImageTk
from mutagen.mp3 import MP3


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="light yellow", relief="solid", borderwidth=1,
                         font=("Arial", 10))
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


class MusicPlayerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("1200x400+200+200")
        self.is_paused = False

        # Color Scheme
        self.primary_color = "deep sky blue"
        self.secondary_color = "white"
        self.button_color = "light sky blue"

        self.track_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.current_song_index = None
        self.shuffle_mode = False
        style = ttk.Style()
        style.configure("Player.TButton", font=("Arial", 16, "bold"))
        track_frame = tk.LabelFrame(self.root, text="Song Track", font=("Arial", 15, "bold"), bg=self.primary_color,
                                    fg=self.secondary_color, bd=5, relief="groove")
        track_frame.place(x=0, y=0, width=800, height=100)

        self.song_track = tk.Label(track_frame, textvariable=self.track_var, width=20, font=("Arial", 24, "bold"),
                                   bg=self.primary_color, fg=self.secondary_color, anchor="w")
        self.song_track.pack(side=tk.LEFT, padx=10, pady=5)

        track_status = tk.Label(track_frame, textvariable=self.status_var, font=("Arial", 24, "bold"),
                                bg=self.primary_color, fg=self.secondary_color)
        track_status.pack(side=tk.LEFT, padx=10, pady=5)

        self.scroll_track_delay = 250  # Initial delay for name scrolling

        button_frame = tk.LabelFrame(self.root, text="Control Panel", font=("Arial", 15, "bold"), bg=self.primary_color,
                                     fg=self.secondary_color, bd=5, relief=tk.GROOVE)
        button_frame.place(x=0, y=100, width=800, height=100)
        self.duration_var = tk.StringVar(value="00:00 / 00:00")
        self.duration_label = tk.Label(track_frame, textvariable=self.duration_var, font=("Arial", 16, "bold"),
                                       bg=self.primary_color, fg=self.secondary_color)
        self.duration_label.pack(side=tk.LEFT, padx=10, pady=5)

        play_img = Image.open("icons/211876_play_icon.png")  # Replace with the actual path to your play icon image
        play_img = play_img.resize((32, 32))  # Resize the image as needed
        self.play_icon = ImageTk.PhotoImage(play_img)
        pause_img = Image.open("icons/211871_pause_icon.png")  # Replace with the actual path to your pause icon image
        pause_img = pause_img.resize((32, 32))  # Resize the image as needed
        self.pause_icon = ImageTk.PhotoImage(pause_img)
        unpause_img = Image.open("icons/9044200_continue_filled_icon.png")  # Replace with the actual path to your unpause icon image
        unpause_img = unpause_img.resize((32, 32))  # Resize the image as needed
        self.unpause_icon = ImageTk.PhotoImage(unpause_img)
        stop_img = Image.open("icons/216325_media_stop_icon.png")  # Replace with the actual path to your stop icon image
        stop_img = stop_img.resize((32, 32))  # Resize the image as needed
        self.stop_icon = ImageTk.PhotoImage(stop_img)
        next_img = Image.open("icons/forward-button.png")  # Replace with the actual path to your stop icon image
        next_img = next_img.resize((32, 32))  # Resize the image as needed
        self.next_icon = ImageTk.PhotoImage(next_img)
        previous_img = Image.open("icons/rewind-button.png")  # Replace with the actual path to your stop icon image
        previous_img = previous_img.resize((32, 32))  # Resize the image as needed
        self.previous_icon = ImageTk.PhotoImage(previous_img)
        volume_img = Image.open("icons/9004796_speaker_sound_music_audio_volume_icon.png")  # Replace with the actual path to your stop icon image
        volume_img = volume_img.resize((12, 12))  # Resize the image as needed
        self.volume_icon = ImageTk.PhotoImage(volume_img)

        play_btn = ttk.Button(button_frame, image=self.play_icon, command=self.play_song, style="Player.TButton")
        play_btn.grid(row=0, column=0, padx=10, pady=5)
        Tooltip(play_btn, "Play")

        pause_btn = ttk.Button(button_frame, image=self.pause_icon, command=self.pause_song, style="Player.TButton")
        pause_btn.grid(row=0, column=1, padx=10, pady=5)
        Tooltip(pause_btn, "Pause")

        unpause_btn = ttk.Button(button_frame, image=self.unpause_icon, command=self.unpause_song, style="Player.TButton")
        unpause_btn.grid(row=0, column=2, padx=10, pady=5)
        Tooltip(unpause_btn, "Unpause")

        stop_btn = ttk.Button(button_frame, image=self.stop_icon, command=self.stop_song, style="Player.TButton")
        stop_btn.grid(row=0, column=3, padx=10, pady=5)
        Tooltip(stop_btn, "Stop")

        self.shuffle_var = tk.StringVar(value="Shuffle: OFF")

        bottom_frame = tk.Frame(self.root, bg=self.primary_color)
        bottom_frame.place(x=0, y=210, width=800, height=100)

        next_btn = ttk.Button(button_frame, image=self.next_icon, command=self.next_song, style="Player.TButton")
        next_btn.grid(row=0, column=7, padx=10, pady=5)
        Tooltip(next_btn, "Next")

        previous_btn = ttk.Button(button_frame, image=self.previous_icon, command=self.previous_song, style="Player.TButton")
        previous_btn.grid(row=0, column=6, padx=10, pady=5)
        Tooltip(previous_btn, "Previous")

        shuffle_btn = tk.Button(bottom_frame, textvariable=self.shuffle_var, command=self.toggle_shuffle, width=10,
                                height=1, font=("Arial", 16, "bold"), fg=self.secondary_color, bg=self.button_color)
        shuffle_btn.pack(side=tk.LEFT, padx=5, pady=5)

        volume_btn = ttk.Button(button_frame, image=self.volume_icon,style="Player.TButton")
        volume_btn.grid(row=0, column=10, padx=5, pady=5)
        Tooltip(volume_btn, "Volume")

        self.volume_slider = tk.Scale(button_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume, font=("Arial", 10), bg=self.primary_color, fg=self.secondary_color, highlightbackground=self.primary_color)
        self.volume_slider.set(50)  # Default volume
        self.volume_slider.grid(row=0, column=11, padx=0, pady=5,ipadx=20)

        songs_frame = tk.LabelFrame(self.root, text="Song Playlist", font=("Arial", 15, "bold"), bg=self.primary_color,
                                    fg=self.secondary_color, bd=5, relief="groove")
        songs_frame.place(x=800, y=0, width=400, height=700)

        scroll_y = tk.Scrollbar(songs_frame, orient="vertical")
        self.playlist = tk.Listbox(songs_frame, yscrollcommand=scroll_y.set, selectbackground="gold",
                                   selectmode="single", font=("Arial", 12, "bold"), bg=self.secondary_color,
                                   fg=self.primary_color, bd=5, relief="groove")

        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_y.config(command=self.playlist.yview)
        self.playlist.pack(fill="both")

        os.chdir("song list")
        song_tracks = os.listdir()
        for track in song_tracks:
            self.playlist.insert(tk.END, track)

        pygame.init()
        pygame.mixer.init()

    def play_song(self):
        try:
            selected_song = self.playlist.get(tk.ACTIVE)
            self.track_var.set(selected_song)
            self.status_var.set("-Playing")
            self.current_song_index = self.playlist.curselection()[0]  # Get the current song index
            pygame.mixer.music.load(selected_song)
            pygame.mixer.music.play()
            self.scroll_track_delay = 230
            # Reset the delay for name scrolling
        except pygame.error as e:
            messagebox.showerror("Error", str(e))

    def scroll_track(self):
        if self.status_var.get() == "-Playing":
            track_text = self.track_var.get()
            self.song_track.config(text=track_text)
            if len(track_text) > 20:
                self.track_var.set(track_text[1:] + track_text[0])
        self.song_track.after(self.scroll_track_delay, self.scroll_track)

    def pause_song(self):
        if self.status_var.get() == "-Playing" and pygame.mixer.music.get_busy():
            self.status_var.set("-Paused")
            self.song_track.after_cancel(self.scroll_track)
            pygame.mixer.music.pause()
            self.is_paused = True

    def unpause_song(self):
        if self.status_var.get() == "-Paused" and self.is_paused:
            self.status_var.set("-Playing")
            if not self.is_stop_clicked:
                self.scroll_track()
            pygame.mixer.music.unpause()
            self.is_paused = False

    def stop_song(self):
        self.status_var.set("-Stopped")
        self.track_var.set(self.playlist.get(tk.ACTIVE))
        pygame.mixer.music.stop()
        self.is_stop_clicked = True
        self.song_track.after_cancel(self.scroll_track)
        self.scroll_track()  # Reset the song track position

    def next_song(self):
        if self.shuffle_mode:
            self.play_random_song()

        else:
            next_index = self.current_song_index + 1 if self.current_song_index is not None else 0
            self.play_song_by_index(next_index)


    def previous_song(self):
        if self.shuffle_mode:
            self.play_random_song()

        else:
            prev_index = self.current_song_index - 1 if self.current_song_index is not None else 0
            self.play_song_by_index(prev_index)


    def play_song_by_index(self, index):
        self.playlist.selection_clear(0, tk.END)
        self.playlist.selection_set(index)
        self.current_song_index = index
        selected_song = self.playlist.get(index)
        self.track_var.set(selected_song)
        self.status_var.set("-Playing")
        pygame.mixer.music.load(selected_song)
        pygame.mixer.music.play()
        self.scroll_track_delay = 230
        # Reset the delay for name scrolling

    def toggle_shuffle(self):
        if self.shuffle_mode:
            self.shuffle_var.set("Shuffle: OFF")
            self.shuffle_mode = False
        else:
            self.shuffle_var.set("Shuffle: ON")
            self.shuffle_mode = True

    def play_random_song(self):
        self.playlist.selection_clear(0, tk.END)
        random_index = random.randint(0, self.playlist.size() - 1)
        self.playlist.selection_set(random_index)
        self.current_song_index = random_index
        selected_song = self.playlist.get(random_index)
        self.track_var.set(selected_song)
        self.status_var.set("-Playing")
        pygame.mixer.music.load(selected_song)
        pygame.mixer.music.play()
        self.scroll_track_delay = 230
        # Reset the delay for name scrolling

    def set_volume(self, volume):
        volume = int(volume) / 100
        pygame.mixer.music.set_volume(volume)




if __name__ == "__main__":
    root = tkk.ThemedTk()
    root.get_themes()
    root.set_theme("breeze")
    MusicPlayerGUI(root)
    root.mainloop()
