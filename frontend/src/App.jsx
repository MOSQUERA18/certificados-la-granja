import { useState } from 'react';
import axios from 'axios';
import Plantilla from './Plantilla';
import './App.css'; // Importar el archivo de estilos
// import ProductCard from './card';

function App() {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState('');  // Estado para almacenar el nombre del archivo
  const [message, setMessage] = useState('');

  // Maneja el cambio en el archivo seleccionado
  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    setFile(selectedFile);
    setFileName(selectedFile ? selectedFile.name : ''); // Actualizar el nombre del archivo
        // Limpiar el mensaje si se seleccionó un archivo
        if (selectedFile) {
          setMessage('');
        }
  };

  // Maneja el envío del formulario
  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!file) {
      setMessage('Por favor, selecciona un archivo antes de continuar.');
      return;
    }


    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:3000/upload', formData);
      setMessage(response.data);
    } catch (error) {
      console.log(error);
      setMessage('Error al generar los certificados');
    }
  };

  return (

    
    <div className="container">
      <header className="header">
        <img src="sena.png" alt="Sena Logo" className="logo" />
        <h1>Generador de Certificados Sena</h1>
      </header>

      <Plantilla />

      <form onSubmit={handleSubmit} className="upload-form">
        <input
          type="file"
          onChange={handleFileChange}
          className="file-input"
        />
        <button type="submit" className="submit-button">
          Generar Certificados
        </button>
      </form>

      {/* Mostrar el nombre del archivo si está seleccionado */}
      {fileName && (
        <p className="file-name">Archivo seleccionado: {fileName}</p>
      )}

      {message && <p className="message">{message}</p>}


      {/* <div className="app">
            <ProductCard
                name="Café Sello Rojo"
                price="2000"
                imgSrc="/cafe.jpg" // Aquí pones la imagen del producto
            />
        </div> */}


    </div>


  );
}

export default App;
