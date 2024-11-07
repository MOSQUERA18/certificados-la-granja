// App.jsx
import { useState } from 'react';
import axios from 'axios';
import Plantilla from './Plantilla';
import './App.css'; // Importar el archivo de estilos

//  const RUTA_UPLOADS = process.env.REACT_APP_RUTA_UPLOADS || 'http://localhost:3000/upload'

function App() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

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
        <input type="file" onChange={handleFileChange} className="file-input" />
        <button type="submit" className="submit-button">Generar Certificados</button>
      </form>

      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default App;
