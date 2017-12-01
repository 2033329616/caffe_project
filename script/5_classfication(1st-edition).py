# coding=utf-8
# 加载必要的库
import numpy as np

import sys
import os
import cv2

# 设置当前目录
caffe_root = '/home/david/caffe-master/cifar10/'
# sys.path.insert(0, caffe_root + 'python')
import caffe
# os.chdir(caffe_root)

net_file = caffe_root + 'prototxt/cifar10_full_deploy.prototxt'
caffe_model = caffe_root + 'model/cifar10_full_iter_65000.caffemodel'
mean_file = caffe_root + 'data/lmdb/mean.npy'

net = caffe.Net(net_file, caffe_model, caffe.TEST)
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2, 0, 1))
transformer.set_mean('data', np.load(mean_file).mean(1).mean(1))
transformer.set_raw_scale('data', 255)
transformer.set_channel_swap('data', (2, 1, 0))

# im = caffe.io.load_image(caffe_root + 'data/image/test/9_1424.jpg')
im = caffe.io.load_image(caffe_root + 'script/test_img/fish-bike.jpg')
net.blobs['data'].data[...] = transformer.preprocess('data', im)
out = net.forward()
print(out)

labels_filename = caffe_root + 'script/test_img/class_labels.txt'
labels = np.loadtxt(labels_filename, str, delimiter='\n')
print(labels[0])
print(type(labels))
# top_k = net.blobs['prob'].data[0].flatten().argsort()[-1:-6:-1]
# for i in np.arange(top_k.size):
# print top_k[i], labels[top_k[i]]
output_prob = out['prob'][0]
print(output_prob)
class_num = output_prob.argmax()
# 输出概率
print('predicted class num is:', output_prob.argmax())
print('predicted class is:', labels[class_num])
print('predicted probability is:', output_prob[class_num])
# 输出最大可能性
im2 = cv2.resize(im, (512, 512))
cv2.imshow('image', im2)
cv2.waitKey(0)
