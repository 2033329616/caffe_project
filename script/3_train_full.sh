#!/usr/bin/env sh
set -e
CAFFE_HOME=/home/david/caffe-master
CIFAR10_HOME=/home/david/caffe-master/cifar10

TOOLS=$CAFFE_HOME/build/tools

$TOOLS/caffe train \
    --solver=${CIFAR10_HOME}/prototxt/cifar10_full_solver.prototxt $@

# reduce learning rate by factor of 10
$TOOLS/caffe train \
    --solver=${CIFAR10_HOME}/prototxt/cifar10_full_solver_lr1.prototxt \
    --snapshot=${CIFAR10_HOME}/model/cifar10_full_iter_60000.solverstate $@

# reduce learning rate by factor of 10
$TOOLS/caffe train \
    --solver=${CIFAR10_HOME}/prototxt/cifar10_full_solver_lr2.prototxt \
    --snapshot=${CIFAR10_HOME}/model/cifar10_full_iter_65000.solverstate $@
