import { useState, useEffect } from "react";
import "./CSS/style.css";
import FileUploader from "./componentes/FileUploader";
import ProgressBar from "./componentes/ProgressBar";
import useFileUpload from "./componentes/useFileUpload";
import DownloadTemplate from "./componentes/DownloadTemplate";
import { FaFileExcel, FaHome } from "react-icons/fa"; // Iconos de Excel y Home
import axios from "axios"; 
import Swal from "sweetalert2"; // Importamos SweetAlert2

const VITE_API_URL = import.meta.env.VITE_API_URL;  

function App() {
  const { fileInputRef, handleFileChange, handleUpload, progress, isLoading, automatizacionCompleta } =
    useFileUpload();
  const [mostrarSoloImagen, setMostrarSoloImagen] = useState(false);
  const [resultadosDescargados, setResultadosDescargados] = useState(false);

  useEffect(() => {
    const handleBeforeUnload = (event) => {
      event.preventDefault();
      event.returnValue = "El proceso aún está en ejecución. ¿Estás seguro de que quieres salir?";
    };
  
    if (isLoading) {
      window.addEventListener("beforeunload", handleBeforeUnload);
    }
  
    return () => {
      window.removeEventListener("beforeunload", handleBeforeUnload);
    };
  }, [isLoading]);
  

  useEffect(() => {
    if (automatizacionCompleta) {
      setMostrarSoloImagen(true);
    }
  }, [automatizacionCompleta]);

  const handleRegresar = () => {
    window.location.reload();
  };

  const handleDownloadResults = async () => {
    if (resultadosDescargados) {
      Swal.fire({
        icon: "info",
        title: "Resultados ya descargados",
        text: "Ya has descargado los resultados anteriormente.",
        confirmButtonColor: "#218838",
        iconColor: "#218838"
      });
      return;
    }

    try {
      const response = await axios.get(`${VITE_API_URL}/descargar-resultados`, { responseType: 'blob' });

      // Crear un enlace para descargar el archivo
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'resultados_certificados.xlsx');
      document.body.appendChild(link);
      link.click();
      link.remove();

      setResultadosDescargados(true);

      Swal.fire({
        icon: "success",
        title: "Descarga exitosa",
        text: "Los resultados se han descargado correctamente.",
        confirmButtonColor: "#218838",
        iconColor: "#218838"
      });

    } catch (error) {
      console.error("Error al descargar el archivo:", error);
      Swal.fire({
        icon: "error",
        title: "Error en la descarga",
        text: "No se pudo descargar el archivo. Inténtalo nuevamente.",
        confirmButtonColor: "#218838",
      });
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
        </>
      )}
    </div>
  );
}

export default App;