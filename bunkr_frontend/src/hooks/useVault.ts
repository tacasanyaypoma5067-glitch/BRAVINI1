import { useState } from 'react';
import { vaultService, VaultUnlockData, VaultStatus, VaultFile } from '../services/vault';

export const useVault = () => {
  const [isUnlocked, setIsUnlocked] = useState(false);
  const [vaultFiles, setVaultFiles] = useState<VaultFile[]>([]);
  const [vaultStatus, setVaultStatus] = useState<VaultStatus | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const unlock = async (pin: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const status = await vaultService.unlock({ pin });
      setVaultStatus(status);
      setIsUnlocked(status.is_unlocked);
      return status;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'PIN incorrecto');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const lock = async () => {
    try {
      await vaultService.lock();
      setIsUnlocked(false);
      setVaultStatus(null);
      setVaultFiles([]);
    } catch (err: any) {
      setError('Error al bloquear la bóveda');
      throw err;
    }
  };

  const loadVaultFiles = async () => {
    if (!isUnlocked) return;
    
    setIsLoading(true);
    setError(null);
    try {
      const files = await vaultService.getVaultFiles();
      setVaultFiles(files);
      return files;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al cargar archivos de la bóveda');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const uploadFile = async (file: File, title: string, description?: string) => {
    if (!isUnlocked) throw new Error('La bóveda está bloqueada');
    
    try {
      const uploadedFile = await vaultService.uploadVaultFile(file, title, description);
      setVaultFiles(prev => [uploadedFile, ...prev]);
      return uploadedFile;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al subir archivo a la bóveda');
      throw err;
    }
  };

  const downloadFile = async (fileId: number) => {
    try {
      const blob = await vaultService.downloadVaultFile(fileId);
      return blob;
    } catch (err: any) {
      setError('Error al descargar el archivo');
      throw err;
    }
  };

  return {
    isUnlocked,
    vaultFiles,
    vaultStatus,
    isLoading,
    error,
    unlock,
    lock,
    loadVaultFiles,
    uploadFile,
    downloadFile,
  };
};
