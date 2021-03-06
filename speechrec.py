import wave
import os
import pyaudio
import speech_recognition as sr
import shutil
import time
from google_images_search.fetch_resize_save import FetchResizeSave
from google_images_search import GoogleImagesSearch
import cv2

r = sr.Recognizer()
mic = sr.Microphone(device_index=5)
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 2
API_KEY= 'AIzaSyCki8KIN6wWL06X5bvbVVykYBrLgQoMofw'
CX = '009518592146397428949:hm3iqr4gpv4'
gis = GoogleImagesSearch(API_KEY, CX)
WAVE_OUTPUT_FILENAME = "recorded_audio.wav"
frames = []

query_images = {
        'images': [],
        'coords': []
    }

def get_image(self):
    # Audio
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("recording...")
    # frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
    print("finished recording")
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    raud = sr.AudioFile(r'D:\LiveED\LiveEd_2\recorded_audio.wav')
    with raud as source:
        raudio = r.record(source)
        word = r.recognize_google(raudio)
        _search_params = {
            'q': word,
            'num': 1,
            'searchType': 'image'
        }
        if os.path.exists(r"D:\LiveED\LiveEd_2\pics"):
            shutil.rmtree(r'D:\LiveED\LiveEd_2\pics')
        gis.search(search_params=_search_params, path_to_dir=r'D:\LiveED\LiveEd_2\pics')

        pic = os.listdir(r'D:\LiveED\LiveEd_2\pics')[0]
        global picfname
        picfname = os.path.join('D:\LiveED\LiveEd_2\pics', pic)

        query_img = cv2.imread(picfname)
        query_img = cv2.resize(query_img, (128, 128))
        query_images['images'].append(query_img)
        query_images['coords'].append(1)
        print("Your word: " + word)
    buffer = 1
    render_image = True
    self.query_image = picfname

get_image()