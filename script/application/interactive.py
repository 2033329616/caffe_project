#encoding:utf-8

import voice.voice_recognition as rec   #导入语音识别
import voice.voice_generate as syn      #导入语音合成
import voice.turing as tur
import network.classfication as net
import random
import os

# 图像分类的网络参数路径
"""['airplane' 'automobile' 'bird' 'cat' 'deer' 'dog' 'frog' 'horse' 'ship'
 'truck']"""
caffe_root   = '/home/david/caffe-master/cifar10/'
net_file     = caffe_root + 'prototxt/cifar10_full_deploy.prototxt'
caffe_model  = caffe_root + 'model/cifar10_full_iter_70000.caffemodel'
mean_file    = caffe_root + 'data/lmdb/mean.npy'
labels_file  = caffe_root + 'script/test_img/class_labels.txt'
image_path   = caffe_root + 'script/test_img/picture/'

if __name__ == '__main__':
	content = ''
	robot_rec = rec.voice_recognition()   #初始化一个语音识别类
	voice = syn.voice_synthesis()         #初始化一个语音合成类	
	understand = tur.turing()             #初始化一个图灵机器人类
	classfy_net = net.Net_Object(net_file, caffe_model, mean_file, labels_file)    #初始化图像分类网络类

	file_list = os.listdir(image_path)    #列出测试图像的文件名
	# print(file_list)
	# for i in range(len(file_list)):
	# 	if 'wrong' not in file_list[i]:
	# 		print('**********************************************************')
	# 		print(file_list[i])
	# 		classfy_net.prediction(image_path + file_list[i])
	# classfy_net.show_image()
	# print(random.randint(0, 9))

	while True:
		content = robot_rec.recognition()    #返回语音识别的内容
		if content != '':                    #已经识别成功,开始交互
			if '图像' in content:
				# print('robot: 开始识别图像')
				voice.play_audio('我已经开始识别图像了')
				index = random.randint(0, 32)   #随机识别一个类
				classfy_net.prediction(image_path + file_list[index])
				classfy_net.show_image()
			else:
				interactive_content = understand.interactive(content)
				voice.play_audio(interactive_content)
