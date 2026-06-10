import api from './api';

export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user?: {
    id: number;
    email: string;
    full_name?: string;
  };
}

export const authService = {
  login: async (data: LoginData): Promise<AuthResponse> => {
    const response = await api.post('/auth/login', data);
    if (response.data.access_token) {
      localStorage.setItem('bunkr_token', response.data.access_token);
    }
    return response.data;
  },

  register: async (data: RegisterData): Promise<AuthResponse> => {
    const response = await api.post('/auth/register', data);
    if (response.data.access_token) {
      localStorage.setItem('bunkr_token', response.data.access_token);
    }
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('bunkr_token');
  },

  getToken: (): string | null => {
    return localStorage.getItem('bunkr_token');
  },

  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('bunkr_token');
  }
};
