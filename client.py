import socket
from threading import Thread
import os
import time

from tkinter import *
from tkinter import ttk, filedialog
import ftplib
from ftplib import FTP
import ntpath
from pathlib import Path

from playsound import playsound
import pygame
from pygame import mixer

SERVER = None
IP_ADDRESS = '127.0.0.1'
PORT = 8050
BUFFER_SIZE = 4096

name = None
listbox =  None
infoLabel = None
playButton = None
filePathLabel = None

song_counter = 0
song_selected = None
playtime = 0
pause = False

font = "Calibri"

def play():
  global song_selected
  song_selected = listbox.get(ANCHOR)

  pygame
  mixer.init()
  mixer.music.load("shared_files/"+song_selected)
  mixer.music.play()
  if(song_selected != ""):
    infoLabel.configure(text="Now Playing: "+song_selected)
    playButton.configure(text="I I", command=pause)
  else:
    infoLabel.configure(text="")

def pause():
  global playtime, pause
  pause = not pause

  pygame
  mixer.init()
  mixer.music.load("shared_files/"+song_selected)
  mixer.music.pause()

  if pause:
    # resume
    playButton.configure(text="I I")
    mixer.music.play(start=playtime/1000)
  else:
    # pause
    playButton.configure(text="▶")
    playtime = mixer.music.get_pos() + playtime

def stop():
  global playtime
  playtime = 0

  pygame
  mixer.init()
  mixer.music.load("shared_files/"+song_selected)
  mixer.music.pause()
  print(mixer.music.get_pos())
  infoLabel.configure(text="")
  playButton.configure(text="▶", command=play)

def skip(dir):
  global playtime

  pygame
  mixer.init()
  mixer.music.load("shared_files/"+song_selected)
  mixer.music.pause()

  if dir:
    playtime = mixer.music.get_pos() + playtime + 5000
    if(playtime < 0): playtime = 0
  else:
    playtime = mixer.music.get_pos() + playtime - 5000
  
  mixer.music.play(start=playtime/1000)
  playButton.configure(text="I I")

def musicWindow():
  global listbox, infoLabel, playButton
  global song_counter

  window = Tk()
  window.title("Music Window")
  window.geometry("300x300")
  window.configure(bg="#87CEFA")

  selectLabel = Label(window, text="Select Song", bg="#87CEFA", font=(font, 8))
  selectLabel.place(x=2, y=1)

  listbox = Listbox(window, height=10, width=39, activestyle="dotbox", bg="#87CEFA", borderwidth=2, font=(font, 10))
  listbox.place(x=10, y=18)

  for file in os.listdir("shared_files"):
    fileName = os.fsdecode(file)
    listbox.insert(song_counter, fileName)
    song_counter = song_counter + 1

  scrollbar1 = Scrollbar(listbox)
  scrollbar1.place(relheight=1, relx=1)
  scrollbar1.config(command=listbox.yview)

  playButton = Button(window, text="▶", width=4, bg="#87CEFA", bd=0, font=(font, 20, "bold"), command=play)
  playButton.place(x=85, y=185)

  stopButton = Button(window, text="■", width=4, bg="#87CEFA", bd=0, font=(font, 20), command=stop)
  stopButton.place(x=215, y=185)

  rewindButton = Button(window, text="I🞀🞀", width=4, bg="#87CEFA", bd=0, font=(font, 20), command=lambda: skip(False))
  rewindButton.place(x=20, y=185)

  forwardButton = Button(window, text="🞂🞂I", width=4, bg="#87CEFA", bd=0, font=(font, 20), command=lambda: skip(True))
  forwardButton.place(x=150, y=185)

  uploadButton = Button(window, text="Upload", width=10, bg="#87CEEB", bd=1, font=(font, 10), command=browseFiles)
  uploadButton.place(x=40, y=250)

  downloadButton = Button(window, text="Download", width=10, bg="#87CEEB", bd=1, font=(font, 10))
  downloadButton.place(x=180, y=250)

  infoLabel = Label(window, text="", bg="#87CEEB", fg="#00F", font=(font, 8))
  infoLabel.place(x=4, y=280)

  window.resizable(False, False)
  window.mainloop()

def browseFiles():
  try:
    fileName = filedialog.askopenfilename()
    HOSTNAME = '127.0.0.1'
    USERNAME = "lftpd"
    PASSWORD = "lftpd"

    ftp_server = FTP(HOSTNAME, USERNAME, PASSWORD)
    ftp_server.encoding = "utf-8"
    ftp_server.cwd("shared_files")
    fName = ntpath.basename(fileName)
    with open(fileName, "rb") as file:
      ftp_server.storbinary(f"STOR {fName}", file)

    ftp_server.dir()
    ftp_server.quit()

  except FileNotFoundError:
    print("Cancel Button Pressed")

def setup():
  global SERVER, IP_ADDRESS, PORT
  SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  SERVER.connect((IP_ADDRESS, PORT))

  musicWindow()

setup()