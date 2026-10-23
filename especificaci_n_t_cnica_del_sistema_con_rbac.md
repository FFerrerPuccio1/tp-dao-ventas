# Especificación de Requerimientos y Arquitectura de Software (`specs.md`)
**Proyecto:** Sistema de Ventas, Inventario y Logística Interna (CD a Locales) — Tema 3  
**Cátedra:** Desarrollo de Aplicaciones con Objetos (DAO) - 2026  

---

## 1. Descripción General y Arquitectura del Sistema

El sistema es una solución integral de tipo ERP ligero para un comercio minorista estructurado bajo un modelo **Hub & Spoke** (un Centro de Distribución central que abastece a múltiples Sucursales/Locales comerciales), gobernado por un esquema de **Control de Acceso Basado en Roles (RBAC)** donde cada operador interactúa únicamente con los módulos de su nodo asignado.

### 1.1. Stack Tecnológico y Arquitectura
* **Estilo Arquitectónico:** Monolito Modular en Capas (Layered Architecture) con clara separación de responsabilidades para respetar los principios **SOLID** y el paradigma **Orientado a Objetos**.
* **Lenguaje:** Python 3.11+
* **Base de Datos:** SQLite3 (persistencia relacional en archivo único `sistema_logistica.db`, con `PRAGMA foreign_keys = ON`).
* **Estructura de Capas del Monolito:**
  1. **Capa de Presentación (UI / Controllers o Views):** Interfaz de usuario filtrada dinámicamente por el Rol y la Ubicación de la sesión activa (`SessionContext`), sin contener lógica de negocio.
  2. **Capa de Aplicación / Servicios (`services/`):** Coordina los casos de uso, valida permisos RBAC, maneja las transacciones de base de datos (Unit of Work) e invoca a los objetos de dominio.
  3. **Capa de Dominio (`domain/`):** El corazón del TP. Contiene las Clases de Entidad, Objetos de Valor, **Patrones de Diseño (State, Strategy, etc.)** y todas las validaciones de negocio puras en Python.
  4. **Capa de Infraestructura / Persistencia (`repositories/`):** Implementación del patrón *Repository* o *DAO (Data Access Object)* con consultas SQL parametrizadas hacia `sqlite3`.

---

## 2. Seguridad y Control de Acceso Basado en Roles (RBAC)

El sistema aísla estrictamente las vistas y operaciones según el rol y el nodo físico del usuario autenticado:

| Rol del Sistema | Ubicación Asociada | Módulos Visibles y Permitidos | Módulos Ocultos y Prohibidos |
| :--- | :--- | :--- | :--- |
| **`ROL_OPERADOR_CD`** | Centro de Distribución (`CD-01`) | • ABM de Productos, Categorías y Precios.<br>• ABM de Proveedores e Ingreso de Compras al CD.<br>• ABM de Sucursales y CD.<br>• Matriz de Stock y Mínimos.<br>• Empaque y Precintado de Bultos (Proceso 4).<br>• Despacho y Trazabilidad de Bultos (Proceso 5). | • Solicitar Orden de Reposición desde Local.<br>• Recepción y Verificación en Local.<br>• Punto de Venta (POS).<br>• Devoluciones y Caja de Sucursal. |
| **`ROL_ENCARGADO_LOCAL`** | Sucursal Específica (`LOC-01`, `LOC-02`, `LOC-03`) | • Consulta de Stock y Faltantes de su propio Local.<br>• Solicitud de Orden de Reposición al CD (Proceso 3).<br>• Recepción Física y Verificación de Precintos (Proceso 6).<br>• Punto de Venta (POS) y Cobros (Proceso 7A).<br>• Devoluciones y Movimientos de Caja (Proceso 7B). | • ABM de Catálogo, Precios y Proveedores.<br>• Registro de Compras a Proveedores.<br>• ABM de Sucursales.<br>• Empaque, Precintado y Despacho del CD.<br>• Operaciones de otros locales ajenos. |
| **`ROL_ADMIN_GERENCIAL`** | Global (`TODAS`) | • Los 5 Reportes Gerenciales y de Auditoría.<br>• Consulta de Trazabilidad Inmutable de Bultos.<br>• Vista de Red de Sucursales y Valorización de Stock. | • Operación directa de caja diaria (POS) o armado físico de bultos. |

---

## 3. Patrones de Diseño (Orientados a Objetos)

La cátedra exige **al menos dos patrones de diseño GoF (Gang of Four)** aplicados al dominio y evaluará críticamente el ciclo de vida del bulto. Implementaremos **3 patrones principales**:

### 3.1. Patrón STATE (Obligatorio / Crítico para el Ciclo de Vida del Bulto)
* **Problema que resuelve:** El `Bulto` atraviesa una secuencia estricta de estados (`Preparado` $\rightarrow$ `Precintado` $\rightarrow$ `EnTransito` $\rightarrow$ `Recibido` $\rightarrow$ `Verificado` | `Rechazado`). Cada estado habilita o prohíbe ciertas acciones (ej. no se puede despachar un bulto sin precintar; no se puede verificar un bulto que no fue recibido). Evita tener condicionales gigantes (`if/elif/else`) dentro de la clase `Bulto`.
* **Estructura de Clases:**
  * `Bulto` (Contexto): Mantiene una referencia a una instancia de `EstadoBulto` y una lista inmutable de `CambioEstadoBulto`.
  * `EstadoBulto` (Clase Abstracta / Interfaz): Define los métodos `precintar(bulto, nro_precinto)`, `despachar(bulto)`, `recibir(bulto)`, `verificar_precinto_sano(bulto)`, `rechazar_por_precinto_roto(bulto, motivo)`. Por defecto, en la clase base todos lanzan `TransicionEstadoInvalidaException`.
  * **Subclases Concretas:**
    * `EstadoPreparado`: Solo permite `precintar()`, transicionando a `EstadoPrecintado`.
    * `EstadoPrecintado`: Solo permite `despachar()`, transicionando a `EstadoEnTransito` y descontando el stock físico del CD.
    * `EstadoEnTransito`: Solo permite `recibir()`, transicionando a `EstadoRecibido`.
    * `EstadoRecibido`: Permite `verificar_precinto_sano()` (transiciona a `EstadoVerificado` e **impacta el stock como Disponible en el Local**) o `rechazar_por_precinto_roto()` (transiciona a `EstadoRechazado`, registra merma y **bloquea el ingreso a stock vendible**).
    * `EstadoVerificado` y `EstadoRechazado`: Estados finales (inmutables, no permiten más transiciones).

### 3.2. Patrón STRATEGY (Para Medios de Pago y Cobros en Caja)
* **Problema que resuelve:** El proceso 7 exige cobrar ventas con distintos medios de pago (Efectivo, Tarjeta de Débito, Tarjeta de Crédito, Transferencia/QR) y gestionar su impacto en caja y validaciones particulares (ej. validación de número de cupón/operación, cálculo de vuelto).
* **Estructura de Clases:**
  * `EstrategiaMedioPago` (Clase Abstracta): Define el método `procesar_pago(monto_base: float, datos_pago: dict) -> ResultadoPago`.
  * **Subclases Concretas:**
    * `PagoEfectivoStrategy`: Valida que el monto entregado sea $\ge$ monto base, calcula vuelto e impacta en el arqueo de efectivo físico del local.
    * `PagoTarjetaStrategy`: Exige código de autorización/cupón y últimos 4 dígitos; impacta en la cuenta de recaudación bancaria del local.
    * `PagoTransferenciaQRStrategy`: Exige identificador de transacción digital.

### 3.3. Patrón REPOSITORY (Arquitectónico / Persistencia)
* **Problema que resuelve:** Desacopla el modelo de dominio en Python de las sentencias SQL específicas de `sqlite3`.
* **Aplicación:** Clases como `ProductoRepository`, `BultoRepository`, `VentaRepository` se encargan de reconstruir el grafo de objetos (incluyendo el estado actual del bulto y su historial) a partir de las filas de SQLite.

---

## 4. Procesos de Negocio Obligatorios (Especificación Funcional)

> **Nota de Alcance:** Se excluyen todos los procesos opcionales (órdenes de compra sugeridas automáticas, promociones/descuentos/listas de precios, lotes/vencimientos, clientes frecuentes/cuentas corrientes e inventarios físicos).

### Proceso 1: Administración de Ubicaciones (Centro de Distribución y Locales) — `[Rol: CD]`
* **Objetivo:** Gestionar las entidades físicas donde se almacena o vende mercadería.
* **Reglas de Negocio:**
  * Existe **1 único Centro de Distribución (CD)** activo como nodo abastecedor central y **$N$ Sucursales/Locales** comerciales (`LOC-01`, `LOC-02`, `LOC-03`).
  * Cada ubicación posee un código único, nombre, dirección, teléfono y estado (Activo/Inactivo).
  * Cada ubicación tiene su propio inventario independiente por producto (`StockUbicacion`) y su propia Caja (`CajaSucursal`).

### Proceso 2: Administración de Catálogo (Productos, Categorías, Precios, Stock Mínimo y Proveedores) + Abastecimiento al CD — `[Rol: CD]`
* **Objetivo:** Mantener el maestro de artículos, proveedores y permitir el ingreso de mercadería al CD para que exista stock que distribuir y costo base para calcular márgenes.
* **Reglas de Negocio:**
  * **Proveedores:** Identificados por `CUIT` único y Razón Social. **Validación:** No se permiten dos proveedores con el mismo CUIT.
  * **Categorías:** Clasificación simple (ID, Nombre, Descripción).
  * **Productos:** Identificados por `SKU` (Código alfanumérico único) y `CodigoBarras` (EAN13 único). Poseen nombre, categoría, proveedor habitual, `costo_unitario_actual` y `precio_venta_unitario`.
  * **Niveles Mínimos de Existencia:** Cada producto tiene parametrizado un `stock_minimo` por cada Ubicación (`StockUbicacion`).
  * **Ingreso de Stock al CD (Compra a Proveedor):** Permite registrar una factura/remito de proveedor ingresando unidades al stock del CD y actualizando el costo unitario del producto.

### Proceso 3: Consolidación de Necesidades y Orden de Reposición (Local $\rightarrow$ CD) — `[Rol: Local]`
* **Objetivo:** Solicitar mercadería desde un Local hacia el Centro de Distribución.
* **Flujo:**
  1. El encargado del Local opera sobre su **Local Destino** solicitando al **CD Origen**.
  2. El sistema muestra los productos del local resaltando aquellos donde `stock_disponible <= stock_minimo`.
  3. Se agregan ítems (`Producto`, `cantidad_solicitada > 0`) a una **Orden de Reposición**.
  4. La orden se guarda en estado `Solicitada` con fecha de emisión y número correlativo (`OR-2026-XXXX`).

### Proceso 4: Empaquetado en Bultos, Asignación de Remito y Precinto — `[Rol: CD]`
* **Objetivo:** Preparar físicamente la mercadería solicitada en contenedores seguros y trazables.
* **Flujo y Reglas:**
  1. En el CD se selecciona una `OrdenReposicion` pendiente.
  2. Se crea un **Remito de Despacho** (`REM-XXXX`) asociado a la orden (indicando CD Origen y Local Destino).
  3. Se crean uno o más **Bultos / Contenedores** (`BUL-XXXX`) asociados al Remito.
  4. Se asignan productos y cantidades dentro de cada Bulto (validando que el CD tenga stock disponible suficiente). Al crearse el bulto con sus ítems, nace en estado **`Preparado`** (registrando el primer hito en `HistorialEstadoBulto`).
  5. **Precintado:** El operario coloca físicamente el precinto y registra el **Código de Precinto de Seguridad** (único e irrepetible, ej. `PREC-774102`). El bulto ejecuta `bulto.precintar(codigo)` y pasa a estado **`Precintado`**.

### Proceso 5: Despacho de Bultos desde el Centro de Distribución — `[Rol: CD]`
* **Objetivo:** Dar salida efectiva a los bultos hacia el local destino.
* **Flujo y Reglas:**
  1. Solo se pueden despachar bultos cuyo estado actual sea **`Precintado`**.
  2. Al confirmar el despacho del Remito/Bultos:
     * Cada bulto ejecuta `bulto.despachar()`, cambiando su estado a **`En Tránsito`** y grabando el timestamp exacto de salida en el historial inmutable.
     * El stock en el CD se descuenta de `stock_disponible` y pasa a `stock_en_transito` hacia el local destino.

### Proceso 6: Recepción y Verificación de Precinto en el Local Destino — `[Rol: Local]`
* **Objetivo:** Controlar la integridad del envío antes de habilitar la mercadería para la venta.
* **Flujo y Reglas:**
  1. **Arribo físico (`Recibido`):** Cuando el transporte llega al local, el bulto se marca como **`Recibido`** (registra timestamp de llegada, cerrando el tiempo de tránsito). **Importante:** En estado `Recibido`, el stock **AÚN NO** está disponible para la venta (queda en cuarentena de recepción).
  2. **Inspección de Precinto y Contenido (`Verificado` vs. `Rechazado`):**
     * El receptor del local inspecciona el precinto físico y lo compara con el `codigo_precinto` del sistema:
     * **Camino Feliz (Precinto Íntegro):** Marca el bulto como **`Verificado`**. En este exacto instante, dentro de una transacción atómica, el sistema suma las cantidades del bulto al `stock_disponible` del Local Destino y descuenta de `stock_en_transito`.
     * **Camino de Excepción (Precinto Violado / Roto / Adulterado):** El usuario selecciona "Precinto Violado/Roto" e ingresa observación obligatoria. El bulto pasa a estado **`Rechazado`** (Rechazo Logístico). **Validación Crítica:** La mercadería de ese bulto **NO ingresa al stock disponible** del local; queda registrada como stock retenido/merma logística por rotura de precinto.

### Proceso 7: Ventas en Local, Cobros, Comprobante y Devoluciones — `[Rol: Local]`
* **Objetivo:** Operación comercial minorista en cada sucursal.
* **7.A. Registro de Venta:**
  * Se opera siempre sobre el **Local activo** con su **Caja abierta**.
  * Se agregan 1 o más productos (`DetalleVenta`: Producto, Cantidad, Precio Unitario vigente, Subtotal).
  * **Validación Crítica:** Por cada renglón, `cantidad_a_vender <= stock_disponible` (verificado) de ese Local. Si supera el stock, se impide agregar o confirmar la venta.
  * **Cobro:** Se selecciona el Medio de Pago (aplicando `EstrategiaMedioPago`: Efectivo, Débito, Crédito, QR/Transferencia). Se registra el ingreso en `MovimientoCaja`.
  * **Confirmación:** Descuenta el `stock_disponible` del Local y emite un **Comprobante de Venta** único (`TCK-LOC01-000451`) con fecha, hora, detalle de ítems, total y medio de pago.
* **7.B. Gestión de Devoluciones:**
  * **Validación Crítica:** No se aceptan devoluciones libres. Toda devolución debe buscar y vincular obligatoriamente un **Comprobante de Venta registrado** previamente.
  * **Reglas de validación de devolución:**
    1. El producto a devolver debe existir en el comprobante original.
    2. La `cantidad_a_devolver` no puede superar la `(cantidad_comprada - cantidad_ya_devuelta_previamente)` de ese ítem en esa venta.
    3. La venta debe estar dentro del plazo de devolución permitido ($\le 30$ días corridos).
  * **Impacto:**
    * **En Stock:** El producto devuelto en condiciones reingresa sumando al `stock_disponible` del Local.
    * **En Caja:** Genera un `MovimientoCaja` de tipo **Egreso por Devolución** por el monto exacto devuelto, restando de la recaudación de la caja del local.

---

## 5. Modelo de Datos Relacional (SQLite3)

1. **`ubicaciones`**: `id` (PK), `codigo` (UNIQUE), `nombre`, `tipo` (`'CD'` o `'LOCAL'`), `direccion`, `activo` (BOOLEAN).
2. **`usuarios`**: `id` (PK), `username` (UNIQUE), `nombre_completo`, `rol` (`'ROL_OPERADOR_CD'`, `'ROL_ENCARGADO_LOCAL'`, `'ROL_ADMIN_GERENCIAL'`), `ubicacion_id` (FK NULLABLE para Gerencia).
3. **`proveedores`**: `id` (PK), `cuit` (UNIQUE), `razon_social`, `telefono`, `email`, `activo` (BOOLEAN).
4. **`categorias`**: `id` (PK), `nombre` (UNIQUE), `descripcion`.
5. **`productos`**: `id` (PK), `sku` (UNIQUE), `codigo_barras` (UNIQUE), `nombre`, `categoria_id` (FK), `proveedor_id` (FK), `costo_unitario` (REAL), `precio_venta` (REAL), `activo` (BOOLEAN).
6. **`stock_ubicacion`**: `id` (PK), `ubicacion_id` (FK), `producto_id` (FK), `cantidad_disponible` (INTEGER), `cantidad_en_transito` (INTEGER), `cantidad_rechazada` (INTEGER), `stock_minimo` (INTEGER). *Constraint:* `UNIQUE(ubicacion_id, producto_id)` y `CHECK(cantidad_disponible >= 0)`.
7. **`ingresos_cd`** y **`detalle_ingresos_cd`**: `id` (PK), `proveedor_id` (FK), `nro_factura_remito`, `fecha_hora`, `total_costo`.
8. **`ordenes_reposicion`** y **`detalle_orden_reposicion`**: `id` (PK), `nro_orden` (UNIQUE), `origen_cd_id` (FK), `destino_local_id` (FK), `fecha_solicitud`, `estado` (`'SOLICITADA'`, `'PROCESADA'`, `'COMPLETADA'`).
9. **`remitos_despacho`**: `id` (PK), `nro_remito` (UNIQUE), `orden_reposicion_id` (FK), `origen_cd_id` (FK), `destino_local_id` (FK), `fecha_emision`, `estado` (`'EMITIDO'`, `'EN_TRANSITO'`, `'PROCESADO_DESTINO'`).
10. **`bultos`**: `id` (PK), `codigo_bulto` (UNIQUE), `remito_id` (FK), `codigo_precinto` (UNIQUE, NULLABLE hasta precintar), `estado_actual` (`'PREPARADO'`, `'PRECINTADO'`, `'EN_TRANSITO'`, `'RECIBIDO'`, `'VERIFICADO'`, `'RECHAZADO'`), `observacion_rechazo` (TEXT).
11. **`detalle_bulto`**: `id` (PK), `bulto_id` (FK), `producto_id` (FK), `cantidad` (INTEGER).
12. **`historial_estado_bulto`** *(Tabla Inmutable - Solo `INSERT`)*: `id` (PK), `bulto_id` (FK), `estado_anterior` (TEXT), `estado_nuevo` (TEXT), `fecha_hora` (DATETIME ISO8601), `usuario_responsable` (TEXT), `observaciones` (TEXT).
13. **`ventas`** y **`detalle_ventas`**: `id` (PK), `nro_comprobante` (UNIQUE), `local_id` (FK), `fecha_hora`, `medio_pago`, `referencia_pago`, `total_venta` (REAL), `estado`. En `detalle_ventas`: `id`, `venta_id` (FK), `producto_id` (FK), `cantidad`, `cantidad_devuelta`, `costo_unitario_historico`, `precio_unitario_historico`, `subtotal`.
14. **`devoluciones`** y **`detalle_devoluciones`**: `id` (PK), `nro_devolucion` (UNIQUE), `venta_id` (FK obligatoria), `local_id` (FK), `fecha_hora`, `motivo`, `total_reintegrado` (REAL).
15. **`movimientos_caja`**: `id` (PK), `local_id` (FK), `fecha_hora`, `tipo_movimiento` (`'INGRESO_VENTA'`, `'EGRESO_DEVOLUCION'`), `medio_pago`, `monto` (REAL), `referencia_id`.