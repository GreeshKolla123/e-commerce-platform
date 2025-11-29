import api from './api.js';

const auth = {
  login: async (username, password) => {
    const response = await api.post('/login', { username, password });
    return response.data.token;
  },
  register: async (username, email, password) => {
    const response = await api.post('/register', { username, email, password });
    return response.data.token;
  },
};

export default auth;