import sys
# if '/opt/ros/kinetic/lib/python2.7/dist-packages' in sys.path: sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2                                
import numpy as np                       
import matplotlib.pyplot as plt           
import pyrealsense2 as rs  
import time
import os 
# import pclpy 
# from pclpy import pcl

print("Environment Ready")

# Setup for camera 1:
# Left camera
p_1 = rs.pipeline()
cfg_1 = rs.config()
cfg_1.enable_device('845112071195')
p_1.start(cfg_1)

#Setup for camera2:
#Front camera 
p_2 = rs.pipeline()
cfg_2 = rs.config()
cfg_2.enable_device('902512070320')
p_2.start(cfg_2)

# Skip 5 first frames to give the Auto-Exposure time to adjust
for x in range(20):
  p_1.wait_for_frames()
  p_2.wait_for_frames()
  
# Store next frameset_1 for later processing:
frameset_1 = p_1.wait_for_frames()
color_frame_1 = frameset_1.get_color_frame()
depth_frame_1 = frameset_1.get_depth_frame()

# Store next frameset_2 for later processing:
frameset_2 = p_2.wait_for_frames()
color_frame_2 = frameset_2.get_color_frame()
depth_frame_1 = frameset_2.get_depth_frame()


p_1.stop()
p_2.stop()

print("Frames Captured")

#######################   Save colored image from camera 1   ##########################
color_1 = np.asanyarray(color_frame_1.get_data())
if os.path.exists('/home/student/dataset/Color_lcam_.png'):
    cv2.imwrite('/home/student/dataset/Color_lcam_{}.png'.format(int(time.time())),color_1)
else:
    cv2.imwrite('/home/student/dataset/Color_lcam_.png',color_1)

colorizer_1 = rs.colorizer()
# colorized_depth_1 = np.asanyarray(colorizer_1.colorize(depth_frame_1).get_data())
# cv2.imwrite('colorized.png',colorized_depth_1)

# # Create alignment primitive with color as its target stream:
align = rs.align(rs.stream.color)
frameset_1 = align.process(frameset_1)

# # Update color and depth frames:
aligned_depth_frame_1 = frameset_1.get_depth_frame()
a = aligned_depth_frame_1
b = np.array(a.get_data())
# c = (b / 10).astype(np.uint8)
# cv2.imwrite("/home/student/dataset/depth_Data_C.png", c)

# colorized_depth_1 = np.asanyarray(colorizer_1.colorize(aligned_depth_frame_1).get_data())

if os.path.exists('/home/student/dataset/Depth_lcam_.png'):
    cv2.imwrite('/home/student/dataset/Depth_lcam_{}.png'.format(int(time.time())), b)
else:
    cv2.imwrite('/home/student/dataset/Depth_lcam_.png',b)



################   Save colored image from camera 2 ####################

color_2 = np.asanyarray(color_frame_2.get_data())
if os.path.exists('/home/student/dataset/Color_fcam_.png'):
    cv2.imwrite('/home/student/dataset/Color_fcam_{}.png'.format(int(time.time())),color_2)
else:
    cv2.imwrite('/home/student/dataset/Color_fcam_.png',color_2)

colorizer_2 = rs.colorizer()
# colorized_depth_2 = np.asanyarray(colorizer_2.colorize(depth_frame_2).get_data())
# cv2.imwrite('colorized.png',colorized_depth_1)

# # Create alignment primitive with color as its target stream:
align = rs.align(rs.stream.color)
frameset_2 = align.process(frameset_2)

# # Update color and depth1 frames:
aligned_depth_frame_2 = frameset_2.get_depth_frame()
a2 = aligned_depth_frame_2
b2 = np.array(a2.get_data())

# colorized_depth_2 = np.asanyarray(colorizer_2.colorize(aligned_depth_frame_2).get_data())
if os.path.exists('/home/student/dataset/Depth_fcam_.png'):
    cv2.imwrite('/home/student/dataset/Depth_fcam_{}.png'.format(int(time.time())),b2)
else:
    cv2.imwrite('/home/student/dataset/Depth_fcam_.png',b2)
