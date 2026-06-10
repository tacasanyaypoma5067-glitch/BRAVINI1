import { motion } from 'framer-motion';
import { Link, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { FoxIcon } from '../components/VixenIcon';

const Register = () => {
  const navigate = useNavigate();
  const { register, isLoading, error } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [formError, setFormError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError('');

    if (!email || !password) {
      setFormError('Por favor completa todos los campos requeridos');
      return;
    }

    if (password !== confirmPassword) {
      setFormError('Las contraseñas no coinciden');
      return;
    }

    if (password.length < 6) {
      setFormError('La contraseña debe tener al menos 6 caracteres');
      return;
    }

    try {
      await register({ email, password, full_name: fullName || undefined });
      navigate('/');
    } catch (err: any) {
      // Error ya manejado por el hook
    }
  };

  return (
    <div className="min-h-screen bg-nordic-void flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="w-full max-w-md"
      >
        {/* Vixen Header */}
        <div className="text-center mb-12">
          <motion.div
            animate={{ y: [0, -10, 0] }}
            transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
            className="inline-block mb-6"
          >
            <FoxIcon size={80} className="text-nordic-accent mx-auto" />
          </motion.div>
          <h1 className="text-3xl font-display text-nordic-text mb-2">BUNKR</h1>
          <p className="text-nordic-muted text-sm">Crea tu búnker digital</p>
        </div>

        {/* Register Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label htmlFor="fullName" className="block text-sm text-nordic-muted mb-2">
              Nombre completo <span className="text-nordic-gray">(opcional)</span>
            </label>
            <input
              type="text"
              id="fullName"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              className="w-full px-4 py-3 bg-nordic-dark border border-nordic-gray rounded-lg text-nordic-text focus:outline-none focus:border-nordic-accent transition-colors"
              placeholder="Tu nombre"
              autoComplete="name"
            />
          </div>

          <div>
            <label htmlFor="email" className="block text-sm text-nordic-muted mb-2">
              Correo electrónico
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 bg-nordic-dark border border-nordic-gray rounded-lg text-nordic-text focus:outline-none focus:border-nordic-accent transition-colors"
              placeholder="tu@correo.com"
              autoComplete="email"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm text-nordic-muted mb-2">
              Contraseña
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 bg-nordic-dark border border-nordic-gray rounded-lg text-nordic-text focus:outline-none focus:border-nordic-accent transition-colors"
              placeholder="••••••••"
              autoComplete="new-password"
            />
          </div>

          <div>
            <label htmlFor="confirmPassword" className="block text-sm text-nordic-muted mb-2">
              Confirmar contraseña
            </label>
            <input
              type="password"
              id="confirmPassword"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="w-full px-4 py-3 bg-nordic-dark border border-nordic-gray rounded-lg text-nordic-text focus:outline-none focus:border-nordic-accent transition-colors"
              placeholder="••••••••"
              autoComplete="new-password"
            />
          </div>

          {(error || formError) && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-red-400 text-sm text-center"
            >
              {error || formError}
            </motion.p>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3 bg-nordic-accent hover:bg-nordic-accentLight text-white rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Creando cuenta...' : 'Crear Cuenta'}
          </button>
        </form>

        {/* Login Link */}
        <p className="text-center mt-8 text-nordic-muted text-sm">
          ¿Ya tienes cuenta?{' '}
          <Link to="/login" className="text-nordic-accent hover:text-nordic-accentLight transition-colors">
            Iniciar sesión
          </Link>
        </p>
      </motion.div>
    </div>
  );
};

export default Register;
