# Seen-n-Pick: Object Detection & Segregation using Mirobot

Our goal is to use state-of-art computer vision techniques coupled with low cost depth cameras for identifying objects on a production line.

We then use the Mirobot robot arm to segregate objects by class to prepare these objects for delivery. 

 * [Project Poster](https://drive.google.com/file/d/1IhJ5JxWvTOD48baTFk1SDgBTMWksTkgd/view?usp=sharing)
 * [Paper](https://arxiv.org/abs/2011.12948)
 * [Video](https://www.youtube.com/watch?v=MrKrnHhk8IA)


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

### Launch

First starting calibration, tf, and motion planning:

```shell
roslaunch see-pick-mirobot pick-place.launch
```

Then connect DepthAI and start yolov4 node:

```shell
roslaunch see-pick-mirobot yolov4_depthai.launch
```

### Art's TODO

1. Move the manipulator to the target position.
2. Transform the target position.

## References

### For coordinate System Transform

<https://wiki.ros.org/tf/Overview/Transformations>

### Important

It seems that in the MoveIt workspace, the x axis is the direction arm is facing after homing.

joint_goal = move_group.get_current_joint_values()
joint_goal[0] = 0
joint_goal[1] = 1.1089
joint_goal[2] = -0.6339
joint_goal[3] = 0
joint_goal[4] = -0.483
joint_goal[5] = 0
pose_goal.orientation.w = 0
pose_goal.position.x = 0.28
pose_goal.position.y = 0.0
pose_goal.position.z = 0.09
