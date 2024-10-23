// App.jsx (Frontend - React)

import { useState } from 'react';
import axios from 'axios';

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
    // eslint-disable-next-line no-unused-vars
    } catch (error) {
      setMessage('Error al generar los certificados');
    }
  };

  return (
    <div>
      <h1>Generador de Certificados</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Subir archivo</button>
      </form>
      <p>{message}</p>
    </div>
  );
}

export default App;
