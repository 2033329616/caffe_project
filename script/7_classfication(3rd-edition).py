# coding=utf-8
# copyright david
"""
                             class_number
--------------------------------------------------------------------------------
'airplane' 'automobile' 'bird' 'cat' 'deer' 'dog' 'frog' 'horse' 'ship' 'truck'
    0           1          2     3     4      5      6      7       8      9
--------------------------------------------------------------------------------

"""
# 加载必要的库
import numpy as np
import sys
import os
import cv2
import caffe

# 设置当前目录
# sys.path.insert(0, caffe_root + 'python')
# os.chdir(caffe_root)

caffe_root   = '/home/david/caffe-master/cifar10/'
net_file     = caffe_root + 'prototxt/cifar10_full_deploy.prototxt'
caffe_model  = caffe_root + 'model/cifar10_full_iter_70000.caffemodel'
mean_file    = caffe_root + 'data/lmdb/mean.npy'
labels_file  = caffe_root + 'script/test_img/class_labels.txt'


class Net_Object(object):
	"""
	a class to init the net and predict the input image to return the probability

	"""
	def __init__(self,net_file, model, mean_file, labels_file):
		# init the net, 3 parameters
		self._net_file = net_file
		self._model = model
		self._mean_file = mean_file
		self._labels_file = labels_file
		self._net = caffe.Net(self._net_file, self._model, caffe.TEST)   # init the net

		self._transformer = caffe.io.Transformer({'data':self._net.blobs['data'].data.shape})   #?? 
		self._transformer.set_transpose('data', (2, 0, 1))
		self._transformer.set_mean('data', np.load(self._mean_file).mean(1).mean(1))      # ??
		self._transformer.set_raw_scale('data', 255)
		self._transformer.set_channel_swap('data', (2, 1, 0))   # ??

	def prediction(self, image):
		# image-the test image file; labels_file-the labels that includes all class and order number
		self._image = image

		img = caffe.io.load_image(self._image) # read the image
		img = cv2.resize(img, (50, 50))        # resize the input image 50*50
		self._net.blobs['data'].data[...] = self._transformer.preprocess('data', img)
		prob_out = self._net.forward()              # a dictionary which storges the probability of all class
		# {'prob': array([[  2.13724487e-02, .... ,2.64757383e-03]], dtype=float32)}
		output_prob = prob_out['prob'][0]
		print(output_prob)

		class_num = output_prob.argmax()  # find the number of the max probability
		labels = np.loadtxt(self._labels_file, str, delimiter='\n')  # read the txt && storge in the nparray
		print(labels)
		print('--------------------------------------------')
		print('{:>15}{:>3}{:^15}{:<20}'.format('class', ' ', 'class_num', 'probability'))
		print('{:>15}{:>3}{:^15}{:<20}'.format(labels[class_num], ' ', class_num, '%.3f' % output_prob[class_num]))
		print('--------------------------------------------')
		# top_k = net.blobs['prob'].data[0].flatten().argsort()[-1:-6:-1]
		# for i in np.arange(top_k.size):
		# print top_k[i], labels[top_k[i]]
		# show the image

	def show_image(self):
		img = cv2.imread(self._image, 1)
		img = cv2.resize(img, (512, 512))
		cv2.imshow(str(self._image).split('/')[-1], img)


if __name__ == '__main__':

	image_file = caffe_root + 'script/test_img/cat.jpg'
	image_file2 = caffe_root + 'data/image/test/1_305.jpg'
	image_list = [image_file, image_file2]
	net1 = Net_Object(net_file, caffe_model, mean_file, labels_file)
	for file in image_list:	
		net1.prediction(file)
		net1.show_image()
	cv2.waitKey(0)