"""Datos de la demo y las mutaciones del flujo. Se pierde al reiniciar el proceso."""

import hashlib
from datetime import datetime, timedelta

# shortcut: mapa de estados en vez del patrón State, reemplazar cuando exista domain/
SIGUIENTE = {
    ("PREPARADO", "precintar"): "PRECINTADO",
    ("PRECINTADO", "despachar"): "EN_TRANSITO",
    ("EN_TRANSITO", "recibir"): "RECIBIDO",
    ("RECIBIDO", "verificar"): "VERIFICADO",
    ("RECIBIDO", "rechazar"): "RECHAZADO",
}

AHORA = datetime(2026, 10, 23, 15, 20, 0)
LOCAL = "LOC-01"
CD = "CD-01"


def hash_clave(clave):
    return hashlib.sha256(clave.encode()).hexdigest()


def clave_ok(guardada, clave):
    return guardada == hash_clave(clave)


def _dt(hora, minuto, dia=23, segundo=0):
    return datetime(2026, 10, dia, hora, minuto, segundo)


class Store:
    def __init__(self):
        self.notice = ""
        self.form_error = ""
        self.held = {}
        self.draft = []
        self.cart = []
        self.medio = "efectivo"
        self.venta_q = ""
        self._seed()

    def _seed(self):
        self.seq = {"or": 42, "rem": 89, "bul": 101, "tck": 451, "dev": 12}
        self.categorias = [
            {"id": "CAT-01", "nombre": "Audio", "descripcion": "Auriculares, parlantes y equipos de sonido"},
            {"id": "CAT-02", "nombre": "Periféricos", "descripcion": "Teclados, mouses y dispositivos de entrada"},
            {"id": "CAT-03", "nombre": "Accesorios", "descripcion": "Cables, cargadores y adaptadores"},
        ]
        self.proveedores = [
            {"cuit": "30-71234567-8", "razon": "TecnoSur S.A.", "tel": "011-4552-9000", "email": "ventas@tecnosur.com.ar", "rubros": ["Audio", "Periféricos"], "activo": True},
            {"cuit": "30-69854123-4", "razon": "Digital Global SRL", "tel": "011-4881-2200", "email": "pedidos@digitalglobal.com", "rubros": ["Periféricos", "Accesorios"], "activo": True},
            {"cuit": "30-70551682-9", "razon": "Conecta Argentina S.A.", "tel": "0351-422-8910", "email": "logistica@conecta.com.ar", "rubros": ["Accesorios"], "activo": True},
        ]
        self.productos = [
            self._prod("PROD-0014", "7791234560012", "Auriculares Bluetooth Pro", "CAT-01", "30-71234567-8", 12500, 19900),
            self._prod("PROD-0021", "7791234560029", "Teclado Mecánico RGB", "CAT-02", "30-71234567-8", 9200, 14900),
            self._prod("PROD-0035", "7791234560036", "Mouse Inalámbrico", "CAT-02", "30-69854123-4", 4800, 8500),
            self._prod("PROD-0042", "7791234560043", "Parlante Portátil Mini", "CAT-01", "30-71234567-8", 8900, 15900),
            self._prod("PROD-0058", "7791234560050", "Cargador USB-C 30W", "CAT-03", "30-69854123-4", 3400, 6900),
            self._prod("PROD-0063", "7791234560067", "Cable USB-C 1 metro", "CAT-03", "30-70551682-9", 1200, 2900),
        ]
        self.ubicaciones = [
            {"codigo": "CD-01", "nombre": "Centro de Distribución Central", "tipo": "CD", "direccion": "Av. Circunvalación y Autopista, Parque Industrial, Córdoba", "tel": "0351-480-1000", "activo": True, "caja": 0, "caja_abierta": False},
            {"codigo": "LOC-01", "nombre": "Local 01 - Sucursal Centro", "tipo": "LOCAL", "direccion": "Av. Colón 250, Centro", "tel": "0351-422-1100", "activo": True, "caja": 450200, "caja_abierta": True},
            {"codigo": "LOC-02", "nombre": "Local 02 - Sucursal Norte", "tipo": "LOCAL", "direccion": "Av. Rafael Núñez 4120, Cerro", "tel": "0351-481-2200", "activo": True, "caja": 312500, "caja_abierta": True},
            {"codigo": "LOC-03", "nombre": "Local 03 - Sucursal Sur", "tipo": "LOCAL", "direccion": "Av. O'Higgins 3200, Jardín", "tel": "0351-460-3300", "activo": True, "caja": 290000, "caja_abierta": True},
        ]
        mins = {
            "PROD-0014": {"CD-01": 100, "LOC-01": 20, "LOC-02": 15, "LOC-03": 15},
            "PROD-0021": {"CD-01": 80, "LOC-01": 10, "LOC-02": 10, "LOC-03": 10},
            "PROD-0035": {"CD-01": 60, "LOC-01": 7, "LOC-02": 8, "LOC-03": 10},
            "PROD-0042": {"CD-01": 40, "LOC-01": 10, "LOC-02": 6, "LOC-03": 8},
            "PROD-0058": {"CD-01": 50, "LOC-01": 10, "LOC-02": 10, "LOC-03": 10},
            "PROD-0063": {"CD-01": 40, "LOC-01": 8, "LOC-02": 5, "LOC-03": 8},
        }
        disp = {
            "PROD-0014": {"CD-01": 240, "LOC-01": 12, "LOC-02": 18, "LOC-03": 25},
            "PROD-0021": {"CD-01": 320, "LOC-01": 4, "LOC-02": 12, "LOC-03": 20},
            "PROD-0035": {"CD-01": 280, "LOC-01": 8, "LOC-02": 10, "LOC-03": 18},
            "PROD-0042": {"CD-01": 260, "LOC-01": 2, "LOC-02": 8, "LOC-03": 16},
            "PROD-0058": {"CD-01": 250, "LOC-01": 6, "LOC-02": 9, "LOC-03": 16},
            "PROD-0063": {"CD-01": 190, "LOC-01": 6, "LOC-02": 7, "LOC-03": 15},
        }
        self.stock = {}
        for prod in self.productos:
            sku = prod["sku"]
            for ubi in self.ubicaciones:
                cod = ubi["codigo"]
                self.stock[(cod, sku)] = {
                    "disp": disp[sku][cod],
                    "transito": 0,
                    "cuarentena": 0,
                    "rechazada": 0,
                    "minimo": mins[sku][cod],
                }
        self.stock[("LOC-01", "PROD-0014")].update(transito=40, cuarentena=30, rechazada=10)
        self.stock[("LOC-01", "PROD-0021")]["cuarentena"] = 10
        self.ordenes = [
            {
                "nro": "OR-2026-0041",
                "destino": LOCAL,
                "fecha": _dt(7, 40),
                "estado": "PROCESADA",
                "items": [{"sku": "PROD-0014", "qty": 80}, {"sku": "PROD-0021", "qty": 10}],
            },
            {
                "nro": "OR-2026-0042",
                "destino": LOCAL,
                "fecha": _dt(9, 0),
                "estado": "SOLICITADA",
                "items": [
                    {"sku": "PROD-0014", "qty": 20},
                    {"sku": "PROD-0021", "qty": 15},
                    {"sku": "PROD-0042", "qty": 10},
                    {"sku": "PROD-0063", "qty": 40},
                ],
            },
        ]
        self.remitos = [
            {"nro": "REM-00088", "orden": "OR-2026-0041", "destino": LOCAL, "fecha": _dt(8, 0), "estado": "EN_TRANSITO"},
            {"nro": "REM-00089", "orden": "OR-2026-0042", "destino": LOCAL, "fecha": _dt(9, 10), "estado": "EMITIDO"},
        ]
        self.bultos = [
            self._bulto("BUL-2026-0098", "REM-00088", "OR-2026-0041", "PREC-551209", "EN_TRANSITO", "", [{"sku": "PROD-0014", "qty": 40}], [
                ("", "PREPARADO", _dt(8, 0, segundo=10), "Creado en CD-01 (Remito #REM-00088)."),
                ("PREPARADO", "PRECINTADO", _dt(8, 12), "Precinto asignado: PREC-551209."),
                ("PRECINTADO", "EN_TRANSITO", _dt(8, 30), "Despachado desde CD-01 hacia Local 01 - Centro."),
            ]),
            self._bulto("BUL-2026-0099", "REM-00088", "OR-2026-0041", "PREC-551210", "RECIBIDO", "", [{"sku": "PROD-0014", "qty": 30}, {"sku": "PROD-0021", "qty": 10}], [
                ("", "PREPARADO", _dt(8, 0, segundo=10), "Creado en CD-01 (Remito #REM-00088)."),
                ("PREPARADO", "PRECINTADO", _dt(8, 15, segundo=40), "Precinto asignado: PREC-551210."),
                ("PRECINTADO", "EN_TRANSITO", _dt(8, 30), "Despachado desde CD-01 hacia Local 01 - Centro."),
                ("EN_TRANSITO", "RECIBIDO", _dt(12, 45, segundo=12), "Arribo físico en Local 01. Stock en cuarentena."),
            ]),
            self._bulto("BUL-2026-0090", "REM-00088", "OR-2026-0041", "PREC-44109", "RECHAZADO", "Precinto PREC-44109 cortado al arribar al local", [{"sku": "PROD-0014", "qty": 10}], [
                ("", "PREPARADO", _dt(8, 1), "Creado en CD-01 (Remito #REM-00088)."),
                ("PREPARADO", "PRECINTADO", _dt(8, 16), "Precinto asignado: PREC-44109."),
                ("PRECINTADO", "EN_TRANSITO", _dt(8, 31), "Despachado desde CD-01 hacia Local 01 - Centro."),
                ("EN_TRANSITO", "RECIBIDO", _dt(12, 50), "Arribo físico en Local 01."),
                ("RECIBIDO", "RECHAZADO", _dt(13, 5), "Precinto PREC-44109 cortado al arribar al local."),
            ]),
            self._bulto("BUL-2026-0100", "REM-00089", "OR-2026-0042", "PREC-774102", "PRECINTADO", "", [{"sku": "PROD-0042", "qty": 10}], [
                ("", "PREPARADO", _dt(9, 15, segundo=4), "Creado en CD-01 (Remito #REM-00089)."),
                ("PREPARADO", "PRECINTADO", _dt(9, 42, segundo=18), "Precinto asignado: PREC-774102."),
            ]),
            self._bulto("BUL-2026-0101", "REM-00089", "OR-2026-0042", None, "PREPARADO", "", [{"sku": "PROD-0014", "qty": 20}, {"sku": "PROD-0021", "qty": 15}], [
                ("", "PREPARADO", _dt(9, 50), "Creado en CD-01 (Remito #REM-00089)."),
            ]),
        ]
        self.ventas = [{
            "nro": "TCK-LOC01-000451",
            "local": LOCAL,
            "fecha": _dt(14, 10, dia=22),
            "medio": "efectivo",
            "ref": "EF-451",
            "total": 54700.0,
            "items": [
                {"sku": "PROD-0014", "qty": 2, "devuelta": 0, "precio": 19900.0, "costo": 12500.0},
                {"sku": "PROD-0021", "qty": 1, "devuelta": 0, "precio": 14900.0, "costo": 9200.0},
            ],
        }]
        self.devoluciones = []
        self.movimientos = [{
            "fecha": _dt(14, 10, dia=22),
            "local": LOCAL,
            "tipo": "INGRESO_VENTA",
            "medio": "efectivo",
            "monto": 54700.0,
            "ref": "Venta #TCK-LOC01-000451",
        }]
        self.ingresos = []

    def _prod(self, sku, barra, nombre, cat, prov, costo, precio):
        return {"sku": sku, "barra": barra, "nombre": nombre, "categoria": cat, "proveedor": prov, "costo": float(costo), "precio": float(precio), "activo": True}

    def _bulto(self, codigo, remito, orden, precinto, estado, obs, items, hitos):
        return {
            "codigo": codigo,
            "remito": remito,
            "orden": orden,
            "precinto": precinto,
            "estado": estado,
            "obs": obs,
            "items": items,
            "historial": [
                {"anterior": a, "nuevo": n, "fecha": f, "usuario": "Operador CD Central", "obs": o}
                for a, n, f, o in hitos
            ],
        }

    def producto(self, sku):
        return next((p for p in self.productos if p["sku"] == sku), None)

    def proveedor(self, cuit):
        return next((p for p in self.proveedores if p["cuit"] == cuit), None)

    def ubicacion(self, codigo):
        return next((u for u in self.ubicaciones if u["codigo"] == codigo), None)

    def categoria(self, cid):
        return next((c for c in self.categorias if c["id"] == cid), None)

    def bulto(self, codigo):
        return next((b for b in self.bultos if b["codigo"] == codigo), None)

    def orden(self, nro):
        return next((o for o in self.ordenes if o["nro"] == nro), None)

    def venta(self, nro):
        return next((v for v in self.ventas if v["nro"] == nro), None)

    def cat_nombre(self, cid):
        cat = self.categoria(cid)
        return cat["nombre"] if cat else cid

    def prov_de(self, cuit):
        prov = self.proveedor(cuit)
        return prov["razon"] if prov else cuit

    def st(self, ubi, sku):
        return self.stock[(ubi, sku)]

    def productos_de(self, cuit):
        return sum(1 for p in self.productos if p["proveedor"] == cuit)

    def productos_cat(self, cid):
        return sum(1 for p in self.productos if p["categoria"] == cid)

    def filtrar_productos(self, q="", cat="", prov=""):
        q = (q or "").strip().lower()
        out = []
        for p in self.productos:
            if cat and p["categoria"] != cat:
                continue
            if prov and p["proveedor"] != prov:
                continue
            blob = f"{p['sku']} {p['barra']} {p['nombre']}".lower()
            if q and q not in blob:
                continue
            out.append(p)
        return out

    def stock_cd(self):
        return sum(self.st(CD, p["sku"])["disp"] for p in self.productos)

    def unidades_local(self, cod):
        return sum(self.st(cod, p["sku"])["disp"] for p in self.productos)

    def bajo_minimo(self, cod):
        return sum(1 for p in self.productos if self.st(cod, p["sku"])["disp"] <= self.st(cod, p["sku"])["minimo"])

    def _siguiente(self, bulto, accion):
        nuevo = SIGUIENTE.get((bulto["estado"], accion))
        if not nuevo:
            return f"No se puede {accion} un bulto en estado {bulto['estado']}."
        return None

    def _pasar(self, bulto, accion, obs, usuario):
        error = self._siguiente(bulto, accion)
        if error:
            return error
        anterior = bulto["estado"]
        bulto["estado"] = SIGUIENTE[(anterior, accion)]
        bulto["historial"].append({
            "anterior": anterior,
            "nuevo": bulto["estado"],
            "fecha": AHORA,
            "usuario": usuario,
            "obs": obs,
        })
        return None

    def _reservado_cd(self, sku):
        total = 0
        for bulto in self.bultos:
            if bulto["estado"] in ("PREPARADO", "PRECINTADO"):
                total += sum(it["qty"] for it in bulto["items"] if it["sku"] == sku)
        return total

    def empaquetado(self, nro, sku):
        total = 0
        for bulto in self.bultos:
            if bulto["orden"] == nro:
                total += sum(it["qty"] for it in bulto["items"] if it["sku"] == sku)
        return total

    def guardar_producto(self, data, nuevo):
        sku = data["sku"].strip().upper()
        if not sku or not data["nombre"].strip() or not data["barra"].strip():
            return "Completá SKU, código de barras y nombre."
        otro = self.producto(sku)
        if nuevo and otro:
            return f"El SKU '{sku}' ya se encuentra registrado en el sistema (Validación de no duplicidad)."
        if not nuevo and not otro:
            return "El producto no existe."
        barra = data["barra"].strip()
        for p in self.productos:
            if p["barra"] == barra and p["sku"] != sku:
                return f"El código de barras '{barra}' ya está usado por {p['sku']}."
        try:
            costo = float(data["costo"])
            precio = float(data["precio"])
        except ValueError:
            return "Costo y precio tienen que ser números."
        if costo < 0 or precio < 0:
            return "Costo y precio no pueden ser negativos."
        if nuevo:
            self.productos.append(self._prod(sku, barra, data["nombre"].strip(), data["categoria"], data["proveedor"], costo, precio))
            for ubi in self.ubicaciones:
                self.stock[(ubi["codigo"], sku)] = {"disp": 0, "transito": 0, "cuarentena": 0, "rechazada": 0, "minimo": 0}
        else:
            otro.update(barra=barra, nombre=data["nombre"].strip(), categoria=data["categoria"], proveedor=data["proveedor"], costo=costo, precio=precio)
        for ubi in self.ubicaciones:
            raw = data["minimos"].get(ubi["codigo"], "0") or "0"
            try:
                minimo = int(raw)
            except ValueError:
                return "El stock mínimo tiene que ser un entero."
            if minimo < 0:
                return "El stock mínimo no puede ser negativo."
            self.st(ubi["codigo"], sku)["minimo"] = minimo
        self.notice = f"Producto {sku} guardado."
        self.form_error = ""
        return None

    def guardar_proveedor(self, data, nuevo):
        cuit = data["cuit"].strip()
        razon = data["razon"].strip()
        original = (data.get("cuit_original") or "").strip()
        if not cuit or not razon or not data["tel"].strip() or not data["email"].strip():
            return "Completá CUIT, razón social, teléfono y email."
        tomado = self.proveedor(cuit)
        if not nuevo:
            actual = self.proveedor(original or cuit)
            if actual is None:
                return "El proveedor no existe."
            if tomado and tomado is not actual:
                return f"El CUIT '{cuit}' ya pertenece al proveedor registrado '{tomado['razon']}' (Validación de no duplicidad)."
            for prod in self.productos:
                if prod["proveedor"] == actual["cuit"]:
                    prod["proveedor"] = cuit
            actual.update(cuit=cuit, razon=razon, tel=data["tel"].strip(), email=data["email"].strip(), rubros=data["rubros"], activo=data["activo"])
        elif tomado:
            return f"El CUIT '{cuit}' ya pertenece al proveedor registrado '{tomado['razon']}' (Validación de no duplicidad)."
        else:
            self.proveedores.append({"cuit": cuit, "razon": razon, "tel": data["tel"].strip(), "email": data["email"].strip(), "rubros": data["rubros"], "activo": data["activo"]})
        self.notice = f"Proveedor {razon} guardado."
        self.form_error = ""
        return None

    def guardar_sucursal(self, data):
        codigo = data["codigo"].strip().upper()
        if not codigo or not data["nombre"].strip() or not data["direccion"].strip():
            return "Completá código, nombre y dirección."
        if data["tipo"] == "CD" or codigo.startswith("CD"):
            return "Ya existe un Centro de Distribución activo (CD-01). No se puede crear otro."
        if self.ubicacion(codigo):
            ubi = self.ubicacion(codigo)
            if ubi["tipo"] == "CD":
                return "El CD-01 no se da de alta de nuevo. Editá sus datos desde la tarjeta del nodo central."
            ubi.update(nombre=data["nombre"].strip(), direccion=data["direccion"].strip(), tel=data["tel"].strip(), caja_abierta=data["caja"])
            self.notice = f"Sucursal {codigo} actualizada."
            return None
        self.ubicaciones.append({
            "codigo": codigo, "nombre": data["nombre"].strip(), "tipo": "LOCAL",
            "direccion": data["direccion"].strip(), "tel": data["tel"].strip(),
            "activo": True, "caja": 0, "caja_abierta": data["caja"],
        })
        for prod in self.productos:
            self.stock[(codigo, prod["sku"])] = {"disp": 0, "transito": 0, "cuarentena": 0, "rechazada": 0, "minimo": 0}
        self.notice = f"Sucursal {codigo} creada."
        self.form_error = ""
        return None

    def guardar_categoria(self, nombre, descripcion):
        nombre = (nombre or "").strip()
        if not nombre:
            return "El nombre de la categoría es obligatorio."
        if any(c["nombre"].lower() == nombre.lower() for c in self.categorias):
            return "Esa categoría ya existe."
        self.categorias.append({
            "id": f"CAT-{len(self.categorias) + 1:02d}",
            "nombre": nombre,
            "descripcion": (descripcion or "").strip(),
        })
        self.notice = f"Categoría {nombre} creada."
        self.form_error = ""
        return None

    def editar_cd(self, nombre, direccion, tel):
        cd = self.ubicacion(CD)
        if not nombre.strip() or not direccion.strip():
            return "Completá nombre y dirección del CD."
        cd.update(nombre=nombre.strip(), direccion=direccion.strip(), tel=tel.strip())
        self.notice = "Datos del CD actualizados."
        return None

    def registrar_compra(self, cuit, factura, lineas):
        if not self.proveedor(cuit):
            return "Elegí un proveedor."
        if not factura.strip():
            return "Ingresá el número de factura o remito."
        limpias = []
        for sku, qty_raw, costo_raw in lineas:
            if not sku:
                continue
            if not self.producto(sku):
                return "Hay un producto que no existe."
            try:
                qty = int(qty_raw)
                costo = float(costo_raw)
            except ValueError:
                return "Cantidad y costo tienen que ser números."
            if qty < 0 or costo < 0:
                return "La cantidad y el costo no pueden ser negativos."
            if qty == 0:
                continue
            limpias.append((sku, qty, costo))
        if not limpias:
            return "Agregá al menos un producto."
        total = 0
        unidades = 0
        for sku, qty, costo in limpias:
            self.st(CD, sku)["disp"] += qty
            self.producto(sku)["costo"] = costo
            self.producto(sku)["proveedor"] = cuit
            total += qty * costo
            unidades += qty
        self.ingresos.append({"proveedor": cuit, "factura": factura.strip(), "fecha": AHORA, "total": total, "unidades": unidades})
        self.notice = f"Ingreso en CD-01: +{unidades} u. por {factura.strip()}."
        self.form_error = ""
        return None

    def agregar_draft(self, sku):
        prod = self.producto(sku)
        if not prod:
            return "Producto inexistente."
        if any(it["sku"] == sku for it in self.draft):
            return None
        falta = self.st(LOCAL, sku)["minimo"] - self.st(LOCAL, sku)["disp"]
        self.draft.append({"sku": sku, "qty": max(falta, 1)})
        return None

    def quitar_draft(self, sku):
        self.draft = [it for it in self.draft if it["sku"] != sku]

    def confirmar_orden(self, cantidades):
        items = []
        for it in self.draft:
            raw = cantidades.get(it["sku"], it["qty"])
            try:
                qty = int(raw)
            except (TypeError, ValueError):
                return "La cantidad solicitada tiene que ser un entero."
            if qty <= 0:
                return "Cada ítem tiene que pedir una cantidad mayor a cero."
            items.append({"sku": it["sku"], "qty": qty})
        if not items:
            return "Agregá al menos un producto a la orden."
        self.seq["or"] += 1
        nro = f"OR-2026-{self.seq['or']:04d}"
        self.ordenes.append({"nro": nro, "destino": LOCAL, "fecha": AHORA, "estado": "SOLICITADA", "items": items})
        self.draft = []
        self.notice = f"Orden {nro} enviada al CD."
        return None

    def _remito_de_orden(self, orden):
        remito = next((r for r in self.remitos if r["orden"] == orden["nro"]), None)
        if remito:
            return remito
        self.seq["rem"] += 1
        remito = {"nro": f"REM-{self.seq['rem']:05d}", "orden": orden["nro"], "destino": orden["destino"], "fecha": AHORA, "estado": "EMITIDO"}
        self.remitos.append(remito)
        return remito

    def crear_bulto(self, nro_orden):
        orden = self.orden(nro_orden)
        if not orden or orden["estado"] != "SOLICITADA":
            return "Esa orden no está pendiente de empaque."
        remito = self._remito_de_orden(orden)
        self.seq["bul"] += 1
        codigo = f"BUL-2026-{self.seq['bul']:04d}"
        self.bultos.append(self._bulto(codigo, remito["nro"], orden["nro"], None, "PREPARADO", "", [], [
            ("", "PREPARADO", AHORA, f"Creado en CD-01 (Remito #{remito['nro']})."),
        ]))
        self.notice = f"Bulto {codigo} creado en estado Preparado."
        return None

    def asignar_a_bulto(self, codigo, sku, qty_raw):
        bulto = self.bulto(codigo)
        if not bulto:
            return "El bulto no existe."
        if bulto["estado"] != "PREPARADO":
            return "Solo se agregan ítems a un bulto en estado Preparado."
        orden = self.orden(bulto["orden"])
        pedido = next((it["qty"] for it in orden["items"] if it["sku"] == sku), 0)
        try:
            qty = int(qty_raw)
        except (TypeError, ValueError):
            return "La cantidad tiene que ser un entero."
        if qty <= 0:
            return "La cantidad a asignar tiene que ser mayor a cero."
        pendiente = pedido - self.empaquetado(orden["nro"], sku)
        if qty > pendiente:
            return f"Pendiente de empaquetar de {sku}: {pendiente} u."
        if self._reservado_cd(sku) + qty > self.st(CD, sku)["disp"]:
            return f"El CD no tiene stock suficiente de {sku}."
        fila = next((it for it in bulto["items"] if it["sku"] == sku), None)
        if fila:
            fila["qty"] += qty
        else:
            bulto["items"].append({"sku": sku, "qty": qty})
        self.notice = f"{qty} u. de {sku} asignadas a {codigo}."
        return None

    def precintar(self, codigo, precinto, usuario="Operador CD Central"):
        bulto = self.bulto(codigo)
        if not bulto:
            return "El bulto no existe."
        precinto = (precinto or "").strip().upper()
        if not precinto:
            return "Ingresá el código de precinto."
        if not bulto["items"]:
            return "El bulto no tiene productos."
        if any(b["precinto"] == precinto for b in self.bultos):
            return f"El precinto '{precinto}' ya está usado."
        error = self._pasar(bulto, "precintar", f"Precinto asignado: {precinto}.", usuario)
        if error:
            return error
        bulto["precinto"] = precinto
        self.notice = f"{codigo} pasó a Precintado ({precinto})."
        return None

    def despachar(self, codigo, usuario="Operador CD Central"):
        bulto = self.bulto(codigo)
        if not bulto:
            return "El bulto no existe."
        if bulto["estado"] == "PREPARADO":
            return "Falta precintar el bulto antes de despacharlo."
        destino = self._destino(bulto)
        for it in bulto["items"]:
            if self.st(CD, it["sku"])["disp"] < it["qty"]:
                return f"Stock insuficiente en el CD para {it['sku']}."
        error = self._pasar(bulto, "despachar", f"Despachado desde CD-01 hacia {self.ubicacion(destino)['nombre']}.", usuario)
        if error:
            return error
        for it in bulto["items"]:
            self.st(CD, it["sku"])["disp"] -= it["qty"]
            self.st(destino, it["sku"])["transito"] += it["qty"]
        remito = next(r for r in self.remitos if r["nro"] == bulto["remito"])
        remito["estado"] = "EN_TRANSITO"
        self._cerrar_orden_si_corresponde(bulto["orden"])
        self.notice = f"{codigo} en tránsito hacia {destino}."
        return None

    def _destino(self, bulto):
        return next(r["destino"] for r in self.remitos if r["nro"] == bulto["remito"])

    def _cerrar_orden_si_corresponde(self, nro):
        orden = self.orden(nro)
        bultos = [b for b in self.bultos if b["orden"] == nro]
        if not bultos:
            return
        cubierto = all(self.empaquetado(nro, it["sku"]) >= it["qty"] for it in orden["items"])
        despachados = all(b["estado"] not in ("PREPARADO", "PRECINTADO") for b in bultos)
        if cubierto and despachados:
            orden["estado"] = "PROCESADA"

    def recibir(self, codigo, usuario="Encargado Local 01"):
        bulto = self.bulto(codigo)
        if not bulto:
            return "El bulto no existe."
        if self._destino(bulto) != LOCAL:
            return "Ese bulto no corresponde a este local."
        error = self._pasar(bulto, "recibir", "Arribo físico en Local 01. Stock en cuarentena.", usuario)
        if error:
            return error
        for it in bulto["items"]:
            fila = self.st(LOCAL, it["sku"])
            fila["transito"] -= it["qty"]
            fila["cuarentena"] += it["qty"]
        self.notice = f"{codigo} recibido. La mercadería sigue en cuarentena."
        return None

    def verificar(self, codigo, usuario="Encargado Local 01"):
        bulto = self.bulto(codigo)
        if not bulto:
            return "El bulto no existe."
        error = self._pasar(bulto, "verificar", f"Precinto {bulto['precinto']} verificado íntegro en Local 01.", usuario)
        if error:
            return error
        for it in bulto["items"]:
            fila = self.st(LOCAL, it["sku"])
            fila["cuarentena"] -= it["qty"]
            fila["disp"] += it["qty"]
        self._cerrar_remito(bulto["remito"])
        self.notice = f"{codigo} verificado. El stock ya se puede vender."
        return None

    def rechazar(self, codigo, motivo, usuario="Encargado Local 01"):
        bulto = self.bulto(codigo)
        if not bulto:
            return "El bulto no existe."
        motivo = (motivo or "").strip()
        if not motivo:
            return "El motivo del rechazo es obligatorio."
        error = self._pasar(bulto, "rechazar", motivo, usuario)
        if error:
            return error
        bulto["obs"] = motivo
        for it in bulto["items"]:
            fila = self.st(LOCAL, it["sku"])
            fila["cuarentena"] -= it["qty"]
            fila["rechazada"] += it["qty"]
        self._cerrar_remito(bulto["remito"])
        self.notice = f"{codigo} rechazado. Esa mercadería no entra a stock vendible."
        return None

    def _cerrar_remito(self, nro):
        bultos = [b for b in self.bultos if b["remito"] == nro]
        if bultos and all(b["estado"] in ("VERIFICADO", "RECHAZADO") for b in bultos):
            next(r for r in self.remitos if r["nro"] == nro)["estado"] = "PROCESADO_DESTINO"

    def agregar_carrito(self, sku, qty_raw):
        prod = self.producto(sku)
        if not prod:
            return "No hay un producto con ese código."
        try:
            qty = int(qty_raw)
        except (TypeError, ValueError):
            return "La cantidad tiene que ser un entero."
        if qty <= 0:
            return "La cantidad tiene que ser mayor a cero."
        actual = next((it for it in self.cart if it["sku"] == sku), None)
        nueva = qty if actual is None else actual["qty"] + qty
        disp = self.st(LOCAL, sku)["disp"]
        if nueva > disp:
            return f"No se puede vender {nueva} u. El stock disponible y verificado en Local 01 es de {disp} u."
        if actual:
            actual["qty"] = nueva
        else:
            self.cart.append({"sku": sku, "qty": qty})
        return None

    def cambiar_carrito(self, sku, qty_raw):
        it = next((x for x in self.cart if x["sku"] == sku), None)
        if not it:
            return "Ese ítem no está en el ticket."
        try:
            qty = int(qty_raw)
        except (TypeError, ValueError):
            return "La cantidad tiene que ser un entero."
        if qty <= 0:
            self.cart = [x for x in self.cart if x["sku"] != sku]
            return None
        disp = self.st(LOCAL, sku)["disp"]
        if qty > disp:
            return f"No se puede vender {qty} u. El stock disponible y verificado en Local 01 es de {disp} u."
        it["qty"] = qty
        return None

    def quitar_carrito(self, sku):
        self.cart = [it for it in self.cart if it["sku"] != sku]

    def total_carrito(self):
        return sum(it["qty"] * self.producto(it["sku"])["precio"] for it in self.cart)

    def cobrar(self, medio, datos):
        if not self.cart:
            return "El ticket está vacío.", None
        for it in self.cart:
            disp = self.st(LOCAL, it["sku"])["disp"]
            if it["qty"] > disp:
                return f"No se puede vender {it['qty']} u. de {it['sku']}. Disponible: {disp} u.", None
        total = self.total_carrito()
        medio = medio or "efectivo"
        if medio == "efectivo":
            try:
                paga = float(datos.get("paga_con") or 0)
            except ValueError:
                return "El monto en efectivo tiene que ser un número.", None
            if paga < total:
                return "El efectivo entregado no cubre el total.", None
            ref = f"Vuelto {paga - total:.2f}"
        elif medio in ("debito", "credito"):
            cupon = (datos.get("cupon") or "").strip()
            ultimos = (datos.get("ultimos") or "").strip()
            if not cupon or len(ultimos) != 4 or not ultimos.isdigit():
                return "La tarjeta exige cupón y los últimos 4 dígitos.", None
            ref = f"Cupón {cupon} · ****{ultimos}"
        elif medio == "qr":
            tx = (datos.get("tx") or "").strip()
            if not tx:
                return "La transferencia exige el identificador de la operación.", None
            ref = tx
        else:
            return "Medio de pago desconocido.", None
        self.seq["tck"] += 1
        nro = f"TCK-LOC01-{self.seq['tck']:06d}"
        items = []
        for it in self.cart:
            prod = self.producto(it["sku"])
            self.st(LOCAL, it["sku"])["disp"] -= it["qty"]
            items.append({"sku": it["sku"], "qty": it["qty"], "devuelta": 0, "precio": prod["precio"], "costo": prod["costo"]})
        self.ventas.append({"nro": nro, "local": LOCAL, "fecha": AHORA, "medio": medio, "ref": ref, "total": total, "items": items})
        self.movimientos.append({"fecha": AHORA, "local": LOCAL, "tipo": "INGRESO_VENTA", "medio": medio, "monto": total, "ref": f"Venta #{nro}"})
        self.ubicacion(LOCAL)["caja"] += total
        self.cart = []
        self.notice = f"Comprobante {nro} emitido."
        self.form_error = ""
        return None, nro

    def confirmar_devolucion(self, nro, cantidades, motivo):
        venta = self.venta((nro or "").strip())
        if not venta or venta["local"] != LOCAL:
            return "Comprobante no encontrado. No se admiten devoluciones sin venta registrada."
        if AHORA - venta["fecha"] > timedelta(days=30):
            return "La venta está fuera del plazo de devolución (30 días)."
        motivo = (motivo or "").strip()
        if not motivo:
            return "El motivo de la devolución es obligatorio."
        lineas = []
        for item in venta["items"]:
            raw = cantidades.get(item["sku"], 0)
            try:
                qty = int(raw or 0)
            except (TypeError, ValueError):
                return "La cantidad a devolver tiene que ser un entero."
            if qty < 0:
                return "La cantidad a devolver no puede ser negativa."
            if qty == 0:
                continue
            pendiente = item["qty"] - item["devuelta"]
            if qty > pendiente:
                return f"De {item['sku']} se pueden devolver hasta {pendiente} u."
            lineas.append((item, qty))
        if not lineas:
            return "Indicá al menos una unidad a devolver."
        total = 0
        for item, qty in lineas:
            item["devuelta"] += qty
            self.st(LOCAL, item["sku"])["disp"] += qty
            total += qty * item["precio"]
        self.seq["dev"] += 1
        nro_dev = f"DEV-{self.seq['dev']:04d}"
        self.devoluciones.append({"nro": nro_dev, "venta": venta["nro"], "local": LOCAL, "fecha": AHORA, "motivo": motivo, "total": total})
        self.movimientos.append({
            "fecha": AHORA, "local": LOCAL, "tipo": "EGRESO_DEVOLUCION", "medio": venta["medio"],
            "monto": -total, "ref": f"{nro_dev} (Venta #{venta['nro']})",
        })
        self.ubicacion(LOCAL)["caja"] -= total
        self.notice = f"Devolución {nro_dev} registrada por {total:.2f}."
        self.form_error = ""
        self.venta_q = ""
        return None

    def reporte_comercial(self, desde, hasta, ubi, cat):
        ventas = [v for v in self.ventas if desde <= v["fecha"] <= hasta and (not ubi or v["local"] == ubi)]
        ingresos = 0
        cmv = 0
        ranking = {}
        cruce = {}
        for venta in ventas:
            if cat and not any(self.producto(it["sku"])["categoria"] == cat for it in venta["items"]):
                continue
            for it in venta["items"]:
                prod = self.producto(it["sku"])
                if cat and prod["categoria"] != cat:
                    continue
                netas = it["qty"] - it["devuelta"]
                ingresos += netas * it["precio"]
                cmv += netas * it["costo"]
                fila = ranking.setdefault(it["sku"], {"sku": it["sku"], "nombre": prod["nombre"], "netas": 0, "ingresos": 0, "costo": 0})
                fila["netas"] += netas
                fila["ingresos"] += netas * it["precio"]
                fila["costo"] += netas * it["costo"]
            cruce.setdefault(venta["local"], {}).setdefault(venta["medio"], 0)
            cruce[venta["local"]][venta["medio"]] += venta["total"]
            for dev in self.devoluciones:
                if dev["venta"] == venta["nro"]:
                    cruce[venta["local"]][venta["medio"]] -= dev["total"]
        merma = 0
        for bulto in self.bultos:
            if bulto["estado"] != "RECHAZADO":
                continue
            if not (desde <= bulto["historial"][-1]["fecha"] <= hasta):
                continue
            destino = self._destino(bulto)
            if ubi and destino != ubi:
                continue
            for it in bulto["items"]:
                prod = self.producto(it["sku"])
                if cat and prod["categoria"] != cat:
                    continue
                valor = it["qty"] * prod["costo"]
                merma += valor
                if it["sku"] in ranking:
                    ranking[it["sku"]]["merma"] = ranking[it["sku"]].get("merma", 0) + valor
        for fila in ranking.values():
            fila.setdefault("merma", 0)
            fila["ganancia"] = fila["ingresos"] - fila["costo"] - fila["merma"]
            fila["margen"] = (fila["ganancia"] / fila["ingresos"] * 100) if fila["ingresos"] else 0
        ordenado = sorted(ranking.values(), key=lambda f: f["netas"], reverse=True)
        margen = ingresos - cmv - merma
        return {"ingresos": ingresos, "cmv": cmv, "merma": merma, "margen": margen, "ranking": ordenado, "cruce": cruce}

    def reporte_logistico(self, ubi):
        por_local = {}
        for bulto in self.bultos:
            destino = self._destino(bulto)
            if ubi and destino != ubi:
                continue
            if bulto["estado"] not in ("RECIBIDO", "VERIFICADO", "RECHAZADO"):
                continue
            h = {e["nuevo"]: e["fecha"] for e in bulto["historial"]}
            if "EN_TRANSITO" not in h or "RECIBIDO" not in h:
                continue
            mins = int((h["RECIBIDO"] - h["EN_TRANSITO"]).total_seconds() // 60)
            fila = por_local.setdefault(destino, {"mins": [], "ok": 0, "bad": 0})
            fila["mins"].append(mins)
            if bulto["estado"] == "RECHAZADO":
                fila["bad"] += 1
            elif bulto["estado"] == "VERIFICADO":
                fila["ok"] += 1
        criticos = []
        for ubi_row in self.ubicaciones:
            if ubi and ubi_row["codigo"] != ubi:
                continue
            for prod in self.productos:
                fila = self.st(ubi_row["codigo"], prod["sku"])
                if fila["disp"] <= fila["minimo"]:
                    criticos.append({
                        "ubi": ubi_row["codigo"], "nombre_ubi": ubi_row["nombre"], "sku": prod["sku"],
                        "nombre": prod["nombre"], "disp": fila["disp"], "minimo": fila["minimo"],
                        "valor": fila["disp"] * prod["costo"],
                    })
        rechazados = []
        for bulto in self.bultos:
            if bulto["estado"] != "RECHAZADO":
                continue
            destino = self._destino(bulto)
            if ubi and destino != ubi:
                continue
            unidades = sum(it["qty"] for it in bulto["items"])
            valor = sum(it["qty"] * self.producto(it["sku"])["costo"] for it in bulto["items"])
            rechazados.append({
                "fecha": bulto["historial"][-1]["fecha"], "codigo": bulto["codigo"], "remito": bulto["remito"],
                "destino": destino, "precinto": bulto["precinto"], "unidades": unidades, "valor": valor, "obs": bulto["obs"],
            })
        return {"transito": por_local, "criticos": criticos, "rechazados": rechazados}
