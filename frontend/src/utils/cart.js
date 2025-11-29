import api from './api.js';

const cart = {
  addProduct: async (productId, quantity) => {
    const response = await api.post('/cart', { productId, quantity });
    return response.data.cart;
  },
  getCart: async () => {
    const response = await api.get('/cart');
    return response.data.cart;
  },
};

export default cart;