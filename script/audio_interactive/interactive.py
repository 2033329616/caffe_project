#encoding:utf-8

import voice.voice_recognition as rec   #导入语音识别
import voice.voice_generate as syn      #导入语音合成
import voice.turing as tur

if __name__ == '__main__':
	content = ''
	robot_rec = rec.voice_recognition()   #初始化一个语音识别类
	voice = syn.voice_synthesis()         #初始化一个语音合成类	
	understand = tur.turing()             #初始化一个图灵机器人类

	while True:
		content = robot_rec.recognition()    #返回语音识别的内容
		if content != '':                    #已经识别成功,开始交互
			interactive_content = understand.interactive(content)
			voice.play_audio(interactive_content)

		# interactive_content = understand.interactive('哈哈哈')
		# print(content)