import React from "react";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { Grid } from "@mui/material";
import { useNavigate } from "react-router-dom";

function Main() {
  const navigate = useNavigate();
  const github = "https://github.com/FJiangArthur/2952O_Final_Project";

  return (
    <div>
      <Typography variant="h2" align="center">
        See-n-Pick
      </Typography>
      <Typography variant="h4" align="center">
        2952-O Final Project
      </Typography>
      <Typography variant="body1" align="left" sx={{ mt: 4, padding: 1 }}>
        Traditionally, object manipulation and sorting using a robotic arm uses
        expensive hardware, cameras, and non-generalizable approaches. Through
        our final project for Brown's CS2952-O (Advanced 3D Perception for
        Robotics), we aim to provide a generalizable interface for object
        detection and un-clustering using the Mirobot Robotic Arm. We compare 2
        off the shelve low-cost cameras - the Intel Realsense and the OpenCV
        OAKD-Lite for this task. We also test our approach using 2 pre-trained
        object detection models, the MaskRCNN and the YOLOv5. In short, we
        create and end-to-end workflow of object detection, un-clustering, and
        delivery using the Mirobot and a generalizable and accessible user
        interface.
      </Typography>
      <Grid
        container
        spacing={2}
        alignItems="center"
        justifyContent="center"
        mt={4}
        padding={1}
      >
        <Grid item xs={3}>
          <Button
            onClick={() => navigate("/simple")}
            sx={{ height: "20vh", width: "100%" }}
            variant="outlined"
          >
            Simple Video Stream
          </Button>
        </Grid>
        <Grid item xs={3}>
          <Button
            onClick={() => navigate("/realsenseMask")}
            sx={{ height: "20vh", width: "100%" }}
            variant="outlined"
          >
            Intel RealSense
          </Button>
        </Grid>
        <Grid item xs={3}>
          <Button
            onClick={() => navigate("/realsenseYolo")}
            sx={{ height: "20vh", width: "100%" }}
            variant="outlined"
          >
            Intel RealSense
          </Button>
        </Grid>
        <Grid item xs={3}>
          <Button
            onClick={() => navigate("/")}
            sx={{ height: "20vh", width: "100%" }}
            variant="outlined"
          >
            OpenCV Oak-D Lite
          </Button>
        </Grid>
      </Grid>
      <Typography variant="body1" align="center" sx={{ mt: 4, padding: 1 }}>
        <a href={github} target="_blank">
          GitHub
        </a>
      </Typography>
      <Typography variant="body1" align="center" sx={{ padding: 1 }}>
        <a href={""} target="_blank">
          Poster
        </a>
      </Typography>
      <Typography variant="body1" align="center" sx={{ padding: 1 }}>
        <b>Team:</b> Fengyi Arthur, Alejandro Romero, Tarun Rajnish
      </Typography>
    </div>
  );
}

export default Main;
