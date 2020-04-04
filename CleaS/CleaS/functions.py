import requests
import json
import sounddevice as sd
from scipy.io.wavfile import write
from .settings import API_ENDPOINT, TOKEN


def recognize_speech(AUDIO_FILENAME):
	"""Speech to text"""
	headers = {'Authorization': 'Bearer ' + TOKEN, 'Content-Type': 'audio/wav'}
	resp = requests.post(API_ENDPOINT, headers=headers, data=open(AUDIO_FILENAME, 'rb'))
	return resp.json()['_text']


def audio_recording(filename, seconds:int=3):
	"""Audio recording in filename (duration: seconds)"""
	fs = 44100
	myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
	sd.wait()
	write(filename, fs, myrecording)
