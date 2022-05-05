# 2952O_Final_Project

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
