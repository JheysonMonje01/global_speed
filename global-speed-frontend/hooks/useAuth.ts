import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';

export const useAuthHook = () => {
  const { user, login, logout } = useAuth();

  const handleLogin = async (credentials: { email: string; password: string }) => {
    try {
      const response = await axios.post('/api/auth/login', credentials);
      const userData = response.data;
      login(userData);
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  const handleLogout = () => {
    logout();
  };

  return {
    user,
    login: handleLogin,
    logout: handleLogout,
  };
};
