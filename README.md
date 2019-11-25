# Install two realsense cameras

Install the Intel RealSense SDK 2.0 (librealsense) for Linux following the instructions [here](https://github.com/IntelRealSense/librealsense/blob/master/doc/installation.md).

Install ROS wrapper for librealsense from [here](https://github.com/IntelRealSense/realsense-ros/releases) .

## Launch two cameras

Obtain each camera's serial number

Front camera: 902512070320

Side camera: 845112071195

```bash
	
roslaunch realsense2_camera rs_camera.launch camera:=cam_1 serial_no:=902512070320 filters:=spatial,temporal,pointcloud_
	
roslaunch realsense2_camera rs_camera.launch camera:=cam_2 serial_no:=845112071195 filters:=spatial,temporal,pointcloud_
```

## Set cameras transform :
```bash
python src/realsense/realsense2_camera/scripts/set_cams_transforms.py cam_1_link cam_2_link 0.7 -1.1 0.4 72.0 19.0 -31.0
```

### Run rviz 
