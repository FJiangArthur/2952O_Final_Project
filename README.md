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

## Getting Started
### 
```shell
bash -c "$(curl -fL https://docs.luxonis.com/install_dependencies.sh)"
```
```shell 
python3 -m pip install opencv-python --force-reinstall --no-cache-dir
```


## References

### For coordinate System Transform

<https://wiki.ros.org/tf/Overview/Transformations>

### MaskRCNN Repo
https://github.com/matterport/Mask_RCNN

### Yolov5 Repo
https://github.com/killnice/yolov5-D435i?fbclid=IwAR179t_eFRqL0AOv8SmjYIf-Nk9mSCuWmFElyD33Ctui9GHwFjNJHfd9UaE

