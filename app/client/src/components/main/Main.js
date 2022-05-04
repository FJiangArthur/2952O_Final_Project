import React from "react";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { Grid } from "@mui/material";
import { useNavigate } from "react-router-dom";

function Main() {
  const navigate = useNavigate();

  return (
    <div>
      <Typography variant="h2" align="center">
        See-n-Pick
      </Typography>
      <Typography variant="h4" align="center">
        2952-O Final Project
      </Typography>
      <Typography variant="body1" align="left" sx={{ mt: 4, padding: 1 }}>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
        veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
        commodo consequat. Duis aute irure dolor in reprehenderit in voluptate
        velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint
        occaecat cupidatat non proident, sunt in culpa qui officia deserunt
        mollit anim id est laborum.
      </Typography>
      <Grid
        container
        spacing={2}
        alignItems="center"
        justifyContent="center"
        mt={4}
        padding={1}
      >
        <Grid item xs={4}>
          <Button
            onClick={() => navigate("/simple")}
            sx={{ height: "20vh", width: "100%" }}
            variant="outlined"
          >
            Simple Video Stream
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button
            onClick={() => navigate("/realsense")}
            sx={{ height: "20vh", width: "100%" }}
            variant="outlined"
          >
            Intel RealSense
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button
            onClick={"/"}
            sx={{ height: "20vh", width: "100%" }}
            variant="outlined"
          >
            OpenCV Oak-D Lite
          </Button>
        </Grid>
      </Grid>
    </div>
  );
}

export default Main;
