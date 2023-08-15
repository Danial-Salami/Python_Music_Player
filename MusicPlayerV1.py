import tkinter as tk
from tkinter import messagebox
import pygame
import os

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

        play_btn = tk.Button(button_frame, text="PLAY", command=self.play_song, width=10, height=1,
                             font=("Arial", 16, "bold"), fg=self.secondary_color, bg=self.button_color)
        play_btn.grid(row=0, column=0, padx=10, pady=5)

        pause_btn = tk.Button(button_frame, text="PAUSE", command=self.pause_song, width=8, height=1,
                              font=("Arial", 16, "bold"), fg=self.secondary_color, bg=self.button_color)
        pause_btn.grid(row=0, column=1, padx=5, pady=5)

        unpause_btn = tk.Button(button_frame, text="UNPAUSE", command=self.unpause_song, width=10, height=1,
                                font=("Arial", 16, "bold"), fg=self.secondary_color, bg=self.button_color)
        unpause_btn.grid(row=0, column=2, padx=5, pady=5)

        stop_btn = tk.Button(button_frame, text="STOP", command=self.stop_song, width=10, height=1,
                             font=("Arial", 16, "bold"), fg=self.secondary_color, bg=self.button_color)
        stop_btn.grid(row=0, column=3, padx=5, pady=5)

        volume_label = tk.Label(button_frame, text="Volume", font=("Arial", 10), bg=self.primary_color,
                                fg=self.secondary_color)
        volume_label.grid(row=0, column=4, padx=5, pady=5)

        self.volume_slider = tk.Scale(button_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                      command=self.set_volume, font=("Arial", 10), bg=self.primary_color,
                                      fg=self.secondary_color, highlightbackground=self.primary_color)
        self.volume_slider.set(50)  # Default volume
        self.volume_slider.grid(row=0, column=5, padx=5, pady=5)

        songs_frame = tk.LabelFrame(self.root, text="Song Playlist", font=("Arial", 15, "bold"), bg=self.primary_color,
                                    fg=self.secondary_color, bd=5, relief="groove")
        songs_frame.place(x=800, y=0, width=400, height=400)

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
        self.status_var.set("-Paused")
        self.song_track.after_cancel(self.scroll_track)
        pygame.mixer.music.pause()

    def unpause_song(self):
        if self.status_var.get() != "-Paused":
            return
        self.status_var.set("-Playing")
        if not self.is_stop_clicked:
            self.scroll_track()
        pygame.mixer.music.unpause()

    def stop_song(self):
        self.status_var.set("-Stopped")
        self.track_var.set(self.playlist.get(tk.ACTIVE))
        pygame.mixer.music.stop()
        self.is_stop_clicked = True
        self.song_track.after_cancel(self.scroll_track)
        self.scroll_track()  # Reset the song track position

    def set_volume(self, value):
        pygame.mixer.music.set_volume(float(value) / 100)


if __name__ == "__main__":
    root = tk.Tk()
    MusicPlayerGUI(root)
    root.mainloop()
