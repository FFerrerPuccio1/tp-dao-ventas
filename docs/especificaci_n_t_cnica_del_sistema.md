# Especificación de Requerimientos y Arquitectura de Software (`specs.md`)
**Proyecto:** Sistema de Ventas, Inventario y Logística Interna (CD a Locales) — Tema 3  
**Cátedra:** Desarrollo de Aplicaciones con Objetos (DAO) - 2026  

---

## 1. Descripción General y Arquitectura del Sistema

El sistema es una solución integral de tipo ERP ligero para un comercio minorista estructurado bajo un modelo **Hub & Spoke** (un Centro de Distribución central que abastece a múltiples Sucursales/Locales comerciales).

### 1.1. Stack Tecnológico y Arquitectura
* **Estilo Arquitectónico:** Monolito Modular en Capas (Layered Architecture) con clara separación de responsabilidades para respetar los principios **SOLID** y el paradigma **Orientado a Objetos**.
* **Lenguaje:** Python 3.11+
* **Base de Datos:** SQLite3 (persistencia relacional en archivo único `sistema_logistica.db`, con `PRAGMA foreign_keys = ON`).
* **Estructura de Capas del Monolito:**
  1. **Capa de Presentación (UI / Controllers o Views):** Interfaz de usuario (Web vía Flask/FastAPI + Jinja2 o Desktop vía PyQt6/CustomTkinter) que captura eventos y muestra datos sin contener lógica de negocio.
  2. **Capa de Aplicación / Servicios (`services/`):** Coordina los casos de uso, maneja las transacciones de base de datos (Unit of Work) e invoca a los objetos de dominio.
  3. **Capa de Dominio (`domain/`):** El corazón del TP. Contiene las Clases de Entidad, Objetos de Valor, **Patrones de Diseño (State, Strategy, etc.)** y todas las validaciones de negocio puras en Python.
  4. **Capa de Infraestructura / Persistencia (`repositories/`):** Implementación del patrón *Repository* o *DAO (Data Access Object)* con consultas SQL parametrizadas hacia `sqlite3` (o mapeo mediante SQLAlchemy).

---

## 2. Patrones de Diseño (Orientados a Objetos)

La cátedra exige **al menos dos patrones de diseño GoF (Gang of Four)** aplicados al dominio y evaluará críticamente el ciclo de vida del bulto. Implementaremos **3 patrones principales**:

### 2.1. Patrón STATE (Obligatorio / Crítico para el Ciclo de Vida del Bulto)
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

### 2.2. Patrón STRATEGY (Para Medios de Pago y Cobros en Caja)
* **Problema que resuelve:** El proceso 7 exige cobrar ventas con distintos medios de pago (Efectivo, Tarjeta de Débito, Tarjeta de Crédito, Transferencia/QR) y gestionar su impacto en caja y validaciones particulares (ej. recargos, validación de número de cupón/operación, cálculo de vuelto).
* **Estructura de Clases:**
  * `EstrategiaMedioPago` (Clase Abstracta): Define el método `procesar_pago(monto_base: float, datos_pago: dict) -> ResultadoPago`.
  * **Subclases Concretas:**
    * `PagoEfectivoStrategy`: Valida que el monto entregado sea $\ge$ monto base, calcula vuelto e impacta en el arqueo de efectivo físico del local.
    * `PagoTarjetaStrategy`: Exige código de autorización/cupón y últimos 4 dígitos; impacta en la cuenta de recaudación bancaria del local.
    * `PagoTransferenciaQRStrategy`: Exige identificador de transacción digital.

### 2.3. Patrón REPOSITORY (Arquitectónico / Persistencia)
* **Problema que resuelve:** Desacopla el modelo de dominio en Python de las sentencias SQL específicas de `sqlite3`.
* **Aplicación:** Clases como `ProductoRepository`, `BultoRepository`, `VentaRepository` se encargan de reconstruir el grafo de objetos (incluyendo el estado actual del bulto y su historial) a partir de las filas de SQLite.

---

## 3. Procesos de Negocio Obligatorios (Especificación Funcional)

> **Nota de Alcance:** Se excluyen todos los procesos opcionales (órdenes de compra sugeridas automáticas, promociones/listas de precios, lotes/vencimientos, clientes frecuentes/cuentas corrientes e inventarios físicos).

### Proceso 1: Administración de Ubicaciones (Centro de Distribución y Locales)
* **Objetivo:** Gestionar las entidades físicas donde se almacena o vende mercadería.
* **Reglas de Negocio:**
  * Existe **1 único Centro de Distribución (CD)** activo como nodo abastecedor central y **$N$ Sucursales/Locales** comerciales.
  * Cada ubicación posee un código único (ej. `CD-01`, `LOC-001`), nombre, dirección, teléfono y estado (Activo/Inactivo).
  * Cada ubicación tiene su propio inventario independiente por producto (`StockUbicacion`) y su propia Caja (`CajaSucursal`).

### Proceso 2: Administración de Catálogo (Productos, Categorías, Precios, Stock Mínimo y Proveedores) + Abastecimiento al CD
* **Objetivo:** Mantener el maestro de artículos, proveedores y permitir el ingreso de mercadería al CD para que exista stock que distribuir y costo base para calcular márgenes.
* **Reglas de Negocio:**
  * **Proveedores:** Identificados por `CUIT` único y Razón Social. **Validación:** No se permiten dos proveedores con el mismo CUIT.
  * **Categorías:** Clasificación jerárquica simple (ID, Nombre, Descripción).
  * **Productos:** Identificados por `SKU` (Código alfanumérico único) y `CodigoBarras` (EAN13 único). Poseen nombre, categoría, proveedor habitual, `costo_unitario_actual` (último precio de compra) y `precio_venta_unitario`.
  * **Niveles Mínimos de Existencia:** Cada producto tiene parametrizado un `stock_minimo` por cada Ubicación (`StockUbicacion`).
  * **Ingreso de Stock al CD (Compra a Proveedor):** Permite registrar una factura/remito de proveedor ingresando unidades al stock del CD y actualizando el costo unitario del producto.

### Proceso 3: Consolidación de Necesidades y Orden de Reposición (Local $\rightarrow$ CD)
* **Objetivo:** Solicitar mercadería desde un Local hacia el Centro de Distribución.
* **Flujo:**
  1. El encargado del Local (o el operador central) selecciona el **Local Destino** y el **CD Origen**.
  2. El sistema puede mostrar todos los productos y resaltar aquellos donde `stock_disponible <= stock_minimo` en ese local.
  3. Se agregan ítems (`Producto`, `cantidad_solicitada > 0`) a una **Orden de Reposición**.
  4. La orden se guarda en estado `Solicitada` con fecha de emisión y número correlativo (`OR-2026-XXXX`).

### Proceso 4: Empaquetado en Bultos, Asignación de Remito y Precinto (en el CD)
* **Objetivo:** Preparar físicamente la mercadería solicitada en contenedores seguros y trazables.
* **Flujo y Reglas:**
  1. En el CD se selecciona una `OrdenReposicion` pendiente.
  2. Se crea un **Remito de Despacho** (`REM-XXXX`) asociado a la orden (indicando CD Origen y Local Destino).
  3. Se crean uno o más **Bultos / Contenedores** (`BUL-XXXX`) asociados al Remito.
  4. Se asignan productos y cantidades dentro de cada Bulto (validando que el CD tenga stock disponible suficiente). Al crearse el bulto con sus ítems, nace en estado **`Preparado`** (registrando el primer hito en `HistorialEstadoBulto`).
  5. **Precintado:** El operario coloca físicamente el precinto y registra el **Código de Precinto de Seguridad** (único e irrepetible, ej. `PREC-998123`). El bulto ejecuta `bulto.precintar(codigo)` y pasa a estado **`Precintado`**.

### Proceso 5: Despacho de Bultos desde el Centro de Distribución
* **Objetivo:** Dar salida efectiva a los bultos hacia el local destino.
* **Flujo y Reglas:**
  1. Solo se pueden despachar bultos cuyo estado actual sea **`Precintado`**.
  2. Al confirmar el despacho del Remito/Bultos:
     * Cada bulto ejecuta `bulto.despachar()`, cambiando su estado a **`En Tránsito`** y grabando el timestamp exacto de salida en el historial inmutable.
     * El stock en el CD se descuenta de `stock_disponible` y pasa a `stock_en_transito` hacia el local destino.

### Proceso 6: Recepción y Verificación de Precinto en el Local Destino
* **Objetivo:** Controlar la integridad del envío antes de habilitar la mercadería para la venta.
* **Flujo y Reglas (2 pasos o pantalla unificada de recepción y control):**
  1. **Arribo físico (`Recibido`):** Cuando el transporte llega al local, el bulto se marca como **`Recibido`** (registra timestamp de llegada, cerrando el tiempo de tránsito). **Importante:** En estado `Recibido`, el stock **AÚN NO** está disponible para la venta.
  2. **Inspección de Precinto y Contenido (`Verificado` vs. `Rechazado`):**
     * El receptor del local inspecciona el precinto físico y lo compara con el `codigo_precinto` del sistema:
     * **Camino Feliz (Precinto Íntegro):** Marca el bulto como **`Verificado`**. En este exacto instante, dentro de una transacción atómica, el sistema suma las cantidades del bulto al `stock_disponible` del Local Destino y descuenta de `stock_en_transito`.
     * **Camino de Excepción (Precinto Violado / Roto / Adulterado):** El usuario selecciona "Precinto Roto/Violado" e ingresa observación obligatoria. El bulto pasa a estado **`Rechazado`** (Rechazo Logístico). **Validación Crítica:** La mercadería de ese bulto **NO ingresa al stock disponible** del local; queda registrada como stock retenido/merma logística por rotura de precinto.

### Proceso 7: Ventas en Local, Cobros, Comprobante y Devoluciones
* **Objetivo:** Operación comercial minorista en cada sucursal.
* **7.A. Registro de Venta:**
  * Se opera siempre sobre un **Local específico** con su **Caja abierta**.
  * Se agregan 1 o más productos (`DetalleVenta`: Producto, Cantidad, Precio Unitario vigente, Subtotal).
  * **Validación Crítica:** Por cada renglón, `cantidad_a_vender <= stock_disponible` (verificado) de ese Local. Si supera el stock, se impide agregar o confirmar la venta.
  * **Cobro:** Se selecciona el Medio de Pago (aplicando `EstrategiaMedioPago`: Efectivo, Débito, Crédito, QR/Transferencia). Se registra el ingreso en `MovimientoCaja`.
  * **Confirmación:** Descuenta el `stock_disponible` del Local y emite un **Comprobante de Venta** único (`TICKET-LOC01-000123`) con fecha, hora, detalle de ítems, total y medio de pago.
* **7.B. Gestión de Devoluciones:**
  * **Validación Crítica:** No se aceptan devoluciones libres. Toda devolución debe buscar y vincular obligatoriamente un **Comprobante de Venta registrado** previamente.
  * **Reglas de validación de devolución:**
    1. El producto a devolver debe existir en el comprobante original.
    2. La `cantidad_a_devolver` no puede superar la `(cantidad_comprada - cantidad_ya_devuelta_previamente)` de ese ítem en esa venta.
    3. La venta debe estar dentro del plazo de devolución permitido (ej. $\le 30$ días corridos desde la fecha de venta).
  * **Impacto:**
    * **En Stock:** Si el producto devuelto está en condiciones de venta, reingresa sumando al `stock_disponible` del Local. (Opcionalmente, si es por falla, puede ir a stock defectuoso, pero por regla general reintegra stock al local).
    * **En Caja:** Genera un `MovimientoCaja` de tipo **Egreso / Nota de Crédito** por el monto exacto devuelto, restando de la recaudación de la caja del local.

---

## 4. Modelo de Datos Relacional (SQLite3)

A continuación se definen las tablas principales que componen la base de datos `sqlite3`:

1. **`ubicaciones`**:
   * `id` (PK), `codigo` (UNIQUE), `nombre`, `tipo` (`'CD'` o `'LOCAL'`), `direccion`, `activo` (BOOLEAN).
2. **`proveedores`**:
   * `id` (PK), `cuit` (UNIQUE), `razon_social`, `telefono`, `email`, `activo` (BOOLEAN).
3. **`categorias`**:
   * `id` (PK), `nombre` (UNIQUE), `descripcion`.
4. **`productos`**:
   * `id` (PK), `sku` (UNIQUE), `codigo_barras` (UNIQUE), `nombre`, `categoria_id` (FK), `proveedor_id` (FK), `costo_unitario` (REAL), `precio_venta` (REAL), `activo` (BOOLEAN).
5. **`stock_ubicacion`**:
   * `id` (PK), `ubicacion_id` (FK), `producto_id` (FK), `cantidad_disponible` (INTEGER), `cantidad_en_transito` (INTEGER), `cantidad_rechazada` (INTEGER), `stock_minimo` (INTEGER).
   * *Constraint:* `UNIQUE(ubicacion_id, producto_id)` y `CHECK(cantidad_disponible >= 0)`.
6. **`ingresos_cd`** y **`detalle_ingresos_cd`** (Compras a proveedores para abastecer el CD):
   * `id` (PK), `proveedor_id` (FK), `nro_factura_remito`, `fecha_hora`, `total_costo`.
7. **`ordenes_reposicion`** y **`detalle_orden_reposicion`**:
   * `id` (PK), `nro_orden` (UNIQUE), `origen_cd_id` (FK), `destino_local_id` (FK), `fecha_solicitud`, `estado` (`'SOLICITADA'`, `'PROCESADA'`, `'COMPLETADA'`).
8. **`remitos_despacho`**:
   * `id` (PK), `nro_remito` (UNIQUE), `orden_reposicion_id` (FK), `origen_cd_id` (FK), `destino_local_id` (FK), `fecha_emision`, `estado` (`'EMITIDO'`, `'EN_TRANSITO'`, `'PROCESADO_DESTINO'`).
9. **`bultos`**:
   * `id` (PK), `codigo_bulto` (UNIQUE), `remito_id` (FK), `codigo_precinto` (UNIQUE, NULLABLE hasta precintar), `estado_actual` (`'PREPARADO'`, `'PRECINTADO'`, `'EN_TRANSITO'`, `'RECIBIDO'`, `'VERIFICADO'`, `'RECHAZADO'`), `observacion_rechazo` (TEXT).
10. **`detalle_bulto`**:
    * `id` (PK), `bulto_id` (FK), `producto_id` (FK), `cantidad` (INTEGER).
11. **`historial_estado_bulto`** *(Tabla Inmutable - Solo `INSERT`, prohibido `UPDATE`/`DELETE`)*:
    * `id` (PK), `bulto_id` (FK), `estado_anterior` (TEXT), `estado_nuevo` (TEXT), `fecha_hora` (DATETIME ISO8601), `usuario_responsable` (TEXT), `observaciones` (TEXT).
12. **`ventas`** y **`detalle_ventas`**:
    * `id` (PK), `nro_comprobante` (UNIQUE), `local_id` (FK), `fecha_hora`, `medio_pago` (`'EFECTIVO'`, `'DEBITO'`, `'CREDITO'`, `'QR_TRANSFERENCIA'`), `referencia_pago`, `total_venta` (REAL), `estado` (`'COMPLETADA'`, `'DEVUELTA_PARCIAL'`, `'DEVUELTA_TOTAL'`).
    * En `detalle_ventas`: `id`, `venta_id` (FK), `producto_id` (FK), `cantidad`, `cantidad_devuelta` (default 0), `costo_unitario_historico` (para reporte de margen exacto), `precio_unitario_historico`, `subtotal`.
13. **`devoluciones`** y **`detalle_devoluciones`**:
    * `id` (PK), `nro_devolucion` (UNIQUE), `venta_id` (FK obligatoria), `local_id` (FK), `fecha_hora`, `motivo`, `total_reintegrado` (REAL).
14. **`movimientos_caja`**:
    * `id` (PK), `local_id` (FK), `fecha_hora`, `tipo_movimiento` (`'INGRESO_VENTA'`, `'EGRESO_DEVOLUCION'`), `medio_pago`, `monto` (REAL, positivo para venta, negativo para devolución), `referencia_id` (ID de venta o devolución).

---

## 5. Especificación de los 5 Reportes No Triviales (Obligatorio mín. 4)

Implementaremos los 5 reportes sugeridos para superar ampliamente el mínimo de 4 exigido:

1. **Reporte de Ventas e Ingresos Netos por Período, Local y Medio de Pago:**
   * **Filtros:** Rango de fechas (`desde`, `hasta`), Local (Todos o uno específico).
   * **Cálculo:** Agrupa ventas brutas, resta devoluciones del período, desglosa por medio de pago y muestra el Neto en Caja.
2. **Reporte de Productos Más Vendidos y Margen de Ganancia-Pérdida Estimado:**
   * **Filtros:** Rango de fechas, Categoría, Local.
   * **Cálculo Financiero:**
     $$\text{Ingresos Netos} = \sum (\text{cant\_vendida} - \text{cant\_devuelta}) \times \text{precio\_unitario\_historico}$$
     $$\text{Costo Mercadería Vendida (CMV)} = \sum (\text{cant\_vendida} - \text{cant\_devuelta}) \times \text{costo\_unitario\_historico}$$
     $$\text{Pérdida por Rechazo Logístico} = \sum \text{cant\_rechazada\_en\_bultos} \times \text{costo\_unitario}$$
     $$\text{Margen Neto Estimado} = \text{Ingresos Netos} - \text{CMV} - \text{Pérdida por Rechazo Logístico}$$
3. **Reporte de Existencias Actuales, Valorización de Inventario y Alertas de Stock Mínimo:**
   * **Filtros:** Ubicación (CD o Locales), Solo bajo stock mínimo (Switch Sí/No).
   * **Columnas:** SKU, Producto, Ubicación, Stock Disponible, Stock en Tránsito, Stock Mínimo, Estado (`CRÍTICO` si $\text{Disponible} \le \text{Mínimo}$, `OK` si supera), Valorización a Costo ($\text{Disponible} \times \text{Costo}$).
4. **Reporte de Auditoría de Bultos Rechazados y Mermas por Rotura de Precinto:**
   * **Filtros:** Rango de fechas, Local Destino.
   * **Detalle:** Lista todos los bultos en estado `RECHAZADO`, mostrando Código de Bulto, Remito, Código de Precinto violado, Fecha/Hora de despacho vs. Fecha/Hora de rechazo, Productos afectados, Costo total de la merma retenida y Observación del receptor.
5. **Reporte de Desempeño Logístico (Tiempo Promedio de Tránsito CD $\rightarrow$ Locales):**
   * **Cálculo no trivial sobre `historial_estado_bulto`:** Calcula para cada Local Destino la diferencia de tiempo ($\Delta t$ en horas y minutos) entre el timestamp del estado `EN_TRANSITO` y el timestamp del estado `RECIBIDO` de todos sus bultos, informando Tiempo Mínimo, Tiempo Promedio, Tiempo Máximo y Tasa de Efectividad de Entregas ($\%$ Verificados vs. $\%$ Rechazados).