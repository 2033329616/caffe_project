# encoding:utf-8

#加载模块与图像参数设置
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (10, 10)        # large images
plt.rcParams['image.interpolation'] = 'nearest'  # don't interpolate: show square pixels
plt.rcParams['image.cmap'] = 'gray' 

#模型路径deploy
import caffe
import os

caffe.set_mode_cpu()

model_def = caffe_root + 'examples/faceDetech/deploy.prototxt'
model_weights = caffe_root + 'examples/faceDetech/alexnet_iter_50000_full_conv.caffemodel'


#模型加载
net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)

transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
  # 那么reshape操作，就是自动将验证图片进行放缩
transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
  # transpose将RGB变为BGR,都要做transpose
  # BGR谁放在前面，譬如3*300*100，这里设定3在前面
transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
  # 像素点rescale操作，将数据的像素点集中在[0,255]区间内
transformer.set_channel_swap('data', (2,1,0))  

  # CPU classification              
 net.blobs['data'].reshape(50,        # batch size
                          3,         # 3-channel (BGR) images
                          227, 227) 

 image = caffe.io.load_image("/caffe/data/trainlmdb/val/test_female/image_00010.jpg") 
# 导入图片         
transformed_image = transformer.preprocess('data', image)        
# 预处理图片
output = net.forward()            
# 前向传播一次，找出参数
net.blobs['data'].data[...] = transformed_image         
output_prob = output['prob'][0]                
# 输出概率
print 'predicted class is:', output_prob.argmax() 
# 输出最大可能性