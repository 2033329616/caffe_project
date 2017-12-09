# encoding:utf-8

import pyaudio
import wave
import sys
import numpy as np
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


	# 判断是否有声音录入,有则返回1,无返回0,读取录制好的音频,看它的帧数
	def speaking(self, audiofile, threshold=70):
		wavfile = wave.open(audiofile, "rb")
		# print(wavfile)
		params = wavfile.getparams()
		framesra,frameswav= params[2],params[3]
		datawav = wavfile.readframes(frameswav)
		datause = np.fromstring(datawav,dtype = np.short)
		average = np.average(abs(datause),weights=abs(datause))
		time = np.arange(0, frameswav) * (1.0/framesra)
		# print(abs(datause))
		# print('datause=', datause)
		# print('time=', time)
		# print('average=', average) #计算加权平均,提升输出值大权重的占比
		if average > threshold:    #大于阈值,有声音录入
			return True
		else:
			return False

	# recognition the voice
	def recognition(self):
		# aipSpeech.setConnectionTimeoutInMillis(3000)
		# aipSpeech.setSocketTimeoutInMillis(5000)
		file_name = self.record()   #调用录音函数
		if self.speaking(file_name):  #有声音录入
			print("Please wait for recognizing ...")
			with open(file_name, 'rb') as wav_file:
				# 识别本地文件
				#print(type(wav_file))
				# a= aipSpeech.asr(get_file_content('public/test.pcm'), 'pcm', 16000, { 'lan': 'zh',})
				reponse_result =self._aipSpeech.asr(wav_file.read(), 'wav', 16000, { 'lan': 'zh',})
				if len(reponse_result)>3:    #识别错误后返回3个长度的字典
					rec_content = reponse_result['result'][0].strip().strip('，')
					print('human:', rec_content)
					return rec_content
				else:
					print(reponse_result)
					print("robot: sorry, I can't listen clearly!")
					return ''    # 如果识别失败返回空字符
		else:
			print('robot: Please continue to speak!')
			return ''           # 如果没有声音录入也返回空字符

if __name__ == '__main__':
	voice = voice_recognition()  #实例化一个类
	content = voice.recognition()          #调用识别函数
	# print(content)
