

const Plantilla = () => {
  const handleDownload = () => {
    // Ruta del archivo en la carpeta `public`
    const filePath = `/plantilla.xlsx`;
    // Crear un enlace de descarga
    const link = document.createElement('a');
    link.href = filePath;
    link.download = 'plantilla.xlsx';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div>
      <button onClick={handleDownload} className="download-button">
        Descargar plantilla de Excel
      </button>
    </div>
  );
};

export default Plantilla;
