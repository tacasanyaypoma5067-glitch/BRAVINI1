import api from './api';

export interface FileUploadData {
  file: File;
  title?: string;
  description?: string;
  tag_ids?: number[];
  is_vault?: boolean;
}

export interface UploadedFile {
  id: number;
  filename: string;
  file_path: string;
  file_type: string;
  title?: string;
  description?: string;
  created_at: string;
  tags?: Array<{
    id: number;
    name: string;
    color: string;
  }>;
  is_vault: boolean;
}

export const filesService = {
  uploadFile: async (data: FileUploadData): Promise<UploadedFile> => {
    const formData = new FormData();
    formData.append('file', data.file);
    
    if (data.title) formData.append('title', data.title);
    if (data.description) formData.append('description', data.description);
    if (data.tag_ids) {
      data.tag_ids.forEach(id => formData.append('tag_ids', id.toString()));
    }
    if (data.is_vault) formData.append('is_vault', 'true');

    const response = await api.post('/files/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },

  getFiles: async (tagId?: number, isVault?: boolean): Promise<UploadedFile[]> => {
    const params: Record<string, any> = {};
    if (tagId) params.tag_id = tagId;
    if (isVault) params.is_vault = true;
    
    const response = await api.get('/files/', { params });
    return response.data;
  },

  deleteFile: async (fileId: number) => {
    await api.delete(`/files/${fileId}`);
  }
};
