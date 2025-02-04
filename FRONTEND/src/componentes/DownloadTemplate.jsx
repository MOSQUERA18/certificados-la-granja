import React from "react";
import axios from "axios";

const DownloadTemplate = () => {
  const handleDownload = async () => {      
    try {
        const response = await axios.get("http://localhost:5000/descargar-plantilla");

        if (response.status !== 200) {
            throw new Error("No se pudo descargar la plantilla");
        }

        const { archivo_base64, nombre } = response.data; // Extraer el Base64 del JSON
        
        // Convertir Base64 a un Blob
        const byteCharacters = atob(archivo_base64);
        const byteNumbers = new Uint8Array(byteCharacters.length)
            .map((_, i) => byteCharacters.charCodeAt(i));
        const blob = new Blob([byteNumbers], { 
            type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" 
        });

        // Crear URL de descarga
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = nombre;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        alert("Plantilla descargada correctamente!")

    } catch (error) {          
        console.error("Error al descargar la plantilla:", error);
    }
};  

  return (
    <button onClick={handleDownload} className="download-button">
      Descargar Plantilla
    </button>
  );
};

export default DownloadTemplate;
