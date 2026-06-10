# 🏛️ BUNKR - Tu Búnker Digital Personal

## Documento de Diseño de Producto & UX/UI

> **Filosofía:** Minimalismo Absoluto × Organización Máxima × Privacidad Total  
> **Lema:** *"Donde lo importante permanece en silencio"*

---

## 1. 🗝️ SISTEMA DE BÓVEDA OCULTA Y SEGURIDAD BIOMÉTRICA

### Concepto: "La Capa Fantasma"

#### Diseño UX

**Acceso Principal Fluído:**
- **Pantalla de bloqueo invisible:** La app no muestra logo ni nombre en el launcher. Se presenta como una calculadora o app de notas genérica ("Notas Rápidas")
- **Desbloqueo biométrico silencioso:** 
  - Al abrir la app, solicita Face ID/Touch ID inmediatamente
  - Sin animaciones llamativas, solo un sutil pulso de luz en el borde superior
  - Si falla el reconocimiento, la app muestra contenido "falso" (notas genéricas de ejemplo)

**La Capa Fantasma (Vault Within Vault):**
```
Nivel 1 → App Principal (contenido normal)
    ↓ (gesto específico: tocar 3 esquinas + mantener)
Nivel 2 → Bóveda Estándar (archivos privados)
    ↓ (gesto específico: deslizar desde abajo con 3 dedos)
Nivel 3 → CAPA FANTASMA (hiperconfidencial)
```

**Interacción con la Capa Fantasma:**
- **Activación por gesto secreto:** Mantener presionadas simultáneamente las esquinas superior izquierda e inferior derecha por 2 segundos
- **Sin indicador visual:** No hay icono, no hay etiqueta, no hay contador de archivos
- **Autodestrucción de sesión:** Al salir de la capa fantasma, se borra cualquier cache temporal inmediatamente
- **Modo pánico:** Si el sistema detecta 3 intentos fallidos biométricos consecutivos, la capa fantasma se "oculta" por 24 horas

**Flujo de Acceso Biométrico:**
```
┌─────────────────────────────────┐
│  [App se abre]                  │
│         ↓                       │
│  [Face ID automático]           │
│         ↓                       │
│  ✓ Exitoso → Acceso directo     │
│  ✗ Fallido → Contenido señuelo  │
│         ↓                       │
│  [Gesto secreto]                │
│         ↓                       │
│  [Segunda verificación]         │
│         ↓                       │
│  ✓ Capa Fantasma activada       │
└─────────────────────────────────┘
```

#### Beneficio
- **Privacidad por diseño:** Nadie sospecharía que existe contenido ultra-secreto
- **Protección multicapa:** Incluso si alguien accede a tu bóveda principal, la capa fantasma permanece invisible
- **Acceso rápido pero seguro:** La biometría fluida elimina fricción sin comprometer seguridad
- **Tranquilidad mental:** Saber que tus documentos más sensibles tienen protección extrema

---

## 2. 🏷️ ETIQUETADO CROSS-FORMAT POR "CONTEXTO O PROYECTOS"

### Concepto: "Orbitas Contextuales"

#### Diseño UX

**Sistema Visual de Etiquetas Dinámicas:**

En lugar de carpetas jerárquicas, implementamos **"Órbitas"** - espacios contextuales donde coexisten todos los formatos:

```
┌─────────────────────────────────────────────┐
│  MIS ÓRBITAS                                │
│                                             │
│  ● Proyecto Personal                        │
│    └─ 3 fotos · 2 PDFs · 5 notas            │
│                                             │
│  ● Trámites 2024                            │
│    └─ 8 documentos · 1 nota                 │
│                                             │
│  ● Inspiración                              │
│    └─ 15 fotos · 3 links · 7 notas          │
│                                             │
│  ● Salud                                    │
│    └─ 4 PDFs · 2 fotos · 1 nota médica      │
└─────────────────────────────────────────────┘
```

**Interfaz de Vista Unificada:**
- **Grid inteligente:** Todos los archivos dentro de una órbita se muestran en un grid adaptativo
  - Fotos: thumbnails cuadrados con bordes redondeados suaves
  - PDFs: iconos minimalistas con las primeras 3 letras del título
  - Notas: tarjetas con preview de 2 líneas de texto
  - Todo mezclado cronológicamente o por relevancia

**Creación Rápida de Contenido Contextual:**
```
Botón "+" flotante (siempre visible)
    ↓
[¿Qué quieres añadir?]
    ├── 📸 Foto/Cámara
    ├── 📄 Archivo
    ├── ✍️ Nota rápida
    └── 🔗 Enlace
        ↓
[Selecciona Órbita existente o crea nueva]
        ↓
[Contenido añadido con etiqueta automática]
```

**Sistema de Etiquetas Anidadas:**
- Cada órbita puede tener **sub-etiquetas** opcionales
- Ejemplo: `Proyecto Personal > Viaje Japón > Día 3`
- Visualmente: breadcrumbs horizontales en la parte superior
- Navegación: swipe horizontal entre niveles

**Búsqueda Inteligente Cross-Formato:**
- Barra de búsqueda única que indexa TODO
- Resultados agrupados por órbita, no por tipo de archivo
- Filtros rápidos: "Solo fotos", "Solo documentos", "Últimos 7 días"

**Vista de Línea de Tiempo por Órbita:**
```
PROYECTO PERSONAL
────────────────────────────────────
Hoy
  📝 Nota: "Ideas para el redesign"
  📸 Foto_234.png
  
Ayer
  📄 Contrato_v2.pdf
  📸 Foto_231.png
  📝 Nota: "Reunión con equipo"
  
15 Oct 2024
  📸 Foto_220.png
  📄 Presupuesto.xlsx
────────────────────────────────────
```

#### Beneficio
- **Contexto sobre categoría:** Agrupas por significado, no por tipo de archivo
- **Flexibilidad total:** Un PDF de contrato y una foto del firmado viven juntos
- **Reducción de fricción:** No decides "dónde guardarlo", decides "a qué contexto pertenece"
- **Recuperación intuitiva:** Encuentras todo relacionado con un proyecto en un solo lugar
- **Escalabilidad:** Puedes tener 5 ó 500 órbitas sin perder claridad visual

---

## 3. 📅 LÍNEA DE TIEMPO DE RECUERDOS Y NOTAS

### Concepto: "El Muro Silencioso"

#### Diseño UX

**Diseño de Interfaz Minimalista:**

```
┌─────────────────────────────────┐
│  ←  Octubre 2024           ⚙️  │
│                                 │
│  ───────────────────────────    │
│                                 │
│  28  LUN                        │
│  ─────────                      │
│  [Foto del atardecer]           │
│  "Día perfecto en la playa"     │
│                                 │
│  27  DOM                        │
│  ─────────                      │
│  [Foto café] [Nota]             │
│  "Reflexiones matutinas..."     │
│                                 │
│  26  SÁB                        │
│  ─────────                      │
│  "Día de productividad"         │
│  📄 Documento adjunto           │
│                                 │
│  ⋮                              │
│                                 │
│  ───────────────────────────    │
│  [+ Nuevo recuerdo]             │
└─────────────────────────────────┘
```

**Características Clave:**

1. **Scroll Infinito Temporal:**
   - Navegación vertical suave por meses/años
   - Indicador de mes/año aparece sutilmente al hacer scroll
   - Swipe lateral para cambiar entre vista mensual/anual

2. **"Un Día Como Hoy" (On This Day):**
   - Notificación discreta una vez al día (configurable)
   - Al abrir: carousel horizontal con recuerdos de años anteriores
   - Diseño: tarjetas full-width con foto principal + pequeña nota
   - Opción de "revivir" (añadir nota nueva al recuerdo antiguo)

3. **Entradas Mixtas Automáticas:**
   - El sistema sugiere automáticamente combinar fotos + notas del mismo día
   - Tú decides si aceptar o mantener separados
   - Ejemplo: 5 fotos de un evento + 1 nota = 1 entrada consolidada

4. **Modo "Solo Hoy":**
   - Botón flotante que te lleva directamente a hoy
   - Tecla rápida para añadir nota/foto del momento
   - Timestamp automático preciso (hora exacta)

5. **Vista de Calendario Minimalista:**
   - Toggle para cambiar de timeline a vista de calendario
   - Días con contenido tienen un punto sutil debajo del número
   - Toque en un día → expande ese día en vista detallada

6. **Búsqueda Temporal Inteligente:**
   - "Mostrar recuerdos de verano 2023"
   - "Notas de marzo donde mencioné 'proyecto'"
   - "Fotos de cumpleaños de los últimos 5 años"

**Micro-interacciones:**
- Pull-to-refresh muestra la fecha actual con animación sutil
- Tocar una foto la expande en fullscreen con gesto de pellizco
- Deslizar una entrada hacia la izquierda → opciones (editar, eliminar, exportar)
- Deslizar hacia la derecha → añadir nota rápida a esa entrada

#### Beneficio
- **Narrativa personal continua:** Tu vida documentada sin esfuerzo
- **Contexto emocional:** Las notas dan significado a las fotos
- **Descubrimiento serendípico:** Reencuentras momentos olvidados
- **Cero ruido:** Solo lo importante, presentado elegantemente
- **Legado digital:** Una cronología curada de tu vida

---

## 4. 🎨 INTERFAZ VISUAL MINIMALISTA

### Concepto: "Nordic Void" (Vacío Nórdico)

#### Paleta de Colores

**Modo Oscuro (Principal - 90% uso):**
```
Fondo Principal:      #0A0A0C (Negro casi puro, ligeramente azulado)
Fondo Secundario:     #141416 (Para tarjetas/secciones)
Borde Sutil:          #1F1F22 (Separadores casi invisibles)
Texto Primario:       #E8E8EA (Blanco roto, nunca #FFFFFF puro)
Texto Secundario:     #8E8E93 (Gris medio para metadatos)
Acento Principal:     #5E6AD2 (Índigo nórdico - botones, links)
Acento Secundario:    #2D5D51 (Verde bosque profundo - éxito/confirmación)
Alerta/Peligro:       #A84646 (Rojo apagado, nunca saturado)
```

**Modo Claro (Opcional - 10% uso):**
```
Fondo Principal:      #FAFAFB (Blanco con toque grisáceo)
Fondo Secundario:     #F2F2F4 (Tarjetas)
Borde Sutil:          #E5E5E8
Texto Primario:       #1A1A1C (Negro suave)
Texto Secundario:     #6E6E73
Acento Principal:     #5E6AD2 (Mismo índigo)
```

**Transiciones entre modos:**
- Fade suave de 300ms
- Nunca usar toggle visible, sigue configuración del sistema
- Opción de "modo automático según hora del día"

#### Tipografía

**Familia Principal:** `Inter` (Google Fonts) o `SF Pro Display` (iOS nativo)

```
Títulos Grandes:      Inter Regular, 24px, #E8E8EA
Subtítulos:           Inter Medium, 18px, #E8E8EA
Cuerpo de Texto:      Inter Regular, 16px, #E8E8EA
Metadatos/Feitas:     Inter Regular, 13px, #8E8E93
Botones/CTA:          Inter Medium, 15px, #E8E8EA
Labels Pequeños:      Inter Regular, 12px, #8E8E93
```

**Reglas Tipográficas:**
- Nunca más de 2 pesos diferentes en una pantalla
- Interlineado generoso: 1.5x para cuerpo, 1.3x para títulos
- Alineación siempre a la izquierda (nada centrado excepto logos)
- Máximo 45-65 caracteres por línea para legibilidad

#### Layout y Distribución

**Principios de Diseño:**

1. **Espacio Negativo Activo:**
   - Márgenes generosos: mínimo 24px en bordes de pantalla
   - Padding interno: 16-20px entre elementos relacionados
   - El vacío NO es desperdicio, es respiración visual

2. **Jerarquía por Espacio, no por Color:**
   ```
   ┌─────────────────────────────────┐
   │  24px                           │
   │  Título Principal               │
   │  20px                           │
   │  Subtítulo/descripción breve    │
   │  32px                           │
   │  [Contenido principal]          │
   │  24px                           │
   │  [Elemento secundario]          │
   │  24px                           │
   └─────────────────────────────────┘
   ```

3. **Grid Flexible de 4 Columnas:**
   - Móvil: 4 columnas con gutter de 16px
   - Tablet: 8 columnas con gutter de 24px
   - Web: 12 columnas con gutter de 32px
   - Elementos importantes ocupan 4 columnas (full-width en móvil)

4. **Componentes Esenciales:**

   **Tarjeta Minimalista:**
   ```
   ┌─────────────────────────────┐
   │                             │
   │  [Imagen/Icono opcional]    │
   │                             │
   │  Título                     │
   │  Metadata en gris pequeño   │
   │                             │
   └─────────────────────────────┘
   ```
   - Border-radius: 12px (suave pero definido)
   - Sin sombras, solo contraste de color de fondo
   - Borde de 1px solo cuando es necesario diferenciar

   **Botón Primario:**
   ```
   ┌─────────────────┐
   │   Texto CTA     │
   └─────────────────┘
   ```
   - Altura: 48px (touch-friendly)
   - Fondo: #5E6AD2 (índigo)
   - Texto: #FFFFFF
   - Border-radius: 10px
   - Sin iconos innecesarios

   **Botón Secundario:**
   - Mismo tamaño, solo borde (#1F1F22), fondo transparente
   - Para acciones menos críticas

5. **Navegación Inferior (Tab Bar):**
   ```
   ┌─────────────────────────────────┐
   │                                 │
   │     🏠      📂      📅      ⚙️   │
   │   Inicio  Órbitas  Tiempo  Ajustes
   └─────────────────────────────────┘
   ```
   - 4 pestañas máximo
   - Iconos lineales de 24px
   - Label solo debajo del icono activo
   - Altura: 64px
   - Borde superior sutil: 1px #1F1F22

#### Micro-interacciones

**Principio:** "Susurros, no gritos"

1. **Feedback Táctil:**
   - Haptic feedback ligero en todas las acciones confirmatorias
   - Duración: 10-15ms (casi imperceptible pero presente)

2. **Animaciones de Transición:**
   - Duración estándar: 250ms
   - Easing: `cubic-bezier(0.4, 0.0, 0.2, 1)` (suave, natural)
   - Nunca animar más de 2 propiedades simultáneamente

3. **Estados de Carga:**
   - Skeleton screens en lugar de spinners
   - Fade-in progresivo del contenido
   - Nunca mostrar "loading" por más de 2 segundos sin feedback

4. **Hover States (Web):**
   - Ligero aumento de brillo en elementos interactivos
   - Cambio de cursor a pointer
   - Transición de 150ms

5. **Pull-to-Refresh:**
   - Indicador minimalista: solo una línea que se expande
   - Color: #5E6AD2 (índigo)
   - Haptic feedback al completar

6. **Confirmaciones Silenciosas:**
   - Al guardar/eliminar: toast notification de 2 segundos
   - Aparece desde abajo, desaparece automáticamente
   - Sin sonido, solo visual + haptic ligero

#### Ejemplo de Pantalla Completa

```
┌─────────────────────────────────────────────┐
│  12:30                               🔋 100%│
├─────────────────────────────────────────────┤
│                                             │
│  24px                                       │
│  Mis Órbitas                                │
│  20px                                       │
│  6 proyectos activos                        │
│  32px                                       │
│  ┌─────────────────────────────────────┐   │
│  │                                     │   │
│  │  ●  Proyecto Personal               │   │
│  │     3 fotos · 2 PDFs · 5 notas      │   │
│  │                                     │   │
│  └─────────────────────────────────────┘   │
│  16px                                       │
│  ┌─────────────────────────────────────┐   │
│  │                                     │   │
│  │  ●  Trámites 2024                   │   │
│  │     8 documentos · 1 nota           │   │
│  │                                     │   │
│  └─────────────────────────────────────┘   │
│  16px                                       │
│  ┌─────────────────────────────────────┐   │
│  │                                     │   │
│  │  ●  Inspiración                     │   │
│  │     15 fotos · 3 links · 7 notas    │   │
│  │                                     │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  32px                                       │
│                                             │
├─────────────────────────────────────────────┤
│           🏠      📂      📅      ⚙️        │
│         Inicio  Órbitas  Tiempo  Ajustes    │
└─────────────────────────────────────────────┘
```

#### Beneficio
- **Paz visual:** Tu mente descansa al usar la app, no se cansa
- **Enfoque sostenido:** Sin distracciones, solo lo esencial
- **Claridad inmediata:** Sabes dónde estás y qué puedes hacer
- **Experiencia premium:** El minimalismo bien ejecutado se siente lujoso
- **Accesibilidad:** Alto contraste, textos legibles, touch targets grandes

---

## 🌟 CONCEPTO ÚNICO: "El Principio del Iceberg"

### Innovación Diferenciadora

**Filosofía:** *Lo que ves es solo el 10%, el 90% está protegido bajo la superficie*

**Implementación:**

1. **Dashboard "Zen Mode":**
   - Por defecto, la pantalla de inicio muestra SOLO:
     - Fecha actual
     - Una frase/motivación personal (configurable)
     - Botón "+" para añadir contenido
   - Nada más. Sin contadores, sin previews, sin ruido.

2. **Revelación Progresiva:**
   - Swipe hacia arriba → revela tus órbitas recientes
   - Swipe hacia abajo → revela línea de tiempo de hoy
   - Toque largo en cualquier lugar → modo edición/organización
   - La interfaz "respira" y muestra información solo cuando la necesitas

3. **Inteligencia Contextual Silenciosa:**
   - La app aprende tus patrones sin preguntar
   - Mañanas: prioriza notas y trámites
   - Noches: prioriza recuerdos y reflexión
   - Fines de semana: prioriza fotos e inspiración
   - Todo esto ocurre sin configuraciones explícitas

4. **Modo "Enfoque Total":**
   - Activado por gesto o automáticamente en ciertas horas
   - Oculta TODAS las órbitas excepto 1 que tú elijas
   - La app se convierte en un espacio monolítico para ese contexto
   - Ideal para sesiones de trabajo profundas

5. **Exportación/Emergencia:**
   - "Modo maleta": exporta toda una órbita en un paquete cifrado
   - Código de emergencia: si ingresas un PIN especial bajo coerción, muestra contenido falso creíble
   - Backup automático cifrado en ubicación que solo tú conoces

---

## 📊 RESUMEN DE CARACTERÍSTICAS POR PLATAFORMA

| Característica | Móvil (iOS/Android) | Web |
|---------------|---------------------|-----|
| Biometría | Face ID / Touch ID | WebAuthn / YubiKey |
| Capa Fantasma | ✅ Gestos táctiles | ✅ Combinación de teclas |
| Órbitas | ✅ Vista unificada | ✅ Grid adaptable |
| Línea de Tiempo | ✅ Scroll infinito | ✅ Vista calendario |
| Modo Oscuro | ✅ Nativo | ✅ Sistema + manual |
| Offline | ✅ Completo | ❌ Limitado |
| Notificaciones | ✅ Push discretas | ✅ Browser notifications |
| Widgets | ✅ iOS/Android home | ❌ N/A |

---

## 🚀 ROADMAP SUGERIDO

### Fase 1: MVP (Mes 1-3)
- [ ] Autenticación biométrica básica
- [ ] Sistema de órbitas (crear, editar, eliminar)
- [ ] Upload de fotos, PDFs, notas
- [ ] Línea de tiempo básica
- [ ] Modo oscuro nórdico

### Fase 2: Seguridad Avanzada (Mes 4-5)
- [ ] Capa fantasma con gestos
- [ ] Cifrado de extremo a extremo
- [ ] Contenido señuelo
- [ ] Modo pánico

### Fase 3: Inteligencia & Automatización (Mes 6-7)
- [ ] Búsqueda cross-formato inteligente
- [ ] Sugestión automática de agrupación
- [ ] "Un día como hoy"
- [ ] Modo enfoque contextual

### Fase 4: Expansión (Mes 8+)
- [ ] Versión web completa
- [ ] Sincronización multi-dispositivo
- [ ] Widgets personalizables
- [ ] API para integraciones limitadas

---

## 🎯 MÉTRICAS DE ÉXITO (UX)

1. **Tiempo para añadir contenido:** < 5 segundos desde abrir la app
2. **Tasa de retención a 30 días:** > 80% (uso diario)
3. **NPS (Net Promoter Score):** > 70
4. **Reducción de estrés reportada:** Medido mediante survey trimestral
5. **Contenido promedio por usuario:** > 50 items en primeros 3 meses

---

## 🦊 MASCOTA: "VIXEN" - EL ZORRO BORDADO (CONCEPTO HARLEY MARY)

**Inspiración:** Estilo bordado artesanal mexicano (tipo suéter/chompa de Harley Mary), con hilos de colores vibrantes sobre textura de lana visible.

### Diseño Visual:
- **Estética:** Zorro estilizado con puntadas visibles, ojos grandes tipo "ojo de cerradura", orejas puntiagudas con interior rosa bordado
- **Colores:** 
  - Naranja quemado (`#D97706`) para el cuerpo
  - Blanco hueso (`#FEF3C7`) para pecho y punta de cola
  - Negro carbón (`#1F2937`) para contornos
  - Rosa suave (`#FCA5A5`) para detalles interiores
- **Textura:** Efecto de tejido visible en los bordes, como si estuviera cosido directamente en la interfaz
- **Expresiones:** 
  - 😌 **Neutral:** Zorro sentado, cola enrollada (estado normal)
  - 👀 **Alerta:** Orejas erguidas, mirada atenta (al abrir bóveda)
  - ✨ **Feliz:** Cola moviéndose suavemente (al completar backup)
  - 🔒 **Guardián:** Con pequeño candado bordado en el pecho (modo seguridad activa)

### Integración UX:
- **Aparición discreta en:**
  - Pantalla de carga inicial (sentado esperando)
  - Confirmación de acciones importantes (guardar en bóveda, crear nueva órbita)
  - Empty states (cuando no hay contenido en una sección)
  - Logros de organización (después de etiquetar 10 archivos, limpiar duplicados)

- **Micro-interacciones:**
  - Al tocar a Vixen: Pequeño guiño o movimiento de cola (haptic feedback sutil)
  - En modo oscuro: Los hilos del bordado brillan tenuemente como hilo reflectante
  - Transiciones: Vixen puede "correr" de un lado a otro durante cargas largas

- **Personalidad:**
  - Guardián silencioso: Nunca habla, solo observa y protege
  - Cómplice organizacional: Celebra tus logros con gestos sutiles
  - Misterioso: Aparece y desaparece según el contexto, nunca es intrusivo

### Beneficio Emocional:
✅ **Conexión afectiva:** Transforma una app fría en un espacio con personalidad
✅ **Identidad única:** El estilo Harley Mary la hace memorable vs. apps corporativas
✅ **Calidez artesanal:** Contrasta con la tecnología, creando "hogar digital"
✅ **Gamificación sutil:** Sin puntos ni rankings, solo la satisfacción de hacer sonreír a tu zorro

### Implementación Técnica:
- SVG animado con filtros CSS para simular textura de bordado
- Animaciones Lottie para movimientos fluidos manteniendo estética "hecha a mano"
- Modo accesibilidad: Opción para reducir animaciones o usar versión estática

---

## 📱 WIREFRAMES DETALLADOS CON VIXEN

### Dashboard - Zen Mode (Con Vixen)
```
┌─────────────────────────────────┐
│  9:41                    🔋     │
│                                 │
│         [Vixen dormitando]      │
│              💤                 │
│        (bordado suave)          │
│                                 │
│    "Buenas noches, Alex"        │
│                                 │
│  ┌───────────────────────────┐  │
│  │   ÓRBITAS RECIENTES       │  │
│  │   🏠 Casa      📋 Trabajo │  │
│  │   ✈️ Viajes    🎨 Ideas   │  │
│  └───────────────────────────┘  │
│                                 │
│  ┌───────────────────────────┐  │
│  │  📸 12    📄 5    📝 3    │  │
│  │  Fotos    Docs   Notas   │  │
│  └───────────────────────────┘  │
│                                 │
│            ┌─────┐              │
│            │  +  │              │
│            └─────┘              │
│                                 │
│  🏠      🕰️      🔍      ⚙️    │
└─────────────────────────────────┘
```

### Bóveda Fantasma - Activación por Gestos
```
┌─────────────────────────────────┐
│  ← Bóveda               [?]    │
│                                 │
│  [Vixen con candado en pecho]   │
│         🔒                      │
│                                 │
│  "Toca y mantén para revelar"   │
│                                 │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│  ░ CONTENIDO OCULTO         ░   │
│  ░ 🆔 Pasaporte             ░   │
│  ░ 📜 Contrato Casa         ░   │
│  ░ 💾 Backup Cripto         ░   │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│                                 │
│  [Desliza hacia abajo para      │
│   activar Modo Pánico]          │
└─────────────────────────────────┘
```

### Órbita Contextual - "Proyecto Casa"
```
┌─────────────────────────────────┐
│  ← Proyecto Casa        ⋮      │
│                                 │
│  ╭─────────────────────────╮    │
│  │   🏠 CASA               │    │
│  │   8 archivos • 3 notas  │    │
│  │   [Vixen señalando] 👉  │    │
│  ╰─────────────────────────╯    │
│                                 │
│  FILTROS: [Todos] [📸] [📄] [📝]│
│                                 │
│  ┌───────────────────────────┐  │
│  │ [Foto: Plano casa]        │  │
│  │ 📸 15 oct • Nota adjunta  │  │
│  └───────────────────────────┘  │
│                                 │
│  ┌───────────────────────────┐  │
│  │ [PDF: Contrato compra]    │  │
│  │ 📄 12 oct • Firmado       │  │
│  └───────────────────────────┘  │
│                                 │
│  ┌───────────────────────────┐  │
│  │ [Nota: Lista reformas]    │  │
│  │ 📝 10 oct • 3 items       │  │
│  └───────────────────────────┘  │
│                                 │
│            ┌─────┐              │
│            │  +  │              │
│            └─────┘              │
└─────────────────────────────────┘
```

---

## 🎨 SISTEMA DE DISEÑO ACTUALIZADO CON VIXEN

### Paleta de Colores Extendida
| Color | Hex | Uso |
|-------|-----|-----|
| **Zorro Naranja** | `#D97706` | Acentos principales, icono de Vixen |
| **Zorro Blanco** | `#FEF3C7` | Fondos secundarios, detalles de Vixen |
| **Hilo Negro** | `#1F2937` | Contornos del bordado, texto importante |
| **Hilo Rosa** | `#FCA5A5` | Interior de orejas de Vixen, notificaciones suaves |
| **Lana Gris** | `#4B5563` | Texturas de fondo, elementos deshabilitados |

### Tipografía con Personalidad
- **Títulos:** Inter Bold (limpio, moderno)
- **Cuerpo:** Inter Regular (legibilidad máxima)
- **Detalles artesanales:** En secciones especiales (diario, logros), usar fuente "handwritten" sutil para notas personales

### Iconografía Híbrida
- **Iconos funcionales:** Líneas limpias, minimalistas (SF Symbols style)
- **Iconos emocionales:** Detalles bordados cuando aparecen junto a Vixen
- **Transiciones:** Iconos se "transforman" en versión bordada en contextos especiales

---

## 🚀 ROADMAP CON FASES TEMÁTICAS DE VIXEN

### Fase 1: "El Despertar de Vixen" (MVP - 6 semanas)
- Dashboard Zen Mode con Vixen estático
- Sistema básico de Órbitas
- Bóveda Fantasma nivel 1 (PIN + Biometría)
- Línea de tiempo esencial

### Fase 2: "Vixen Cobra Vida" (8 semanas)
- Animaciones de Vixen (Lottie)
- Micro-interacciones táctiles
- Expresiones contextuales de Vixen
- Notificaciones personalizadas con Vixen

### Fase 3: "El Guardián Bordado" (6 semanas)
- Modo Pánico avanzado
- Contenido señuelo inteligente
- Personalización de Vixen (diferentes "chompas")
- Integración con widgets del sistema

### Fase 4: "La Manada" (Futuro)
- Múltiples guardianes (otros animales bordados)
- Coleccionables por logros de organización
- Historias mínimas de Vixen en fechas especiales
- Comunidad secreta de usuarios BUNKR (solo estética)

---

## 📊 MÉTRICAS DE ÉXITO UX CON VIXEN

| Métrica | Objetivo | Cómo Vixen ayuda |
|---------|----------|------------------|
| **Retención D7** | >65% | Conexión emocional aumenta engagement |
| **NPS** | >50 | Factor sorpresa y deleite |
| **Tiempo en bóveda** | <30 seg | Eficiencia + confianza visual |
| **Órbitas creadas/usuaria** | >5 en primer mes | Gamificación sutil motiva organización |
| **Backup automático activado** | >80% | Vixen "feliz" refuerza comportamiento positivo |

---

## 💡 PRINCIPIOS DE DISEÑO CON VIXEN

1. **"Vixen nunca interfiere"** - Siempre discreto, nunca bloquea contenido importante
2. **"El bordado es el detalle, no el protagonista"** - La funcionalidad primero, la estética acompaña
3. **"Menos es más, pero con alma"** - Minimalismo no significa frío o sin personalidad
4. **"Tu búnker, tu compañero"** - Sensación de privacidad compartida con un guardián confiable
5. **"Artesanal en lo digital"** - Contraste deliberado entre tecnología y hecho a mano

---

## 💭 PALABRAS FINALES

**BUNKR** no es solo una app de almacenamiento. Es tu santuario digital, el lugar donde lo importante vive en paz, organizado con precisión quirúrgica pero presentado con la calma de un fiordo nórdico, acompañado por Vixen, tu zorro guardián bordado.

Cada decisión de diseño responde a una pregunta: *¿Esto añade valor o solo añade ruido?*

Si la respuesta no es claramente "valor", se elimina.

Porque en un mundo de sobrecarga informativa, tu búnker es el último refugio de claridad... con un toque de calidez artesanal mexicana.

---

*Documento creado para BUNKR - Tu Búnker Digital Personal*  
*Diseñado con filosofía: Minimalismo Nórdico + Alma Artesanal Mexicana*  
*© 2024 - Concepto exclusivo con Vixen el Zorro Bordado*  
*Versión 2.0 - "Nordic Void meets Harley Mary"*
