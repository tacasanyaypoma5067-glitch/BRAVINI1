import api from './api';

export interface VaultUnlockData {
  pin: string;
  biometric_token?: string;
}

export interface VaultFile {
  id: number;
  filename: string;
  file_path: string;
  file_type: string;
  title: string;
  description?: string;
  created_at: string;
  encrypted: boolean;
}

export interface VaultStatus {
  is_unlocked: boolean;
  unlocked_at?: string;
  expires_at?: string;
}

export const vaultService = {
  unlock: async (data: VaultUnlockData): Promise<VaultStatus> => {
    const response = await api.post('/vault/unlock', data);
    return response.data;
  },

  lock: async (): Promise<void> => {
    await api.post('/vault/lock');
  },

  getStatus: async (): Promise<VaultStatus> => {
    const response = await api.get('/vault/status');
    return response.data;
  },

  uploadVaultFile: async (file: File, title: string, description?: string): Promise<VaultFile> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', title);
    if (description) formData.append('description', description);

    const response = await api.post('/vault/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },

  getVaultFiles: async (): Promise<VaultFile[]> => {
    const response = await api.get('/vault/files');
    return response.data;
  },

  downloadVaultFile: async (fileId: number): Promise<Blob> => {
    const response = await api.get(`/vault/files/${fileId}/download`, {
      responseType: 'blob',
    });
    return response.data;
  }
};
