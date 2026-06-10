import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { authService } from './services/auth';
import Login from './pages/Login';
import Register from './pages/Register';
import Home from './pages/Home';

// Componente para rutas protegidas
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const isAuthenticated = authService.isAuthenticated();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return <>{children}</>;
};

// Componente para rutas públicas (redirige si ya está autenticado)
const PublicRoute = ({ children }: { children: React.ReactNode }) => {
  const isAuthenticated = authService.isAuthenticated();
  
  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }
  
  return <>{children}</>;
};

function App() {
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);

  useEffect(() => {
    // Verificar autenticación al cargar
    setIsCheckingAuth(false);
  }, []);

  if (isCheckingAuth) {
    return (
      <div className="min-h-screen bg-nordic-void flex items-center justify-center">
        <div className="text-nordic-muted">Cargando...</div>
      </div>
    );
  }

  return (
    <BrowserRouter>
      <Routes>
        {/* Rutas Públicas */}
        <Route
          path="/login"
          element={
            <PublicRoute>
              <Login />
            </PublicRoute>
          }
        />
        <Route
          path="/register"
          element={
            <PublicRoute>
              <Register />
            </PublicRoute>
          }
        />

        {/* Rutas Protegidas */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />

        {/* Ruta por defecto */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
