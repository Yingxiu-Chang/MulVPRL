# Multi-Supervised Contrastive Prospective Learning (MulSCPL) for Visual-based Mapless UAV Indoor Autonomous Navigation
This repository contains the trained MulSCPL model, codes for UAV control policy and experimental videos.

## Introduction
The MulSCPL aims to simultaneously learn the prospective regression-aware and classification-aware representations based on contrastive learning for Visual-based Mapless UAV Indoor Autonomous Navigation. The experiments were conducted in real-world environments upon Nano-UAV (Crazyflie). We released our trained MulSCPL model along with codes for convenient verification and shared the recorded videos.

## Running the code
### Requirements
This code has been tested on Ubuntu 20.04, and on Python 3.7.

Dependencies:
* TensorFlow 2.6.0
* Keras 2.6.0 (Make sure that the Keras version is correct!)
* NumPy 1.21.5
* OpenCV 4.8.0
* scipy 1.7.3
* Python gflags
* Python matplotlib
* h5py 3.1.0
