""" pygame.examples.audiocapture
A pygame 2 experiment.
* record sound from a microphone
* play back the recorded sound
"""
import pygame as pg
import time
import wave
# from scipy.io.wavfile import write
from scipy.io import wavfile
import noisereduce as nr

from pygame._sdl2 import (
    get_audio_device_names,
    AudioDevice,
    AUDIO_F32,
    AUDIO_ALLOW_FORMAT_CHANGE,
)
from pygame._sdl2.mixer import set_post_mix



class audio():
    def __init__(self,sound,sound_chunks,audio):
        self.sound = sound
        self.sound_chunks = sound_chunks
        self.audio = audio
    def start_audio(self):
        pg.mixer.pre_init(44100, 32, 2, 512)
        pg.init()
        print(pg.mixer.get_init())
        names = get_audio_device_names(True)
        print(names)

        def callback(audiodevice, audiomemoryview):
            """This is called in the sound thread.
            Note, that the frequency and such you request may not be what you get.
            """
            # print(type(audiomemoryview), len(audiomemoryview))
            # print(audiodevice)
            self.sound_chunks.append(bytes(audiomemoryview))

        def postmix_callback(postmix, audiomemoryview):
            """This is called in the sound thread.
            At the end of mixing we get this data.
            """
            pass
            # print(type(audiomemoryview), len(audiomemoryview))
            # print(postmix)

        set_post_mix(postmix_callback)

        self.audio = AudioDevice(
            devicename=names[0],
            iscapture=True,
            frequency=44100,
            audioformat=AUDIO_F32,
            numchannels=2,
            chunksize=512,
            allowed_changes=0,
            callback=callback,
        )
        # start recording.
        self.audio.pause(0)

        print(self.audio)

        print("recording with '%s'" % names[0])

    def stop_audio(self):
        print("Turning data into a pg.mixer.Sound")
        self.sound = pg.mixer.Sound(buffer=b"".join(self.sound_chunks))

    def play_audio(self):
        print("playing back recorded sound")
        self.sound.play()
        while pg.mixer.get_busy():
            time.sleep(.1)
        print(pg.mixer.get_init())
        file = wave.open('test.wav','w')
        file.setnchannels(2)
        file.setframerate(44100)
        file.setsampwidth(4)
        file.writeframes(self.sound.get_raw())
        file.close()

        pg.quit()

audio1 = audio([],[],False)
audio1.start_audio()
input()
audio1.stop_audio()
time.sleep(2)
audio1.play_audio()

def clean_audio(file):
    print("Hi")
    # load data
    rate, data = wavfile.read(file)
    # perform noise reduction
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    wavfile.write("mywav_reduced_noise.wav", rate, reduced_noise)

clean_audio("test.wav")
