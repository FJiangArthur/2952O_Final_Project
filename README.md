# Seen-n-Pick: Object Detection & Segregation using Mirobot

Our goal is to use state-of-art computer vision techniques coupled with low cost depth cameras for identifying objects on a production line.

We then use the Mirobot robot arm to segregate objects by class to prepare these objects for delivery. 

 * [Project Poster](https://drive.google.com/file/d/1IhJ5JxWvTOD48baTFk1SDgBTMWksTkgd/view?usp=sharing)
 * [Paper](https://arxiv.org/abs/2011.12948)
 * [Video](https://drive.google.com/file/d/1t1JLBH4yuk6mLWVN-YUgFcyieSbIKyHM/view?usp=sharing)


## Launching app

### Frontend

cd client
npm start

### Backend

cd flask-server
python3 server.py


If the frontend does not work, the MaskRCNN backend can still be run assuming Realsense and Mirobot packages are installed, and the appropriate devices are plugged in.
Entry point for backend-only: python3 measure_object_distance.py

## Getting Started
### 
```shell
bash -c "$(curl -fL https://docs.luxonis.com/install_dependencies.sh)"
```
```shell 
python3 -m pip install opencv-python --force-reinstall --no-cache-dir
```

## Our ROS 2 Mirobot Integration Solution Repos

* https://github.com/FJiangArthur/2952O-Mirobot-ROS2?fbclid=IwAR10b7i5iCZ0xhmTA8glrdVILWPPsRZK3OQZC7pMPIK9e5iSY-jzqDBjcVY
* https://github.com/FJiangArthur/2952O-Serial-ROS2?fbclid=IwAR20j-dqh4PlA0UrDKbhWKJLZd0KFNiyyKF8Ho4j1mtoCDuow0sROuRmvSw


## References

### For coordinate System Transform

<https://wiki.ros.org/tf/Overview/Transformations>

### MaskRCNN Repo
https://github.com/matterport/Mask_RCNN

### Yolov5 Repo
https://github.com/killnice/yolov5-D435i?fbclid=IwAR179t_eFRqL0AOv8SmjYIf-Nk9mSCuWmFElyD33Ctui9GHwFjNJHfd9UaE

