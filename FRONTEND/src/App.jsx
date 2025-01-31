import { useState, useRef } from "react";
import "./CSS/style.css";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [mensaje, setMensaje] = useState("");
  const [progress, setProgress] = useState(0);
  const fileInputRef = useRef(null); // Referencia al input de archivo

  // Manejo de selección de archivo
  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (!selectedFile) {
      alert("No seleccionaste ningún archivo.");
      return;
    }

    // Validación de tipo de archivo (solo Excel)
    const validExtensions = ["application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"];
    if (!validExtensions.includes(selectedFile.type)) {
      alert("Formato no válido. Selecciona un archivo Excel (.xls, .xlsx)");
      console.warn("Archivo rechazado:", selectedFile.name, selectedFile.type);

      // Limpiar campo de archivo
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }

      setFile(null);
      return;
    }

    setFile(selectedFile);
  };

  // Manejo de subida de archivo
  const handleUpload = async () => {
    if (!file) {
      alert("Selecciona un archivo primero.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:5000/subir-excel", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setProgress(percentCompleted);
        },
      });

      if (response.status === 200) {
        setMensaje(response.data.mensaje || "Archivo subido correctamente.");
        alert("Archivo subido con éxito.");
      } else {
        setMensaje("Error al subir archivo.");
        alert("Error en la subida del archivo.");
      }

      setProgress(0);

      // Iniciar automatización después de subir archivo
      try {
        const autoResponse = await axios.post("http://localhost:5000/iniciar-automatizacion");

        if (autoResponse.status === 200) {
          setMensaje(autoResponse.data.mensaje || "Automatización completada.");
          alert("Automatización completada con éxito.");
        } else {
          setMensaje("Error en la automatización.");
          alert("Hubo un problema al iniciar la automatización.");
        }
      } catch (autoError) {
        console.error("Error en la automatización:", autoError);
        alert("Error al conectar con el servidor para la automatización.");
        setMensaje("Error al conectar con el servidor para la automatización.");
      }
    } catch (error) {
      console.error("Error al subir archivo:", error);
      alert("Error al conectar con el servidor para subir el archivo.");
      setMensaje("Error al conectar con el servidor.");
      setProgress(0);
    }
  };

  return (
    <div className="container">
      <h1>Subir Archivo Excel</h1>
      <img src="/sena.png" alt="Logo" />
      <input type="file" ref={fileInputRef} onChange={handleFileChange} />
      <button onClick={handleUpload}>Cargar y Ejecutar</button>
      {progress > 0 && <progress value={progress} max="100"></progress>}
      <p>{mensaje}</p>
    </div>
  );
}

export default App;
