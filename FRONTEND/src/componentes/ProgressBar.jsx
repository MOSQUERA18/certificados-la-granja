import React from "react";

const ProgressBar = ({ progress }) => {
    return (
      <div className="progress-bar-container">
        <progress value={progress} max="100" className="progress-bar"></progress>
        <span>{progress}%</span>
      </div>
    );
  };  

export default ProgressBar;