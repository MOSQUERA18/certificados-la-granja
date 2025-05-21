// componentes/CarpetaCreator.jsx
import React from "react";
import './CarpetaCreator.css';

function CarpetaCreator({ nombreCarpeta, setNombreCarpeta }) {
  return (
    <div className="carpeta-creator">
      <input
        type="text"
        placeholder="Nombre de la carpeta"
        value={nombreCarpeta}
        onChange={(e) => setNombreCarpeta(e.target.value)}
        className="input-carpeta"
      />
    </div>
  );
}

export default CarpetaCreator;
