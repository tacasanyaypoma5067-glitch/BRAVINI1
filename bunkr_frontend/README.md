# BUNKR Frontend

Frontend de la aplicación BUNKR - Tu búnker digital personal.

## Stack Tecnológico

- **React 18** con TypeScript
- **Vite** como bundler
- **Tailwind CSS** para estilos
- **Framer Motion** para animaciones
- **React Router** para navegación
- **Axios** para peticiones API

## Instalación

```bash
# Instalar dependencias
npm install

# Copiar variables de entorno
cp .env.example .env

# Iniciar servidor de desarrollo
npm run dev
```

## Estructura de Carpetas

```
src/
├── components/       # Componentes reutilizables
│   ├── VixenIcon.tsx
│   ├── TimelineCard.tsx
│   ├── FloatingActionButton.tsx
│   └── VaultModal.tsx
├── pages/           # Páginas principales
│   ├── Login.tsx
│   ├── Register.tsx
│   └── Home.tsx
├── services/        # Capa de servicios API
│   ├── api.ts
│   ├── auth.ts
│   ├── timeline.ts
│   ├── files.ts
│   └── vault.ts
├── hooks/           # Custom hooks
│   ├── useAuth.ts
│   ├── useTimeline.ts
│   └── useVault.ts
├── types/           # Tipos TypeScript
└── App.tsx          # Configuración de rutas
```

## Características Implementadas

### Autenticación
- Registro de usuario
- Login con JWT
- Persistencia de sesión
- Rutas protegidas

### Timeline
- Visualización cronológica de notas y archivos
- Creación de nuevas notas
- Feature "Un Día Como Hoy"
- Integración con backend real

### Bóveda Secreta
- Modal con teclado numérico para PIN
- Desbloqueo seguro
- Visualización de archivos encriptados
- Bloqueo manual

### Diseño
- Estética "Nordic Void" (modo oscuro nórdico)
- Icono de zorro bordado (Vixen)
- Animaciones suaves con Framer Motion
- Totalmente responsive

## Conexión con Backend

El frontend se conecta al backend en `http://localhost:8000` por defecto.
Asegúrate de tener el backend corriendo antes de iniciar el frontend.

```bash
# En una terminal, iniciar backend
cd ../bunkr_backend
uvicorn app.main:app --reload

# En otra terminal, iniciar frontend
cd bunkr_frontend
npm run dev
```

## Variables de Entorno

```env
VITE_API_URL=http://localhost:8000
```

## Scripts Disponibles

- `npm run dev` - Servidor de desarrollo
- `npm run build` - Build para producción
- `npm run preview` - Preview del build
- `npm run lint` - Linting del código
