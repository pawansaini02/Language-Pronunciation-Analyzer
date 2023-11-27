import pyaudio
import wave
import time
import asyncio
import tkinter as tk
import json
import random
from gtts import gTTS
from playsound import playsound
import get_audio_data
from tkinter import ttk
from tkscrolledframe import ScrolledFrame
# import tkinter as tk


import requests
import os
playing = input("Tongue/One:")

def play_word(word):
    myobj = gTTS(text=word, lang="en", slow=False)
    myobj.save("play_word.mp3")
    playsound('play_word.mp3')

def read_json(json_file):
    with open(json_file,'r') as f:
        data = json.load(f)
        return data
def dump_json(data,json_file):
    # data = json.loads(data)
    with open(json_file, 'w') as f:
        json.dump(data,f)

def start_audio(word):
    audio = pyaudio.PyAudio()
    frames = []
    sound_file = wave.open('test2.wav', 'wb')

    stop = 0
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    if playing == "One":
        range_ = 100
    elif playing == "Tongue":
        range_ = 150
    for x in range(range_):
        data = stream.read(1024)
        frames.append(data)
        print(range_-x)

    print("DOne")
    stream.stop_stream()
    stream.close()
    # stream.terminate()
    sound_file = wave.open('output.wav', 'wb')
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()
    print("Recording DOne")

    # key = "Insert your API key here"
    # api_endpoint = "Insert your API end point here"
    # url = api_endpoint + "/api/scoring/text/v0.5/json"
    # dialect = "en-us"
    # user_id = "81ozow"
    # url += '?' + 'key=' + key + '&dialect=' + dialect + '&user_id=' + user_id
    # payload = {'text': word};
    # user_file_handle = open('output.wav', 'rb')
    # files = {'user_audio_file': user_file_handle}
    # response = requests.post(url, data=payload, files=files).text
    # print(response)
    response = get_audio_data.get_audio_data(word)
    print(response)


    clear = tk.Label(top,text="                                                                                                    \n                                                                                                                                       ")
    clear.pack()
    clear.grid(row=3, column=0, columnspan=2, padx=5, pady=1)

    rows = 5 - 1
    for x in range(100):
        clear = tk.Label(top,text="                                                                                                                                                                                                                ")
        clear.pack()
        clear.grid(row=rows+x,column=0,columnspan=2,padx=5,pady=1)

    array_text = []


    word_text = word+"\n"
    for x in range(len(response["array"])):
        for y in range(len(response["array"][x])-1):
            word_text += response["array"][x][y+1][0]
            word_text += "-"
        word_text = word_text[:-1]

        word_text += " "
    word_text = word_text[:-1]
    text = tk.Label(top,text=word_text,font=("Arial", 15))
    text.pack()
    text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)


    text2 = tk.Label(top,text="Score: "+str(response["score"]),font=("Arial", 12))
    text2.pack()
    text2.grid(row=4, column=0, columnspan=2, padx=5, pady=1)


    labels = []
    for x in range(len(response["array"])):
        rows += 1
        labels.append([tk.Label(top,text=response["array"][x][0],font=("Arial", 15))])
        labels[x][0].pack()
        labels[x][0].grid(row=rows,column=0,columnspan=2,padx=5,pady=1)
        labels[x].append([])
        for y in range(len(response["array"][x])-1):
            rows += 1
            z = y + 1
            labels[x][1].append(tk.Label(top,text=response["array"][x][z][0],font=("Arial", 10)))
            labels[x][1][y*2].pack()
            labels[x][1][y*2].grid(row=rows, column=0, columnspan=1, padx=5, pady=1)
            labels[x][1].append(tk.Label(top,text=response["array"][x][z][1],font=("Arial", 10)))
            labels[x][1][y*2+1].pack()
            labels[x][1][y*2+1].grid(row=rows, column=1, columnspan=1, padx=5, pady=1)
    print(labels)




# Create a root window
root = tk.Tk()
root.geometry("1200x800")
root.title("Language Pronunciation Technology")
frame_top = tk.Frame(root, width=400, height=250)
frame_top.pack(side="top", expand=1, fill="both")
# Create a ScrolledFrame widget
sf = ScrolledFrame(frame_top, width=380, height=240)
sf.pack(side="top", expand=1, fill="both")
# Bind the arrow keys and scroll wheel
sf.bind_arrow_keys(frame_top)
sf.bind_scroll_wheel(frame_top)
top = sf.display_widget(tk.Frame)



entry = tk.Entry(top,width=70,borderwidth=5)
entry.grid(row=1,column=0,columnspan=2, padx=5,pady=5)
if playing == "One":
    words = read_json('words.json')["hard_words"]
elif playing == "Tongue":
    words = read_json('words.json')["Tongue"]
word = random.choice(words)
entry.insert(0,word)

button_1 = tk.Button(top,text="Start Recording",padx=40,pady=20,command=lambda: start_audio(entry.get()))
button_1.pack()
button_1.grid(row=2,column=0,columnspan=2, padx=10,pady=5)

button_2 = tk.Button(top,text="How to say it?",padx=40,pady=20,command=lambda: play_word(entry.get()))
button_2.pack()
button_2.grid(row=0,column=0,columnspan=2, padx=10,pady=5)

root.mainloop()
