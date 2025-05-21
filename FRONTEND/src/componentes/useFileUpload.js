import { useState, useRef } from "react";
import axios from "axios";
import Swal from "sweetalert2";

const API_URL = import.meta.env.VITE_API_URL;

const useFileUpload = () => {
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef(null);

  const customSwal = (icon, title, text) => {
    Swal.fire({
      icon,
      title,
      text,
      confirmButtonColor: "#218838",
      confirmButtonText: "Aceptar",
      iconColor: "#218838",
    });
  };

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (!selectedFile) {
      customSwal("warning", "Archivo no seleccionado", "Por favor selecciona un archivo antes de continuar.");
      return;
    }

    const validExtensions = [
      "application/vnd.ms-excel",
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ];

    if (!validExtensions.includes(selectedFile.type)) {
      customSwal("error", "Formato no válido", "Selecciona un archivo Excel (.xls, .xlsx)");
      if (fileInputRef.current) fileInputRef.current.value = "";
      setFile(null);
      return;
    }

    const maxSize = 5 * 1024 * 1024;
    if (selectedFile.size > maxSize) {
      customSwal("error", "Archivo demasiado grande", "El tamaño máximo permitido es de 5MB.");
      if (fileInputRef.current) fileInputRef.current.value = "";
      setFile(null);
      return;
    }

    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) {
      customSwal("warning", "Ningún archivo seleccionado", "Selecciona un archivo primero.");
      return;
    }

    setIsLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post(`${API_URL}/subir-excel`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          setProgress(percentCompleted);
        },
      });

      // Iniciar automatización sin mostrar ventana final
      await axios.post(`${API_URL}/iniciar-automatizacion`);
    } catch (error) {
      console.error("Error al subir archivo:", error);
      customSwal("error", "Error de conexión", "No se pudo conectar con el servidor. Inténtalo nuevamente.");
    } finally {
      setProgress(0);
      setIsLoading(false);
    }
  };

  return {
    fileInputRef,
    handleFileChange,
    handleUpload,
    progress,
    isLoading,
  };
};

export default useFileUpload;
