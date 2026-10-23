"""Servidor del mock. Desde la raíz del proyecto: python -m ui.server"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

from ui.render import csv_comercial, csv_logistica, render
from ui.store import Store

ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"
SESSIONS = {}
HOME = {
    "ROL_OPERADOR_CD": "/cd/catalogo",
    "ROL_ENCARGADO_LOCAL": "/local/stock",
    "ROL_ADMIN_GERENCIAL": "/gerencia/comercial",
}
ZONA = (
    ("/cd", "ROL_OPERADOR_CD"),
    ("/local", "ROL_ENCARGADO_LOCAL"),
    ("/gerencia", "ROL_ADMIN_GERENCIAL"),
)


def zona_de(path):
    for prefijo, rol in ZONA:
        if path == prefijo or path.startswith(prefijo + "/"):
            return rol
    return None


def unicos(form):
    data = {clave: valores[0] for clave, valores in form.items()}
    data["rubros"] = form.get("rubros", [])
    return data


class Handler(BaseHTTPRequestHandler):
    def sesion(self):
        sid = ""
        raw = self.headers.get("Cookie", "")
        for parte in raw.split(";"):
            nombre, _, valor = parte.strip().partition("=")
            if nombre == "sid":
                sid = valor
        if sid in SESSIONS:
            return sid, SESSIONS[sid]
        sid = f"{len(SESSIONS) + 1:x}{id(self):x}"
        SESSIONS[sid] = {"rol": "ROL_OPERADOR_CD", "store": Store()}
        return sid, SESSIONS[sid]

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith("/static/"):
            self.archivo(parsed.path)
            return
        sid, ses = self.sesion()
        q = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        rol_ruta = zona_de(parsed.path.removesuffix(".csv"))
        if parsed.path in ("/", ""):
            self.redirect(HOME[ses["rol"]], sid)
            return
        if rol_ruta and rol_ruta != ses["rol"]:
            self.redirect(HOME[ses["rol"]], sid)
            return
        store = ses["store"]
        if q.get("keep") != "1":
            store.form_error = ""
            store.held = {}
        if "medio" in q:
            store.medio = q["medio"]
        if parsed.path == "/gerencia/comercial.csv":
            self.texto(csv_comercial(store, q), "text/csv; charset=utf-8", sid)
            return
        if parsed.path == "/gerencia/logistica.csv":
            self.texto(csv_logistica(store, q), "text/csv; charset=utf-8", sid)
            return
        html = render(ses["rol"], store, parsed.path, q)
        if html is None:
            self.texto("Página no encontrada", "text/plain; charset=utf-8", sid, 404)
            return
        self.texto(html, "text/html; charset=utf-8", sid)

    def do_POST(self):
        parsed = urlparse(self.path)
        sid, ses = self.sesion()
        largo = int(self.headers.get("Content-Length", "0") or 0)
        form = parse_qs(self.rfile.read(largo).decode("utf-8"), keep_blank_values=True)
        data = unicos(form)
        rol_ruta = zona_de(parsed.path)
        if parsed.path != "/sesion" and rol_ruta and rol_ruta != ses["rol"]:
            self.redirect(HOME[ses["rol"]], sid)
            return
        destino = self.accion(ses, parsed.path, data, form)
        self.redirect(destino, sid)

    def accion(self, ses, path, data, form):
        store = ses["store"]
        if path == "/sesion":
            rol = data.get("rol", "")
            if rol in HOME:
                ses["rol"] = rol
            return HOME[ses["rol"]]
        error = None
        volver = data.get("volver") or HOME[ses["rol"]]
        if path == "/cd/producto":
            error = store.guardar_producto({
                "sku": data.get("sku", ""),
                "barra": data.get("barra", ""),
                "nombre": data.get("nombre", ""),
                "categoria": data.get("categoria", ""),
                "proveedor": data.get("proveedor", ""),
                "costo": data.get("costo", ""),
                "precio": data.get("precio", ""),
                "minimos": {u["codigo"]: data.get(f"min_{u['codigo']}", "0") for u in store.ubicaciones},
            }, data.get("nuevo", "1") == "1")
            if error:
                store.form_error = error
                return self.fallo(store, data, f"{volver}?modal=producto&sku={quote(data.get('sku', ''))}")
            return volver
        if path == "/cd/proveedor":
            rubros = data.get("rubros", [])
            if isinstance(rubros, str):
                rubros = [rubros]
            error = store.guardar_proveedor({
                "cuit": data.get("cuit", ""),
                "razon": data.get("razon", ""),
                "tel": data.get("tel", ""),
                "email": data.get("email", ""),
                "rubros": rubros,
                "activo": "activo" in data,
                "cuit_original": data.get("cuit_original", ""),
            }, data.get("nuevo", "1") == "1")
            if error:
                store.form_error = error
                return self.fallo(store, data, f"{volver}?modal=proveedor&cuit={quote(data.get('cuit_original') or data.get('cuit', ''))}")
            return volver
        if path == "/cd/categoria":
            error = store.guardar_categoria(data.get("nombre", ""), data.get("descripcion", ""))
            if error:
                store.form_error = error
                return self.fallo(store, data, "/cd/proveedores")
            return "/cd/proveedores"
        if path == "/cd/sucursal":
            error = store.guardar_sucursal({
                "codigo": data.get("codigo", ""),
                "nombre": data.get("nombre", ""),
                "direccion": data.get("direccion", ""),
                "tel": data.get("tel", ""),
                "tipo": data.get("tipo", "LOCAL"),
                "caja": "caja" in data,
            })
            if error:
                store.form_error = error
                return self.fallo(store, data, f"/cd/sucursales?modal=sucursal&codigo={quote(data.get('codigo', ''))}")
            return "/cd/sucursales"
        if path == "/cd/datos":
            error = store.editar_cd(data.get("nombre", ""), data.get("direccion", ""), data.get("tel", ""))
            if error:
                store.form_error = error
                return self.fallo(store, data, "/cd/sucursales?modal=cd")
            return "/cd/sucursales"
        if path == "/cd/compra":
            lineas = list(zip(form.get("sku", []), form.get("qty", []), form.get("costo", [])))
            error = store.registrar_compra(data.get("cuit", ""), data.get("factura", ""), lineas)
            if error:
                store.form_error = error
                return self.fallo(store, data, "/cd/catalogo?modal=compra")
            return "/cd/catalogo"
        if path == "/cd/empaque/bulto":
            error = store.crear_bulto(data.get("orden", ""))
            destino = f"/cd/empaque?orden={quote(data.get('orden', ''))}"
            if error:
                store.form_error = error
                return self.fallo(store, data, destino)
            return destino
        if path == "/cd/empaque/asignar":
            error = store.asignar_a_bulto(data.get("bulto", ""), data.get("sku", ""), data.get("qty", ""))
            destino = f"/cd/empaque?orden={quote(data.get('orden', ''))}"
            if error:
                store.form_error = error
                return self.fallo(store, data, destino)
            return destino
        if path == "/cd/empaque/precinto":
            error = store.precintar(data.get("bulto", ""), data.get("precinto", ""))
            destino = f"/cd/empaque?orden={quote(data.get('orden', ''))}"
            if error:
                store.form_error = error
                return self.fallo(store, data, destino)
            return destino
        if path == "/cd/despacho":
            error = store.despachar(data.get("bulto", ""))
            if error:
                store.form_error = error
                return self.fallo(store, data, "/cd/despacho")
            return "/cd/despacho"
        if path == "/local/reposicion/agregar":
            error = store.agregar_draft(data.get("sku", ""))
            if error:
                store.form_error = error
                return self.fallo(store, data, "/local/reposicion")
            return "/local/reposicion"
        if path == "/local/reposicion/quitar":
            store.quitar_draft(data.get("sku", ""))
            return "/local/reposicion"
        if path == "/local/reposicion/confirmar":
            cantidades = {it["sku"]: data.get(f"qty_{it['sku']}", it["qty"]) for it in store.draft}
            error = store.confirmar_orden(cantidades)
            if error:
                store.form_error = error
                return self.fallo(store, data, "/local/reposicion")
            return "/local/reposicion"
        if path == "/local/recepcion/arribo":
            error = store.recibir(data.get("bulto", ""))
            destino = f"/local/recepcion?bulto={quote(data.get('bulto', ''))}"
            if error:
                store.form_error = error
                return self.fallo(store, data, destino)
            return destino
        if path == "/local/recepcion/verificar":
            error = store.verificar(data.get("bulto", ""))
            if error:
                store.form_error = error
                return self.fallo(store, data, f"/local/recepcion?bulto={quote(data.get('bulto', ''))}")
            return "/local/pos"
        if path == "/local/recepcion/rechazar":
            error = store.rechazar(data.get("bulto", ""), data.get("motivo", ""))
            if error:
                store.form_error = error
                return self.fallo(store, data, f"/local/recepcion?bulto={quote(data.get('bulto', ''))}")
            return "/local/recepcion"
        if path == "/local/pos/agregar":
            error = store.agregar_carrito(data.get("sku", ""), data.get("qty", ""))
            if error:
                store.form_error = error
                return self.fallo(store, data, f"/local/pos?medio={quote(data.get('medio', 'efectivo'))}")
            return f"/local/pos?medio={quote(data.get('medio', store.medio))}"
        if path == "/local/pos/qty":
            error = store.cambiar_carrito(data.get("sku", ""), data.get("qty", ""))
            if error:
                store.form_error = error
                return self.fallo(store, data, f"/local/pos?medio={quote(data.get('medio', 'efectivo'))}")
            return f"/local/pos?medio={quote(data.get('medio', store.medio))}"
        if path == "/local/pos/quitar":
            store.quitar_carrito(data.get("sku", ""))
            return "/local/pos"
        if path == "/local/pos/cobrar":
            error, nro = store.cobrar(data.get("medio", "efectivo"), data)
            if error:
                store.form_error = error
                return self.fallo(store, data, f"/local/pos?medio={quote(data.get('medio', 'efectivo'))}")
            return f"/local/pos?ticket={quote(nro)}"
        if path == "/local/devolucion/buscar":
            nro = data.get("nro", "").strip()
            venta = store.venta(nro)
            if not venta or venta["local"] != "LOC-01":
                store.venta_q = ""
                return self.fallo(store, data, "/local/devoluciones", "Comprobante no encontrado. No se admiten devoluciones sin venta registrada.")
            store.venta_q = nro
            store.form_error = ""
            return "/local/devoluciones"
        if path == "/local/devolucion/confirmar":
            cantidades = {}
            venta = store.venta(data.get("nro", ""))
            if venta:
                for it in venta["items"]:
                    cantidades[it["sku"]] = data.get(f"qty_{it['sku']}", "0")
            error = store.confirmar_devolucion(data.get("nro", ""), cantidades, data.get("motivo", ""))
            if error:
                store.venta_q = data.get("nro", "")
                store.form_error = error
                return self.fallo(store, data, "/local/devoluciones")
            return "/local/devoluciones"
        return HOME[ses["rol"]]

    def fallo(self, store, data, destino, mensaje=None):
        if mensaje:
            store.form_error = mensaje
        store.held = data
        separador = "&" if "?" in destino else "?"
        return f"{destino}{separador}keep=1"

    def redirect(self, destino, sid):
        self.send_response(303)
        self.send_header("Location", destino)
        self.send_header("Set-Cookie", f"sid={sid}; Path=/; HttpOnly; SameSite=Lax")
        self.end_headers()

    def texto(self, cuerpo, content_type, sid, status=200):
        raw = cuerpo.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Set-Cookie", f"sid={sid}; Path=/; HttpOnly; SameSite=Lax")
        self.end_headers()
        self.wfile.write(raw)

    def archivo(self, path):
        rel = path[len("/static/"):]
        destino = (STATIC / rel).resolve()
        if not str(destino).startswith(str(STATIC.resolve())) or not destino.is_file():
            self.send_error(404)
            return
        tipo = "image/svg+xml" if destino.suffix == ".svg" else "text/css; charset=utf-8"
        raw = destino.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, fmt, *args):
        return


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("LogiRetail mock en http://127.0.0.1:8000")
    server.serve_forever()


if __name__ == "__main__":
    main()
