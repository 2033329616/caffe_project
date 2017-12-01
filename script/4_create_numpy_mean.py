import caffe
import numpy as np

# 待转换的pb格式图像均值文件路径
MEAN_PROTO_PATH = '/home/david/caffe-master/cifar10/data/lmdb/mean.binaryproto'
# 转换后的numpy格式图像均值文件路径
MEAN_NPY_PATH = '/home/david/caffe-master/cifar10/data/lmdb/mean.npy'

blob = caffe.proto.caffe_pb2.BlobProto()           # 创建protobuf blob
data = open(MEAN_PROTO_PATH, 'rb').read()         # 读入mean.binaryproto文件内容
blob.ParseFromString(data)                         # 解析文件内容到blob

# 将blob中的均值转换成numpy格式，array的shape （mean_number，channel, hight, width）
array = np.array(caffe.io.blobproto_to_array(blob))
# 一个array中可以有多组均值存在，故需要通过下标选择其中一组均值
mean_npy = array[0]
np.save(MEAN_NPY_PATH, mean_npy)