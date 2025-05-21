// App.jsx
import { useState, useEffect } from "react";
import "./CSS/style.css";
import FileUploader from "./componentes/FileUploader";
import ProgressBar from "./componentes/ProgressBar";
import useFileUpload from "./componentes/useFileUpload";
import DownloadTemplate from "./componentes/DownloadTemplate";
import CarpetaCreator from "./componentes/CarpetaCreator";
import axios from "axios";
import Swal from "sweetalert2";

const VITE_API_URL = import.meta.env.VITE_API_URL;

function App() {
  const {
    fileInputRef,
    handleFileChange,
    handleUpload,
    progress,
    isLoading,
  } = useFileUpload();

  const [nombreCarpeta, setNombreCarpeta] = useState("");

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

  const handleCrearCarpeta = async () => {
    if (!nombreCarpeta.trim()) {
      Swal.fire({
        icon: "warning",
        title: "Nombre requerido",
        text: "Por favor ingresa un nombre de carpeta.",
        confirmButtonColor: "#218838",
        iconColor: "#ffc107"
      });
      return false;
    }

    try {
      const response = await axios.post(`${VITE_API_URL}/crear-carpeta-descargas`, {
        nombre: nombreCarpeta.trim()
      });

      Swal.fire({
        icon: "success",
        title: "Carpeta creada",
        text: response.data.mensaje,
        confirmButtonColor: "#218838",
        iconColor: "#28a745"
      });

      setNombreCarpeta(nombreCarpeta.trim());
      return true;
    } catch (error) {
      console.error("Error al crear carpeta:", error);
      Swal.fire({
        icon: "error",
        title: "Error",
        text: error.response?.data?.error || "No se pudo crear la carpeta.",
        confirmButtonColor: "#218838"
      });
      return false;
    }
  };

  const handleUploadWithFolderCreation = async () => {
    const carpetaCreada = await handleCrearCarpeta();
    if (carpetaCreada) {
      handleUpload();
    }
  };

  return (
    <div className="container">
      <img src="/Logo.png" alt="Logo" className="logo" />
      <div className="contenido">
        <DownloadTemplate />
        <CarpetaCreator nombreCarpeta={nombreCarpeta} setNombreCarpeta={setNombreCarpeta} />
        <FileUploader onFileChange={handleFileChange} fileInputRef={fileInputRef} />
        <button onClick={handleUploadWithFolderCreation} className="upload-button" disabled={isLoading}>
          {isLoading ? "Cargando..." : "Cargar y Ejecutar"}
        </button>
        {/* Mostrar ProgressBar solo si isLoading es true y progress es menor que 100 */}
        {isLoading && progress < 100 && <ProgressBar progress={progress} />}
        {/* Mostrar el spinner solo si isLoading es true */}
        {isLoading && <div className="spinner"></div>}
      </div>
    </div>
  );
}

export default App;
