#!/bin/bash

DATA_HOME=/home/david/caffe-master/cifar10/data

echo "Creating train.txt..."
rm -rf $DATA_HOME/label/train.txt
cd $DATA_HOME/image/train
for file in $(ls *)
do
	class_num=$(echo $file | cut -d '_' -f 1)
	echo $file ${class_num} | tee -a $DATA_HOME/label/train.txt
done

echo "Creating test.txt..."
rm -rf $DATA_HOME/label/test.txt
cd $DATA_HOME/image/test
for file in $(ls *)
do
	class_num=$(echo $file | cut -d '_' -f 1)
	echo $file ${class_num} | tee -a $DATA_HOME/label/test.txt
done