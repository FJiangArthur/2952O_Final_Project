import React from "react";

function Simple() {
  return (
    <div>
      <img
        style={{
          background: "transparent",
          width: "100%",
          height: "100vh",
        }}
        src="http://127.0.0.1:5000/video_feed"
        alt="Video"
      />
    </div>
  );
}

export default Simple;
