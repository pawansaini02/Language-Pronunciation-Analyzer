# import asyncio
# import time
# async def foo(text):
#     print(text)
#     await asyncio.sleep(1)
#     print(text)
#
# async def loop(text):
#     for x in range(10):
#         print(text)
#         await asyncio.sleep(1)
#
# async def main():
#     task1 = asyncio.create_task(loop("loop"))
#     task2 = asyncio.create_task(foo("foo"))
#     await task1
#
# asyncio.run(main())
# import pyaudio
# import wave
# import time
# import asyncio
# import tkinter as tk
# # import tkMessageBox
# # class Audio:
# #     def __init__(self):
# #         self.audio = pyaudio.PyAudio()
# #         self.frames = []
# #         self.sound_file = wave.open('test2.wav','wb')
# #         # self.stream = False
# #
# #     def start_audio(self):
# #         def callback(audiodevice, audiomemoryview,a,b):
# #             """This is called in the sound thread.
# #             Note, that the frequency and such you request may not be what you get.
# #             """
# #             # print(type(audiomemoryview), len(audiomemoryview))
# #             # print(audiodevice)
# #             self.frames.append(bytes(audiomemoryview))
# #         self.stop = 0
# #         self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True,frames_per_buffer=1024)
# #         for x in range(100):
# #             data = self.stream.read(1024)
# #             self.frames.append(data)
# #             # time.sleep(.1)
# #             print("Hi")
# #         self.stop_audio()
# #         #
# #
# #         #
# #
# #     def stop_audio(self):
# #         print("Done")
# #         self.stop = 1
# #         self.stream.stop_stream()
# #         self.stream.close()
# #         # self.stream.terminate()
# #         sound_file = wave.open('test2.wav', 'wb')
# #         sound_file.setnchannels(1)
# #         sound_file.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
# #         sound_file.setframerate(44100)
# #         sound_file.writeframes(b''.join(self.frames))
# #         sound_file.close()
import data as data
import requests
import pprint
import json
import http.client
import base64

def read_json(json_file):
    with open(json_file,'r') as f:
        data = json.load(f)
        return data
def dump_json(data,json_file):
    # data = json.loads(data)
    with open(json_file, 'w') as f:
        json.dump(data,f)

def get_audio_data(word):
    enc = base64.b64encode(open("output.wav", "rb").read())


    conn = http.client.HTTPSConnection("pronunciation-assessment1.p.rapidapi.com")

    headers = {
        'content-type': "application/json",
        'x-rapidapi-host': "pronunciation-assessment1.p.rapidapi.com",
        'x-rapidapi-key': "INSERT KEY HERE"
        }
    data = read_json('audio_detail.json')
    data["audio_base64"] = enc.decode("ascii")
    data["audio_format"] = "wav"
    data["text"] = word
    dump_json(data,"audio_detail.json")
    payload = json.dumps(read_json('audio_detail.json'))


    conn.request("POST", "/pronunciation", payload, headers)

    res = conn.getresponse()

#    data = res.read()
#    data = json.loads(data.decode("utf-8"))
#
#    dump_json(data,'audio_pronun_detail.json')
#    array_text = {"array":[],"score":0,"accent":[]}
#
#    for y in range(len(data["words"])):
#        array_text["array"].append([])
#        array_text["array"][y].append(data["words"][y]["label"])
#        for x in data["words"][y]["syllables"]:
#            array_text["array"][y].append([x["label"],x["score"]])


#    array_text["score"] = data["score"]
#    max_accent = max([data["accent_predictions"]["en_US"],data["accent_predictions"]["en_UK"],data["accent_predictions"]["en_AU"]])
#    max_accent_name = ""
#    if max_accent == data["accent_predictions"]["en_US"]:
#        max_accent_name = "en_US"
#    elif max_accent == data["accent_predictions"]["en_UK"]:
#        max_accent_name = "en_UK"
#    elif max_accent == data["accent_predictions"]["en_AU"]:
#        max_accent_name = "en_AU"
#    array_text["accent"].append(max_accent)
#    array_text["accent"].append(max_accent_name)
#    return array_text

#print(get_audio_data("Happy Joe"))

    response_data = json.loads(res.read().decode("utf-8"))
    dump_json(response_data, 'audio_pronun_detail.json')

    array_text = {"array": [], "score": 0, "accent": []}
    if "words" in response_data:
     for y in range(len(response_data["words"])):
        array_text["array"].append([])
        array_text["array"][y].append(response_data["words"][y]["label"])
        for x in response_data["words"][y]["syllables"]:
            array_text["array"][y].append([x["label"], x["score"]])

     array_text["score"] = response_data.get("score", 0)

     accent_predictions = response_data.get("accent_predictions", {})
     max_accent = max(accent_predictions.values(), default=0)
     max_accent_name = [k for k, v in accent_predictions.items() if v == max_accent]
     if max_accent_name:
         array_text["accent"].extend([max_accent, max_accent_name[0]])

     return array_text

print(get_audio_data("Happy Joe"))


