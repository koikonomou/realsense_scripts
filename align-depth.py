import sys
if '/opt/ros/kinetic/lib/python2.7/dist-packages' in sys.path: sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2                                # state of the art computer vision algorithms library
import numpy as np                        # fundamental package for scientific computing
import matplotlib.pyplot as plt           # 2D plotting library producing publication quality figures
import pyrealsense2 as rs                 # Intel RealSense cross-platform open-source API


print("Environment Ready")

# Setup for camera 1:
#left camera
p_1 = rs.pipeline()
cfg_1 = rs.config()
cfg_1.enable_device('845112071195')
p_1.start(cfg_1)

# Skip 5 first frames 
for x in range(10):
  p_1.wait_for_frames()
  # p_2.wait_for_frames()
  
# Store frameset_1 
frameset_1 = p_1.wait_for_frames()
color_frame_1 = frameset_1.get_color_frame()
depth_frame_1 = frameset_1.get_depth_frame()

p_1.stop()
# p_2.stop()

print("Frames Captured")
#Save colored image from camera 1
color_1 = np.asanyarray(color_frame_1.get_data())
cv2.imwrite('/home/student/dataset/color1.png',color_1)

colorizer_1 = rs.colorizer()

# # Create alignment primitive with color as its target stream:
align = rs.align(rs.stream.color)
frameset_1 = align.process(frameset_1)

# # Update color and depth frames:
aligned_depth_frame_1 = frameset_1.get_depth_frame()
colorized_depth_1 = np.asanyarray(colorizer_1.colorize(aligned_depth_frame_1).get_data())
cv2.imwrite('/home/student/dataset/depth1.png',colorized_depth_1)

# # Show the two frames together:
# images = np.hstack((color, colorized_depth))
# plt.imshow(color)
# plt.savefig("color_2.png")
# plt.imshow(colorized_depth)
# plt.savefig("depth2.png")