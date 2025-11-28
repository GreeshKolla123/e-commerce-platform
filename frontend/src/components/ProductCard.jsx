import React from 'react';
function ProductCard({ product }) {
  return (
    <div>
      <h2>{product.name}</h2>
      <p>{product.description}</p>
      <p>Price: {product.price}</p>
    </div>
  );
}
export default ProductCard;