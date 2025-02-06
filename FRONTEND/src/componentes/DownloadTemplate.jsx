import React from "react";
import { FaFileDownload, FaBook } from "react-icons/fa"; // Importamos los iconos
import axios from "axios";

const DownloadTemplate = () => {
  const handleDownload = async () => {      
    try {
        const response = await axios.get("http://localhost:5000/descargar-plantilla");

        if (response.status !== 200) {
            throw new Error("No se pudo descargar la plantilla");
        }

        const { archivo_base64, nombre } = response.data;
        const byteCharacters = atob(archivo_base64);
        const byteNumbers = new Uint8Array(byteCharacters.length)
            .map((_, i) => byteCharacters.charCodeAt(i));
        const blob = new Blob([byteNumbers], { 
            type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" 
        });

        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = nombre;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        alert("Plantilla descargada correctamente!");

    } catch (error) {          
        console.error("Error al descargar la plantilla:", error);
    }
  };  

  return (
    <div className="download-container">
      <div className="icon-wrapper" onClick={handleDownload} title="Descargar Plantilla">
        <FaFileDownload className="icon" />
      </div>
      <div className="icon-wrapper" title="Manual de Usuario">
        <FaBook className="icon" />
      </div>
    </div>
  );
};

export default DownloadTemplate;
