#encoding:utf-8

import voice.voice_recognition as rec   #导入语音识别
import voice.voice_generate as syn      #导入语音合成

if __name__ == '__main__':
	content = ''
	robot_rec = rec.voice_recognition()  #初始化一个类
	content = robot_rec.recognition()    #返回语音识别的内容

	voice = syn.voice_synthesis()
	voice.play_audio('我是中国人')