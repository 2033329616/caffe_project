#encoding:utf-8

import re
import os

class_name = ['飞机','汽车','鸟','猫','鹿','狗','青蛙','马','船','卡车']

def count_substring(string, sub_string):
	reg=re.compile("(?="+sub_string+")")
	length=len(reg.findall(string))
	return length


if __name__ == '__main__':
	# string = input().strip()
	# sub_string = input().strip()
	# count = count_substring(string,sub_string)
	# print (count)
	s = '识别一个猫的图猫像'
	# for content in class_name:
	# 	print('***', content, '****')
	# 	print('***', content.strip(), '****')
	# 	print(len(content))
	# 	print(type(content))
	# 	result = s.find('猫的')
	# 	index = s.index('猫')   #??????为什么换成变就出现错
	# 	print('result=',result,'index=', index)

	# if os.path.isfile('/home/david/caffe-master/cifar10/script/test_img/0_10.jpg'):
	# 	print('hahahha')
	# if os.path.isdir('/home/david/caffe-master/cifar10/script/test_img/picture/wrong_img'):
	# 	print('lalalal')

	if '2' or '3'  in s:
		print('in the string')
		print(('2'in s) or ('个' in s))
	else:
		print('not in the string')