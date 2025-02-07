import React, { useState, useEffect } from "react";
import "./CSS/style.css";
import FileUploader from "./componentes/FileUploader";
import ProgressBar from "./componentes/ProgressBar";
import useFileUpload from "./componentes/useFileUpload";
import DownloadTemplate from "./componentes/DownloadTemplate";
import { FaFileExcel, FaHome } from "react-icons/fa"; // Iconos de Excel y Home
import axios from "axios"; // Asegúrate de importar axios

const API_URL = import.meta.env.VITE_API_URL;  

function App() {
  const { fileInputRef, handleFileChange, handleUpload, progress, isLoading, mensaje, automatizacionCompleta } =
    useFileUpload();
  const [mostrarSoloImagen, setMostrarSoloImagen] = useState(false);
  const [resultadosDescargados, setResultadosDescargados] = useState(false); // Nuevo estado

  useEffect(() => {
    if (automatizacionCompleta) {
      setMostrarSoloImagen(true);
    }
  }, [automatizacionCompleta]);

  const handleRegresar = () => {
    window.location.reload(); // Recarga la página para volver al inicio
  };

  const handleDownloadResults = async () => {
    if (resultadosDescargados) {
      alert("Ya has descargado los resultados."); // Mensaje si ya se descargó
      return;
    }

    try {
      const response = await axios.get(`${API_URL}/descargar-resultados`, { responseType: 'blob' });

      // Crear un enlace para descargar el archivo
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'resultados_certificados.xlsx'); // Nombre del archivo
      document.body.appendChild(link);
      link.click();
      link.remove();

      // Marcar que los resultados han sido descargados
      setResultadosDescargados(true);
    } catch (error) {
      console.error("Error al descargar el archivo:", error);
      alert("Error al descargar el archivo.");
    }
  };

  return (
    <div className="container">
      {mostrarSoloImagen ? (
        <div className="resultado">
          <img src="/Logo.png" alt="Logo Final" className="logo" />
          <p className="mensaje-final">
            La generación de certificados ha finalizado.  
            Descarga el reporte desde el ícono de abajo para consultar el estado de tus certificados en el proceso :).
          </p>

          <div className="download-container">
            <div className="icon-wrapper" onClick={handleDownloadResults}>
              <FaFileExcel className="icon" title="Resultados de los Certificados" />
            </div>
            <div className="icon-wrapper" onClick={handleRegresar}>
              <FaHome className="icon" title="Volver al principio" />
            </div>
          </div>
        </div>
      ) : (
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