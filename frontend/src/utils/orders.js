import api from './api.js';

const orders = {
  placeOrder: async (cart) => {
    const response = await api.post('/orders', { cart });
    return response.data.orderId;
  },
  getOrders: async () => {
    const response = await api.get('/orders');
    return response.data.orders;
  },
};

export default orders;