
import "./CSS/style.css";
import FileUploader from "./componentes/FileUploader";
import ProgressBar from "./componentes/ProgressBar";
import useFileUpload from "./componentes/useFileUpload";
import DownloadTemplate from "./componentes/DownloadTemplate";

function App() {
  const { fileInputRef, handleFileChange, handleUpload, progress, isLoading, mensaje } = useFileUpload();

  return (
    <div className="container">
      <img src="/Logo.png" alt="Logo" className="logo" />
      <DownloadTemplate />
      <FileUploader onFileChange={handleFileChange} fileInputRef={fileInputRef} />
      <button onClick={handleUpload} className="upload-button" disabled={isLoading}>
        {isLoading ? "Cargando..." : "Cargar y Ejecutar"}
      </button>
      {progress > 0 && <ProgressBar progress={progress} />}
      {isLoading && <div className="spinner"></div>}
      <p className="message">{mensaje}</p>
    </div>
  );
}

export default App;