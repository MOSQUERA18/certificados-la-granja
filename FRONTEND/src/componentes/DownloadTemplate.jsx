import React, { useState } from "react";
import { FaFileDownload, FaBook } from "react-icons/fa";
import axios from "axios";
import Swal from "sweetalert2";

const API_URL = import.meta.env.VITE_API_URL;

const DownloadTemplate = () => {
  const [templateDownloaded, setTemplateDownloaded] = useState(false);

  const handleDownload = async () => {
    if (templateDownloaded) {
      Swal.fire({
        icon: "info",
        title: "Plantilla ya descargada",
        text: "Ya has descargado la plantilla anteriormente.",
        confirmButtonColor: "#218838",
        iconColor: "#218838",
      });
      return;
    }

    setTemplateDownloaded(true); // Bloquear nuevas descargas inmediatamente

    try {
      const response = await axios.get(`${API_URL}/descargar-plantilla`);

      if (response.status !== 200) {
        throw new Error("No se pudo descargar la plantilla");
      }

      const { archivo_base64, nombre } = response.data;
      const byteCharacters = atob(archivo_base64);
      const byteNumbers = new Uint8Array(byteCharacters.length).map(
        (_, i) => byteCharacters.charCodeAt(i)
      );
      const blob = new Blob([byteNumbers], {
        type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      });

      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = nombre;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);

      // Mostrar la alerta después de la descarga con un pequeño retardo
      setTimeout(() => {
        Swal.fire({
          icon: "success",
          title: "Descarga exitosa",
          text: "La plantilla se ha descargado correctamente.",
          confirmButtonColor: "#218838",
          iconColor: "#28a745",
        });
      }, 500);

    } catch (error) {
      console.error("Error al descargar la plantilla:", error);
      setTemplateDownloaded(false); // Permitir reintentar la descarga si falla

      Swal.fire({
        icon: "error",
        title: "Error en la descarga",
        text: "Hubo un problema al descargar la plantilla. Inténtalo nuevamente.",
        confirmButtonColor: "#218838",
        iconColor: "#dc3545",
      });
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
