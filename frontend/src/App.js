import React, { useState, useEffect } from 'react';
import './App.css';
import { authAPI, usersAPI, contactsAPI } from './services/api';

function App() {
  const [user, setUser] = useState(null);
  const [currentView, setCurrentView] = useState('login');
  const [users, setUsers] = useState([]);
  const [contacts, setContacts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    // Verificar si hay un usuario logueado
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    if (token && userData) {
      setUser(JSON.parse(userData));
      setCurrentView('dashboard');
    }
  }, []);

  const login = async (email, password) => {
    try {
      setLoading(true);
      setError('');
      const response = await authAPI.login(email, password);
      
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      
      setUser(response.data.user);
      setCurrentView('dashboard');
      setSuccess('Login exitoso!');
    } catch (error) {
      setError(error.response?.data?.detail || 'Error en el login');
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    setCurrentView('login');
    setUsers([]);
    setContacts([]);
  };

  const loadUsers = async () => {
    try {
      const response = await usersAPI.getUsers();
      setUsers(response.data);
    } catch (error) {
      setError('Error cargando usuarios');
    }
  };

  const loadContacts = async () => {
    try {
      const response = await contactsAPI.getContacts();
      setContacts(response.data);
    } catch (error) {
      setError('Error cargando contactos');
    }
  };

  useEffect(() => {
    if (user && currentView === 'users' && user.rol === 'admin') {
      loadUsers();
    }
    if (user && currentView === 'contacts') {
      loadContacts();
    }
  }, [currentView, user]);

  const createUser = async (userData) => {
    try {
      await usersAPI.createUser(userData);
      setSuccess('Usuario creado exitosamente');
      loadUsers();
    } catch (error) {
      setError(error.response?.data?.detail || 'Error creando usuario');
    }
  };

  const deleteUser = async (id) => {
    if (window.confirm('¿Estás seguro de eliminar este usuario?')) {
      try {
        await usersAPI.deleteUser(id);
        setSuccess('Usuario eliminado');
        loadUsers();
      } catch (error) {
        setError('Error eliminando usuario');
      }
    }
  };

  const createContact = async (contactData) => {
    try {
      setError('');
      setSuccess('');
      await contactsAPI.createContact(contactData);
      setSuccess('Contacto creado exitosamente');
      loadContacts();

      // Limpiar el mensaje de éxito después de 3 segundos
      setTimeout(() => setSuccess(''), 3000);
    } catch (error) {
      const errorMsg = error.response?.data?.detail || 'Error creando contacto';
      setError(errorMsg);

      // Limpiar el mensaje de error después de 5 segundos
      setTimeout(() => setError(''), 5000);
    }
  };

  const deleteContact = async (id) => {
    if (window.confirm('¿Estás seguro de eliminar este contacto?')) {
      try {
        await contactsAPI.deleteContact(id);
        setSuccess('Contacto eliminado');
        loadContacts();
      } catch (error) {
        setError('Error eliminando contacto');
      }
    }
  };

  if (!user) {
    return <LoginComponent onLogin={login} loading={loading} error={error} />;
  }

  return (
    <div className="App">
      <nav className="navbar">
        <div className="nav-brand">
          <h2>🔐 Sistema de Agenda</h2>
        </div>
        <div className="nav-links">
          <button 
            className={currentView === 'dashboard' ? 'active' : ''}
            onClick={() => setCurrentView('dashboard')}
          >
            Dashboard
          </button>
          <button 
            className={currentView === 'contacts' ? 'active' : ''}
            onClick={() => setCurrentView('contacts')}
          >
            Contactos
          </button>
          {user.rol === 'admin' && (
            <button 
              className={currentView === 'users' ? 'active' : ''}
              onClick={() => setCurrentView('users')}
            >
              Usuarios
            </button>
          )}
          <button onClick={logout} className="logout-btn">
            Cerrar Sesión
          </button>
        </div>
      </nav>

      <div className="container">
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}

        {currentView === 'dashboard' && (
          <DashboardComponent user={user} contacts={contacts} />
        )}
        
        {currentView === 'contacts' && (
          <ContactsComponent 
            contacts={contacts}
            onCreateContact={createContact}
            onDeleteContact={deleteContact}
          />
        )}
        
        {currentView === 'users' && user.rol === 'admin' && (
          <UsersComponent 
            users={users}
            onCreateUser={createUser}
            onDeleteUser={deleteUser}
            currentUserId={user.id}
          />
        )}
      </div>
    </div>
  );
}

// Componente de Login
function LoginComponent({ onLogin, loading, error }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onLogin(email, password);
  };

  const fillCredentials = (userEmail, userPassword) => {
    setEmail(userEmail);
    setPassword(userPassword);
  };

  return (
    <div className="login-container">
      <div className="login-form">
        <h2>Iniciar Sesión</h2>

        {/* Credenciales de prueba */}
        <div className="credentials-info">
          <h3>Credenciales de Prueba:</h3>
          <div className="credential-card">
            <h4>👤 Usuario Normal</h4>
            <p><strong>Email:</strong> usuario_nuevo@test.com</p>
            <p><strong>Contraseña:</strong> 1234567</p>
            <button
              type="button"
              onClick={() => fillCredentials('usuario_nuevo@test.com', '1234567')}
              className="fill-btn"
            >
              Usar estas credenciales
            </button>
          </div>
          <div className="credential-card admin">
            <h4>👨‍💼 Administrador</h4>
            <p><strong>Email:</strong> bejaranojoshua@gmail.com</p>
            <p><strong>Contraseña:</strong> 123456</p>
            <button
              type="button"
              onClick={() => fillCredentials('bejaranojoshua@gmail.com', '123456')}
              className="fill-btn"
            >
              Usar estas credenciales
            </button>
          </div>
        </div>

        {error && <div className="error">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email:</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Ingresa tu email"
              required
            />
          </div>
          <div className="form-group">
            <label>Contraseña:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Ingresa tu contraseña"
              required
            />
          </div>
          <button type="submit" disabled={loading}>
            {loading ? 'Iniciando...' : 'Iniciar Sesión'}
          </button>
        </form>
      </div>
    </div>
  );
}

// Componente Dashboard
function DashboardComponent({ user, contacts }) {
  return (
    <div className="dashboard">
      <h2>Bienvenido, {user.nombre}</h2>
      <div className="user-info">
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Rol:</strong> {user.rol}</p>
      </div>
      <div className="stats">
        <div className="stat-card">
          <h3>📞 Total de Contactos</h3>
          <p className="stat-number">{contacts.length}</p>
        </div>
      </div>
    </div>
  );
}

// Componente Contactos
function ContactsComponent({ contacts, onCreateContact, onDeleteContact }) {
  const [formData, setFormData] = useState({
    nombre: '',
    email: '',
    telefono: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onCreateContact(formData);
    setFormData({ nombre: '', email: '', telefono: '' });
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="contacts">
      <h2>Mis Contactos</h2>
      
      <div className="form-section">
        <h3>Agregar Contacto</h3>
        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label>Nombre:</label>
              <input
                type="text"
                name="nombre"
                value={formData.nombre}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Email:</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label>Teléfono:</label>
              <input
                type="tel"
                name="telefono"
                value={formData.telefono}
                onChange={handleChange}
              />
            </div>
          </div>
          <button type="submit">Guardar Contacto</button>
        </form>
      </div>

      <div className="contacts-list">
        <h3>Lista de Contactos ({contacts.length})</h3>
        {contacts.length === 0 ? (
          <p>No tienes contactos aún.</p>
        ) : (
          <div className="contacts-grid">
            {contacts.map(contact => (
              <div key={contact.id} className="contact-card">
                <div className="contact-info">
                  <h4>{contact.nombre}</h4>
                  <p>📧 {contact.email || 'Sin email'}</p>
                  <p>📞 {contact.telefono || 'Sin teléfono'}</p>
                </div>
                <button 
                  onClick={() => onDeleteContact(contact.id)}
                  className="delete-btn"
                >
                  Eliminar
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// Componente Usuarios (Solo Admin)
function UsersComponent({ users, onCreateUser, onDeleteUser, currentUserId }) {
  const [formData, setFormData] = useState({
    nombre: '',
    email: '',
    password: '',
    rol: 'user'
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onCreateUser(formData);
    setFormData({ nombre: '', email: '', password: '', rol: 'user' });
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="users">
      <h2>Gestión de Usuarios</h2>
      
      <div className="form-section">
        <h3>Crear Usuario</h3>
        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label>Nombre:</label>
              <input
                type="text"
                name="nombre"
                value={formData.nombre}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Email:</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Contraseña:</label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Rol:</label>
              <select
                name="rol"
                value={formData.rol}
                onChange={handleChange}
              >
                <option value="user">Usuario</option>
                <option value="admin">Administrador</option>
              </select>
            </div>
          </div>
          <button type="submit">Crear Usuario</button>
        </form>
      </div>

      <div className="users-list">
        <h3>Lista de Usuarios ({users.length})</h3>
        <div className="users-grid">
          {users.map(user => (
            <div key={user.id} className="user-card">
              <div className="user-info">
                <h4>{user.nombre}</h4>
                <p>📧 {user.email}</p>
                <p>👤 {user.rol}</p>
              </div>
              {user.id !== currentUserId ? (
                <button 
                  onClick={() => onDeleteUser(user.id)}
                  className="delete-btn"
                >
                  Eliminar
                </button>
              ) : (
                <span className="current-user">Tú</span>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
