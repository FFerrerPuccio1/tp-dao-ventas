# Especificación de Actualización para Figma: Modelo RBAC y Pantallas Faltantes (`figma.md`)

**Objetivo de este documento:** Instrucciones exactas y sin ambigüedades ("Zero-Interpretation") para actualizar el prototipo actual en Figma incorporando **Control de Acceso Basado en Roles (RBAC)** (ocultando módulos de Local cuando opera el CD y viceversa) y diseñando las **pantallas y modales faltantes** detectados en la auditoría.

---

## PARTE 1: Rediseño Estructural por RBAC (Control de Acceso Basado en Roles)

### 1.1. Regla de Oro de Visibilidad (Aislamiento de Vistas)
Actualmente, todas las pantallas muestran los mismos 7 ítems en el `Sidebar Izquierdo` sin importar quién opera. **Esto debe cambiarse aplicando RBAC estricto:**
* **En la vista del Centro de Distribución (`ROL_OPERADOR_CD`):** **NO** se ven las pantallas operativas exclusivas de los locales (`Órdenes de Reposición (Solicitar)`, `Local: Recepción de Bultos`, `Local: Punto de Venta (POS)`, `Local: Devoluciones y Caja`).
* **En la vista de Sucursal/Local (`ROL_ENCARGADO_LOCAL`):** **NO** se ven las pantallas exclusivas del CD ni de administración central (`Catálogo y Proveedores`, `Sucursales y CD`, `CD: Empaque y Despacho`).
* **En la vista Gerencial / Auditoría (`ROL_ADMIN_GERENCIAL`):** Ve el módulo de administración global, stock global y los `Reportes Gerenciales`.

---

### 1.2. Las 3 Variantes del Componente `Sidebar Navigation` (`260px` $\times$ `900px`)

Modificá el componente del menú lateral izquierdo en Figma para que tenga **3 variantes exactas** según la pantalla:

#### VARIANTE A: `Sidebar - Vista Centro de Distribución (CD)`
*Aplicar obligatoriamente en: Página 1 (Catálogo/Compras CD), Nuevas Pantallas 1B y 1C (Proveedores y Sucursales), Página 3 (Empaque y Precintado) y Página 4 (Despacho).*
* **Header del Sidebar:** `LogiRetail ERP` | Badge Azul: `[ROL: OPERADOR CD CENTRAL]`
* **Sección: ADMINISTRACIÓN Y ABASTECIMIENTO CD**
  1. `📦 Catálogo y Compras CD` *(Procesos 1 y 2)*
  2. `🏢 Sucursales, CD y Stock` *(Procesos 1 y 2)*
* **Sección: LOGÍSTICA DE SALIDA (HUB)**
  3. `📥 Solicitudes de Locales (Recibidas)` *(Vista en CD de las Órdenes de Reposición entrantes)*
  4. `🔒 CD: Empaque y Precintado` *(Proceso 4)*
  5. `🚚 CD: Despacho y Trazabilidad` *(Proceso 5)*
* *(Ocultar por completo: Recepción en Local, POS y Devoluciones/Caja).*
* **Footer del Sidebar (Perfil de Usuario):**
  * Avatar: `CD` (Fondo `#2563EB`)
  * Nombre: `Operador LogiRetail CD`
  * Rol y Nodo: `Rol: Logística Central • Nodo: CD-01`
  * Botón pequeño: `"⇄ Cambiar Rol / Sesión (Demo)"`

#### VARIANTE B: `Sidebar - Vista Sucursal / Local Comercial`
*Aplicar obligatoriamente en: Página 2 (Órdenes de Reposición), Página 5 (Recepción de Bultos), Página 6 (Punto de Venta POS) y Página 7 (Devoluciones y Caja).*
* **Header del Sidebar:** `LogiRetail ERP` | Badge Verde: `[ROL: ENCARGADO DE SUCURSAL]`
* **Sección: INVENTARIO Y REPOSICIÓN DEL LOCAL**
  1. `📊 Mi Stock y Faltantes (Local 01)` *(Consulta de stock propio)*
  2. `📋 Solicitar Reposición al CD` *(Proceso 3)*
  3. `🔍 Recepción y Control de Precintos` *(Proceso 6)*
* **Sección: OPERACIÓN COMERCIAL Y CAJA**
  4. `🛒 Punto de Venta (POS)` *(Proceso 7A)*
  5. `↩️ Devoluciones y Movimientos de Caja` *(Proceso 7B)*
* *(Ocultar por completo: ABM de Catálogo/Proveedores, Compras a Proveedor, ABM de Sucursales y Empaque/Despacho del CD).*
* **Footer del Sidebar (Perfil de Usuario):**
  * Avatar: `L1` (Fondo `#15803D`)
  * Nombre: `Encargado Local 01`
  * Rol y Nodo: `Rol: Ventas y Recepción • Nodo: LOC-01 Centro`
  * Botón pequeño: `"⇄ Cambiar Rol / Sesión (Demo)"`

#### VARIANTE C: `Sidebar - Vista Gerencial / Auditoría`
*Aplicar en: Página 8 (Reportes Comerciales) y Página 9 (Reportes Logísticos).*
* **Header del Sidebar:** `LogiRetail ERP` | Badge Violeta: `[ROL: AUDITORÍA Y GERENCIA]`
* **Sección: CONTROL GERENCIAL**
  1. `📈 Reportes Comerciales y Margen` *(Reportes 1 y 2)*
  2. `🚨 Reportes Logísticos y Mermas` *(Reportes 3, 4 y 5)*
  3. `🏢 Vista Global de Sucursales y CD` *(Solo lectura / Auditoría)*

---

## PARTE 2: Nuevas Pantallas a Diseñar (Ubicación Exacta y Detalle)

A continuación se especifican los **3 Frames de pantalla completa** y los **3 Modales** que faltan en el archivo actual. Mantené exactamente el mismo estilo visual (`1440px` $\times$ `900px`, fuente `Inter`, bordes `#E2E8F0` y tarjetas blancas sobre fondo `#F8FAFC`).

---

### NUEVA PANTALLA 1: Vista de Pestaña "Proveedores y Categorías" (Proceso 2)
* **¿Dónde va ubicada?:** Es la continuación directa de la **Página 1 actual** (`Catálogo y abastecimiento CD`), cuando el usuario hace clic en la 3° pestaña superior: **`[Proveedores y Categorías]`**.
* **Sidebar a mostrar:** `VARIANTE A (Vista CD)`.
* **Topbar:** `Administración / Catálogo y abastecimiento` | Badge Derecha: `🏢 Operando en: Centro de Distribución Central (Rol: CD)`.
* **Barra de Pestañas Superior:**
  * `[Productos y Precios]` | `[Stock por Ubicación y Mínimos]` | **`[● Proveedores y Categorías (ACTIVA)]`** | `[Sucursales y CD]`
* **Layout del Contenido Principal (Dividido en 2 columnas: 8 columnas izquierda para Proveedores, 4 columnas derecha para Categorías):**
  * **Columna Izquierda (`740px` ancho): "Directorio de Proveedores Oficiales (Abastecimiento CD)"**
    * **Header de la Card:**
      * Título: `Proveedores registrados (3)`
      * Buscador: `"Buscar por CUIT o Razón Social..."`
      * Botón Primario (`#2563EB`): `"+ Nuevo Proveedor"`
    * **Tabla de Proveedores (6 Columnas):**
      1. `CUIT (ID Único)` (Monoespaciado negrita)
      2. `RAZÓN SOCIAL`
      3. `RUBRO / CATEGORÍAS`
      4. `CONTACTO / EMAIL`
      5. `PROD. ASOCIADOS`
      6. `ESTADO / ACCIONES`
    * **Filas exactas a dibujar (Coherentes con tu Página 1):**
      * **Fila 1:** `30-71234567-8` | **TecnoSur S.A.** | Badge: `Audio`, `Periféricos` | `ventas@tecnosur.com.ar` / `011-4552-9000` | `3 productos` | Badge Verde `ACTIVO` | `Editar`
      * **Fila 2:** `30-69854123-4` | **Digital Global SRL** | Badge: `Periféricos`, `Accesorios` | `pedidos@digitalglobal.com` / `011-4881-2200` | `2 productos` | Badge Verde `ACTIVO` | `Editar`
      * **Fila 3:** `30-70551682-9` | **Conecta Argentina S.A.** | Badge: `Accesorios` | `logistica@conecta.com.ar` / `0351-422-8910` | `1 producto` | Badge Verde `ACTIVO` | `Editar`
  * **Columna Derecha (`360px` ancho): "Categorías de Productos"**
    * **Header de la Card:** Título `Categorías activas (3)` + Botón Secundario `"+ Nueva Categoría"`.
    * **Lista de Tarjetas Internas (3 ítems):**
      * **Ítem 1:** `CAT-01 • Audio` — *"Auriculares, parlantes y equipos de sonido"* — Badge: `2 productos` — Ícono Editar.
      * **Ítem 2:** `CAT-02 • Periféricos` — *"Teclados, mouses y dispositivos de entrada"* — Badge: `2 productos` — Ícono Editar.
      * **Ítem 3:** `CAT-03 • Accesorios` — *"Cables, cargadores y adaptadores"* — Badge: `2 productos` — Ícono Editar.

---

### NUEVA PANTALLA 2: Vista de Pestaña "Sucursales y CD" (Proceso Obligatorio 1)
* **¿Dónde va ubicada?:** Es la 4° pestaña superior de la **Página 1 actual**, cuando el usuario hace clic en **`[Sucursales y CD]`** (o hace clic en el menú `Sucursales, CD y Stock`). Cubre el **Proceso Obligatorio N° 1**.
* **Sidebar a mostrar:** `VARIANTE A (Vista CD)`.
* **Barra de Pestañas Superior:**
  * `[Productos y Precios]` | `[Stock por Ubicación y Mínimos]` | `[Proveedores y Categorías]` | **`[● Sucursales y CD (ACTIVA)]`**
* **Header de Sección:**
  * Título: `Red Logística: Centro de Distribución y Sucursales`
  * Subtítulo: `Administrá el nodo central de abastecimiento y los locales comerciales habilitados para operar.`
  * Botón Primario a la derecha (`#2563EB`): `"+ Nueva Sucursal / Local"`
* **Bloque Superior Destacado (Card de Ancho Completo `1132px` con borde azul `#2563EB`): "Nodo Central de Abastecimiento (Hub Único)"**
  * Badge Azul: `[NODO CENTRAL ACTIVO - ROL: CD]`
  * Código: **`CD-01`** | Nombre: **`Centro de Distribución Central`**
  * Dirección: `Av. Circunvalación y Autopista, Parque Industrial, Córdoba` | Responsable: `Jefe de Logística CD`
  * KPIs a la derecha de la tarjeta: `Stock Total en CD: 1.540 u.` | `Locales Abastecidos: 3 sucursales` | `Bultos en Tránsito: 7` | Botón: `"Editar Datos CD"`.
* **Bloque Inferior: "Sucursales / Locales Comerciales (Spokes)" — Tabla de 7 Columnas:**
  * Columnas: `CÓDIGO` | `NOMBRE DE SUCURSAL` | `TIPO` | `DIRECCIÓN Y TELÉFONO` | `CAJA Y POS` | `STOCK VERIFICADO ACTUAL` | `ESTADO / ACCIONES`
  * **Filas exactas a dibujar (Coherentes con tus Páginas 4, 8 y 9):**
    * **Fila 1:** `LOC-01` | **Local 01 - Sucursal Centro** | Badge: `LOCAL MINORISTA` | `Av. Colón 250, Centro` | `Caja Abierta ($450.200)` | `38 u. (5 bajo mínimo ⚠️)` | Badge Verde `OPERATIVO` | `Editar` • `Ver Stock`
    * **Fila 2:** `LOC-02` | **Local 02 - Sucursal Norte** | Badge: `LOCAL MINORISTA` | `Av. Rafael Núñez 4120, Cerro` | `Caja Abierta ($312.500)` | `64 u. (1 bajo mínimo ⚠️)` | Badge Verde `OPERATIVO` | `Editar` • `Ver Stock`
    * **Fila 3:** `LOC-03` | **Local 03 - Sucursal Sur** | Badge: `LOCAL MINORISTA` | `Av. O'Higgins 3200, Jardín` | `Caja Abierta ($290.000)` | `110 u. (0 bajo mínimo ✅)` | Badge Verde `OPERATIVO` | `Editar` • `Ver Stock`

---

### NUEVA PANTALLA 3: Vista de Pestaña "Stock por Ubicación y Mínimos" (Proceso 2)
* **¿Dónde va ubicada?:** Es la 2° pestaña superior de la **Página 1 actual** (`[Stock por Ubicación y Mínimos]`).
* **Objetivo Visual:** Mostrar la matriz consolidada de stock en el CD vs. los 3 Locales, diferenciando **Stock Disponible**, **Stock en Tránsito** y **Stock Retenido/Rechazado por Precinto Roto**.
* **Tabla Matriz (8 Columnas):**
  * `SKU / PRODUCTO` | `STOCK EN CD-01 (DISP.)` | `LOC-01 CENTRO (DISP. / MÍN.)` | `LOC-02 NORTE (DISP. / MÍN.)` | `LOC-03 SUR (DISP. / MÍN.)` | `TOTAL EN TRÁNSITO` | `TOTAL RETENIDO (PRECINTO ROTO)` | `ACCIÓN`
  * Ejemplo Fila 1 (`PROD-0014 Auriculares Bluetooth Pro`):
    * CD-01: `240 u. (Mín: 100)`
    * LOC-01: **`12 u.` (en rojo)** `/ Mín: 20 u.` *(+30 u. en cuarentena)*
    * LOC-02: `18 u. / Mín: 15 u.`
    * LOC-03: `25 u. / Mín: 15 u.`
    * En Tránsito: `40 u.`
    * Retenido (Merma): `10 u. (Bulto #BUL-2026-0090)`
    * Botón: `"Ajustar Mínimos"`

---

## PARTE 3: Los 3 Nuevos Modales Obligatorios (Para colocar junto a la Página 10)

En tu PDF actual, las páginas 10, 11 y 12 son modales independientes. Creá **3 páginas/modales nuevos** con el mismo tamaño y estilo que la Página 10 (`560px` a `640px` de ancho):

---

### NUEVO MODAL A: "Nuevo / Editar Proveedor" (Con Validación de CUIT Duplicado)
* **¿De dónde se abre?:** Desde el botón `"+ Nuevo Proveedor"` de la Página 1 y de la Nueva Pantalla 1.
* **Por qué es obligatorio:** El enunciado exige en la página 2: *"Evitar productos **o proveedores** duplicados según identificadores definidos"*.
* **Contenido del Modal (`540px` ancho):**
  * **Título:** `Nuevo / Editar Proveedor`
  * **Subtítulo:** `Registrá un proveedor para el abastecimiento del Centro de Distribución. El CUIT es único.`
  * **Campo 1 (Con estado de Error en Rojo `#B91C1C`):**
    * Label: `CUIT (IDENTIFICADOR ÚNICO) *`
    * Input con borde rojo: `30-71234567-8`
    * **Mensaje de validación en rojo debajo del input:**
      `⚠️ Error: El CUIT '30-71234567-8' ya pertenece al proveedor registrado 'TecnoSur S.A.' (Validación de no duplicidad).`
  * **Campo 2:** `RAZÓN SOCIAL / NOMBRE LEGAL *` $\rightarrow$ Input: `TecnoSur S.A.`
  * **Campo 3 (2 columnas):** `TELÉFONO DE CONTACTO *` (`011-4552-9000`) | `EMAIL COMERCIAL *` (`ventas@tecnosur.com.ar`)
  * **Campo 4:** `RUBROS / CATEGORÍAS QUE PROVEE` $\rightarrow$ Checkboxes marcados: `[☑ Audio]`, `[☑ Periféricos]`, `[☐ Accesorios]`.
  * **Campo 5:** `CONDICIÓN FISCAL Y ESTADO` $\rightarrow$ `Responsable Inscripto • Activo`
  * **Footer del Modal:** Texto gris `"Corregí el CUIT duplicado para habilitar el guardado"` + Botón `"Cancelar"` + Botón `"Guardar Proveedor"` (Deshabilitado por el error).

---

### NUEVO MODAL B: "Registrar Compra / Ingreso de Stock en CD" (Abastecimiento Inicial)
* **¿De dónde se abre?:** Desde el botón `"📥 Registrar Compra/Ingreso en CD"` arriba a la derecha en la Página 1.
* **Por qué es obligatorio:** Explica cómo entra la mercadería al Centro de Distribución desde los proveedores y de dónde sale el `Costo Unitario` usado para el reporte de margen de ganancia.
* **Contenido del Modal (`640px` ancho):**
  * **Título:** `Registrar Compra a Proveedor (Ingreso de Stock a CD-01)`
  * **Subtítulo:** `Ingresá mercadería adquirida a proveedores directamente al stock disponible del Centro de Distribución Central.`
  * **Fila Superior (3 Campos):**
    1. `DESTINO DE INGRESO (BLOQUEADO):` `[🔒 CD-01 Centro de Distribución Central]`
    2. `PROVEEDOR OFICIAL *:` `[TecnoSur S.A. (CUIT 30-71234567-8) ▾]`
    3. `NRO. FACTURA / REMITO PROVEEDOR *:` `[FAC-A-0004-00098122]`
  * **Tabla Interna: "Detalle de Artículos Recibidos del Proveedor":**
    * Columnas: `SKU / PRODUCTO` | `STOCK ACTUAL CD` | `CANT. A INGRESAR *` | `COSTO UNIT. COMPRA ($) *` | `SUBTOTAL COSTO`
    * **Fila 1:** `PROD-0014 Auriculares Bluetooth Pro` | `140 u.` | Input: `[ 100 ]` | Input: `[ 12.500,00 ]` | `$1.250.000,00`
    * **Fila 2:** `PROD-0021 Teclado Mecánico RGB` | `100 u.` | Input: `[ 80 ]` | Input: `[ 9.200,00 ]` | `$736.000,00`
    * Botón abajo de la tabla: `"+ Agregar otro producto del proveedor"`
  * **Caja de Resumen de Impacto (Fondo verde claro `#DCFCE7`):**
    * `📦 Impacto inmediato en CD-01: +180 unidades pasan a Stock Disponible en CD Central.`
    * `💰 Costo Total de la Compra: $1.986.000,00 (Actualiza costo histórico para cálculo de CMV).`
  * **Footer del Modal:** Botón `"Cancelar"` + Botón Primario Azul `"Confirmar Ingreso de Compra en CD"`.

---

### NUEVO MODAL C: "Nueva / Editar Sucursal o Local" (Proceso 1)
* **¿De dónde se abre?:** Desde el botón `"+ Nueva Sucursal / Local"` de la Nueva Pantalla 2 (`Sucursales y CD`).
* **Contenido del Modal (`500px` ancho):**
  * **Título:** `Alta / Edición de Ubicación (Sucursal o CD)`
  * **Campos:**
    1. `CÓDIGO DE UBICACIÓN (ÚNICO) *:` `[LOC-04]`
    2. `TIPO DE NODO LOGÍSTICO *:` Radio Buttons: `[🔘 Sucursal / Local Comercial (Venta y Recepción)]` | `[⚪ Centro de Distribución (Bloqueado: Ya existe CD-01 activo)]`
    3. `NOMBRE DE LA SUCURSAL *:` `[Local 04 - Sucursal Oeste]`
    4. `DIRECCIÓN FÍSICA *:` `[Av. Fuerza Aérea 2100, Córdoba]`
    5. `HABILITAR PUNTO DE VENTA (POS) Y CAJA INICIAL:` `[☑ Habilitar Caja y Ventas Minoristas]`
  * **Footer:** Botón `"Cancelar"` + Botón Primario `"Guardar Sucursal"`.

---

## PARTE 4: Retoques Puntuales en las Pantallas que Ya Hiciste

Para que el archivo quede **100% libre de observaciones**, aplicá estos 4 ajustes rápidos sobre las páginas existentes de tu PDF:

1. **En Página 11 (`Modal: Trazabilidad inmutable del bulto`):**
   * Actualmente muestra solo 3 eventos (`PREPARADO`, `PRECINTADO`, `EN TRÁNSITO`).
   * **Ajuste:** Cambiá el título del modal a `#BUL-2026-0099` (o agregá debajo los 2 eventos que faltan) para que la línea de tiempo muestre los **5 estados completos exigidos por la cátedra**:
     * Evento 1 (`08:00:10`): **`● PREPARADO`** — *Creado en CD-01 (Remito #REM-00088).*
     * Evento 2 (`08:15:40`): **`● PRECINTADO`** — *Precinto asignado: `PREC-551210`.*
     * Evento 3 (`08:30:00`): **`● EN TRÁNSITO`** — *Despachado desde CD-01 hacia Local 01 - Centro.*
     * Evento 4 (`12:45:12`): **`● RECIBIDO`** — *Arribo físico registrado en Local 01 (Stock en cuarentena).*
     * Evento 5 (`12:55:00`): **`● VERIFICADO`** (Badge Verde) — *Precinto `PREC-551210` verificado íntegro en Local 01. +40 u. liberadas a Stock Disponible.*
   * *(Opcionalmente, al lado podés poner una mini-tarjeta mostrando cómo se ve el Evento 5 cuando termina en **`● RECHAZADO`** en rojo para el bulto `#BUL-2026-0090` por rotura del precinto `PREC-44109`).*

2. **En Página 8 (`Reportes comerciales y de margen`):**
   * En el texto pequeño del pie de página (abajo a la izquierda), dice:
     `"380 u. netas · Ingresos $4.850.000 - CMV $2.910.000 - merma $145.000 = $1.795.000. Incluye descuentos y devoluciones."`
   * **Ajuste:** Reemplazá `"Incluye descuentos y devoluciones"` por **`"Valores netos de devoluciones registradas"`** (ya que el proceso de descuentos y promociones es opcional y no forma parte del alcance).

3. **En Página 10 (`Modal: Nuevo / Editar Producto`):**
   * En la tabla inferior `"Niveles de Stock Mínimo por Sucursal"`, aparecen `Local 01 - Centro`, `Local 02 - Norte` y `CD Central`.
   * **Ajuste:** Agregá una fila más para **`Local 03 - Sur`** con Stock Mínimo **`15`**, así coincide con los 3 locales que aparecen en los reportes de las Páginas 8 y 9.

4. **En todas las Páginas (1 a 9) — Aplicar el `Sidebar` según RBAC:**
   * **Páginas 1, 3 y 4:** Dejar solo los ítems del `Sidebar - Vista CD` (ocultando POS, Recepción en Local y Devoluciones).
   * **Páginas 2, 5, 6 y 7:** Dejar solo los ítems del `Sidebar - Vista Local` (ocultando Catálogo/Compras CD y Empaque/Despacho CD).
   * **Páginas 8 y 9:** Dejar el `Sidebar - Vista Gerencial / Auditoría`.