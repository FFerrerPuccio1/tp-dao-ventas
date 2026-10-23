import html
from datetime import datetime

from ui.store import CD, LOCAL

MESES = "ene feb mar abr may jun jul ago sep oct nov dic".split()
ESTADO = {
    "PREPARADO": ("b-prep", "PREPARADO"),
    "PRECINTADO": ("b-prec", "PRECINTADO"),
    "EN_TRANSITO": ("b-trans", "EN TRÁNSITO"),
    "RECIBIDO": ("b-recib", "RECIBIDO"),
    "VERIFICADO": ("b-ok", "VERIFICADO"),
    "RECHAZADO": ("b-bad", "RECHAZADO"),
    "SOLICITADA": ("b-recib", "SOLICITADA"),
    "PROCESADA": ("b-prec", "PROCESADA"),
    "COMPLETADA": ("b-ok", "COMPLETADA"),
    "EMITIDO": ("b-prep", "EMITIDO"),
    "EN_TRANSITO_R": ("b-trans", "EN TRÁNSITO"),
    "PROCESADO_DESTINO": ("b-ok", "PROCESADO"),
    "ACTIVO": ("b-ok", "ACTIVO"),
    "OPERATIVO": ("b-ok", "OPERATIVO"),
}


def esc(value):
    return html.escape(str(value if value is not None else ""), quote=True)


def money(value):
    neg = float(value) < 0
    n = abs(float(value))
    ent = int(n)
    cen = int(round((n - ent) * 100))
    if cen == 100:
        ent += 1
        cen = 0
    txt = f"{ent:,}".replace(",", ".")
    return f"{'-' if neg else ''}${txt},{cen:02d}"


def miles(value):
    return f"{int(value):,}".replace(",", ".")


def dia(dt):
    return f"{dt.day} {MESES[dt.month - 1]} {dt.year}"


def cuando(dt):
    return dt.strftime("%d/%m/%Y %H:%M:%S")


def icon(name, w, h):
    return f'<img src="/static/icons/{name}.svg" width="{w}" height="{h}" alt="">'


def badge(estado):
    cls, label = ESTADO.get(estado, ("b-prep", estado))
    return f'<span class="badge {cls}"><i></i>{esc(label)}</span>'


def take_notice(store):
    msg = store.notice
    store.notice = ""
    return msg


def shell(rol, active, crumb, ctx, body, modal=""):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LogiRetail ERP</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;700&display=swap">
<link rel="stylesheet" href="/static/app.css">
</head>
<body>
<div class="app">
{sidebar(rol, active)}
<div class="work">
{topbar(rol, crumb, ctx)}
<div class="content">{body}</div>
</div>
</div>
{modal}
</body>
</html>"""


def sidebar(rol, active):
    if rol == "ROL_OPERADOR_CD":
        grupos = [
            ("ADMINISTRACIÓN Y ABASTECIMIENTO CD", [
                ("/cd/catalogo", "package-search", 20, 20, "Catálogo y Precios"),
                ("/cd/proveedores", "warehouse-nav", 20, 20, "Proveedores y Categorías"),
                ("/cd/sucursales", "clipboard", 20, 20, "Sucursales y CD"),
                ("/cd/stock", "barcode", 20, 20, "Stock por Ubicación y Mínimos"),
            ]),
            ("LOGÍSTICA DE SALIDA (CD CENTRAL)", [
                ("/cd/empaque", "package-check", 20, 20, "CD: Empaque y Precintado"),
                ("/cd/despacho", "truck", 20, 20, "CD: Despacho y Trazabilidad"),
            ]),
        ]
        avatar, who, pill, pill_cls = "CD", "Operador CD Central", "Rol: Logística CD • Nodo: CD-01", ""
    elif rol == "ROL_ENCARGADO_LOCAL":
        grupos = [
            ("INVENTARIO Y REPOSICIÓN DEL LOCAL", [
                ("/local/stock", "barcode", 20, 20, "Mi Stock y Faltantes"),
                ("/local/reposicion", "clipboard", 20, 20, "Solicitar Reposición al CD"),
                ("/local/recepcion", "package-check", 20, 20, "Recepción y Control de Precintos"),
            ]),
            ("OPERACIÓN COMERCIAL Y CAJA", [
                ("/local/pos", "package-search", 20, 20, "Punto de Venta (POS)"),
                ("/local/devoluciones", "sliders", 18, 18, "Devoluciones y Movimientos de Caja"),
            ]),
        ]
        avatar, who, pill, pill_cls = "L1", "Encargado Local 01", "Rol: Ventas y Recepción • Nodo: LOC-01 Centro", "local"
    else:
        grupos = [
            ("CONTROL GERENCIAL", [
                ("/gerencia/comercial", "sliders", 18, 18, "Reportes Comerciales y Margen"),
                ("/gerencia/logistica", "truck", 20, 20, "Reportes Logísticos y Mermas"),
                ("/gerencia/red", "warehouse-nav", 20, 20, "Vista Global de Sucursales y CD"),
            ]),
        ]
        avatar, who, pill, pill_cls = "GR", "Auditoría y Gerencia", "Rol: Auditoría • Nodo: TODAS", "ger"
    nav = []
    for titulo, items in grupos:
        nav.append(f'<p class="nav-label{" gap" if nav else ""}">{esc(titulo)}</p>')
        for href, nombre, w, h, label in items:
            cls = "active" if href == active else ""
            nav.append(f'<a class="{cls}" href="{href}">{icon(nombre, w, h)}<span>{esc(label)}</span></a>')
    opciones = [
        ("ROL_OPERADOR_CD", "Operador CD"),
        ("ROL_ENCARGADO_LOCAL", "Encargado LOC-01"),
        ("ROL_ADMIN_GERENCIAL", "Gerencia"),
    ]
    opts = "".join(
        f'<option value="{val}"{" selected" if val == rol else ""}>{esc(txt)}</option>'
        for val, txt in opciones
    )
    av_cls = "local" if pill_cls == "local" else "ger" if pill_cls == "ger" else ""
    return f"""<aside class="sidebar">
  <div class="brand"><div class="mark">{icon("boxes", 23, 23)}</div><div><strong>LogiRetail ERP</strong><span>CD &amp; Sucursales</span></div></div>
  <nav class="nav">{''.join(nav)}</nav>
  <div class="side-foot">
    <div class="online">{icon("dot", 6, 6)}<span>Sistema operativo · {esc(dia(datetime(2026, 10, 23)))}</span></div>
    <div class="user">
      <div class="avatar {av_cls}">{esc(avatar)}</div>
      <div><p class="who">{esc(who)}</p><p class="sub">Sesión autorizada</p></div>
      {icon("logout", 18, 18)}
    </div>
    <div class="role-pill {pill_cls}">{icon("dot-blue", 6, 6)}<span>{esc(pill)}</span></div>
    <form class="role-form" method="post" action="/sesion">
      <select name="rol" aria-label="Cambiar rol">{opts}</select>
      <button type="submit">Cambiar rol</button>
    </form>
  </div>
</aside>"""


def topbar(rol, crumb, ctx):
    if rol == "ROL_ENCARGADO_LOCAL":
        caja = f'<div class="caja-pill">Caja abierta: {esc(ctx["caja"])}</div>'
        pill = f'<div class="ctx local">{icon("warehouse", 18, 18)}<span>Operando en: Local 01 - Centro</span>{icon("chevron", 16, 16)}</div>'
    elif rol == "ROL_ADMIN_GERENCIAL":
        caja = ""
        pill = f'<div class="ctx ger">{icon("warehouse", 18, 18)}<span>Operando en: Todas las ubicaciones</span>{icon("chevron", 16, 16)}</div>'
    else:
        caja = ""
        pill = f'<div class="ctx">{icon("warehouse", 18, 18)}<span>Operando en: Centro de Distribución Central</span>{icon("chevron", 16, 16)}</div>'
    return f'<header class="topbar"><p class="crumb">{esc(crumb)}</p>{pill}{caja}{icon("bell", 18, 18)}</header>'


def notice_html(store):
    msg = take_notice(store)
    if not msg:
        return ""
    return f'<div class="banner ok">{esc(msg)}</div>'


def tabs(actual):
    items = [
        ("/cd/catalogo", "Productos y Precios"),
        ("/cd/stock", "Stock por Ubicación y Mínimos"),
        ("/cd/proveedores", "Proveedores y Categorías"),
        ("/cd/sucursales", "Sucursales y CD"),
    ]
    links = "".join(
        f'<a class="{"on" if href == actual else ""}" href="{href}">{esc(label)}</a>'
        for href, label in items
    )
    return f'<div class="tabs">{links}</div>'


def head(kicker, title, lead):
    return f'<p class="kicker">{esc(kicker)}</p><h1>{esc(title)}</h1><p class="lead">{esc(lead)}</p>'


def overlay(inner, drawer=False):
    cls = "overlay drawer-wrap" if drawer else "overlay"
    return f'<div class="{cls}">{inner}</div>'


def modal_box(title, sub, body, close, wide=False, ticket=False):
    cls = "modal" + (" wide" if wide else "") + (" ticket" if ticket else "")
    return f'<div class="{cls}"><div class="modal-h"><div><h2>{esc(title)}</h2><p class="subhead">{esc(sub)}</p></div><a href="{esc(close)}" aria-label="Cerrar">×</a></div>{body}</div>'


def page_catalogo(rol, store, q):
    texto = q.get("q", "")
    cat = q.get("cat", "")
    prov = q.get("prov", "")
    filas = store.filtrar_productos(texto, cat, prov)
    cats = "".join(f'<option value="{esc(c["id"])}"{" selected" if c["id"] == cat else ""}>{esc(c["nombre"])}</option>' for c in store.categorias)
    provs = "".join(f'<option value="{esc(p["cuit"])}"{" selected" if p["cuit"] == prov else ""}>{esc(p["razon"])}</option>' for p in store.proveedores)
    body_rows = []
    for p in filas:
        body_rows.append(f"""<tr>
          <td class="mono">{esc(p["sku"])}</td>
          <td>{esc(p["barra"])}</td>
          <td><strong>{esc(p["nombre"])}</strong></td>
          <td><span class="tag">{esc(store.cat_nombre(p["categoria"]))}</span></td>
          <td>{esc(store.prov_de(p["proveedor"]))}<span class="sub">CUIT {esc(p["proveedor"])}</span></td>
          <td class="mono right">{esc(money(p["costo"]))}</td>
          <td class="mono right"><strong>{esc(money(p["precio"]))}</strong></td>
          <td><div class="actions"><a href="/cd/catalogo?modal=producto&sku={esc(p["sku"])}">{icon("pen", 18, 18)}</a><a href="/cd/catalogo?modal=producto&sku={esc(p["sku"])}">{icon("sliders", 18, 18)}</a></div></td>
        </tr>""")
    n = len(filas)
    body = f"""{notice_html(store)}
    {head("Administración de ubicaciones · Procesos 1 y 2", "Catálogo y abastecimiento CD", "Administrá productos, precios y proveedores. El ingreso de compras se registra en el CD Central.")}
    {tabs("/cd/catalogo")}
    <form class="toolbar" method="get" action="/cd/catalogo">
      <label class="search">{icon("search", 16, 16)}<input name="q" value="{esc(texto)}" placeholder="Buscar por SKU, Código de Barras o Nombre..."></label>
      <label class="select"><select name="cat" onchange="this.form.submit()"><option value="">Todas las categorías</option>{cats}</select></label>
      <label class="select"><select name="prov" onchange="this.form.submit()"><option value="">Todos los proveedores</option>{provs}</select></label>
      <span class="grow"></span>
      <a class="btn" href="/cd/proveedores?modal=proveedor">{icon("plus", 17, 17)} Nuevo Proveedor</a>
      <button class="btn" type="submit">Filtrar</button>
      <a class="btn" href="/cd/catalogo?modal=compra">{icon("package-plus", 17, 17)} Registrar Compra/Ingreso en CD</a>
      <a class="btn primary" href="/cd/catalogo?modal=producto">{icon("plus", 17, 17)} Nuevo Producto</a>
    </form>
    <section class="card">
      <div class="card-h"><h2>Productos registrados</h2><p>{n} productos · Precios en pesos argentinos</p></div>
      <table>
        <thead><tr><th>SKU</th><th>CÓD. BARRAS</th><th>PRODUCTO</th><th>CATEGORÍA</th><th>PROVEEDOR HABITUAL</th><th class="right">COSTO UNIT.</th><th class="right">PRECIO VENTA</th><th>ACCIONES</th></tr></thead>
        <tbody>{''.join(body_rows)}</tbody>
      </table>
      <div class="pager"><span>Mostrando 1–{n} de {n} productos</span><span>Página 1 de 1</span></div>
    </section>
    <p class="hint">{icon("sliders", 18, 18)} Configurá el stock mínimo por local desde cada producto. Los cambios de costo y precio quedan registrados.</p>"""
    return shell(rol, "/cd/catalogo", "Administración / Catálogo y abastecimiento", {}, body, modales_cd(store, q, "/cd/catalogo"))


def page_proveedores(rol, store, q):
    texto = q.get("q", "").lower()
    cards = []
    for prov in store.proveedores:
        blob = f"{prov['cuit']} {prov['razon']}".lower()
        if texto and texto not in blob:
            continue
        rubros = "".join(f'<span class="tag">{esc(r)}</span>' for r in prov["rubros"])
        cards.append(f"""<tr>
          <td class="mono"><strong>{esc(prov["cuit"])}</strong></td>
          <td>{esc(prov["razon"])}</td>
          <td>{rubros}</td>
          <td>{esc(prov["email"])}<span class="sub">{esc(prov["tel"])}</span></td>
          <td>{store.productos_de(prov["cuit"])} productos</td>
          <td>{badge("ACTIVO")}<a href="/cd/proveedores?modal=proveedor&cuit={esc(prov["cuit"])}"> Editar</a></td>
        </tr>""")
    cats = []
    for cat in store.categorias:
        cats.append(f"""<div class="card" style="margin-bottom:12px;padding:12px">
          <strong>{esc(cat["id"])} · {esc(cat["nombre"])}</strong>
          <p class="note">{esc(cat["descripcion"])}</p>
          <span class="tag">{store.productos_cat(cat["id"])} productos</span>
        </div>""")
    err = f'<div class="banner bad">{esc(store.form_error)}</div>' if store.form_error else ""
    body = f"""{notice_html(store)}{err}
    {head("Administración de ubicaciones · Procesos 1 y 2", "Proveedores y categorías", "El CUIT identifica al proveedor y no se puede repetir.")}
    {tabs("/cd/proveedores")}
    <div class="split">
      <section class="card">
        <div class="card-h"><h2>Proveedores registrados ({len(store.proveedores)})</h2>
          <form method="get" action="/cd/proveedores"><label class="search">{icon("search", 16, 16)}<input name="q" value="{esc(q.get("q", ""))}" placeholder="Buscar por CUIT o Razón Social..."></label></form>
          <a class="btn primary" href="/cd/proveedores?modal=proveedor">{icon("plus", 17, 17)} Nuevo Proveedor</a>
        </div>
        <table>
          <thead><tr><th>CUIT</th><th>RAZÓN SOCIAL</th><th>RUBRO</th><th>CONTACTO</th><th>PROD.</th><th>ESTADO</th></tr></thead>
          <tbody>{''.join(cards)}</tbody>
        </table>
      </section>
      <section>
        <div class="card-h" style="padding-left:0"><h2>Categorías activas ({len(store.categorias)})</h2></div>
        {''.join(cats)}
        <form method="post" action="/cd/categoria" class="card" style="padding:12px">
          <div class="field"><label>NUEVA CATEGORÍA</label><input name="nombre" required placeholder="Nombre"></div>
          <div class="field"><label>DESCRIPCIÓN</label><input name="descripcion" placeholder="Descripción"></div>
          <button class="btn" type="submit">+ Nueva Categoría</button>
        </form>
      </section>
    </div>"""
    return shell(rol, "/cd/proveedores", "Administración / Catálogo y abastecimiento", {}, body, modales_cd(store, q, "/cd/proveedores"))


def page_stock(rol, store, q):
    rows = []
    for p in store.productos:
        celdas = []
        for cod in (CD, "LOC-01", "LOC-02", "LOC-03"):
            fila = store.st(cod, p["sku"])
            rojo = ' class="bad"' if fila["disp"] <= fila["minimo"] and cod != CD else ""
            extra = ""
            if fila["cuarentena"]:
                extra = f'<span class="sub">+{fila["cuarentena"]} u. en cuarentena</span>'
            celdas.append(f'<td{rojo}>{fila["disp"]} u. / Mín {fila["minimo"]}{extra}</td>')
        transito = sum(store.st(cod, p["sku"])["transito"] for cod in (CD, "LOC-01", "LOC-02", "LOC-03"))
        retenido = sum(store.st(cod, p["sku"])["rechazada"] for cod in ("LOC-01", "LOC-02", "LOC-03"))
        rows.append(f"""<tr>
          <td><span class="mono">{esc(p["sku"])}</span><span class="sub">{esc(p["nombre"])}</span></td>
          {''.join(celdas)}
          <td>{transito} u.</td>
          <td>{retenido} u.</td>
          <td><a href="/cd/catalogo?modal=producto&sku={esc(p["sku"])}">Ajustar mínimos</a></td>
        </tr>""")
    body = f"""{notice_html(store)}
    {head("Administración de ubicaciones · Procesos 1 y 2", "Stock por ubicación y mínimos", "Disponible, en tránsito y retenido por precinto roto. El disponible del local es lo único vendible.")}
    {tabs("/cd/stock")}
    <section class="card"><table>
      <thead><tr><th>SKU / PRODUCTO</th><th>CD-01 DISP.</th><th>LOC-01</th><th>LOC-02</th><th>LOC-03</th><th>EN TRÁNSITO</th><th>RETENIDO</th><th></th></tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table></section>"""
    return shell(rol, "/cd/stock", "Administración / Stock", {}, body, modales_cd(store, q, "/cd/stock"))


def page_sucursales(rol, store, q, editable=True):
    cd = store.ubicacion(CD)
    locales = [u for u in store.ubicaciones if u["tipo"] == "LOCAL"]
    transito = sum(1 for b in store.bultos if b["estado"] == "EN_TRANSITO")
    rows = []
    for u in locales:
        bajo = store.bajo_minimo(u["codigo"])
        marca = f'{bajo} bajo mínimo' if bajo else "0 bajo mínimo"
        acciones = ""
        if editable:
            acciones = f'<a href="/cd/sucursales?modal=sucursal&codigo={esc(u["codigo"])}">Editar</a>'
        caja = money(u["caja"]) if u["caja_abierta"] else "Sin caja"
        rows.append(f"""<tr>
          <td class="mono">{esc(u["codigo"])}</td>
          <td><strong>{esc(u["nombre"])}</strong></td>
          <td><span class="tag">LOCAL MINORISTA</span></td>
          <td>{esc(u["direccion"])}<span class="sub">{esc(u["tel"])}</span></td>
          <td>{"Caja abierta" if u["caja_abierta"] else "Caja cerrada"} ({esc(caja)})</td>
          <td>{miles(store.unidades_local(u["codigo"]))} u. ({esc(marca)})</td>
          <td>{badge("OPERATIVO")} {acciones}</td>
        </tr>""")
    boton = f'<a class="btn primary" href="/cd/sucursales?modal=sucursal">{icon("plus", 17, 17)} Nueva Sucursal / Local</a>' if editable else ""
    editar_cd = '<a class="btn" href="/cd/sucursales?modal=cd">Editar Datos CD</a>' if editable else ""
    body = f"""{notice_html(store)}
    {head("Administración de ubicaciones · Proceso 1", "Red logística: Centro de Distribución y sucursales", "Administrá el nodo central de abastecimiento y los locales comerciales habilitados para operar.")}
    {tabs("/cd/sucursales") if editable else ""}
    <div class="toolbar"><span class="grow"></span>{boton}</div>
    <section class="hub">
      <div class="meta">
        {badge("ACTIVO")}
        <h2 style="margin-top:8px">{esc(cd["codigo"])} · {esc(cd["nombre"])}</h2>
        <p class="note">{esc(cd["direccion"])}</p>
      </div>
      <div><span class="note">Stock total en CD</span><strong>{esc(miles(store.stock_cd()))} u.</strong></div>
      <div><span class="note">Locales abastecidos</span><strong>{len(locales)} sucursales</strong></div>
      <div><span class="note">Bultos en tránsito</span><strong>{transito}</strong></div>
      {editar_cd}
    </section>
    <section class="card"><table>
      <thead><tr><th>CÓDIGO</th><th>NOMBRE</th><th>TIPO</th><th>DIRECCIÓN</th><th>CAJA Y POS</th><th>STOCK VERIFICADO</th><th>ESTADO</th></tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table></section>"""
    active = "/gerencia/red" if not editable else "/cd/sucursales"
    crumb = "Gerencia / Red" if not editable else "Administración / Sucursales y CD"
    modal = modales_cd(store, q, "/cd/sucursales") if editable else ""
    return shell(rol, active, crumb, {}, body, modal)


def page_empaque(rol, store, q):
    abiertas = [o for o in store.ordenes if o["estado"] == "SOLICITADA"]
    nro = q.get("orden") or (abiertas[0]["nro"] if abiertas else "")
    orden = store.orden(nro) if nro else None
    if not orden:
        cuerpo = '<p class="note">No hay órdenes solicitadas. Cuando un local confirme una reposición, aparece acá.</p>'
    else:
        remito = next((r for r in store.remitos if r["orden"] == orden["nro"]), None)
        opciones = "".join(f'<option value="{esc(o["nro"])}"{" selected" if o["nro"] == orden["nro"] else ""}>{esc(o["nro"])} → {esc(o["destino"])}</option>' for o in abiertas)
        pend = []
        for it in orden["items"]:
            hecho = store.empaquetado(orden["nro"], it["sku"])
            queda = it["qty"] - hecho
            bultos_prep = [b for b in store.bultos if b["orden"] == orden["nro"] and b["estado"] == "PREPARADO"]
            opts = "".join(f'<option value="{esc(b["codigo"])}">{esc(b["codigo"])}</option>' for b in bultos_prep)
            accion = "Creá un bulto para asignar" if not bultos_prep else ""
            form = ""
            if queda > 0 and bultos_prep:
                form = f"""<form method="post" action="/cd/empaque/asignar">
                  <input type="hidden" name="orden" value="{esc(orden["nro"])}">
                  <input type="hidden" name="sku" value="{esc(it["sku"])}">
                  <input class="qty" name="qty" type="number" min="1" max="{queda}" value="{queda}">
                  <select name="bulto">{opts}</select>
                  <button class="btn" type="submit">Asignar a bulto</button>
                </form>"""
            prod = store.producto(it["sku"])
            pend.append(f"""<tr>
              <td class="mono">{esc(it["sku"])}</td><td>{esc(prod["nombre"])}</td>
              <td>{store.st(CD, it["sku"])["disp"]} u.</td><td>{it["qty"]}</td><td>{hecho}</td>
              <td class="{"bad" if queda else ""}">{queda}</td><td>{form}{esc(accion)}</td>
            </tr>""")
        tarjetas = []
        for bulto in [b for b in store.bultos if b["orden"] == orden["nro"]]:
            items = "".join(
                f'<tr><td class="mono">{esc(it["sku"])}</td><td>{esc(store.producto(it["sku"])["nombre"])}</td><td>{it["qty"]} u.</td></tr>'
                for it in bulto["items"]
            ) or "<tr><td colspan='3'>Sin productos todavía.</td></tr>"
            extra = ""
            if bulto["estado"] == "PREPARADO":
                extra = f"""<form class="seal" method="post" action="/cd/empaque/precinto">
                  <input type="hidden" name="orden" value="{esc(orden["nro"])}">
                  <input type="hidden" name="bulto" value="{esc(bulto["codigo"])}">
                  <label>Nro. de precinto de seguridad</label>
                  <input name="precinto" placeholder="PREC-884920" required>
                  <button class="btn violet" type="submit">Colocar precinto y cerrar bulto</button>
                </form>"""
            elif bulto["precinto"]:
                extra = f'<p class="note">Precinto asignado: <span class="mono">{esc(bulto["precinto"])}</span></p>'
            tarjetas.append(f"""<article class="bulto"><header><strong>{esc(bulto["codigo"])}</strong>{badge(bulto["estado"])}</header>
              <table><thead><tr><th>SKU</th><th>PRODUCTO</th><th>CANT.</th></tr></thead><tbody>{items}</tbody></table>
              {extra}</article>""")
        nro_remito = remito["nro"] if remito else "se genera con el primer bulto"
        cuerpo = f"""<form class="toolbar" method="get" action="/cd/empaque">
          <label>Atendiendo orden <select name="orden" onchange="this.form.submit()">{opciones}</select></label>
          <span>Destino: {esc(store.ubicacion(orden["destino"])["nombre"])}</span>
          <span>Remito: <span class="mono">{esc(nro_remito)}</span></span>
          <span class="grow"></span>
        </form>
        <form method="post" action="/cd/empaque/bulto"><input type="hidden" name="orden" value="{esc(orden["nro"])}"><button class="btn primary" type="submit">+ Crear nuevo bulto</button></form>
        <div class="split-3">
          <section class="card"><div class="card-h"><h2>Mercadería pendiente de empaquetar</h2></div>
            <table><thead><tr><th>SKU</th><th>PRODUCTO</th><th>STOCK CD</th><th>PEDIDA</th><th>EMPAQUETADA</th><th>PENDIENTE</th><th></th></tr></thead>
            <tbody>{''.join(pend)}</tbody></table>
          </section>
          <section><h2>Bultos del remito</h2>{''.join(tarjetas) or '<p class="note">Todavía no hay bultos.</p>'}</section>
        </div>"""
    err = f'<div class="banner bad">{esc(store.form_error)}</div>' if store.form_error else ""
    body = f"""{notice_html(store)}{err}
    {head("Logística de salida · Proceso 4", "Empaque y precintado", "El bulto nace Preparado. Sin precinto no se puede despachar.")}
    {cuerpo}"""
    return shell(rol, "/cd/empaque", "Logística / Empaque y precintado", {}, body)


def page_despacho(rol, store, q):
    prec = sum(1 for b in store.bultos if b["estado"] == "PRECINTADO")
    trans = sum(1 for b in store.bultos if b["estado"] == "EN_TRANSITO")
    hoy = sum(1 for r in store.remitos if r["estado"] == "EN_TRANSITO")
    rows = []
    for bulto in store.bultos:
        if bulto["estado"] not in ("PREPARADO", "PRECINTADO", "EN_TRANSITO"):
            continue
        destino = next(r["destino"] for r in store.remitos if r["nro"] == bulto["remito"])
        unidades = sum(it["qty"] for it in bulto["items"])
        ultimo = bulto["historial"][-1]
        if bulto["estado"] == "PRECINTADO":
            accion = f"""<form method="post" action="/cd/despacho"><input type="hidden" name="bulto" value="{esc(bulto["codigo"])}"><button class="btn primary" type="submit">Registrar despacho</button></form>"""
        elif bulto["estado"] == "PREPARADO":
            accion = '<button class="btn" type="button" disabled>Falta precintar</button>'
        else:
            accion = ""
        rows.append(f"""<tr>
          <td class="mono">{esc(bulto["codigo"])}</td>
          <td class="mono">{esc(bulto["remito"])}</td>
          <td>CD-01 → {esc(destino)}</td>
          <td class="mono">{esc(bulto["precinto"] or "—")}</td>
          <td>{unidades} u.</td>
          <td>{badge(bulto["estado"])}</td>
          <td>{esc(cuando(ultimo["fecha"]))}</td>
          <td>{accion} <a href="/cd/despacho?modal=traza&bulto={esc(bulto["codigo"])}">Ver trazabilidad</a></td>
        </tr>""")
    err = f'<div class="banner bad">{esc(store.form_error)}</div>' if store.form_error else ""
    body = f"""{notice_html(store)}{err}
    {head("Logística de salida · Proceso 5", "Despacho y trazabilidad", "Solo sale del CD un bulto precintado. El historial de estados no se edita.")}
    <div class="kpis three">
      <div class="kpi"><span>Precintados listos</span><strong>{prec}</strong></div>
      <div class="kpi"><span>En tránsito</span><strong>{trans}</strong></div>
      <div class="kpi"><span>Remitos en tránsito</span><strong>{hoy}</strong></div>
    </div>
    <section class="card"><table>
      <thead><tr><th>BULTO</th><th>REMITO</th><th>ORIGEN → DESTINO</th><th>PRECINTO</th><th>UNIDADES</th><th>ESTADO</th><th>ÚLTIMO MOVIMIENTO</th><th>ACCIONES</th></tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table></section>"""
    modal = ""
    if q.get("modal") == "traza":
        bulto = store.bulto(q.get("bulto", ""))
        if bulto:
            items = "".join(
                f'<li><span class="muted">{esc(cuando(h["fecha"]))}</span><strong>{esc(ESTADO.get(h["nuevo"], ("", h["nuevo"]))[1])}</strong><span>{esc(h["obs"])}</span><span class="sub">{esc(h["usuario"])}</span></li>'
                for h in bulto["historial"]
            )
            modal = overlay(f"""<aside class="drawer">
              <div class="modal-h"><h2>{esc(bulto["codigo"])}</h2><a href="/cd/despacho">×</a></div>
              <p class="subhead">Trazabilidad inmutable del bulto. Solo lectura.</p>
              <ul class="timeline">{items}</ul>
              <p class="note">Registro de auditoría inmutable (solo lectura).</p>
            </aside>""", drawer=True)
    return shell(rol, "/cd/despacho", "Logística / Despacho", {}, body, modal)


def page_local_stock(rol, store, q):
    solo = q.get("faltantes", "1") == "1"
    rows = []
    for p in store.productos:
        fila = store.st(LOCAL, p["sku"])
        bajo = fila["disp"] <= fila["minimo"]
        if solo and not bajo:
            continue
        rows.append(f"""<tr>
          <td class="mono">{esc(p["sku"])}</td><td>{esc(p["nombre"])}</td>
          <td class="{"bad" if bajo else ""}">{fila["disp"]} u.</td>
          <td>{fila["transito"]} u.</td><td>{fila["cuarentena"]} u.</td><td>{fila["minimo"]} u.</td>
          <td>{max(fila["minimo"] - fila["disp"], 0)} u.</td>
        </tr>""")
    toggle = "0" if solo else "1"
    body = f"""{notice_html(store)}
    {head("Inventario del local · LOC-01", "Mi stock y faltantes", "El stock en tránsito o en cuarentena no se puede vender.")}
    <p><a class="btn" href="/local/stock?faltantes={toggle}">{"Ver todo el catálogo" if solo else "Mostrar solo bajo mínimo"}</a></p>
    <section class="card"><table>
      <thead><tr><th>SKU</th><th>PRODUCTO</th><th>DISPONIBLE</th><th>EN TRÁNSITO</th><th>CUARENTENA</th><th>MÍNIMO</th><th>SUGERIDO</th></tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table></section>"""
    ctx = {"caja": money(store.ubicacion(LOCAL)["caja"])}
    return shell(rol, "/local/stock", "Local 01 / Stock", ctx, body)


def page_reposicion(rol, store, q):
    solo = q.get("faltantes", "1") == "1"
    rows = []
    for p in store.productos:
        fila = store.st(LOCAL, p["sku"])
        bajo = fila["disp"] <= fila["minimo"]
        if solo and not bajo:
            continue
        sugerida = max(fila["minimo"] - fila["disp"], 1 if bajo else 0)
        rows.append(f"""<tr>
          <td class="mono">{esc(p["sku"])}</td><td>{esc(p["nombre"])}</td>
          <td class="{"bad" if bajo else ""}">{fila["disp"]} u.</td>
          <td>{fila["transito"]} u.</td><td>{fila["minimo"]} u.</td><td>{sugerida} u.</td>
          <td><form method="post" action="/local/reposicion/agregar"><input type="hidden" name="sku" value="{esc(p["sku"])}"><button class="btn" type="submit">+ Agregar</button></form></td>
        </tr>""")
    lineas = []
    unidades = 0
    for it in store.draft:
        prod = store.producto(it["sku"])
        unidades += it["qty"]
        lineas.append(f"""<div class="toolbar">
          <span>{esc(prod["nombre"])}</span>
          <input class="qty" form="confirmar" name="qty_{esc(it["sku"])}" type="number" min="1" value="{it["qty"]}">
          <button class="icon-btn" form="quitar-{esc(it["sku"])}" type="submit" aria-label="Quitar">×</button>
        </div>
        <form id="quitar-{esc(it["sku"])}" method="post" action="/local/reposicion/quitar"><input type="hidden" name="sku" value="{esc(it["sku"])}"></form>""")
    err = f'<div class="banner bad">{esc(store.form_error)}</div>' if store.form_error else ""
    toggle = "0" if solo else "1"
    ctx = {"caja": money(store.ubicacion(LOCAL)["caja"])}
    body = f"""{notice_html(store)}{err}
    {head("Reposición · Proceso 3", "Solicitar reposición al CD", "Origen CD-01. Destino fijo: LOC-01 Sucursal Centro.")}
    <div class="split">
      <section class="card">
        <div class="card-h"><h2>Estado de stock del local</h2>
          <a class="btn" href="/local/reposicion?faltantes={toggle}">{"Ver todo" if solo else "Solo bajo mínimo"}</a>
        </div>
        <table><thead><tr><th>SKU</th><th>PRODUCTO</th><th>DISPONIBLE</th><th>TRÁNSITO</th><th>MÍNIMO</th><th>SUGERIDA</th><th></th></tr></thead>
        <tbody>{''.join(rows)}</tbody></table>
      </section>
      <div class="order">
        <h2>Orden de reposición en curso</h2>
        <p class="note">Desde CD Central hacia Local 01 - Centro · {esc(dia(datetime(2026, 10, 23)))}</p>
        {''.join(lineas) or '<p class="note">Todavía no agregaste productos.</p>'}
        <p>{len(store.draft)} productos · {unidades} u. en el borrador</p>
        <button class="btn primary block" type="submit" form="confirmar">Confirmar y enviar orden al CD</button>
      </div>
      <form id="confirmar" method="post" action="/local/reposicion/confirmar"></form>
    </div>"""
    return shell(rol, "/local/reposicion", "Local 01 / Reposición", ctx, body)


def page_recepcion(rol, store, q):
    foco = q.get("bulto", "")
    rows = []
    for bulto in store.bultos:
        destino = next(r["destino"] for r in store.remitos if r["nro"] == bulto["remito"])
        if destino != LOCAL or bulto["estado"] not in ("EN_TRANSITO", "RECIBIDO", "VERIFICADO", "RECHAZADO"):
            continue
        if bulto["estado"] == "EN_TRANSITO":
            accion = f"""<form method="post" action="/local/recepcion/arribo"><input type="hidden" name="bulto" value="{esc(bulto["codigo"])}"><button class="btn" type="submit">1. Marcar arribo físico</button></form>"""
        elif bulto["estado"] == "RECIBIDO":
            accion = f'<a class="btn" href="/local/recepcion?bulto={esc(bulto["codigo"])}">2. Inspeccionar precinto</a>'
        else:
            accion = ""
        rows.append(f"""<tr>
          <td class="mono">{esc(bulto["codigo"])}</td><td class="mono">{esc(bulto["remito"])}</td>
          <td class="mono">{esc(bulto["precinto"] or "—")}</td><td>{badge(bulto["estado"])}</td><td>{accion}</td>
        </tr>""")
    panel = ""
    elegido = store.bulto(foco) if foco else None
    if elegido and elegido["estado"] == "RECIBIDO":
        contenido = "".join(
            f'<li>{it["qty"]} u. {esc(store.producto(it["sku"])["nombre"])}</li>' for it in elegido["items"]
        )
        unidades = sum(it["qty"] for it in elegido["items"])
        panel = f"""<section class="split">
          <div class="card" style="padding:16px">
            <h2>Precinto esperado: <span class="mono">{esc(elegido["precinto"])}</span></h2>
            <ul>{contenido}</ul>
            <div class="banner info">Estas {unidades} u. todavía no suman al stock vendible de Local 01.</div>
          </div>
          <div>
            <form class="choice good on" method="post" action="/local/recepcion/verificar" style="margin-bottom:12px">
              <input type="hidden" name="bulto" value="{esc(elegido["codigo"])}">
              <strong>Precinto íntegro y coincidente</strong>
              <p class="note">El precinto no presenta signos de violación y el contenido coincide.</p>
              <button class="btn green" type="submit">Confirmar VERIFICADO (+{unidades} u. a stock)</button>
            </form>
            <form class="choice bad on" method="post" action="/local/recepcion/rechazar">
              <input type="hidden" name="bulto" value="{esc(elegido["codigo"])}">
              <strong>Precinto violado, roto o adulterado</strong>
              <p class="note">Bloquea el ingreso a stock vendible y registra la merma.</p>
              <textarea name="motivo" required placeholder="Motivo del daño en el precinto"></textarea>
              <button class="btn danger" type="submit">Declarar RECHAZADO</button>
            </form>
          </div>
        </section>"""
    err = f'<div class="banner bad">{esc(store.form_error)}</div>' if store.form_error else ""
    ctx = {"caja": money(store.ubicacion(LOCAL)["caja"])}
    body = f"""{notice_html(store)}{err}
    {head("Recepción · Proceso 6", "Recepción y control de precintos", "Hasta verificar el precinto, la mercadería no está disponible para la venta.")}
    <section class="card"><table>
      <thead><tr><th>BULTO</th><th>REMITO</th><th>PRECINTO</th><th>ESTADO</th><th></th></tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table></section>
    {panel}"""
    return shell(rol, "/local/recepcion", "Local 01 / Recepción", ctx, body)


def page_pos(rol, store, q):
    texto = q.get("q", "").strip()
    medio = q.get("medio") or store.medio
    hits = []
    if texto:
        hits = store.filtrar_productos(texto)[:5]
    resultados = []
    for p in hits:
        fila = store.st(LOCAL, p["sku"])
        resultados.append(f"""<form class="toolbar" method="post" action="/local/pos/agregar">
          <input type="hidden" name="sku" value="{esc(p["sku"])}">
          <input type="hidden" name="medio" value="{esc(medio)}">
          <span><strong>{esc(p["sku"])}</strong> {esc(p["nombre"])} · {esc(money(p["precio"]))}</span>
          <span class="ok">Stock verificado: {fila["disp"]} u.</span>
          <span class="muted">En recepción sin verificar: {fila["cuarentena"]} u.</span>
          <input class="qty" name="qty" type="number" min="1" value="1">
          <button class="btn" type="submit">+ Agregar al ticket</button>
        </form>""")
    carrito = []
    for it in store.cart:
        prod = store.producto(it["sku"])
        carrito.append(f"""<tr>
          <td class="mono">{esc(it["sku"])}</td><td>{esc(prod["nombre"])}</td>
          <td class="mono">{esc(money(prod["precio"]))}</td>
          <td>
            <form method="post" action="/local/pos/qty">
              <input type="hidden" name="sku" value="{esc(it["sku"])}"><input type="hidden" name="medio" value="{esc(medio)}">
              <input class="qty" name="qty" type="number" min="0" value="{it["qty"]}">
              <button class="btn" type="submit">Actualizar</button>
            </form>
          </td>
          <td class="mono">{esc(money(prod["precio"] * it["qty"]))}</td>
          <td><form method="post" action="/local/pos/quitar"><input type="hidden" name="sku" value="{esc(it["sku"])}"><button class="icon-btn" type="submit">×</button></form></td>
        </tr>""")
    total = store.total_carrito()
    medios = [("efectivo", "Efectivo"), ("debito", "Tarjeta débito"), ("credito", "Tarjeta crédito"), ("qr", "QR / Transferencia")]
    pay = "".join(
        f'<a class="{"on" if medio == val else ""}" href="/local/pos?medio={val}">{esc(label)}</a>'
        for val, label in medios
    )
    if medio == "efectivo":
        extra = f"""<div class="field"><label>PAGA CON ($)</label><input name="paga_con" inputmode="decimal" value="{esc(store.held.get("paga_con", ""))}" required></div>"""
    elif medio == "qr":
        extra = '<div class="field"><label>IDENTIFICADOR DE TRANSFERENCIA</label><input name="tx" required></div>'
    else:
        extra = """<div class="grid-2"><div class="field"><label>NRO. DE CUPÓN</label><input name="cupon" required></div>
          <div class="field"><label>ÚLTIMOS 4</label><input name="ultimos" maxlength="4" required></div></div>"""
    err = f'<div class="banner bad">{esc(store.form_error)}</div>' if store.form_error else ""
    ctx = {"caja": money(store.ubicacion(LOCAL)["caja"])}
    unidades = sum(it["qty"] for it in store.cart)
    body = f"""{notice_html(store)}{err}
    {head("Punto de venta · Proceso 7A", "Cobro y comprobante", "Solo se vende el stock disponible ya verificado de Local 01.")}
    <div class="split">
      <section>
        <form class="toolbar" method="get" action="/local/pos">
          <input type="hidden" name="medio" value="{esc(medio)}">
          <label class="search">{icon("search", 16, 16)}<input name="q" value="{esc(texto)}" placeholder="Escanear código de barras o buscar SKU / nombre..."></label>
          <button class="btn" type="submit">Buscar</button>
        </form>
        {''.join(resultados)}
        <section class="card" style="margin-top:12px"><table>
          <thead><tr><th>SKU</th><th>DESCRIPCIÓN</th><th>PRECIO</th><th>CANTIDAD</th><th>SUBTOTAL</th><th></th></tr></thead>
          <tbody>{''.join(carrito) or '<tr><td colspan="6">El ticket está vacío.</td></tr>'}</tbody>
        </table></section>
      </section>
      <form class="card" style="padding:16px" method="post" action="/local/pos/cobrar">
        <input type="hidden" name="medio" value="{esc(medio)}">
        <p class="note">{unidades} unidades</p>
        <p class="note">TOTAL A COBRAR</p>
        <p class="total">{esc(money(total))}</p>
        <div class="pay">{pay}</div>
        {extra}
        <button class="btn green block" type="submit">Cobrar y emitir comprobante ({esc(money(total))})</button>
      </form>
    </div>"""
    modal = ""
    nro = q.get("ticket")
    venta = store.venta(nro) if nro else None
    if venta:
        lineas = "".join(
            f'<tr><td>{esc(store.producto(it["sku"])["nombre"])}</td><td>{it["qty"]}</td><td class="mono">{esc(money(it["precio"] * it["qty"]))}</td></tr>'
            for it in venta["items"]
        )
        modal = overlay(modal_box(
            f"Comprobante {venta['nro']}",
            f"{cuando(venta['fecha'])} · Local 01 - Centro",
            f"""<table><tbody>{lineas}</tbody></table>
            <p class="total">{esc(money(venta["total"]))}</p>
            <p>Medio: {esc(venta["medio"])}</p>
            <p class="note">{esc(venta["ref"])}</p>
            <p class="note">Stock descontado. Ingreso registrado en caja.</p>
            <div class="modal-f"><a class="btn primary" href="/local/pos">Nueva venta</a></div>""",
            "/local/pos",
            ticket=True,
        ))
    return shell(rol, "/local/pos", "Local 01 / Punto de venta", ctx, body, modal)


def page_devoluciones(rol, store, q):
    venta = store.venta(store.venta_q) if store.venta_q else None
    detalle = ""
    if venta:
        filas = []
        for it in venta["items"]:
            pend = it["qty"] - it["devuelta"]
            filas.append(f"""<tr>
              <td>{esc(store.producto(it["sku"])["nombre"])}</td>
              <td class="mono">{esc(money(it["precio"]))}</td>
              <td>{it["qty"]} u.</td><td>{it["devuelta"]} u.</td><td>{pend} u.</td>
              <td><input class="qty" name="qty_{esc(it["sku"])}" type="number" min="0" max="{pend}" value="0"></td>
            </tr>""")
        detalle = f"""<form method="post" action="/local/devolucion/confirmar">
          <input type="hidden" name="nro" value="{esc(venta["nro"])}">
          <p>Comprobante {esc(venta["nro"])} · {esc(cuando(venta["fecha"]))} · plazo vigente</p>
          <table><thead><tr><th>PRODUCTO</th><th>PRECIO</th><th>COMPRADA</th><th>YA DEVUELTA</th><th>MÁXIMO</th><th>DEVOLVER</th></tr></thead>
          <tbody>{''.join(filas)}</tbody></table>
          <div class="field"><label>MOTIVO</label><input name="motivo" required placeholder="Motivo de la devolución"></div>
          <button class="btn primary" type="submit">Confirmar devolución</button>
        </form>"""
    movs = []
    for mov in sorted(store.movimientos, key=lambda m: m["fecha"], reverse=True):
        if mov["local"] != LOCAL:
            continue
        cls = "bad" if mov["monto"] < 0 else "ok"
        tipo = "EGRESO POR DEVOLUCIÓN" if mov["tipo"] == "EGRESO_DEVOLUCION" else "INGRESO POR VENTA"
        movs.append(f"""<tr>
          <td>{esc(cuando(mov["fecha"]))}</td><td>{tipo}</td><td>{esc(mov["ref"])}</td>
          <td>{esc(mov["medio"])}</td><td class="{cls} mono">{esc(money(mov["monto"]))}</td>
        </tr>""")
    err = f'<div class="banner bad">{esc(store.form_error)}</div>' if store.form_error else ""
    ctx = {"caja": money(store.ubicacion(LOCAL)["caja"])}
    body = f"""{notice_html(store)}{err}
    {head("Caja del local · Proceso 7B", "Devoluciones y movimientos de caja", "Toda devolución tiene que corresponder a un comprobante de este local, dentro de los 30 días.")}
    <section class="card" style="padding:16px">
      <h2>Registrar devolución vinculada a un comprobante</h2>
      <form class="toolbar" method="post" action="/local/devolucion/buscar">
        <input name="nro" value="{esc(store.venta_q)}" placeholder="TCK-LOC01-000451" required>
        <button class="btn" type="submit">Buscar venta</button>
      </form>
      {detalle}
    </section>
    <section class="card">
      <div class="card-h"><h2>Movimientos de caja · Local 01</h2><p>Saldo {esc(money(store.ubicacion(LOCAL)["caja"]))}</p></div>
      <table><thead><tr><th>FECHA</th><th>TIPO</th><th>REFERENCIA</th><th>MEDIO</th><th>MONTO</th></tr></thead>
      <tbody>{''.join(movs)}</tbody></table>
    </section>"""
    return shell(rol, "/local/devoluciones", "Local 01 / Devoluciones", ctx, body)


def _filtros(accion, q):
    return f"""<form class="toolbar" method="get" action="{accion}">
      <label>Desde <input name="desde" value="{esc(q.get("desde", "01/10/2026"))}" placeholder="dd/mm/aaaa"></label>
      <label>Hasta <input name="hasta" value="{esc(q.get("hasta", "23/10/2026"))}" placeholder="dd/mm/aaaa"></label>
      <label>Ubicación <select name="ubi">
        <option value="">Todos los locales</option>
        <option value="LOC-01"{" selected" if q.get("ubi") == "LOC-01" else ""}>LOC-01</option>
        <option value="LOC-02"{" selected" if q.get("ubi") == "LOC-02" else ""}>LOC-02</option>
        <option value="LOC-03"{" selected" if q.get("ubi") == "LOC-03" else ""}>LOC-03</option>
      </select></label>
      <button class="btn" type="submit">Actualizar reporte</button>
      <a class="btn" href="{accion}.csv?desde={esc(q.get("desde", "01/10/2026"))}&hasta={esc(q.get("hasta", "23/10/2026"))}&ubi={esc(q.get("ubi", ""))}">Exportar CSV</a>
    </form>"""


def page_comercial(rol, store, q):
    desde, hasta = _rango(q)
    rep = store.reporte_comercial(desde, hasta, q.get("ubi", ""), "")
    pct = (rep["margen"] / rep["ingresos"] * 100) if rep["ingresos"] else 0
    filas = []
    for i, fila in enumerate(rep["ranking"], start=1):
        ancho = max(0, min(100, int(fila["margen"])))
        filas.append(f"""<tr>
          <td>#{i}</td><td><span class="mono">{esc(fila["sku"])}</span> {esc(fila["nombre"])}</td>
          <td>{fila["netas"]}</td><td class="mono">{esc(money(fila["ingresos"]))}</td>
          <td class="mono">{esc(money(fila["costo"]))}</td><td class="mono">{esc(money(fila["merma"]))}</td>
          <td class="mono">{esc(money(fila["ganancia"]))}</td>
          <td><div class="bar"><span style="width:{ancho}%"></span></div> {fila["margen"]:.1f}%</td>
        </tr>""")
    cruce = []
    for local, medios in sorted(rep["cruce"].items()):
        cruce.append(f"""<tr><td>{esc(local)}</td>
          <td class="mono">{esc(money(medios.get("efectivo", 0)))}</td>
          <td class="mono">{esc(money(medios.get("debito", 0)))}</td>
          <td class="mono">{esc(money(medios.get("credito", 0)))}</td>
          <td class="mono">{esc(money(medios.get("qr", 0)))}</td></tr>""")
    body = f"""{head("Gerencia · Reportes 1 y 2", "Reportes comerciales y de margen", "Ingresos netos de devoluciones, CMV y merma por precinto roto.")}
    {_filtros("/gerencia/comercial", q)}
    <div class="kpis">
      <div class="kpi"><span>Ingresos netos</span><strong>{esc(money(rep["ingresos"]))}</strong></div>
      <div class="kpi"><span>CMV</span><strong>{esc(money(rep["cmv"]))}</strong></div>
      <div class="kpi"><span>Merma por precinto</span><strong class="bad">{esc(money(rep["merma"]))}</strong></div>
      <div class="kpi"><span>Margen estimado</span><strong class="{"ok" if rep["margen"] >= 0 else "bad"}">{esc(money(rep["margen"]))} ({pct:.1f}%)</strong></div>
    </div>
    <div class="split">
      <section class="card"><div class="card-h"><h2>Más vendidos y margen</h2></div>
        <table><thead><tr><th>#</th><th>PRODUCTO</th><th>NETAS</th><th>INGRESOS</th><th>COSTO</th><th>MERMA</th><th>GANANCIA</th><th>%</th></tr></thead>
        <tbody>{''.join(filas) or '<tr><td colspan="8">Sin ventas en el rango.</td></tr>'}</tbody></table>
      </section>
      <section class="card"><div class="card-h"><h2>Ventas por local y medio</h2></div>
        <table><thead><tr><th>LOCAL</th><th>EFECTIVO</th><th>DÉBITO</th><th>CRÉDITO</th><th>QR</th></tr></thead>
        <tbody>{''.join(cruce) or '<tr><td colspan="5">Sin movimientos.</td></tr>'}</tbody></table>
      </section>
    </div>
    <p class="note">Valores netos de devoluciones registradas.</p>"""
    return shell(rol, "/gerencia/comercial", "Gerencia / Reportes comerciales", {}, body)


def page_logistica(rol, store, q):
    rep = store.reporte_logistico(q.get("ubi", ""))
    transito = []
    for cod, fila in sorted(rep["transito"].items()):
        prom = sum(fila["mins"]) / len(fila["mins"])
        cerrados = fila["ok"] + fila["bad"]
        efect = (fila["ok"] / cerrados * 100) if cerrados else 0
        transito.append(f"""<tr><td>{esc(cod)}</td><td>{len(fila["mins"])}</td>
          <td>{_hm(min(fila["mins"]))}</td><td>{_hm(prom)}</td><td>{_hm(max(fila["mins"]))}</td>
          <td>{efect:.0f}%</td></tr>""")
    crit = []
    for fila in rep["criticos"]:
        crit.append(f"""<tr><td>{esc(fila["ubi"])}</td><td>{esc(fila["sku"])} {esc(fila["nombre"])}</td>
          <td class="bad">{fila["disp"]} u.</td><td>{fila["minimo"]} u.</td><td class="mono">{esc(money(fila["valor"]))}</td>
          <td>{badge("RECHAZADO").replace("RECHAZADO", "BAJO MÍNIMO")}</td></tr>""")
    malos = []
    for fila in rep["rechazados"]:
        malos.append(f"""<tr><td>{esc(cuando(fila["fecha"]))}</td><td class="mono">{esc(fila["codigo"])}</td>
          <td class="mono">{esc(fila["remito"])}</td><td>{esc(fila["destino"])}</td><td class="mono">{esc(fila["precinto"])}</td>
          <td>{fila["unidades"]}</td><td class="mono">{esc(money(fila["valor"]))}</td><td>{esc(fila["obs"])}</td></tr>""")
    body = f"""{head("Gerencia · Reportes 3, 4 y 5", "Reportes logísticos y de inventario", "Tránsito, existencias bajo mínimo y bultos rechazados por precinto.")}
    {_filtros("/gerencia/logistica", q)}
    <div class="split">
      <section class="card"><div class="card-h"><h2>Tiempo de tránsito CD → local</h2></div>
        <table><thead><tr><th>DESTINO</th><th>RECIBIDOS</th><th>MÍN</th><th>PROMEDIO</th><th>MÁX</th><th>VERIFICADOS</th></tr></thead>
        <tbody>{''.join(transito) or '<tr><td colspan="6">Sin arribos en el filtro.</td></tr>'}</tbody></table>
      </section>
      <section class="card"><div class="card-h"><h2>Existencias en o bajo el mínimo</h2></div>
        <table><thead><tr><th>UBICACIÓN</th><th>PRODUCTO</th><th>DISP.</th><th>MÍNIMO</th><th>VALOR</th><th></th></tr></thead>
        <tbody>{''.join(crit)}</tbody></table>
      </section>
    </div>
    <section class="card"><div class="card-h"><h2>Bultos rechazados por rotura de precinto</h2></div>
      <table><thead><tr><th>FECHA</th><th>BULTO</th><th>REMITO</th><th>DESTINO</th><th>PRECINTO</th><th>UNIDADES</th><th>PÉRDIDA</th><th>OBSERVACIÓN</th></tr></thead>
      <tbody>{''.join(malos) or '<tr><td colspan="8">Sin rechazos.</td></tr>'}</tbody></table>
    </section>"""
    return shell(rol, "/gerencia/logistica", "Gerencia / Reportes logísticos", {}, body)


def _hm(mins):
    mins = int(mins)
    return f"{mins // 60}h {mins % 60:02d}m"


def _rango(q):
    def parse(valor, fin):
        try:
            dt = datetime.strptime(valor, "%d/%m/%Y")
        except ValueError:
            dt = datetime(2026, 10, 1 if not fin else 23)
        if fin:
            return dt.replace(hour=23, minute=59, second=59)
        return dt

    return parse(q.get("desde", "01/10/2026"), False), parse(q.get("hasta", "23/10/2026"), True)


def modales_cd(store, q, volver):
    cual = q.get("modal", "")
    if not cual:
        return ""
    if cual == "producto":
        return overlay(modal_producto(store, q, volver))
    if cual == "proveedor":
        return overlay(modal_proveedor(store, q, volver))
    if cual == "compra":
        return overlay(modal_compra(store, q, volver))
    if cual == "sucursal":
        return overlay(modal_sucursal(store, q, volver))
    if cual == "cd":
        return overlay(modal_cd(store, volver))
    return ""


def _val(store, key, default=""):
    if store.form_error and key in store.held:
        return store.held.get(key, default)
    return default


def modal_producto(store, q, volver):
    sku = q.get("sku", "")
    actual = store.producto(sku) if sku and not store.form_error else None
    held = store.held if store.form_error else {}
    data = actual or {}
    def campo(nombre, fallback=""):
        if store.form_error:
            return held.get(nombre, fallback)
        return data.get(nombre, fallback) if actual else fallback
    cats = "".join(
        f'<option value="{esc(c["id"])}"{" selected" if campo("categoria", store.categorias[0]["id"]) == c["id"] else ""}>{esc(c["nombre"])}</option>'
        for c in store.categorias
    )
    provs = "".join(
        f'<option value="{esc(p["cuit"])}"{" selected" if campo("proveedor", store.proveedores[0]["cuit"]) == p["cuit"] else ""}>{esc(p["razon"])}</option>'
        for p in store.proveedores
    )
    mins = []
    for ubi in store.ubicaciones:
        valor = store.st(ubi["codigo"], actual["sku"])["minimo"] if actual else held.get(f"min_{ubi['codigo']}", "0")
        mins.append(f'<div class="field"><label>MÍNIMO {esc(ubi["codigo"])}</label><input name="min_{esc(ubi["codigo"])}" type="number" min="0" value="{esc(valor)}"></div>')
    error = f'<p class="err">{esc(store.form_error)}</p>' if store.form_error else ""
    sku_val = campo("sku", sku)
    body = f"""<form method="post" action="/cd/producto">
      <input type="hidden" name="nuevo" value="{esc(store.held.get("nuevo", "0" if actual else "1"))}">
      <input type="hidden" name="volver" value="{esc(volver)}">
      <div class="field{" error" if store.form_error and "SKU" in store.form_error else ""}"><label>SKU</label>
        <input name="sku" value="{esc(sku_val)}" {"readonly" if actual else ""} required></div>
      {error}
      <div class="field"><label>CÓDIGO DE BARRAS</label><input name="barra" value="{esc(campo("barra"))}" required></div>
      <div class="field"><label>NOMBRE</label><input name="nombre" value="{esc(campo("nombre"))}" required></div>
      <div class="grid-2"><div class="field"><label>CATEGORÍA</label><select name="categoria">{cats}</select></div>
        <div class="field"><label>PROVEEDOR</label><select name="proveedor">{provs}</select></div></div>
      <div class="grid-2"><div class="field"><label>COSTO UNITARIO</label><input name="costo" value="{esc(campo("costo"))}" required></div>
        <div class="field"><label>PRECIO DE VENTA</label><input name="precio" value="{esc(campo("precio"))}" required></div></div>
      <h3>Niveles de stock mínimo por sucursal</h3>
      {''.join(mins)}
      <div class="modal-f"><a class="btn" href="{esc(volver)}">Cancelar</a><button class="btn primary" type="submit">Guardar producto</button></div>
    </form>"""
    return modal_box("Nuevo / Editar producto", "El SKU y el código de barras son únicos.", body, volver)


def modal_proveedor(store, q, volver):
    actual = store.proveedor(q.get("cuit", "")) if q.get("cuit") and not store.form_error else None
    held = store.held if store.form_error else {}
    def campo(nombre, fallback=""):
        if store.form_error:
            return held.get(nombre, fallback)
        if actual:
            return actual.get(nombre, fallback)
        return fallback
    rubros_actuales = actual["rubros"] if actual else held.get("rubros", [])
    if isinstance(rubros_actuales, str):
        rubros_actuales = [rubros_actuales]
    checks = []
    for cat in store.categorias:
        checked = "checked" if cat["nombre"] in rubros_actuales else ""
        checks.append(f'<label><input type="checkbox" name="rubros" value="{esc(cat["nombre"])}" {checked}> {esc(cat["nombre"])}</label>')
    error = store.form_error
    disabled = "disabled" if error and "CUIT" in error else ""
    body = f"""<form method="post" action="/cd/proveedor">
      <input type="hidden" name="nuevo" value="{esc(store.held.get("nuevo", "0" if actual else "1"))}">
      <input type="hidden" name="cuit_original" value="{esc(actual["cuit"] if actual else held.get("cuit_original", ""))}">
      <input type="hidden" name="volver" value="{esc(volver)}">
      <div class="field{" error" if error and "CUIT" in error else ""}"><label>CUIT (IDENTIFICADOR ÚNICO)</label>
        <input name="cuit" value="{esc(campo("cuit"))}" required></div>
      {f'<p class="err">{esc(error)}</p>' if error else ''}
      <div class="field"><label>RAZÓN SOCIAL</label><input name="razon" value="{esc(campo("razon"))}" required></div>
      <div class="grid-2"><div class="field"><label>TELÉFONO</label><input name="tel" value="{esc(campo("tel"))}" required></div>
        <div class="field"><label>EMAIL</label><input name="email" value="{esc(campo("email"))}" required></div></div>
      <div class="field"><label>RUBROS</label><div class="checks">{''.join(checks)}</div></div>
      <label><input type="checkbox" name="activo" {"checked" if not actual or actual["activo"] else ""}> Activo</label>
      <div class="modal-f"><span class="why">{'Corregí el CUIT duplicado para habilitar el guardado' if disabled else ''}</span>
        <a class="btn" href="{esc(volver)}">Cancelar</a>
        <button class="btn primary" type="submit" {disabled}>Guardar proveedor</button></div>
    </form>"""
    return modal_box("Nuevo / Editar proveedor", "Registrá un proveedor para el abastecimiento del CD. El CUIT es único.", body, volver)


def modal_compra(store, q, volver):
    provs = "".join(f'<option value="{esc(p["cuit"])}">{esc(p["razon"])} ({esc(p["cuit"])})</option>' for p in store.proveedores)
    opciones = "".join(f'<option value="{esc(p["sku"])}">{esc(p["sku"])} {esc(p["nombre"])}</option>' for p in store.productos)
    filas = []
    for i in (1, 2):
        filas.append(f"""<tr>
          <td><select name="sku">{opciones}</select></td>
          <td><input class="qty" name="qty" type="number" min="0" value="0"></td>
          <td><input name="costo" inputmode="decimal" value="0"></td>
        </tr>""")
    error = f'<p class="err">{esc(store.form_error)}</p>' if store.form_error else ""
    body = f"""<form method="post" action="/cd/compra">
      {error}
      <div class="field"><label>DESTINO</label><input value="CD-01 Centro de Distribución Central" readonly></div>
      <div class="grid-2"><div class="field"><label>PROVEEDOR</label><select name="cuit">{provs}</select></div>
        <div class="field"><label>NRO. FACTURA / REMITO</label><input name="factura" required placeholder="FAC-A-0004-00098122"></div></div>
      <table><thead><tr><th>SKU / PRODUCTO</th><th>CANT. A INGRESAR</th><th>COSTO UNIT.</th></tr></thead><tbody>{''.join(filas)}</tbody></table>
      <div class="modal-f"><a class="btn" href="{esc(volver)}">Cancelar</a><button class="btn primary" type="submit">Confirmar ingreso de compra en CD</button></div>
    </form>"""
    return modal_box("Registrar compra a proveedor", "La mercadería entra al stock disponible del CD y actualiza el costo.", body, volver, wide=True)


def modal_sucursal(store, q, volver):
    actual = store.ubicacion(q.get("codigo", "")) if q.get("codigo") and q.get("codigo") != CD else None
    error = f'<p class="err">{esc(store.form_error)}</p>' if store.form_error else ""
    nombre = actual["nombre"] if actual else "Local 04 - Sucursal Oeste"
    direccion = actual["direccion"] if actual else ""
    tel = actual["tel"] if actual else ""
    codigo = actual["codigo"] if actual else "LOC-04"
    caja = "checked" if not actual or actual["caja_abierta"] else ""
    body = f"""<form method="post" action="/cd/sucursal">
      {error}
      <input type="hidden" name="tipo" value="LOCAL">
      <div class="field"><label>CÓDIGO DE UBICACIÓN</label><input name="codigo" value="{esc(codigo)}" {"readonly" if actual else ""} required></div>
      <div class="field"><label>TIPO DE NODO</label>
        <div class="choice on">Sucursal / local comercial (venta y recepción)</div>
        <div class="choice">Centro de distribución bloqueado: ya existe CD-01 activo</div>
      </div>
      <div class="field"><label>NOMBRE</label><input name="nombre" value="{esc(nombre)}" required></div>
      <div class="field"><label>DIRECCIÓN</label><input name="direccion" value="{esc(direccion)}" required></div>
      <div class="field"><label>TELÉFONO</label><input name="tel" value="{esc(tel)}"></div>
      <label><input type="checkbox" name="caja" {caja}> Habilitar caja y ventas minoristas</label>
      <div class="modal-f"><a class="btn" href="{esc(volver)}">Cancelar</a><button class="btn primary" type="submit">Guardar sucursal</button></div>
    </form>"""
    return modal_box("Alta / edición de ubicación", "Hay un único centro de distribución. El resto son locales.", body, volver)


def modal_cd(store, volver):
    cd = store.ubicacion(CD)
    error = f'<p class="err">{esc(store.form_error)}</p>' if store.form_error else ""
    body = f"""<form method="post" action="/cd/datos">
      {error}
      <div class="field"><label>NOMBRE</label><input name="nombre" value="{esc(cd["nombre"])}" required></div>
      <div class="field"><label>DIRECCIÓN</label><input name="direccion" value="{esc(cd["direccion"])}" required></div>
      <div class="field"><label>TELÉFONO</label><input name="tel" value="{esc(cd["tel"])}"></div>
      <div class="modal-f"><a class="btn" href="{esc(volver)}">Cancelar</a><button class="btn primary" type="submit">Guardar CD</button></div>
    </form>"""
    return modal_box("Editar datos del CD", "CD-01 sigue siendo el único nodo de abastecimiento.", body, volver)


def render(rol, store, path, q):
    ctx_pages = {
        "/cd/catalogo": page_catalogo,
        "/cd/proveedores": page_proveedores,
        "/cd/stock": page_stock,
        "/cd/sucursales": page_sucursales,
        "/cd/empaque": page_empaque,
        "/cd/despacho": page_despacho,
        "/local/stock": page_local_stock,
        "/local/reposicion": page_reposicion,
        "/local/recepcion": page_recepcion,
        "/local/pos": page_pos,
        "/local/devoluciones": page_devoluciones,
        "/gerencia/comercial": page_comercial,
        "/gerencia/logistica": page_logistica,
    }
    if path == "/gerencia/red":
        return page_sucursales(rol, store, q, editable=False)
    fn = ctx_pages.get(path)
    if not fn:
        return None
    return fn(rol, store, q)


def csv_comercial(store, q):
    desde, hasta = _rango(q)
    rep = store.reporte_comercial(desde, hasta, q.get("ubi", ""), "")
    lineas = ["sku,netas,ingresos,costo,merma,ganancia"]
    for fila in rep["ranking"]:
        lineas.append(f'{fila["sku"]},{fila["netas"]},{fila["ingresos"]:.2f},{fila["costo"]:.2f},{fila["merma"]:.2f},{fila["ganancia"]:.2f}')
    return "\n".join(lineas) + "\n"


def csv_logistica(store, q):
    rep = store.reporte_logistico(q.get("ubi", ""))
    lineas = ["bulto,destino,precinto,unidades,valor,observacion"]
    for fila in rep["rechazados"]:
        obs = fila["obs"].replace('"', "'")
        lineas.append(f'{fila["codigo"]},{fila["destino"]},{fila["precinto"]},{fila["unidades"]},{fila["valor"]:.2f},"{obs}"')
    return "\n".join(lineas) + "\n"
