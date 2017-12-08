# encoding:utf-8

from aip import AipSpeech
import pyaudio
import wave
import sys
import os

#语音合成的类,初始化和合成
class voice_synthesis(object):
	#初始化语音合成模块
	def __init__(self):
		""" 你的 APPID AK SK """
		self._APP_ID = '10501233'
		self._API_KEY = 'myUhj7qGUQ8q5mzrBf3tGlVK'
		self._SECRET_KEY = '6ac3caabde6ddad16bb5b933977761df'
		self._aipSpeech = AipSpeech(self._APP_ID, self._API_KEY, self._SECRET_KEY)

	#语音合成函数,输入:要合成的语句;返回输出的音频文件
	def synthesis(self, speech_str):
		result  = self._aipSpeech.synthesis(speech_str, 'zh', 1, {'vol': 5,})
		saved_audio = 'syn_auido.wav'
		# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
		if not isinstance(result, dict):
			with open(saved_audio, 'wb') as f:
				f.write(result)
		# print('write done!')
		return saved_audio


	# 播放生成的音频,输入参数:音频文件
	def play_audio(self, audio_str):
		CHUNK = 1024
		# if len(sys.argv) < 2:
		# 	print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
		# 	sys.exit(-1)
		file_name = self.synthesis(audio_str)
		if os.path.exists('temp.wav'):
			os.remove('temp.wav')
		os.system('ffmpeg -i ' + file_name + ' temp.wav')   #将mped格式音频转换为wave格式
		
		with wave.open('temp.wav', 'rb') as wf:
			# instantiate PyAudio (1)
			p = pyaudio.PyAudio()

			# open stream (2)
			stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
							channels=wf.getnchannels(),
							rate=wf.getframerate(),
							output=True)

			# read data
			data = wf.readframes(CHUNK)

			# play stream (3)
			while len(data) > 0:
				stream.write(data)
				data = wf.readframes(CHUNK)

			# stop stream (4)
			stream.stop_stream()
			stream.close()

			# close PyAudio (5)
			p.terminate()

if __name__ == '__main__':
	voice = voice_synthesis()
	voice.play_audio('好的主人,我为你打开相册')