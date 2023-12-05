# ------------------------------------------------------------------
# File Name:        MulSCPL for UAV autonomous navigation control
# Author:           Yingxiu-Chang
# Version:          v1
# Created:          2023/12/05
# ------------------------------------------------------------------
import argparse
import socket, struct, time
import numpy as np
from tensorflow.keras.models import model_from_json
import cv2
from pynput import keyboard

import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

# Args for setting IP/port of AI-deck. Default settings are for when
# AI-deck is in AP mode.
parser = argparse.ArgumentParser(description='Connect to AI-deck JPEG streamer example')
parser.add_argument("-n", default="192.168.4.1", metavar="ip", help="AI-deck IP")
parser.add_argument("-p", type=int, default='5000', metavar="port", help="AI-deck port")
parser.add_argument('--save', action='store_true', help="Save streamed images")
args = parser.parse_args()

deck_port = args.p
deck_ip = args.n

print("Connecting to socket on {}:{}...".format(deck_ip, deck_port))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((deck_ip, deck_port))
print("Socket connected")

imgdata = None
data_buffer = bytearray()

URI = 'radio://0/80/2M'
running = True

# Parameters of UAV control policy
alpha = 0.2 
beta = 0.5
vk = 0
tk = 0
Vmax = 0.2 # Can be customized depending on experimental environments
Smax = 40.0

# Receiving bytes from Crazyflie
def rx_bytes(size):
    data = bytearray()
    while len(data) < size:
        data.extend(client_socket.recv(size - len(data)))
    return data

# Image pre-processing
def process_img(img, target_size):
    img = cv2.resize(img, target_size)
    img = img.reshape((img.shape[0], img.shape[1], 1))

    return np.asarray(img, dtype=np.float32) / np.float32(255)

# Load structure of the MulSCPL
def JsonToModel(json_path):
    with open(json_path, 'r') as json_file:
        loaded_model_json = json_file.read()
    model = model_from_json(loaded_model_json)
    return model

# Using 'Ecs' as an emergency button
def on_key_release(key):
    global running
    if key == keyboard.Key.esc:
        running = False

if __name__ == '__main__':
    # Create a listener for key events
    listener = keyboard.Listener(on_release=on_key_release)
    listener.start()

    # Load model and weights
    model = JsonToModel('./models/MulSCPL/MulSCPL.json')
    model.load_weights('./models/MulSCPL/best_MulSCPL.h5')

    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)

    # Initialize sequential image matrix
    X = np.zeros(shape=(1, 4, 244, 324, 1), dtype=np.float32)

    with SyncCrazyflie(URI) as scf:
        # We take off when the commander is created
        with MotionCommander(scf) as mc:
            print('Taking off! altitude=0.3m')
            time.sleep(1)

            # rising altitude
            print('Moving up 0.2m, altitude=0.5m')
            mc.up(0.2)
            time.sleep(1)

            while running:
                X = np.roll(X, -1, axis=1)
                # First get the info
                packetInfoRaw = rx_bytes(4)
                [length, routing, function] = struct.unpack('<HBB', packetInfoRaw)
                imgHeader = rx_bytes(length - 2)
                [magic, width, height, depth, format, size] = struct.unpack('<BHHBBI', imgHeader)

                # Now we start receiving the image, this will be split up in packages of some size
                imgStream = bytearray()
                while len(imgStream) < size:
                    packetInfoRaw = rx_bytes(4)
                    [length, dst, src] = struct.unpack('<HBB', packetInfoRaw)
                    chunk = rx_bytes(length - 2)
                    imgStream.extend(chunk)

                # Image processing and prediction
                bayer_img = np.frombuffer(imgStream, dtype=np.uint8)
                bayer_img.shape = (244, 324)
                bayer_img = process_img(bayer_img, target_size=(324, 244))
                X[0, -1, ...] = bayer_img
                steer, coll = model.predict(X)
                if steer[0, 0] < -1.0: steer[0, 0] = -1.0
                if steer[0, 0] > 1.0: steer[0, 0] = 1.0
                print(steer[0, 0])

                # UAV Control Policy
                tk = steer[0, 0] * Smax
                vk = (1-alpha)*vk+alpha*(1-coll[0, 0])*Vmax
                mc.start_linear_motion(velocity_x_m=vk, velocity_y_m=0.0, velocity_z_m=0.0, rate_yaw=-tk)
                pass

            # Stop the listener
            listener.stop()
            listener.join()

            print('Moving down 0.3m, altitude=0.2m')
            mc.down(0.3)
            time.sleep(1)

            # We land when the MotionCommander goes out of scope
            print('Landing!')
