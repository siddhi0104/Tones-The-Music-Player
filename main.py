from tkinter import *
from tkinter import filedialog
import PIL
from PIL import ImageTk, Image
import tkinter.font as font
from pygame import mixer
import os

mixer.init()

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title('Tones Music Player')
        self.root.geometry('800x580')
        self.root.configure(background='black')

        # Variables to store the play/pause state and playlist
        self.is_playing = False
        self.is_paused = False
        self.current_song_index = None
        self.playlist = []

        # Adding label
        self.label = Label(self.root, text='Tones The Music Player', bg='#321431', fg='#ffffff', font=('league gothic', 18))
        self.label.place(x=50, y=20)

        # Adding image
        self.photo = ImageTk.PhotoImage(PIL.Image.open("GOOD VIBES.jpg"))
        self.photo_label = Label(self.root, image=self.photo, bg='white', borderwidth=0, highlightthickness=0, padx=0, pady=0)
        self.photo_label.place(x=50, y=70)

        # Label for status
        self.label1 = Label(self.root, text="Play the music", bg="black", fg='#ffffff', font=('algerian', 14))
        self.label1.pack(side=BOTTOM, fill=X)

        # Label for song name
        self.song_name_label = Label(self.root, text="No song loaded", bg="black", fg='#ffffff', font=('arial', 12))
        self.song_name_label.place(x=250, y=430)

        # Play/Pause button function
        def toggle_music():
            if self.is_paused:  # If music is paused, unpause it
                mixer.music.unpause()
                self.label1['text'] = 'Music Playing~'
                self.is_playing = True
                self.is_paused = False
                self.play_button.config(image=self.photo_pause)
            elif self.is_playing:  # If music is playing, pause it
                mixer.music.pause()
                self.label1['text'] = 'Music Paused.'
                self.is_paused = True
                self.is_playing = False
                self.play_button.config(image=self.photo_play)
            else:  # If no music is playing, start playing the loaded music
                if self.current_song_index is not None:
                    mixer.music.play()
                    self.label1['text'] = 'Music Playing~'
                    self.is_playing = True
                    self.is_paused = False
                    self.play_button.config(image=self.photo_pause)

        # Play/Pause button image
        self.photo_play = ImageTk.PhotoImage(PIL.Image.open('play button.jpg'))
        self.photo_pause = ImageTk.PhotoImage(PIL.Image.open('pause button.jpg'))

        # Play/Pause button
        self.play_button = Button(self.root, image=self.photo_play, borderwidth=0, highlightthickness=0, padx=0, pady=0, 
                                  activebackground='black', command=toggle_music)
        self.play_button.place(x=330, y=480)

        # Function to load music
        def load_music():
            files = filedialog.askopenfilenames(initialdir="/", title="Select Songs",
                                               filetypes=(("MP3 Files", "*.mp3"),))
            if files:
                self.playlist = list(files)  # Update the playlist
                self.playlistbox.delete(0, END)  # Clear the listbox first
                for song in self.playlist:
                    self.playlistbox.insert(END, os.path.basename(song))  # Add song names to the listbox
                if self.playlist:  # Automatically load the first song when playlist is loaded
                    self.current_song_index = 0
                    play_selected_song(None)

        # Function to play the selected song from the playlist
        def play_selected_song(event):
            selected_song_index = self.playlistbox.curselection()
            if selected_song_index:
                self.current_song_index = selected_song_index[0]
                mixer.music.load(self.playlist[self.current_song_index])
                mixer.music.play()
                self.song_name_label['text'] = os.path.basename(self.playlist[self.current_song_index])
                self.label1['text'] = 'Music Playing~'
                self.is_playing = True
                self.is_paused = False
                self.play_button.config(image=self.photo_pause)

        # Function to play the next song
        def next_song():
            if self.current_song_index is not None and len(self.playlist) > 1:
                self.current_song_index = (self.current_song_index + 1) % len(self.playlist)
                mixer.music.load(self.playlist[self.current_song_index])
                mixer.music.play()
                self.song_name_label['text'] = os.path.basename(self.playlist[self.current_song_index])
                self.label1['text'] = 'Playing Next Song~'
                self.is_playing = True
                self.is_paused = False
                self.play_button.config(image=self.photo_pause)

        # Function to play the previous song
        def previous_song():
            if self.current_song_index is not None and len(self.playlist) > 1:
                self.current_song_index = (self.current_song_index - 1) % len(self.playlist)
                mixer.music.load(self.playlist[self.current_song_index])
                mixer.music.play()
                self.song_name_label['text'] = os.path.basename(self.playlist[self.current_song_index])
                self.label1['text'] = 'Playing Previous Song~'
                self.is_playing = True
                self.is_paused = False
                self.play_button.config(image=self.photo_pause)

        # Load songs button (Resized image)
        load_button_img = PIL.Image.open('ls3.png')
        resized_img = load_button_img.resize((100, 50))  
        self.load_button_image = ImageTk.PhotoImage(resized_img)

        # Load songs button
        self.load_button = Button(self.root, image=self.load_button_image, borderwidth=0, highlightthickness=0, padx=0, pady=0, 
                                  activebackground='black', command=load_music)
        self.load_button.place(x=100, y=480)

        # Playlist area
        self.playlistbox = Listbox(self.root, bg="black", fg="white", font=('arial', 12), selectbackground='#6639b7')
        self.playlistbox.place(x=500, y=70, width=250, height=360)

        # Bind the Listbox selection to play the selected song
        self.playlistbox.bind('<<ListboxSelect>>', play_selected_song)

        # Previous button image
        self.photo_previous = ImageTk.PhotoImage(PIL.Image.open('previous.jpg'))

        # Previous button
        self.previous_button = Button(self.root, image=self.photo_previous, borderwidth=0, highlightthickness=0, padx=0, pady=0, 
                                      activebackground='black', command=previous_song)
        self.previous_button.place(x=260, y=480)

        # Next button image
        self.photo_next = ImageTk.PhotoImage(PIL.Image.open('next.jpg'))

        # Next button
        self.next_button = Button(self.root, image=self.photo_next, borderwidth=0, highlightthickness=0, padx=0, pady=0, 
                                  activebackground='black', command=next_song)
        self.next_button.place(x=400, y=480)

        # Volume control
        self.scale = Scale(self.root, from_=0, to=100, orient=HORIZONTAL, command=self.volume, fg='#6639b7', background='black', 
                           activebackground='black', highlightthickness=1, highlightbackground='#955891')
        self.scale.set(50)
        self.scale.place(x=500, y=488)

    # Volume function
    def volume(self, vol):
        volume = int(vol) / 100
        mixer.music.set_volume(volume)

# Initialize the main application window
root = Tk()
app = MusicPlayer(root)
root.mainloop()
