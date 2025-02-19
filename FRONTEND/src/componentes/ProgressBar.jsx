
// eslint-disable-next-line react/prop-types
const ProgressBar = ({ progress }) => {
    return (
      <div className="progress-bar-container">
        <progress value={progress} max="100" className="progress-bar"></progress>
        <span>{progress}%</span>
      </div>
    );
  };  

export default ProgressBar;