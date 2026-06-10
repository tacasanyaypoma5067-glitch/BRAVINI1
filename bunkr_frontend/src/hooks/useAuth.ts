import { useState } from 'react';
import { authService, LoginData, RegisterData } from '../services/auth';

export const useAuth = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const login = async (data: LoginData) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await authService.login(data);
      return response;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al iniciar sesión');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (data: RegisterData) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await authService.register(data);
      return response;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al registrar usuario');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    authService.logout();
  };

  const isAuthenticated = () => {
    return authService.isAuthenticated();
  };

  return {
    isLoading,
    error,
    login,
    register,
    logout,
    isAuthenticated,
  };
};
