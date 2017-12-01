#!/usr/bin/env sh
# This script converts the cifar data into leveldb format.
set -e

EXAMPLE=/home/david/caffe-master/cifar10/data/lmdb
DATA_HOME=/home/david/caffe-master/cifar10/data
CAFFE_HOME=/home/david/caffe-master
DBTYPE=lmdb

echo "Creating $DBTYPE..."

rm -rf $EXAMPLE/cifar10_train_$DBTYPE $EXAMPLE/cifar10_test_$DBTYPE

$CAFFE_HOME/build/tools/convert_imageset --shuffle \
   $DATA_HOME/image/train/  $DATA_HOME/label/train.txt \
   $EXAMPLE/cifar10_train_$DBTYPE

$CAFFE_HOME/build/tools/convert_imageset --shuffle \
   $DATA_HOME/image/test/  $DATA_HOME/label/test.txt \
   $EXAMPLE/cifar10_test_$DBTYPE


echo "Computing image mean..."

$CAFFE_HOME/build/tools/compute_image_mean -backend=$DBTYPE \
   $EXAMPLE/cifar10_train_$DBTYPE $EXAMPLE/mean.binaryproto

echo "Done."