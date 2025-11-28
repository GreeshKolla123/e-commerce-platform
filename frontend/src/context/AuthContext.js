import React, { createContext, useState } from 'react';
const AuthContext = createContext();
const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const login = async (username, password) => {
    try {
      const response = await api.post('/login', { username, password });
      const { token, user } = response.data;
      setToken(token);
      setUser(user);
    } catch (error) {
      console.error(error);
    }
  };
  const logout = async () => {
    try {
      await api.post('/logout');
      setToken(null);
      setUser(null);
    } catch (error) {
      console.error(error);
    }
  };
  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
export { AuthProvider, AuthContext };