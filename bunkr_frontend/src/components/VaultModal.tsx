import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';
import { useState } from 'react';
import { useVault } from '../hooks/useVault';

interface VaultModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const VaultModal = ({ isOpen, onClose }: VaultModalProps) => {
  const { unlock, isUnlocked, vaultFiles, isLoading, error, loadVaultFiles, lock } = useVault();
  const [pin, setPin] = useState('');
  const [displayPin, setDisplayPin] = useState('');

  const handleNumberClick = (num: string) => {
    if (displayPin.length < 6) {
      const newPin = displayPin + num;
      setDisplayPin(newPin);
      setPin(prev => prev + num);
    }
  };

  const handleClear = () => {
    setPin('');
    setDisplayPin('');
  };

  const handleSubmit = async () => {
    if (pin.length === 6) {
      try {
        await unlock(pin);
        await loadVaultFiles();
      } catch (err) {
        handleClear();
      }
    }
  };

  const handleClose = () => {
    handleClear();
    onClose();
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={handleClose}
            className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50"
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            className="fixed inset-0 flex items-center justify-center z-50 pointer-events-none"
          >
            <div className="bg-nordic-dark rounded-2xl p-8 max-w-md w-full mx-4 pointer-events-auto border border-nordic-gray">
              {/* Header */}
              <div className="flex items-center justify-between mb-8">
                <h2 className="text-xl font-display text-nordic-text">
                  {isUnlocked ? 'Bóveda Secreta' : 'Desbloquear Bóveda'}
                </h2>
                <button
                  onClick={handleClose}
                  className="text-nordic-muted hover:text-nordic-text transition-colors"
                >
                  <X size={20} />
                </button>
              </div>

              {!isUnlocked ? (
                /* PIN Entry */
                <div className="space-y-6">
                  {/* PIN Display */}
                  <div className="flex justify-center gap-3 mb-8">
                    {[0, 1, 2, 3, 4, 5].map((index) => (
                      <motion.div
                        key={index}
                        initial={{ scale: 0.8, opacity: 0 }}
                        animate={{
                          scale: displayPin.length > index ? 1 : 0.8,
                          opacity: displayPin.length > index ? 1 : 0.5,
                          backgroundColor: displayPin.length > index ? '#5E6AD2' : '#2A2A35'
                        }}
                        className="w-4 h-4 rounded-full"
                      />
                    ))}
                  </div>

                  {/* Error Message */}
                  {error && (
                    <motion.p
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="text-red-400 text-sm text-center"
                    >
                      {error}
                    </motion.p>
                  )}

                  {/* Numeric Keypad */}
                  <div className="grid grid-cols-3 gap-4 max-w-xs mx-auto">
                    {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((num) => (
                      <motion.button
                        key={num}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => handleNumberClick(num.toString())}
                        className="w-16 h-16 rounded-full bg-nordic-gray hover:bg-nordic-light text-nordic-text text-xl font-light transition-colors"
                      >
                        {num}
                      </motion.button>
                    ))}
                    <button
                      onClick={handleClear}
                      className="w-16 h-16 rounded-full bg-nordic-gray hover:bg-red-900/30 text-nordic-muted hover:text-red-400 text-sm transition-colors"
                    >
                      CLR
                    </button>
                    <button
                      onClick={() => handleNumberClick('0')}
                      className="w-16 h-16 rounded-full bg-nordic-gray hover:bg-nordic-light text-nordic-text text-xl font-light transition-colors"
                    >
                      0
                    </button>
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={handleSubmit}
                      disabled={pin.length !== 6 || isLoading}
                      className="w-16 h-16 rounded-full bg-nordic-accent hover:bg-nordic-accentLight text-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      {isLoading ? '⏳' : '✓'}
                    </motion.button>
                  </div>

                  <p className="text-center text-nordic-muted text-xs mt-6">
                    Ingresa tu PIN de 6 dígitos
                  </p>
                </div>
              ) : (
                /* Unlocked State - Vault Files */
                <div className="space-y-4">
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="text-center mb-6"
                  >
                    <p className="text-green-400 text-sm mb-2">✓ Bóveda desbloqueada</p>
                    <p className="text-nordic-muted text-xs">
                      {vaultFiles.length} archivo(s) encriptado(s)
                    </p>
                  </motion.div>

                  <div className="max-h-64 overflow-y-auto space-y-2">
                    {vaultFiles.length === 0 ? (
                      <p className="text-nordic-muted text-sm text-center py-8">
                        No hay archivos en la bóveda
                      </p>
                    ) : (
                      vaultFiles.map((file) => (
                        <motion.div
                          key={file.id}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          className="p-3 bg-nordic-gray rounded-lg flex items-center gap-3"
                        >
                          <div className="w-8 h-8 rounded bg-nordic-accent/20 flex items-center justify-center text-nordic-accent text-xs">
                            {file.file_type.split('/')[0]}
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-nordic-text text-sm truncate">{file.title}</p>
                            <p className="text-nordic-muted text-xs">
                              {new Date(file.created_at).toLocaleDateString()}
                            </p>
                          </div>
                          <span className="text-xs text-nordic-muted px-2 py-1 bg-nordic-light rounded">
                            🔒
                          </span>
                        </motion.div>
                      ))
                    )}
                  </div>

                  <button
                    onClick={lock}
                    className="w-full py-3 mt-4 bg-nordic-gray hover:bg-nordic-light text-nordic-text rounded-lg transition-colors"
                  >
                    Bloquear Bóveda
                  </button>
                </div>
              )}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

export default VaultModal;
