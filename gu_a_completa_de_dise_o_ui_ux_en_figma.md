# Guía de Diseño de Interfaz y Sistema de Diseño (`figma.md`)
**Objetivo del Documento:** Especificación visual y funcional exhaustiva ("Zero-Interpretation Spec") para construir todos los frames, componentes y prototipos del sistema en **Figma** sin dejar ningún detalle librado al azar.

---

## 1. Configuración del Lienzo y Sistema de Diseño (Design Tokens)

### 1.1. Tamaño de Frames y Grilla (Desktop Application / Web App)
* **Dimensiones de cada Frame (Pantalla):** `1440px` de ancho $\times$ `900px` de alto.
* **Layout Estructural Fijo:**
  * **Sidebar Izquierdo (Navegación Principal):** Ancho fijo de `260px`, alto `900px` (`100%`).
  * **Topbar (Barra Superior de Contexto):** Ancho `1180px` (`1440 - 260`), alto fijo de `64px`.
  * **Área de Trabajo Principal (Main Content Canvas):** Ancho `1180px`, alto `836px`. Padding interno de `24px` en los 4 lados. Grilla de 12 columnas, `gutter` (espaciado entre columnas) de `16px`.

### 1.2. Paleta de Colores Exacta (HEX Codes)
Creá estos estilos de color (Color Styles) en Figma antes de empezar:
* **Superficies y Fondos:**
  * `Bg-App-Canvas`: `#F8FAFC` (Gris azulado muy claro para el fondo del área de trabajo).
  * `Bg-Surface-Card`: `#FFFFFF` (Blanco puro para tarjetas, tablas y modales).
  * `Bg-Sidebar`: `#0F172A` (Azul noche profundo / Slate 900 para el menú lateral).
  * `Bg-Sidebar-Hover/Active`: `#1E293B` (Con borde izquierdo de `4px` en color `#3B82F6`).
* **Colores Primarios y de Acción:**
  * `Primary-Brand`: `#2563EB` (Azul Royal para botones principales "Confirmar", "Guardar", "Despachar").
  * `Primary-Hover`: `#1D4ED8`.
  * `Secondary-Action`: `#475569` (Gris pizarra para acciones secundarias, filtros, exportar).
* **Textos y Bordes:**
  * `Text-Primary`: `#0F172A` (Títulos y datos principales).
  * `Text-Secondary`: `#64748B` (Subtítulos, labels de formularios, cabeceras de tabla).
  * `Border-Subtle`: `#E2E8F0` (Bordes de `1px` para tarjetas, inputs y divisores de tabla).
* **Colores Semánticos y Estados del Bulto (CRÍTICOS para el TP):**
  * **Estado 1 - `PREPARADO`:** Fondo `#F1F5F9` | Texto `#334155` | Borde `#CBD5E1` (Gris Neutro).
  * **Estado 2 - `PRECINTADO`:** Fondo `#EDE9FE` | Texto `#6D28D9` | Borde `#C4B5FD` (Violeta Seguridad).
  * **Estado 3 - `EN TRÁNSITO`:** Fondo `#FEF3C7` | Texto `#B45309` | Borde `#FDE68A` (Ámbar / Amarillo Transporte).
  * **Estado 4 - `RECIBIDO`:** Fondo `#E0F2FE` | Texto `#0369A1` | Borde `#BAE6FD` (Celeste Arribo).
  * **Estado 5A - `VERIFICADO` (OK):** Fondo `#DCFCE7` | Texto `#15803D` | Borde `#86EFAC` (Verde Éxito).
  * **Estado 5B - `RECHAZADO` (Precinto Roto / Peligro):** Fondo `#FEE2E2` | Texto `#B91C1C` | Borde `#FCA5A5` (Rojo Alerta Crítica).

### 1.3. Tipografía (Font Styles)
* **Fuente Principal:** `Inter` (disponible gratis en Figma por defecto).
* **Fuente Monoespaciada (Para SKUs, Códigos de Precinto, Remitos, Comprobantes y Montos):** `JetBrains Mono` o `Roboto Mono`.
* **Escala Tipográfica:**
  * `H1 - Título de Pantalla`: `24px`, Bold (`700`), Line-height `32px`.
  * `H2 - Título de Sección / Modal`: `18px`, SemiBold (`600`), Line-height `28px`.
  * `H3 - Subtítulo de Card`: `15px`, SemiBold (`600`), Line-height `22px`.
  * `Body - Regular`: `14px`, Regular (`400`), Line-height `20px`.
  * `Label / Table Header`: `12px`, SemiBold (`600`), Uppercase, Letter-spacing `4%`, Color `#64748B`.
  * `Code / Badge`: `13px`, Medium (`500`), Fuente Monoespaciada.

---

## 2. Componentes Globales Reutilizables (Figma Components)

Antes de armar las pantallas, creá una página en Figma llamada **`00 - Componentes`** con estos elementos:

1. **Componente `Sidebar Navigation` (`260px` $\times$ `900px`):**
   * **Header del Sidebar:** Logo + Texto *"LogiRetail ERP"* + Subtítulo *"CD & Sucursales"*.
   * **Ítems de Menú (Con íconos Lucide/Feather de `20px`):**
     1. `Catálogo y Proveedores` (Procesos 1 y 2)
     2. `Ubicaciones y Stock` (Procesos 1 y 2)
     3. `Órdenes de Reposición` (Proceso 3)
     4. `CD: Empaque y Despacho` (Procesos 4 y 5)
     5. `Local: Recepción de Bultos` (Proceso 6)
     6. `Local: Punto de Venta (POS)` (Proceso 7 - Ventas)
     7. `Local: Devoluciones y Caja` (Proceso 7 - Devoluciones)
     8. `Reportes Gerenciales` (Los 5 Reportes Obligatorios)
2. **Componente `Topbar Context Selector` (`1180px` $\times$ `64px`):**
   * **Izquierda:** Breadcrumb de la pantalla actual (ej. *"Logística Interna / Recepción en Local"*).
   * **Derecha (Vital para entender el sistema):** Un **Selector de Contexto de Ubicación Activa** (Dropdown destacado con ícono de edificio): permite simular en qué lugar físico está parado el usuario operando el sistema (ej. `[🏢 Operando en: Centro de Distribución Central ▾]` o `[🏪 Operando en: Local 01 - Centro ▾]`). Al lado, un badge de estado de Caja (`Caja Abierta: $450.200`).
3. **Componente `Badge Estado Bulto` (6 variantes):**
   * Píldora con `border-radius: 999px`, `padding: 4px 10px`, puntito indicador de `6px` a la izquierda y texto en mayúsculas usando los colores exactos de la sección 1.2.
4. **Componente `Stepper de Trazabilidad Inmutable`:**
   * Línea de tiempo horizontal o vertical con 5 nodos conectados por líneas:
     `[1. Preparado] ──> [2. Precintado] ──> [3. En Tránsito] ──> [4. Recibido] ──> [5. Verificado / Rechazado]`
   * Debajo de cada nodo muestra la fecha y hora exacta (`23/10/2026 14:32:10`) y el código de precinto.

---

## 3. Especificación Detallada Pantalla por Pantalla (Frames en Figma)

Creá una página en Figma llamada **`01 - Pantallas del Sistema`** y diseñá los siguientes **8 Frames principales** (con sus respectivos modales):

---

### FRAME 1: Administración de Ubicaciones, Catálogo y Abastecimiento CD (Procesos 1 y 2)
* **Objetivo Visual:** Mostrar el ABM de Productos, Categorías, Proveedores, Sucursales y el botón de ingreso de stock por compra a proveedor en el CD.
* **Estructura Superior:** Barra de Pestañas (Tabs) con 4 solapas:
  * `[Tab 1: Productos y Precios (Activa)]` | `[Tab 2: Stock por Ubicación y Mínimos]` | `[Tab 3: Proveedores y Categorías]` | `[Tab 4: Sucursales y CD]`
* **Contenido de la Vista Activa (`Productos y Precios`):**
  * **Header de Acciones:**
    * Buscador: Input `"Buscar por SKU, Código de Barras o Nombre..."` (`320px` ancho).
    * Filtro por Categoría y Filtro por Proveedor.
    * Botón Secundario: `"+ Nuevo Proveedor"`.
    * Botón Secundario: `"📥 Registrar Compra/Ingreso en CD"` (Permite meter stock al CD).
    * Botón Primario (`#2563EB`): `"+ Nuevo Producto"`.
  * **Tabla Principal de Productos (8 columnas):**
    1. `SKU` (Monoespaciado, ej. `PROD-0014`)
    2. `Cód. Barras` (`7791234560012`)
    3. `Producto` (Nombre en negrita)
    4. `Categoría` (Badge gris)
    5. `Proveedor Habitual` (Razón Social + CUIT en texto chico gris)
    6. `Costo Unit.` (`$12.500,00`)
    7. `Precio Venta` (`$19.900,00` en negrita)
    8. `Acciones` (Ícono Editar precio/datos, Ícono Configurar Stock Mínimo por Local).
* **Sub-elemento / Modal a dibujar al costado (`Modal: Nuevo / Editar Producto` - `520px` ancho):**
  * Campos obligatorios: `SKU *`, `Código de Barras *`, `Nombre *`, `Categoría (Select) *`, `Proveedor (Select) *`, `Costo Unitario ($) *`, `Precio de Venta ($) *`.
  * Sección inferior dentro del modal: **"Niveles de Stock Mínimo por Sucursal"** (Mini tabla con Local 01, Local 02, CD y un input numérico de Stock Mínimo para cada uno).
  * Mensaje de validación visible en rojo debajo de SKU (para demostrar la regla del TP): *"⚠️ Error: El SKU 'PROD-0014' ya se encuentra registrado en el sistema (Validación de no duplicidad)."*

---

### FRAME 2: Consolidación de Necesidades y Orden de Reposición (Proceso 3)
* **Objetivo Visual:** Que un Local pida mercadería al Centro de Distribución, asistido por las alertas de stock mínimo.
* **Layout de Pantalla Dividida (2 Columnas asimétricas):**
  * **Columna Izquierda (7 columnas de grilla - `660px`): "Estado de Stock del Local y Faltantes"**
    * Selector superior bloqueado o preseleccionado: `Origen: [CD-01 Centro de Distribución Central]` $\rightarrow$ `Destino: [LOC-01 Sucursal Centro]`.
    * Switch de filtro rápido destacado en ámbar: `[🔘 Mostrar solo productos en o bajo Stock Mínimo (6)]`.
    * **Tabla de Selección:**
      * Columnas: `SKU` | `Producto` | `Stock Actual Disponible` (en rojo si es $\le$ mínimo) | `Stock en Tránsito` | `Stock Mínimo` | `Cant. Sugerida` | `Botón [+ Agregar]`.
  * **Columna Derecha (5 columnas de grilla - `450px`): "Orden de Reposición en Curso (Borrador)"**
    * Card blanca con borde azul superior de `4px`.
    * Cabecera: `Orden de Reposición #OR-2026-0042` | Fecha: `23/10/2026`.
    * Datos fijos: `Desde: CD Central` $\rightarrow$ `Hacia: Local 01 - Centro`.
    * Lista de ítems agregados con un input numérico `Cantidad a Solicitar` y botón de papelera para quitar.
    * Footer de la Card: Total de renglones (`4 productos`), Total de unidades solicitadas (`85 u.`), Botón Primario ancho completo: `"Confirmar y Enviar Orden al CD"`.

---

### FRAME 3: CD — Empaquetado en Bultos, Remito y Precintado (Proceso 4)
* **Objetivo Visual:** Esta es una de las pantallas más importantes del TP. Muestra cómo el CD toma una Orden de Reposición, genera el Remito, mete los productos en Bultos y les asigna el **Precinto de Seguridad**.
* **Estructura en 3 Bloques:**
  1. **Barra Superior de la Orden Seleccionada (`1132px` $\times$ `72px`):**
     * Muestra: `Atendiendo Orden: #OR-2026-0042` | `Destino: Local 01 - Centro` | `Remito Generado: #REM-00089` | Botón a la derecha: `"+ Crear Nuevo Bulto / Contenedor"`.
  2. **Mitad Izquierda (`500px`): "Mercadería Pendiente de Empaquetar (de la Orden)"**
     * Tabla con los productos pedidos por el local: `SKU`, `Producto`, `Stock en CD`, `Cant. Pedida`, `Cant. ya Empaquetada`, `Pendiente`, y botón `"Asignar a Bulto ->"`.
  3. **Mitad Derecha (`616px`): "Bultos / Contenedores del Remito #REM-00089"**
     * Aquí se listan tarjetas desplegables (Cards), una por cada Bulto creado. **Dibujá 2 tarjetas de Bulto para mostrar los dos primeros estados del Patrón State:**
     * **Tarjeta Bulto 1 (En estado `PREPARADO`):**
       * Header: `📦 Bulto #BUL-2026-0101` | Badge gris: `[● PREPARADO]`.
       * Tabla interna de contenido: 2 productos adentro (ej. 20 u. de Prod A, 15 u. de Prod B). Botón `"+ Agregar ítem"`.
       * **Caja de Acción de Precintado (Fondo violeta suave `#F5F3FF`):**
         * Input obligatorio con ícono de candado: `"Nro. de Precinto de Seguridad (Ej: PREC-884920)"`.
         * Botón Violeta (`#6D28D9`): `"🔒 Colocar Precinto y Cerrar Bulto"` (Transiciona de `Preparado` a `Precintado` y bloquea la edición de ítems).
     * **Tarjeta Bulto 2 (En estado `PRECINTADO`):**
       * Header: `📦 Bulto #BUL-2026-0100` | Badge violeta: `[● PRECINTADO]`.
       * Dato destacado en fuente monoespaciada: `🔒 Precinto Asignado: PREC-774102` (Con ícono de check verde, bloqueado para edición).
       * Lista de productos adentro (solo lectura).

---

### FRAME 4: CD — Despacho de Bultos y Trazabilidad (Proceso 5)
* **Objetivo Visual:** Registrar la salida de los bultos desde el Centro de Distribución hacia el Local, cambiando su estado a `EN TRÁNSITO` y mostrando la trazabilidad inmutable.
* **Vista Principal:**
  * **KPIs rápidos arriba (3 mini-cards de `360px`):**
    * `Bultos Precintados Listos para Salir: 4`
    * `Bultos Actualmente En Tránsito: 7`
    * `Remitos Despachados Hoy: 3`
  * **Tabla Principal: "Remitos y Bultos Listos para Despacho / En Tránsito":**
    * Columnas: `Checkbox` | `Cód. Bulto` | `Nro. Remito` | `Origen -> Destino` | `Precinto Seguridad` | `Cant. Unidades` | `Estado Actual` (Badges `PRECINTADO` o `EN TRÁNSITO`) | `Último Movimiento` | `Acciones`.
    * En la columna `Acciones`:
      * Si el bulto está `PRECINTADO`: Botón Primario Azul `"🚚 Registrar Despacho"`.
      * Si el bulto está `PREPARADO` (sin precinto): Botón deshabilitado gris `"Falta Precintar"` con tooltip explicativo.
      * Botón secundario en todas las filas: `"🕒 Ver Trazabilidad"`.
* **Drawer / Panel Lateral Derecho o Modal (`Modal: Trazabilidad Inmutable del Bulto #BUL-2026-0100`):**
  * **Importante para la defensa del TP:** Este modal demuestra la validación obligatoria *"Mantener trazabilidad inmutable de estados del bulto"*.
  * Muestra una línea de tiempo vertical con los registros de la tabla `historial_estado_bulto`:
    * `23/10/2026 09:15:04` — **PREPARADO** — *Creado en CD-01 por Operador CD (Remito #REM-00089).*
    * `23/10/2026 09:42:18` — **PRECINTADO** — *Precinto de seguridad asignado: `PREC-774102`.*
    * `23/10/2026 11:05:00` — **EN TRÁNSITO** — *Despachado desde CD-01 hacia Local 01 - Centro.*
  * Nota al pie del modal con ícono de escudo: *"Registro de auditoría inmutable (Solo lectura)."*

---

### FRAME 5: Local — Recepción y Verificación de Precinto (Proceso 6 - CRÍTICO)
* **Objetivo Visual:** Demostrar la regla de oro del enunciado: *"El stock no impacta como Disponible en la sucursal destino hasta que el remito y el contenedor pasen a estado Verificado; si el precinto llega roto pasa a Rechazado y no habilita venta"*.
* **Contexto en el Topbar:** `[🏪 Operando en: Local 01 - Centro]`.
* **Layout de la Pantalla:**
  * **Sección Superior: Tabla de "Bultos en Tránsito o Recibidos Pendientes de Verificación"**
    * Muestra los bultos enviados a este local:
      * Fila 1: `#BUL-2026-0098` | Remito `#REM-00088` | Precinto declarado: `PREC-551209` | Estado: `[● EN TRÁNSITO]` | Botón: `"📥 1. Marcar Arribo Físico (Recibido)"`.
      * Fila 2 (Seleccionada): `#BUL-2026-0099` | Remito `#REM-00088` | Precinto declarado: `PREC-551210` | Estado: `[● RECIBIDO]` | Nota: *"Stock retenido en cuarentena (No disponible para venta)"* | Botón: `"🔍 2. Inspeccionar Precinto y Verificar"`.
  * **Sección Inferior / Panel de Inspección de Precinto (Abierto para `#BUL-2026-0099`):**
    * Card grande dividida en 2 partes:
      * **Izquierda ("Datos del Envío y Contenido Declarado"):**
        * Muestra el Número de Precinto que colocó el CD en grande: **`🔒 Precinto Esperado: PREC-551210`**.
        * Lista de artículos dentro del bulto (ej. 30 Auriculares Bluetooth, 10 Teclados Mecánicos).
        * Banner informativo celeste: *"ℹ️ Estos 40 artículos aún NO suman al stock vendible de Local 01."*
      * **Derecha ("Dictamen de Control de Seguridad del Precinto"):**
        * Pregunta obligatoria con dos grandes tarjetas seleccionables (Radio Cards):
        * **Opción A (Borde Verde `#15803D`, fondo `#DCFCE7`):**
          * **`[✓] Precinto Íntegro y Coincidente (`PREC-551210`)`**
          * Subtexto: *"El precinto no presenta signos de violación ni rotura y el contenido coincide."*
          * Botón Verde Grande: **`"Confirmar VERIFICADO (+40 u. a Stock Disponible)"`**.
        * **Opción B (Borde Rojo `#B91C1C`, fondo `#FEE2E2`):**
          * **`[✕] Precinto Violado, Roto o Adulterado (Rechazo Logístico)`**
          * Subtexto: *"Bloquea el ingreso a stock vendible y registra merma/incidencia."*
          * Textarea obligatorio: `"Motivo / Descripción del daño en el precinto (Ej: Precinto cortado y pegado con cinta)..."`.
          * Botón Rojo Grande: **`"Declarar RECHAZADO (Bloquear Stock)"`**.

---

### FRAME 6: Local — Punto de Venta (POS), Cobro y Comprobante (Proceso 7A)
* **Objetivo Visual:** Registrar ventas con uno o más productos, validar stock disponible verificado, cobrar con distintos medios de pago (Patrón Strategy) y emitir comprobante.
* **Contexto en el Topbar:** `[🏪 Operando en: Local 01 - Centro]` | `[🟢 Caja Abierta]`.
* **Layout POS de 2 Columnas:**
  * **Columna Izquierda (`700px`): "Buscador de Productos y Carrito de Venta"**
    * **Barra de adición rápida:**
      * Input con foco: `"Escanear Código de Barras o buscar SKU/Nombre..."`.
      * Al escribir un producto, muestra en un desplegable o fila seleccionada:
        * `PROD-0014 - Auriculares Bluetooth Pro` | Precio: `$19.900` | **Badge Verde: `Stock Disponible Verificado: 12 u.`** (Y en gris chico al lado: `En recepción sin verificar: 30 u. - No vendibles`).
      * Input `Cantidad: [ 2 ]` + Botón `"+ Agregar al Ticket"`.
      * **Alerta de Validación visible (para mostrar en la entrega):** Si el vendedor pone `Cantidad: 15` (superando los 12 disponibles), borde rojo en el input y mensaje: *"🚫 No se puede vender 15 u. El stock disponible y verificado en Local 01 es de 12 u."*
    * **Tabla del Detalle de Venta (Carrito):**
      * Columnas: `SKU` | `Descripción` | `Precio Unit.` | `Cantidad (Selector - / +)` | `Subtotal` | `Quitar (✕)`.
  * **Columna Derecha (`416px`): "Resumen, Medio de Pago y Emisión de Comprobante"**
    * **Totales:**
      * Cantidad de Ítems: `3 unidades`
      * **TOTAL A COBRAR:** `$54.700,00` (Tipografía `28px` Bold Monoespaciada).
    * **Selector de Medio de Pago (Patrón Strategy - 4 Botones tipo Grilla 2x2):**
      1. `[💵 Efectivo]` (Seleccionado con borde azul)
      2. `[💳 Tarjeta Débito]`
      3. `[💳 Tarjeta Crédito]`
      4. `[📱 QR / Transferencia]`
    * **Panel Dinámico de la Estrategia de Pago:**
      * *Si es Efectivo:* Input `"Paga con ($): [ 60.000 ]"` $\rightarrow$ Muestra `"Vuelto a entregar: $5.300,00"`.
      * *(Nota lateral en Figma: Si es Tarjeta/QR, muestra input `"Nro. de Cupón / Operación *"`).*
    * **Botón Principal (`100%` ancho, alto `52px`, Verde `#15803D`):**
      * **`"✓ COBRAR Y EMITIR COMPROBANTE ($54.700)"`**
* **Modal / Vista Previa de Comprobante Emitido (Dibujar al lado o superpuesto - `380px` ancho, estilo Ticket Térmico):**
  * Título: `COMPROBANTE DE VENTA #TCK-LOC01-000451`.
  * Fecha/Hora, Sucursal: `Local 01 - Centro`, Detalle de productos, Total, Medio de Pago: `Efectivo`, Impacto: `Stock descontado / Ingreso registrado en Caja`. Botones: `"🖨️ Imprimir / PDF"` y `"Nueva Venta"`.

---

### FRAME 7: Local — Gestión de Devoluciones y Movimientos de Caja (Proceso 7B)
* **Objetivo Visual:** Demostrar la validación *"No aceptar devoluciones que no correspondan a una venta registrada o que incumplan las reglas establecidas"* y su doble impacto en Stock y Caja.
* **División de Pantalla (Arriba: Proceso de Devolución | Abajo: Impacto en Caja del Local):**
  * **Bloque 1: "Registrar Devolución Vinculada a Comprobante"**
    * **Paso 1 - Buscador Obligatorio de Venta:**
      * Input: `"Ingresar Nro. de Comprobante de Venta Original (Ej: TCK-LOC01-000451) *"` + Botón `"Buscar Venta"`.
      * *(Si se ingresa un comprobante inexistente, alerta roja: "🚫 Comprobante no encontrado. No se admiten devoluciones sin venta registrada").*
    * **Paso 2 - Selección de Ítems del Comprobante `#TCK-LOC01-000451` (Fecha: 22/10/2026 - Estado: Plazo Vigente ✅):**
      * Tabla que trae los renglones exactos de esa venta:
        * Columna `Producto` | `Precio Pagado` | `Cant. Comprada` (`2 u.`) | `Cant. Ya Devuelta` (`0 u.`) | `Cant. Máx. Devolvible` (`2 u.`) | **Input `Cant. a Devolver Ahora` (`[ 1 ]`)**.
    * **Paso 3 - Motivo y Confirmación de Impacto:**
      * Input: `"Motivo de la devolución *"` (Ej. *"Cambio de parecer del cliente - Producto cerrado en perfecto estado"*).
      * Resumen de Impacto antes de confirmar (2 Badges informativos):
        * `📦 Impacto en Stock Local 01: +1 u. reingresa a Stock Disponible`
        * `💰 Impacto en Caja Local 01: -$19.900,00 (Egreso por Devolución en Efectivo)`
      * Botón Primario: `"Confirmar Devolución y Emitir Nota de Crédito"`.
  * **Bloque 2 (Mitad inferior de la pantalla): "Movimientos de Caja del Día (Local 01)"**
    * Tabla de auditoría de caja:
      * Fila 1: `15:20 hs` | `EGRESO POR DEVOLUCIÓN` | Ref: `DEV-0012 (Venta #TCK-LOC01-000451)` | Medio: `Efectivo` | Monto en rojo: **`-$19.900,00`**.
      * Fila 2: `14:10 hs` | `INGRESO POR VENTA` | Ref: `Venta #TCK-LOC01-000451` | Medio: `Efectivo` | Monto en verde: **`+$54.700,00`**.

---

### FRAME 8: Centro de Reportes Gerenciales (Los 5 Reportes No Triviales)
* **Objetivo Visual:** Cumplir con el requisito obligatorio de al menos 4 reportes no triviales en una interfaz analítica clara y filtrable.
* **Estructura de Navegación Interna (Sub-barra izquierda o 5 Pestañas Superiores):**
  1. `📊 1. Ventas e Ingresos`
  2. `📈 2. Más Vendidos y Margen (Ganancia/Pérdida)`
  3. `📦 3. Existencias, Valorización y Stock Mínimo`
  4. `🚨 4. Bultos Rechazados y Mermas por Precinto`
  5. `⏱️ 5. Tiempos de Tránsito CD -> Locales`
* **Barra de Filtros Globales (Debajo de las pestañas):**
  * `Rango de Fechas: [01/10/2026 - 23/10/2026]` | `Ubicación/Local: [Todos los Locales ▾]` | `Categoría: [Todas ▾]` | Botón `"🔄 Actualizar Reporte"` | Botón `"📄 Exportar CSV/PDF"`.
* **Diseño del Contenido (Para que en un solo Frame de Figma o en 2 variantes se vean los 5 reportes):**
  * Podés diseñar el **Frame 8A (Reportes Comerciales y de Margen - Reportes 1 y 2)** y el **Frame 8B (Reportes Logísticos y de Inventario - Reportes 3, 4 y 5)**:
  * **En Frame 8A (Pestaña Activa: `2. Más Vendidos y Margen Estimado`):**
    * **4 Tarjetas KPI Financieras arriba:**
      * `Ingresos Netos (Ventas - Devoluciones): $4.850.000`
      * `Costo Mercadería Vendida (CMV): -$2.910.000`
      * `Pérdida por Mermas / Precintos Rotos: -$145.000` (En rojo)
      * `Margen Neto de Ganancia Estimado: +$1.795.000 (37,0%)` (En verde destacado)
    * **Tabla Detallada de Ranking de Productos y Margen:**
      * Columnas: `Ranking (#1, #2...)` | `SKU y Producto` | `Unidades Vendidas Netas` | `Ingresos ($)` | `Costo Total ($)` | `Merma Logística ($)` | `Ganancia Neta ($)` | `% Margen` (Barra de progreso visual).
    * **Recuadro lateral: Resumen de Ventas por Local y Medio de Pago (Reporte 1):**
      * Tabla cruzada mostrando Local 01, Local 02, Local 03 desglosados en Efectivo, Débito, Crédito y QR.
  * **En Frame 8B (Vista Combinada de Auditoría Logística: Reportes 3, 4 y 5):**
    * **Bloque Superior Izquierdo (Reporte 5 - Tiempo Promedio de Tránsito CD $\rightarrow$ Locales):**
      * Tabla por Sucursal Destino: `Local Destino` | `Bultos Recibidos` | `Tiempo Mín. Tránsito` | **`Tiempo Promedio Tránsito` (ej. `4h 25m`)** | `Tiempo Máx.` | `% Efectividad (Verificados vs Rechazados)`.
    * **Bloque Superior Derecho (Reporte 3 - Existencias y Stock Mínimo):**
      * Tabla con filtro activo `"Críticos"`: `Ubicación` | `Producto` | `Stock Disponible` | `Stock Mínimo` | `Valorización ($)` | Badge `[⚠️ BAJO MÍNIMO]`.
    * **Bloque Inferior Ancho Completo (Reporte 4 - Bultos Rechazados por Rotura de Precinto):**
      * Tabla con borde rojo suave: `Fecha Rechazo` | `Cód. Bulto` | `Remito` | `Local Destino` | `Precinto Violado` | `Unidades Retenidas` | `Pérdida Valorizada ($)` | `Observación de Auditoría` (ej. *"Precinto PREC-44109 cortado al arribar al local"*).

---

## 4. Mapa de Prototipado Interactivo en Figma (Flujo para la Defensa del TP)

Si quieren conectar las pantallas en la pestaña **Prototype** de Figma para mostrar una demo navegable al profesor, conecten estos 5 enlaces clave (`On Click -> Navigate To`):
1. En **Frame 2 (Orden de Reposición)** $\rightarrow$ Botón `"Confirmar y Enviar Orden al CD"` lleva al **Frame 3 (Empaque y Precintado en CD)**.
2. En **Frame 3 (Empaque en CD)** $\rightarrow$ Botón `"🔒 Colocar Precinto"` cambia el estado de la tarjeta a `PRECINTADO` y lleva al **Frame 4 (Despacho desde CD)**.
3. En **Frame 4 (Despacho desde CD)** $\rightarrow$ Botón `"🕒 Ver Trazabilidad"` abre como `Open Overlay` el **Modal de Historial Inmutable del Bulto**.
4. En **Frame 5 (Recepción en Local)** $\rightarrow$ Botón `"Confirmar VERIFICADO"` lleva al **Frame 6 (Punto de Venta POS)** mostrando el nuevo stock disponible listo para vender.
5. En **Frame 6 (Punto de Venta POS)** $\rightarrow$ Botón `"COBRAR Y EMITIR COMPROBANTE"` abre como `Open Overlay` el **Ticket de Venta Emitido**.