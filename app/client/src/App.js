import React, { useState, useEffect } from "react";
import Container from "@mui/material/Container";
import CssBaseline from "@mui/material/CssBaseline";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { styled } from "@mui/material/styles";
import Paper from "@mui/material/Paper";
import Button from "@mui/material/Button";

import "./App.css";
import { Grid } from "@mui/material";

function App() {
  // const [data, setData] = useState([{}]);

  // useEffect(() => {
  //   fetch("/members")
  //     .then((res) => res.json())
  //     .then((data) => {
  //       setData(data);
  //       console.log(data);
  //     });
  // }, []);

  return (
    <React.Fragment>
      <CssBaseline />
      <Container maxWidth={false}>
        <Box sx={{ bgcolor: "#FAFAFF", height: "100vh" }}>
          <Typography variant="h2" align="center">
            See-n-Pick
          </Typography>
          <Typography variant="h4" align="center">
            2952-O Final Project
          </Typography>
          <Typography variant="body1" align="left" sx={{ mt: 4, padding: 1 }}>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
            ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
            aliquip ex ea commodo consequat. Duis aute irure dolor in
            reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
            pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
            culpa qui officia deserunt mollit anim id est laborum.
          </Typography>
          <Grid
            container
            spacing={2}
            alignItems="center"
            justifyContent="center"
            mt={4}
            padding={1}
          >
            <Grid item xs={6}>
              <Button sx={{ height: "20vh", width: "100%" }} variant="outlined">
                OpenCV Oak-D Lite
              </Button>
            </Grid>
            <Grid item xs={6}>
              <Button
                onClick={async () => {
                  const response = await fetch("/realsense", {
                    method: "POST",
                  });

                  if (response.ok) {
                    console.log("response worked");
                  }
                }}
                sx={{ height: "20vh", width: "100%" }}
                variant="outlined"
              >
                Intel RealSense
              </Button>
            </Grid>
          </Grid>
          {/* <div id="footer">
            This is a footer. This stays at the bottom of the page.
          </div> */}
        </Box>
      </Container>
    </React.Fragment>
  );
}

export default App;
