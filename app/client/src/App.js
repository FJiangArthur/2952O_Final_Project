import React, { useState, useEffect } from "react";
import Container from "@mui/material/Container";
import CssBaseline from "@mui/material/CssBaseline";
import Box from "@mui/material/Box";

import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import "./App.css";
import Main from "./components/main/Main";
import Realsense from "./components/realsense/Realsense";
import Simple from "./components/simple/Simple";

function App() {
  // const [video, setVideo] = useState("");

  // useEffect(() => {
  //   const response = fetch("/realsense", {
  //     method: "POST",
  //   });

  //   if (response.ok) {
  //     console.log("response worked");
  //     console.log(response);
  //     console.log(typeof response);
  //   }
  // }, []);

  return (
    <Router>
      <React.Fragment>
        <CssBaseline />
        <Container maxWidth={false}>
          <Box sx={{ bgcolor: "#FAFAFF", height: "100vh" }}>
            <Routes>
              <Route path="/" element={<Main />}></Route>
              <Route path="/simple" element={<Simple />}></Route>
              <Route path="/realsense" element={<Realsense />}></Route>
            </Routes>
          </Box>
        </Container>
      </React.Fragment>
    </Router>
  );
}

export default App;
