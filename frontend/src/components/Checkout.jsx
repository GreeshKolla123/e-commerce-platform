import React from 'react';
function Checkout() {
  return (
    <div>
      <h2>Checkout</h2>
      <form>
        <label>Payment Method:</label>
        <select>
          <option value="credit">Credit Card</option>
          <option value="paypal">PayPal</option>
        </select>
        <button>Pay Now</button>
      </form>
    </div>
  );
}
export default Checkout;