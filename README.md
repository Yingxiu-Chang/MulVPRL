# Multi-Supervised Contrastive Prospective Learning (MulSCPL) for Visual-based Mapless UAV Indoor Autonomous Navigation
This repository contains the trained MulSCPL model, codes for UAV control policy and experimental videos.

## Videos
Videos are availabel from [here](https://youtu.be/dcDI5X-VHJY) for real-world experiments. 

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

### Crazyflie preparation
Please follow the instructions of [Getting Started](https://www.bitcraze.io/documentation/tutorials/getting-started-with-crazyflie-2-x/) to assemble the Crazyflie and configure the client. 
### AI-deck preparation
Please follow the steps of [AI-deck](https://www.bitcraze.io/documentation/tutorials/getting-started-with-aideck/) to initialize the firmware and WiFi connection. 

### Real-world experiments
When finishing the Crazyflie and AI-deck preparations, download this repository and place the UAV in the experimental environments. Connecting the Crazyflie's Wifi hotspot, you can also double check the connection by going to the [AIdeck example repository](https://github.com/bitcraze/aideck-gap8-examples) and doing:
```
cd examples/other/wifi-img-streamer
python opencv-viewer.py
```
Finally, cd to this repository and typing followings for autonomous navigation. 
```
cd MulSCPL
python MulSCPL_UAV_control.py
```

Hope you will have fun with it. 
