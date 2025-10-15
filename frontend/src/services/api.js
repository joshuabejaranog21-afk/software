import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Interceptor para agregar el token a las requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar respuestas y errores
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Si el error es 401 (no autorizado), el token puede estar expirado
    if (error.response && error.response.status === 401) {
      // Limpiar el localStorage
      localStorage.removeItem('token');
      localStorage.removeItem('user');

      // Redirigir al login
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (email, password) => api.post('/login', { email, password }),
  verifyToken: () => api.get('/verify-token'),
};

export const usersAPI = {
  getUsers: () => api.get('/usuarios'),
  createUser: (userData) => api.post('/usuarios', userData),
  deleteUser: (id) => api.delete(`/usuarios/${id}`),
};

export const contactsAPI = {
  getContacts: () => api.get('/contactos'),
  createContact: (contactData) => api.post('/contactos', contactData),
  updateContact: (id, contactData) => api.put(`/contactos/${id}`, contactData),
  deleteContact: (id) => api.delete(`/contactos/${id}`),
};

export default api;