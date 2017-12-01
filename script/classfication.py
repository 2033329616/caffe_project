# 加载模块与图像参数设置
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (10, 10)        # large images
# don't interpolate: show square pixels
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

# 模型路径deploy
import caffe
# import os

caffe_root = '/home/david/caffe-master/cifar10/'
caffe.set_mode_gpu()

model_def = caffe_root + 'prototxt/cifar10_full.prototxt'
model_weights = caffe_root + 'model/cifar10_full_iter_65000.caffemodel'
mean_file = caffe_root + 'data/lmdb/mean.npy'

# 模型加载
# defines the structure of the model # contains the trained weights
net = caffe.Net(model_def, model_weights, caffe.TEST)

transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
# 那么reshape操作，就是自动将验证图片进行放缩
# move image channels to outermost dimension
transformer.set_transpose('data', (2, 0, 1))
# transpose将RGB变为BGR,都要做transpose
# BGR谁放在前面，譬如3*300*100，这里设定3在前面
transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
# 像素点rescale操作，将数据的像素点集中在[0,255]区间内
transformer.set_channel_swap('data', (2, 1, 0))

transformer.set_mean('data', np.load(mean_file).mean(1).mean(1))
# CPU classification
net.blobs['data'].reshape(1, 3, 32, 32)            # batch size
# 3-channel (BGR) images


image = caffe.io.load_image(caffe_root + "data/image/test/9_1424.jpg")
# 导入图片
transformed_image = transformer.preprocess('data', image)
# 前向传播一次，找出参数
net.blobs['data'].data[...] = transformed_image
# 预处理图片
output = net.forward()

output_prob = output['prob'][0]
print(output_prob)
# 输出概率
print('predicted class is:', output_prob.argmax())
# 输出最大可能性
