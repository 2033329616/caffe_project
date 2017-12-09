#encoding:utf-8

#import
import wave
import numpy as np
import pyaudio
import matplotlib.pyplot as plt

def wavread(path):
	"""双通道"""
	wavfile =  wave.open(path,"rb")
	params = wavfile.getparams()
	framesra,frameswav= params[2],params[3]
	datawav = wavfile.readframes(frameswav)
	wavfile.close()
	datause = np.fromstring(datawav,dtype = np.short)
	datause.shape = -1,2
	datause = datause.T
	time = np.arange(0, frameswav) * (1.0/framesra)
	print('datause=', datause)
	print('time=', time)
	print(len(datause[0]))  #0为左通道,1为右通道
	print(len(time))
	return datause,time

def single_wavread(path):
	"""单通道"""
	wavfile =  wave.open(path,"rb")
	params = wavfile.getparams()
	framesra,frameswav= params[2],params[3]
	datawav = wavfile.readframes(frameswav)
	wavfile.close()
	datause = np.fromstring(datawav,dtype = np.short)
	time = np.arange(0, frameswav) * (1.0/framesra)
	print(abs(datause))
	print('datause=', datause)
	print('time=', time)
	print('mean=', np.average(abs(datause),weights=abs(datause))) #计算加权平均,提升输出值大权重的占比
	# print('mean=', np.max(abs(datause)))
	print(len(datause))
	print(len(time))
	return datause,time

def record():
	"""录音"""
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 16000
	RECORD_SECONDS = 5
	WAVE_OUTPUT_FILENAME = 'recorded_audio.wav'

	# if sys.platform == 'darwin':
	# 	CHANNELS = 1

	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					input=True,
					frames_per_buffer=CHUNK)   ##一个buffer存CHUNK个字节,作为一帧

	print("You can speak now:")

	frames = []  #存放音频数据

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)
	print("Please wait for recognizing ...")

	stream.stop_stream()
	stream.close()
	p.terminate()

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()
	print('-------------------------')
	wavfile = wave.open(WAVE_OUTPUT_FILENAME,"rb")
	print(wavfile)
	params = wavfile.getparams()

	framesra,frameswav= params[2],params[3]
	datawav = wavfile.readframes(frameswav)
	datause = np.fromstring(datawav,dtype = np.short)
	time = np.arange(0, frameswav) * (1.0/framesra)
	print(abs(datause))
	print('datause=', datause)
	print('time=', time)
	print('mean=', np.average(abs(datause),weights=abs(datause))) #计算加权平均,提升输出值大权重的占比

	plt.title("Night.wav's Frames")
	plt.plot(time, abs(datause),color = 'green')
	plt.show()

	

# path = input('test_2_high.wav')
record()
# wavdata,wavtime = single_wavread('test_low.wav')
# wavdata2,wavtime2 = single_wavread('test_lowest.wav')
# plt.title("Night.wav's Frames")
# plt.subplot(211)
# plt.plot(wavtime, abs(wavdata),color = 'green')
# plt.subplot(212)
# plt.plot(wavtime2, abs(wavdata2),color = 'red')
# plt.show()