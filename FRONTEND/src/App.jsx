import React, { useState, useEffect } from "react";
import "./CSS/style.css";
import FileUploader from "./componentes/FileUploader";
import ProgressBar from "./componentes/ProgressBar";
import useFileUpload from "./componentes/useFileUpload";
import DownloadTemplate from "./componentes/DownloadTemplate";
import { FaFileExcel, FaHome } from "react-icons/fa"; // Iconos de Excel y Home

function App() {
  const { fileInputRef, handleFileChange, handleUpload, progress, isLoading, mensaje, automatizacionCompleta } =
    useFileUpload();
  const [mostrarSoloImagen, setMostrarSoloImagen] = useState(false);

  useEffect(() => {
    if (automatizacionCompleta) {
      setMostrarSoloImagen(true);
    }
  }, [automatizacionCompleta]);

  const handleRegresar = () => {
    // Aquí puedes redirigir al inicio o realizar la acción que necesites
    window.location.reload(); // Recarga la página para volver al inicio
  };

  return (
    <div className="container">
      {mostrarSoloImagen ? (
        // Muestra la imagen y el mensaje cuando la automatización se haya completado
        <div className="resultado">
          <img src="/Logo.png" alt="Logo Final" className="logo" />
          <p className="mensaje-final">
            La generación de certificados ha finalizado.  
            Descarga el reporte desde el ícono de abajo para consultar el estado de tus certificados en el proceso :).
          </p>

          {/* Iconos de Excel y para regresar al inicio */}
          <div className="download-container">
            <div className="icon-wrapper">
              <FaFileExcel className="icon" title="Resultados de los Certificados" />
            </div>
            <div className="icon-wrapper" onClick={handleRegresar}>
              <FaHome className="icon" title="Volver al principio" />
            </div>
          </div>
        </div>
      ) : (
        // Muestra la interfaz normal mientras se sube y ejecuta el proceso
        <>
          <img src="/Logo.png" alt="Logo" className="logo" />
          <DownloadTemplate />
          <FileUploader onFileChange={handleFileChange} fileInputRef={fileInputRef} />
          <button onClick={handleUpload} className="upload-button" disabled={isLoading}>
            {isLoading ? "Cargando..." : "Cargar y Ejecutar"}
          </button>
          {progress > 0 && <ProgressBar progress={progress} />}
          {isLoading && <div className="spinner"></div>}
          <p className="message">{mensaje}</p>
        </>
      )}
    </div>
  );
}

export default App;
