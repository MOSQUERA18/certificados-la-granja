// ProductCard.jsx
import React from 'react';
import './ProductCard.css'; // Puedes estilizar con CSS externo

const ProductCard = ({ name, price, imgSrc }) => {
    return (
        <div className="product-card">
            <img className="product-image" src={imgSrc} alt={`${name}`} />
            <h2 className="product-name">{name}</h2>
            <p className="product-price">${price}</p>
        </div>
    );
};

export default ProductCard;
