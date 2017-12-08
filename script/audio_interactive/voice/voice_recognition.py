# encoding:utf-8

import pyaudio
import wave
import sys
from aip import AipSpeech



class voice_recognition(object):
	"""语音识别类"""

	def __init__(self):
		""" 你的 APPID AK SK """
		self._APP_ID = '10498635'
		self._API_KEY = '7H3a8MI3qNAb9N4RunPegIpr'
		self._SECRET_KEY = 'aac58e43cc056ca4b616040df77bd845'
		self._aipSpeech = AipSpeech(self._APP_ID, self._API_KEY, self._SECRET_KEY)

	# record the  sound and write in the wav file
	def record(self):
		CHUNK = 1024
		FORMAT = pyaudio.paInt16
		CHANNELS = 1
		RATE = 16000
		RECORD_SECONDS = 5
		self._WAVE_OUTPUT_FILENAME = 'recorded_audio.wav'

		if sys.platform == 'darwin':
			CHANNELS = 1

		p = pyaudio.PyAudio()

		stream = p.open(format=FORMAT,
						channels=CHANNELS,
						rate=RATE,
						input=True,
						frames_per_buffer=CHUNK)

		print("You can speak now:")

		frames = []

		for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
			data = stream.read(CHUNK)
			frames.append(data)

		print("Please wait for recognizing ...")

		stream.stop_stream()
		stream.close()
		p.terminate()

		wf = wave.open(self._WAVE_OUTPUT_FILENAME, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		wf.close()

		return self._WAVE_OUTPUT_FILENAME

	# recognition the voice
	def recognition(self):
		# aipSpeech.setConnectionTimeoutInMillis(3000)
		# aipSpeech.setSocketTimeoutInMillis(5000)
		file_name = self.record()   #调用录音函数
		with open(file_name, 'rb') as wav_file:
			# 识别本地文件
			# a= aipSpeech.asr(get_file_content('public/test.pcm'), 'pcm', 16000, { 'lan': 'zh',})
			a =self._aipSpeech.asr(wav_file.read(), 'wav', 16000, { 'lan': 'zh',})
			# print(a)
			print('human:', a['result'][0].strip().strip('，'))

if __name__ == '__main__':
	voice = voice_recognition()  #实例化一个类
	voice.recognition()          #调用识别函数
