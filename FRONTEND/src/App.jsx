import React from "react";
import "./CSS/style.css";
import FileUploader from "./componentes/FileUploader";
import ProgressBar from "./componentes/ProgressBar";
import useFileUpload from "./componentes/useFileUpload";
import DownloadTemplate from "./componentes/DownloadTemplate";

function App() {
<<<<<<< HEAD
  const [file, setFile] = useState(null);
  const [mensaje, setMensaje] = useState("");
  const [progress, setProgress] = useState(0);
  const [isProcessing, setIsProcessing] = useState(false); // Estado para saber si está procesando
  const [hasDownloaded, setHasDownloaded] = useState(false); // Nuevo estado para controlar la descarga
  const fileInputRef = useRef(null); // Referencia al input de archivo
  const [downloadClickCount, setDownloadClickCount] = useState(0); // Contador de clics en el botón de descarga

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

    setIsProcessing(true);  // Iniciar proceso
    setProgress(0);  // Restablecer progreso
    setMensaje("");  // Limpiar mensaje previo

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

          // Mensaje con la ubicación del archivo generado
          setMensaje(
            `Automatización completada. Los resultados fueron guardados en: Descargas`
          );
          
          // Limpiar mensaje después de 5 segundos
          setTimeout(() => {
            setMensaje("");
          }, 5000);
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
    } finally {
      // Limpiar después de completar el proceso
      setIsProcessing(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
      setFile(null);  // Limpiar el archivo seleccionado
    }
  };
=======
  const { fileInputRef, handleFileChange, handleUpload, progress, isLoading, mensaje } = useFileUpload();
>>>>>>> f6886d7deada1246084238c845bd60cfcc7d05e7

  const handleDownload = () => {
    setDownloadClickCount((prevCount) => prevCount + 1); // Incrementar contador de clics

    if (downloadClickCount >= 1) {
      alert("Solo puedes descargarlo una vez");
    }
  };
  return (
    <div className="container">
<<<<<<< HEAD
      <h1>Subir Archivo Excel</h1>
      <img src="/sena.png" alt="Logo" />
      <input 
        type="file" 
        ref={fileInputRef} 
        onChange={handleFileChange} 
        disabled={isProcessing} // Deshabilitar durante el proceso
      />
      <button onClick={handleUpload} disabled={isProcessing}>Cargar y Ejecutar</button>
      {progress > 0 && <progress value={progress} max="100"></progress>}
      <p>{mensaje}</p>

      {/* Botón para descargar la plantilla de Excel */}
      <a href="/plantilla.xlsx" download onClick={handleDownload}>
        <button disabled={hasDownloaded}>Descargar Plantilla Excel</button>
      </a>
=======
      <img src="/Logo.png" alt="Logo" className="logo" />
      <DownloadTemplate />
      <FileUploader onFileChange={handleFileChange} fileInputRef={fileInputRef} />
      <button onClick={handleUpload} className="upload-button" disabled={isLoading}>
        {isLoading ? "Cargando..." : "Cargar y Ejecutar"}
      </button>
      {progress > 0 && <ProgressBar progress={progress} />}
      {isLoading && <div className="spinner"></div>}
      <p className="message">{mensaje}</p>
>>>>>>> f6886d7deada1246084238c845bd60cfcc7d05e7
    </div>
  );
}

export default App;