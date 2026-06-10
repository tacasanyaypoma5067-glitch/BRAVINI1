import { motion, AnimatePresence } from 'framer-motion';
import { Plus, Image as ImageIcon, FileText, Tag, X } from 'lucide-react';
import { useState } from 'react';

interface FloatingActionButtonProps {
  onAddNote: () => void;
  onAddFile: () => void;
  onAddTag: () => void;
}

const FloatingActionButton = ({ onAddNote, onAddFile, onAddTag }: FloatingActionButtonProps) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleOpen = () => {
    setIsOpen(!isOpen);
  };

  const handleClose = () => {
    setIsOpen(false);
  };

  const handleAction = (action: () => void) => {
    action();
    handleClose();
  };

  return (
    <div className="fixed bottom-6 right-6 z-40">
      {/* Action Buttons */}
      <AnimatePresence>
        {isOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={handleClose}
              className="fixed inset-0 bg-black/20"
            />

            {/* Add Note Button */}
            <motion.button
              initial={{ opacity: 0, scale: 0.8, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.8, y: 20 }}
              transition={{ delay: 0 }}
              onClick={() => handleAction(onAddNote)}
              className="absolute bottom-20 right-0 flex items-center gap-2 px-4 py-3 bg-nordic-dark border border-nordic-gray rounded-lg text-nordic-text hover:bg-nordic-light hover:border-nordic-accent/50 transition-colors shadow-lg"
            >
              <FileText size={18} className="text-nordic-accent" />
              <span className="text-sm font-medium">Nueva Nota</span>
            </motion.button>

            {/* Add File Button */}
            <motion.button
              initial={{ opacity: 0, scale: 0.8, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.8, y: 20 }}
              transition={{ delay: 0.05 }}
              onClick={() => handleAction(onAddFile)}
              className="absolute bottom-20 right-32 flex items-center gap-2 px-4 py-3 bg-nordic-dark border border-nordic-gray rounded-lg text-nordic-text hover:bg-nordic-light hover:border-nordic-accent/50 transition-colors shadow-lg"
            >
              <ImageIcon size={18} className="text-nordic-accent" />
              <span className="text-sm font-medium">Subir Archivo</span>
            </motion.button>

            {/* Add Tag Button */}
            <motion.button
              initial={{ opacity: 0, scale: 0.8, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.8, y: 20 }}
              transition={{ delay: 0.1 }}
              onClick={() => handleAction(onAddTag)}
              className="absolute bottom-20 right-60 flex items-center gap-2 px-4 py-3 bg-nordic-dark border border-nordic-gray rounded-lg text-nordic-text hover:bg-nordic-light hover:border-nordic-accent/50 transition-colors shadow-lg"
            >
              <Tag size={18} className="text-nordic-accent" />
              <span className="text-sm font-medium">Nueva Etiqueta</span>
            </motion.button>
          </>
        )}
      </AnimatePresence>

      {/* Main FAB */}
      <motion.button
        onClick={toggleOpen}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        animate={{ rotate: isOpen ? 45 : 0 }}
        transition={{ duration: 0.2 }}
        className="w-14 h-14 rounded-full bg-nordic-accent hover:bg-nordic-accentLight text-white shadow-lg flex items-center justify-center transition-colors"
      >
        <Plus size={24} />
      </motion.button>
    </div>
  );
};

export default FloatingActionButton;
