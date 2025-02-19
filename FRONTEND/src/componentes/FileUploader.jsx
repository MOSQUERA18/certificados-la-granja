import { useState } from "react";
import { FaCloudUploadAlt, FaCheckCircle, FaExclamationTriangle } from "react-icons/fa";
import * as XLSX from "xlsx"; // Importamos XLSX
import "./FileUploader.css";

// eslint-disable-next-line react/prop-types
const FileUploader = ({ onFileChange, fileInputRef }) => {
  const [fileName, setFileName] = useState("");
  const [isUploaded, setIsUploaded] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleFileSelect = (event) => {
    const file = event.target.files[0];

    if (file) {
      const allowedExtensions = ["xls", "xlsx"];
      const fileExtension = file.name.split(".").pop().toLowerCase();

      if (!allowedExtensions.includes(fileExtension)) {
        setFileName("");
        setIsUploaded(false);
        setErrorMessage("Formato inválido. Solo se permiten archivos Excel.");
        return;
      }

      // Leer el contenido del archivo
      const reader = new FileReader();
      reader.onload = (e) => {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: "array" });

        const sheetName = workbook.SheetNames[0]; // Tomar la primera hoja
        const sheet = workbook.Sheets[sheetName];
        const jsonData = XLSX.utils.sheet_to_json(sheet);

        if (jsonData.length === 0) {
          setFileName("");
          setIsUploaded(false);
          setErrorMessage("El Excel está vacío. Por favor, suba un archivo con datos.");
          return;
        }

        // Validar que el archivo sea la plantilla correcta (ejemplo: verificamos columnas)
        const expectedHeaders = ['TIPO DE DOCUMENTO', 'NUMERO DE DOCUMENTO', 'NOMBRES Y APELLIDOS', 'DIA', 'MES', 'AÑO']; // Ajusta según la plantilla esperada
        const fileHeaders = Object.keys(jsonData[0]);

        const isValidTemplate = expectedHeaders.every((header) =>
          fileHeaders.includes(header)
        );

        if (!isValidTemplate) {
          setFileName("");
          setIsUploaded(false);
          setErrorMessage("Este Excel no es admitido para este proceso.");
          return;
        }

        // Si pasa todas las validaciones
        setFileName(file.name);
        setIsUploaded(true);
        setErrorMessage(""); 
        onFileChange(event);
      };

      reader.readAsArrayBuffer(file);
    }
  };

  return (
    <div
      className={`file-uploader ${isUploaded ? "uploaded" : ""}`}
      // eslint-disable-next-line react/prop-types
      onClick={() => fileInputRef.current.click()}
    >
      {isUploaded ? (
        <FaCheckCircle className="upload-icon success" />
      ) : errorMessage ? (
        <FaExclamationTriangle className="upload-icon error" />
      ) : (
        <FaCloudUploadAlt className="upload-icon" />
      )}
      <p>
        {errorMessage
          ? errorMessage
          : fileName
          ? `${fileName}, Recibido correctamente!`
          : "Por aquí puedes subir el Excel :)"}
      </p>
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileSelect}
        className="file-input"
        accept=".xls, .xlsx"
      />
    </div>
  );
};

export default FileUploader;
