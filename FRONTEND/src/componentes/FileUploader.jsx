import React from "react";

const FileUploader = ({ onFileChange, fileInputRef }) => {
    return (
      <div className="file-uploader">
        <input type="file" ref={fileInputRef} onChange={onFileChange} className="file-input" />
      </div>
    );
  };
  

export default FileUploader;