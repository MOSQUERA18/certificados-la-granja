import { useState, useRef } from "react";
import axios from "axios";

const useFileUpload = () => {
  const [file, setFile] = useState(null);
  const [mensaje, setMensaje] = useState("");
  const [progress, setProgress] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (!selectedFile) {
      alert("No seleccionaste ningún archivo.");
      return;
    }

    const validExtensions = [
      "application/vnd.ms-excel",
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ];

    if (!validExtensions.includes(selectedFile.type)) {
      alert("Formato no válido. Selecciona un archivo Excel (.xls, .xlsx)");
      if (fileInputRef.current) fileInputRef.current.value = "";
      setFile(null);
      return;
    }

    const maxSize = 5 * 1024 * 1024;
    if (selectedFile.size > maxSize) {
      alert("El archivo es demasiado grande. Máximo 5MB.");
      if (fileInputRef.current) fileInputRef.current.value = "";
      setFile(null);
      return;
    }

    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Selecciona un archivo primero.");
      return;
    }

    setIsLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:5000/subir-excel", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setProgress(percentCompleted);
        }
      });

      setMensaje(response.data.mensaje || "Archivo subido correctamente.");
      alert("Archivo subido con éxito.");
      setProgress(0);

      const autoResponse = await axios.post("http://localhost:5000/iniciar-automatizacion");
      setMensaje(autoResponse.data.mensaje || "Automatización completada.");
      alert("Automatización completada con éxito.");
    } catch (error) {
      console.error("Error al subir archivo:", error);
      alert("Error al conectar con el servidor.");
      setMensaje("Error al conectar con el servidor.");
      setProgress(0);
    } finally {
      setIsLoading(false);
    }
  };

  return { fileInputRef, handleFileChange, handleUpload, progress, isLoading, mensaje };
};

export default useFileUpload;