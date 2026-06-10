import { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import { Lock, LogOut, Key } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { useTimeline } from '../hooks/useTimeline';
import TimelineCard from '../components/TimelineCard';
import FloatingActionButton from '../components/FloatingActionButton';
import VaultModal from '../components/VaultModal';
import { FoxIcon } from '../components/VixenIcon';

const Home = () => {
  const { logout } = useAuth();
  const { timelineItems, onThisDay, isLoading, addNote } = useTimeline();
  const [isVaultOpen, setIsVaultOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Handle scroll for header effect
  const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
    setIsScrolled(e.currentTarget.scrollTop > 20);
  };

  const handleAddNote = () => {
    const content = prompt('Escribe tu nota:');
    if (content && content.trim()) {
      addNote(content.trim());
    }
  };

  const handleAddFile = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Aquí iría la lógica para subir el archivo usando filesService
      alert(`Archivo seleccionado: ${file.name}\n(La funcionalidad de upload está lista para implementar)`);
    }
    // Reset input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleAddTag = () => {
    alert('Funcionalidad de etiquetas: Próximamente');
  };

  const handleLogout = () => {
    if (confirm('¿Cerrar sesión?')) {
      logout();
      window.location.reload();
    }
  };

  return (
    <div className="h-screen bg-nordic-void flex flex-col overflow-hidden">
      {/* Hidden file input */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        className="hidden"
        accept="image/*,application/pdf,*/*"
      />

      {/* Header */}
      <motion.header
        initial={{ y: -60 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.5 }}
        className={`fixed top-0 left-0 right-0 z-30 transition-all duration-300 ${
          isScrolled ? 'bg-nordic-void/95 backdrop-blur-sm shadow-lg' : 'bg-transparent'
        }`}
      >
        <div className="px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <FoxIcon size={32} className="text-nordic-accent" />
            <div>
              <h1 className="text-lg font-display text-nordic-text">BUNKR</h1>
              <p className="text-xs text-nordic-muted">Tu búnker digital</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setIsVaultOpen(true)}
              className="p-2 rounded-lg bg-nordic-gray hover:bg-nordic-light text-nordic-muted hover:text-nordic-accent transition-colors"
              title="Bóveda Secreta"
            >
              <Lock size={18} />
            </button>
            <button
              onClick={handleLogout}
              className="p-2 rounded-lg bg-nordic-gray hover:bg-red-900/30 text-nordic-muted hover:text-red-400 transition-colors"
              title="Cerrar sesión"
            >
              <LogOut size={18} />
            </button>
          </div>
        </div>
      </motion.header>

      {/* Main Content - Timeline */}
      <main
        className="flex-1 overflow-y-auto pt-24 pb-32 px-4 md:px-8 lg:px-16"
        onScroll={handleScroll}
      >
        {/* "Un Día Como Hoy" Section */}
        {onThisDay && onThisDay.items.length > 0 && (
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mb-12"
          >
            <div className="flex items-center gap-2 mb-4">
              <Key size={16} className="text-nordic-accent" />
              <h2 className="text-sm font-display text-nordic-accent uppercase tracking-wider">
                Un Día Como Hoy
              </h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {onThisDay.items.slice(0, 3).map((item) => (
                <TimelineCard key={`otd-${item.id}`} item={item} />
              ))}
            </div>
          </motion.section>
        )}

        {/* Timeline Title */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="mb-8"
        >
          <h2 className="text-2xl font-display text-nordic-text">Línea de Tiempo</h2>
          <p className="text-nordic-muted text-sm mt-1">
            {timelineItems.length} {timelineItems.length === 1 ? 'entrada' : 'entradas'}
          </p>
        </motion.div>

        {/* Timeline Items */}
        <div className="space-y-6 max-w-3xl mx-auto">
          {isLoading && timelineItems.length === 0 ? (
            <div className="text-center py-12">
              <div className="inline-block w-8 h-8 border-2 border-nordic-accent border-t-transparent rounded-full animate-spin" />
              <p className="text-nordic-muted mt-4 text-sm">Cargando recuerdos...</p>
            </div>
          ) : timelineItems.length === 0 ? (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-center py-16"
            >
              <FoxIcon size={64} className="text-nordic-gray mx-auto mb-4 opacity-50" />
              <p className="text-nordic-muted text-lg">Tu búnker está vacío</p>
              <p className="text-nordic-muted text-sm mt-2">
                Comienza añadiendo tu primer recuerdo
              </p>
            </motion.div>
          ) : (
            timelineItems.map((item, index) => (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
              >
                <TimelineCard item={item} />
              </motion.div>
            ))
          )}
        </div>

        {/* End of Timeline Indicator */}
        {!isLoading && timelineItems.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="text-center py-8 mt-8"
          >
            <div className="w-16 h-px bg-nordic-gray mx-auto mb-4" />
            <p className="text-nordic-muted text-xs">Has llegado al principio de tu historia</p>
          </motion.div>
        )}
      </main>

      {/* Floating Action Button */}
      <FloatingActionButton
        onAddNote={handleAddNote}
        onAddFile={handleAddFile}
        onAddTag={handleAddTag}
      />

      {/* Vault Modal */}
      <VaultModal isOpen={isVaultOpen} onClose={() => setIsVaultOpen(false)} />
    </div>
  );
};

export default Home;
