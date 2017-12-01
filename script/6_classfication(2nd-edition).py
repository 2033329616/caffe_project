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

# init the net then return a dictionary of prediction probability 
def net_init(net_file, model, mean_file, image):
    net = caffe.Net(net_file, model, caffe.TEST)    # init the net
    # net.blobs['data'].reshape(1, 3, 32, 32)
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

    transformer.set_transpose('data', (2, 0, 1))    # ??
    transformer.set_mean('data', np.load(mean_file).mean(1).mean(1))
    transformer.set_raw_scale('data', 255)          # scale the image 0~1 -> 0~255
    transformer.set_channel_swap('data', (2, 1, 0))  # ??

    img = caffe.io.load_image(image)   # load the image
    img = cv2.resize(img, (50, 50))
    # cv2.imshow('123', img)
    net.blobs['data'].data[...] = transformer.preprocess('data', img)  #??

    out = net.forward()  # a dictionary which storges the probability of all class
    # {'prob': array([[  2.13724487e-02, .... ,2.64757383e-03]], dtype=float32)}
    return out

# print the class information of the input image
def prediction(prob_out, labels_file):
	output_prob = prob_out['prob'][0]
	print(output_prob)
	class_num = output_prob.argmax()  # find the number of the max probability
	labels = np.loadtxt(labels_file, str, delimiter='\n')  # read the txt && storge in the nparray
	print(labels)
	print(labels[0])
	print('--------------------------------------------')
	print('{:>15}{:>3}{:^15}{:<20}'.format('class', ' ', 'class_num', 'probability'))
	print('{:>15}{:>3}{:^15}{:<20}'.format(labels[class_num], ' ', class_num, '%.3f' % output_prob[class_num]))
	print('--------------------------------------------')
	# top_k = net.blobs['prob'].data[0].flatten().argsort()[-1:-6:-1]
	# for i in np.arange(top_k.size):
	# print top_k[i], labels[top_k[i]]
	# show the image
def show_image(image_file):
	img = cv2.imread(image_file, 1)
	img = cv2.resize(img, (512, 512))
	cv2.imshow('image', img)
	cv2.waitKey(0)


if __name__ == '__main__':
	net_out = dict()
	image_file = caffe_root + 'script/test_img/cat.jpg'
	# image_file = caffe_root + 'data/image/test/1_305.jpg'
	net_out = net_init(net_file, caffe_model, mean_file, image_file)  # init the net
	prediction(net_out, labels_file)
	show_image(image_file)