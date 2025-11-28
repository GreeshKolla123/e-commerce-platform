import React, { useState } from 'react';
function ShoppingCart() {
  const [cart, setCart] = useState([]);
  const handleAddToCart = (product) => {
    setCart([...cart, product]);
  };
  return (
    <div>
      <h2>Shopping Cart</h2>
      <ul>
        {cart.map((product) => (
          <li key={product.id}>{product.name}</li>
        ))}
      </ul>
      <button onClick={() => handleAddToCart({ id: 1, name: 'Product 1' })}>Add to Cart</button>
    </div>
  );
}
export default ShoppingCart;