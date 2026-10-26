from datetime import datetime, date
from io import BytesIO
import pandas as pd
import streamlit as st
from supabase import create_client

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS
# ==========================================
st.set_page_config(page_title="Vena Laboratorios - Logística", layout="wide")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="stApp"] {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #F1F5F9 0%, #334155 100%) !important;
            color: #111827;
        }

        .block-container {
            padding-top: 3rem !important;
            padding-bottom: 2rem !important;
            max-width: 98% !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
        }

        .titulo-principal {
            text-align: left;
            font-size: 12rem;
            font-weight: 1000;
            color: #111827;
            letter-spacing: -0.5px;
            margin: 0px;
        }

        .subtitulo-principal {
            text-align: left;
            font-size: 0.55rem;
            color: #374151;
            font-weight: 600;
            margin-top: 2px;
        }

        .contenedor-modulos-centrado {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
            margin-top: 0.2rem;
            margin-bottom: 1rem;
        }

        div.row-widget.stRadio > div {
            display: flex !important;
            justify-content: center !important;
            gap: 12px;
            background: #FFFFFF;
            padding: 8px 18px;
            border-radius: 12px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
            border: 1px solid #4B5563;
            width: fit-content;
            margin: 0 auto;
        }

        div.row-widget.stRadio label {
            background-color: #F9FAFB !important;
            padding: 8px 20px !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            color: #1F2937 !important;
            border: 1px solid #9CA3AF !important;
            cursor: pointer;
        }

        div[data-testid="stVerticalBlock"] > div[style*="border"] {
            border: 1px solid #4B5563 !important;
            border-radius: 12px !important;
            box-shadow: 0 10px 20px -3px rgba(0, 0, 0, 0.08) !important;
            background-color: #FFFFFF !important;
            padding: 1.6rem !important;
        }

        .stButton > button {
            background: linear-gradient(135deg, #1F2937 0%, #111827 100%) !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 0.55rem 1.2rem !important;
        }

        /* Estilo para el botón de usuario estilo Google en plomo claro */
        div[data-testid="stPopover"] > button {
            background-color: #E5E7EB !important;
            color: #1F2937 !important;
            border: 1px solid #9CA3AF !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CREDENCIALES DE SUPABASE
# ==========================================
SUPABASE_URL = "https://fpktbiatogbvawnmnpam.supabase.co"
SUPABASE_KEY = "sb_publishable_9iIKNYvLoXJpqJIsmYAX9g_GO-wnx5p"

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Error en la inicialización de Supabase: {e}")

# ==========================================
# 3. CONTROL DE AUTENTICACIÓN
# ==========================================
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'usuario_actual' not in st.session_state:
    st.session_state.usuario_actual = None

if not st.session_state.autenticado:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center; color: #111827;'>Acceso Logística & Finanzas</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #374151; font-size: 0.9rem;'>Laboratorios Vena - Control Operativo</p>", unsafe_allow_html=True)
            st.markdown("---")
            
            with st.form("form_login_logistica"):
                correo_ingresado = st.text_input("Correo Electrónico", placeholder="usuario@avenalaboratorios.com")
                password_ingresado = st.text_input("Contraseña", type="password", placeholder="contraseña")
                st.markdown("<br>", unsafe_allow_html=True)
                btn_login = st.form_submit_button("Ingresar al Sistema", use_container_width=True)
                
                if btn_login:
                    if not correo_ingresado or not password_ingresado:
                        st.warning("⚠️ Por favor ingrese su correo y contraseña.")
                    else:
                        try:
                            res = supabase.table("usuarios") \
                                .select("*") \
                                .eq("correo", correo_ingresado.strip()) \
                                .eq("contrasena", password_ingresado.strip()) \
                                .eq("estado", "activo") \
                                .execute()
                            
                            if res.data and len(res.data) > 0:
                                st.session_state.autenticado = True
                                st.session_state.usuario_actual = res.data[0]
                                st.rerun()
                            else:
                                st.error("❌ Credenciales incorrectas o usuario no autorizado.")
                        except Exception as err:
                            st.error(f"Error al verificar credenciales: {err}")
    st.stop()

# ==========================================
# 4. ENCABEZADO, LOGO Y MENÚ DE USUARIO
# ==========================================
c_title, c_logo, c_user_space = st.columns([4.2, 1.3, 0.5])

with c_title:
    st.markdown("<h1 class='titulo-principal'>LOGÍSTICA</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-principal'>Gestión de Pedidos, Lotes y Facturación</p>", unsafe_allow_html=True)

with c_logo:
    try:
        st.image("LOGO VENA.png", width=150)
    except Exception:
        pass

with c_user_space:
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    usuario_nombre = st.session_state.usuario_actual.get('nombre', 'Usuario')
    usuario_rol = st.session_state.usuario_actual.get('rol', 'Colaborador').capitalize()
    iniciales = "".join([n[0] for n in usuario_nombre.split()[:2]]).upper()
    
    with st.popover(f"👤 {iniciales} - Cuenta", use_container_width=True):
        st.markdown(f"**{usuario_nombre}**")
        st.markdown(f"<span style='color: #4B5563; font-size: 0.85rem;'>Rol: {usuario_rol}</span>", unsafe_allow_html=True)
        st.markdown("---")
        if st.button("Cerrar Sesión", use_container_width=True):
            st.session_state.autenticado = False
            st.session_state.usuario_actual = None
            st.rerun()

st.markdown('<div class="contenedor-modulos-centrado">', unsafe_allow_html=True)
menu_logistica = st.radio(
    "Seleccione el módulo:",
    ("📦 Gestión de Pedidos", "🏭 Control de Inventarios (Lotes)", "💳 Facturación y Cobranzas"),
    horizontal=True
)
st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# MÓDULO 1: GESTIÓN DE PEDIDOS (PICKING / PACKING)
# ==========================================
if menu_logistica == "📦 Gestión de Pedidos":
    st.subheader("Bandeja de Pedidos para Almacén")
    
    try:
        pedidos_res = supabase.table("pedidos").select("*").order("f_pedido", desc=True).execute()
        lista_pedidos = pedidos_res.data if pedidos_res.data else []
    except Exception as e:
        lista_pedidos = []
        st.error(f"Error al cargar pedidos: {e}")

    if lista_pedidos:
        df_pedidos = pd.DataFrame(lista_pedidos)
        
        estados_filtro_lista = ["Todos", "En proceso de Alistamiento / picking", "Por Despachar", "En Ruta", "Entregado"]
        
        col_f1, col_f2 = st.columns([2, 2])
        with col_f1:
            estado_filtro = st.selectbox("Filtrar por Estado de Pedido", options=estados_filtro_lista)
        
        if estado_filtro != "Todos":
            df_pedidos_filtrado = df_pedidos[df_pedidos["estado_pedido"] == estado_filtro]
        else:
            df_pedidos_filtrado = df_pedidos

        # Configuración de la tabla interactiva con selección de filas habilitada
        st.write("Seleccione un pedido en la tabla de abajo para ver su detalle de picking y empaque:")
        
        evento_seleccion = st.dataframe(
            df_pedidos_filtrado[["n_pedido", "nombre_cliente", "vendedor", "f_req_despacho", "estado_pedido", "total_pedido_importe"]],
            use_container_width=True,
            selection_mode="single-row",
            on_select="rerun",
            key="tabla_pedidos_almacen"
        )

        # Capturar el pedido seleccionado haciendo clic en la tabla
        filas_seleccionadas = evento_seleccion.get("selection", {}).get("rows", [])
        
        pedido_seleccionado = None
        if filas_seleccionadas:
            indice_fila = filas_seleccionadas[0]
            pedido_seleccionado = df_pedidos_filtrado.iloc[indice_fila]["n_pedido"]

        if pedido_seleccionado:
            st.markdown("---")
            st.subheader(f"Gestión del Pedido: {pedido_seleccionado}")
            
            p_info = next((p for p in lista_pedidos if p["n_pedido"] == pedido_seleccionado), None)
            
            if p_info:
                # Tarjetas de información con contraste adecuado (fondo blanco neutral y texto oscuro)
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    with st.container(border=True):
                        st.markdown(f"**📋 Datos del Cliente**")
                        st.markdown(f"• **Cliente:** {p_info['nombre_cliente']}")
                        st.markdown(f"• **Dirección:** {p_info['direccion']} ({p_info['ciudad']})")
                with col_info2:
                    with st.container(border=True):
                        st.markdown(f"**🚚 Datos de Despacho**")
                        st.markdown(f"• **Fecha Req. Despacho:** {p_info['f_req_despacho']}")
                        st.markdown(f"• **Vendedor:** {p_info['vendedor']}")
                
                detalle_res = supabase.table("detalle_pedidos").select("*").eq("n_pedido", pedido_seleccionado).execute()
                if detalle_res.data:
                    df_detalle_raw = pd.DataFrame(detalle_res.data)
                    
                    # Construir la estructura solicitada para los ítems del pedido
                    df_detalle = pd.DataFrame()
                    df_detalle["Código del Producto"] = df_detalle_raw.get("codigo_producto", "")
                    df_detalle["Producto"] = df_detalle_raw.get("producto", df_detalle_raw.get("descripcion", ""))
                    df_detalle["Cantidad en Unidades"] = df_detalle_raw.get("cantidad", 0)
                    
                    # Calcular cantidad en docenas (asumiendo 12 unidades por docena si existe la columna)
                    if "cantidad" in df_detalle_raw.columns:
                        df_detalle["Cantidad en Docenas"] = df_detalle_raw["cantidad"] / 12.0
                    else:
                        df_detalle["Cantidad en Docenas"] = 0.0
                        
                    # Extraer solo la fecha de pedido (sin hora si viene con formato timestamp)
                    f_pedido_str = str(p_info.get("f_pedido", ""))
                    if "T" in f_pedido_str:
                        f_pedido_str = f_pedido_str.split("T")[0]
                    elif " " in f_pedido_str:
                        f_pedido_str = f_pedido_str.split(" ")[0]

                    df_detalle["Fecha de Pedido"] = f_pedido_str
                    df_detalle["Fecha de Requerimiento de Despacho"] = p_info.get("f_req_despacho", "")

                    st.write("**Ítems del Pedido (Picking y Packing):**")
                    st.dataframe(df_detalle, use_container_width=True)

                    # DataFrame específico para el Excel (Código del pedido y los campos solicitados del detalle)
                    df_excel_export = df_detalle.copy()
                    df_excel_export.insert(0, "N° de Pedido", pedido_seleccionado)

                    # Botón de exportación a Excel para Picking con la estructura solicitada
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df_excel_export.to_excel(writer, sheet_name='Detalle Picking', index=False)
                    output.seek(0)

                    st.download_button(
                        label="📥 Descargar Formato de Picking (Excel)",
                        data=output,
                        file_name=f"Picking_Pedido_{pedido_seleccionado}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                else:
                    st.warning("Este pedido no contiene ítems registrados en el detalle.")

                estados_posibles = ["En proceso de Alistamiento / picking", "Por Despachar", "En Ruta", "Entregado"]
                idx_actual = estados_posibles.index(p_info["estado_pedido"]) if p_info["estado_pedido"] in estados_posibles else 0
                
                nuevo_estado = st.selectbox("Cambiar Estado del Pedido", options=estados_posibles, index=idx_actual)
                
                if st.button("Actualizar Estado de Logística"):
                    try:
                        supabase.table("pedidos").update({"estado_pedido": nuevo_estado}).eq("n_pedido", pedido_seleccionado).execute()
                        st.toast(f"¡Estado del pedido {pedido_seleccionado} actualizado a '{nuevo_estado}'!")
                        st.rerun()
                    except Exception as err:
                        st.error(f"Error al actualizar: {err}")
    else:
        st.warning("No hay pedidos registrados en el sistema.")
        
# ==========================================
# MÓDULO 2: CONTROL DE INVENTARIOS (LOTES)
# ==========================================
elif menu_logistica == "🏭 Control de Inventarios (Lotes)":
    st.subheader("Registro de Nuevos Lotes de Producto Terminado")
    
    try:
        prod_res = supabase.table("productos").select("codigo, producto, stock_actual").execute()
        lista_productos = prod_res.data if prod_res.data else []
    except:
        lista_productos = []

    with st.container(border=True):
        if lista_productos:
            prod_dict = {f"{p['codigo']} - {p['producto']}": p for p in lista_productos}
            prod_sel = st.selectbox("Seleccione el Producto", options=list(prod_dict.keys()), index=None, placeholder="-- Seleccione producto --")
            
            if prod_sel:
                prod_obj = prod_dict[prod_sel]
                codigo_elegido = prod_obj['codigo']
                nombre_producto_limpio = prod_obj['producto']
                
                col_l1, col_l2 = st.columns(2)
                with col_l1:
                    n_lote_input = st.text_input("Número de Lote", placeholder="Ej. LOTE-2026-001")
                    cantidad_lote = st.number_input("Cantidad Inicial Producida (Unidades)", min_value=1, value=100)
                with col_l2:
                    f_prod = st.date_input("Fecha de Producción", value=date.today())
                    f_venc = st.date_input("Fecha de Vencimiento", value=date.today())
                
                if st.button("💾 Registrar Lote en Almacén", use_container_width=True):
                    if not n_lote_input:
                        st.warning("⚠️ Ingrese el número de lote.")
                    else:
                        try:
                            id_lote_gen = f"LOT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                            payload_lote = {
                                "id": id_lote_gen,
                                "codigo_producto": codigo_elegido,
                                "producto": nombre_producto_limpio,
                                "n_lote": n_lote_input.strip(),
                                "cantidad_inicial": int(cantidad_lote),
                                "f_produccion": f_prod.strftime('%Y-%m-%d'),
                                "f_vencimiento": f_venc.strftime('%Y-%m-%d'),
                                "estado_lote": "Disponible"
                            }
                            supabase.table("lotes_inventario").insert(payload_lote).execute()

                            # Sumar la cantidad del nuevo lote al stock_actual en la tabla productos
                            prod_db = supabase.table("productos").select("stock_actual").eq("codigo", codigo_elegido).execute()
                            if prod_db.data:
                                stock_actual_db = int(pd.to_numeric(pd.Series([prod_db.data[0].get("stock_actual", 0)]), errors="coerce").fillna(0).iloc[0])
                                nuevo_stock_total = stock_actual_db + int(cantidad_lote)
                                supabase.table("productos").update({"stock_actual": nuevo_stock_total}).eq("codigo", codigo_elegido).execute()

                            st.toast(f"¡Lote {n_lote_input} registrado y stock actualizado con éxito!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error al guardar lote: {e}")
        else:
            st.warning("No hay productos cargados en la base de datos.")

    st.markdown("---")
    st.subheader("Inventario Actual de Lotes")
    try:
        lotes_res = supabase.table("lotes_inventario").select("*").execute()
        if lotes_res.data:
            df_lotes = pd.DataFrame(lotes_res.data)
            
            # Filtro para buscar por producto (código o descripción)
            filtro_busqueda_lote = st.text_input("🔍 Buscar por Código o Descripción de Producto", placeholder="Ej. 3010005 o Gel...", key="input_filtro_lotes")
            
            if filtro_busqueda_lote:
                filtro_lower = filtro_busqueda_lote.lower()
                df_lotes = df_lotes[
                    df_lotes["codigo_producto"].astype(str).str.lower().str.contains(filtro_lower) | 
                    df_lotes["producto"].astype(str).str.lower().str.contains(filtro_lower)
                ]

            # Seleccionar y renombrar las columnas solicitadas
            cols_disponibles = [col for col in ["codigo_producto", "producto", "n_lote", "cantidad_inicial", "f_produccion", "f_vencimiento", "estado_lote"] if col in df_lotes.columns]
            df_lotes_mostrar = df_lotes[cols_disponibles].rename(columns={
                "codigo_producto": "Código Producto",
                "producto": "Descripción",
                "n_lote": "N° Lote",
                "cantidad_inicial": "Cantidad Inicial",
                "f_produccion": "F. Producción",
                "f_vencimiento": "F. Vencimiento",
                "estado_lote": "Estado"
            })

            st.dataframe(df_lotes_mostrar, use_container_width=True, hide_index=True)
        else:
            st.info("No hay lotes registrados todavía.")
    except Exception as e:
        st.error(f"Error al cargar lotes: {e}")
        
# ==========================================
# MÓDULO 3: FACTURACIÓN Y COBRANZAS
# ==========================================
elif menu_logistica == "💳 Facturación y Cobranzas":
    st.subheader("Emisión de Facturas y Control de Créditos / Cobranzas")
    
    sub_op = st.radio("Seleccione opción de Finanzas", ["Emitir Factura / Guía", "Registrar Abono / Pago", "Estado de Cuentas por Cobrar"], horizontal=True)
    
    if sub_op == "Emitir Factura / Guía":
        with st.container(border=True):
            st.write("**Generar Comprobante de Salida**")
            
            try:
                ped_list_res = supabase.table("pedidos").select("n_pedido, nombre_cliente, total_pedido_importe").execute()
                pedidos_disponibles = ped_list_res.data if ped_list_res.data else []
            except:
                pedidos_disponibles = []

            if pedidos_disponibles:
                ped_dict_f = {f"{p['n_pedido']} - {p['nombre_cliente']} (S/ {p['total_pedido_importe']:.2f})": p for p in pedidos_disponibles}
                ped_sel_f = st.selectbox("Seleccione el Pedido Aprobado", options=list(ped_dict_f.keys()), index=None, placeholder="-- Seleccione pedido --")
                
                if ped_sel_f:
                    datos_p_sel = ped_dict_f[ped_sel_f]
                    
                    col_fac1, col_fac2 = st.columns(2)
                    with col_fac1:
                        n_factura_txt = st.text_input("Número de Factura", placeholder="Ej. F001-00001234")
                        n_guia_txt = st.text_input("Número de Guía de Remisión", placeholder="Ej. G001-00001234")
                        cond_credito = st.selectbox("Condición de Crédito", options=["Contado", "Crédito 30 días", "Crédito 45 días", "Crédito 60 días"])
                    with col_fac2:
                        transportista_txt = st.text_input("Empresa Transportista (Opcional)", placeholder="Ej. Transportes S.A.")
                        placa_txt = st.text_input("Placa de Vehículo (Opcional)", placeholder="Ej. ABC-123")
                        importe_doc = st.number_input("Importe Total (S/)", value=float(datos_p_sel["total_pedido_importe"]))

                    if st.button("💾 Emitir Documento y Registrar Cuentas por Cobrar", use_container_width=True):
                        if not n_factura_txt:
                            st.warning("⚠️ Debe ingresar el número de factura.")
                        else:
                            try:
                                dias = 0
                                if "30" in cond_credito: dias = 30
                                elif "45" in cond_credito: dias = 45
                                elif "60" in cond_credito: dias = 60
                                
                                f_emi = date.today()
                                from datetime import timedelta
                                f_venc = f_emi + timedelta(days=dias)
                                id_doc = f"DOC-{datetime.now().strftime('%Y%m%d%H%M%S')}"

                                payload_doc = {
                                    "id": id_doc,
                                    "n_pedido": datos_p_sel["n_pedido"],
                                    "n_factura": n_factura_txt.strip(),
                                    "n_guia_remision": n_guia_txt.strip() if n_guia_txt else None,
                                    "condicion_credito": cond_credito,
                                    "f_emision": f_emi.isoformat(),
                                    "f_vencimiento": f_venc.strftime('%Y-%m-%d'),
                                    "importe_total": float(importe_doc),
                                    "saldo_pendiente": float(importe_doc),
                                    "estado_factura": "Por Cobrar",
                                    "transportista": transportista_txt,
                                    "vehiculo_placa": placa_txt,
                                    "generado_por": st.session_state.usuario_actual.get('nombre')
                                }
                                
                                supabase.table("documentos_salida").insert(payload_doc).execute()
                                st.toast(f"¡Factura {n_factura_txt} emitida con éxito!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error al emitir factura: {e}")
            else:
                st.warning("No hay pedidos disponibles para facturar.")

    elif sub_op == "Registrar Abono / Pago":
        st.write("**Registrar Pago o Transferencia Bancaria**")
        
        try:
            doc_res = supabase.table("documentos_salida").select("n_factura, saldo_pendiente, importe_total").gt("saldo_pendiente", 0).execute()
            docs_pendientes = doc_res.data if doc_res.data else []
        except:
            docs_pendientes = []

        if docs_pendientes:
            doc_dict_p = {f"Factura: {d['n_factura']} (Saldo Pendiente: S/ {d['saldo_pendiente']:.2f})": d for d in docs_pendientes}
            doc_sel_p = st.selectbox("Seleccione la Factura", options=list(doc_dict_p.keys()), index=None, placeholder="-- Seleccione factura pendiente --")
            
            if doc_sel_p:
                info_d_sel = doc_dict_p[doc_sel_p]
                
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    monto_abono = st.number_input("Monto a Abonar (S/)", min_value=0.01, value=float(info_d_sel["saldo_pendiente"]), step=10.0)
                    f_pago = st.date_input("Fecha de Transferencia", value=date.today())
                    hora_pago = st.text_input("Hora de Operación (Opcional)", placeholder="Ej. 14:35")
                with col_p2:
                    n_operacion = st.text_input("Número de Operación / Código de Transferencia", placeholder="Ej. OP-987654321")
                    banco_destino = st.selectbox("Banco Destino", options=["BCP", "BBVA", "Interbank", "Scotiabank", "Cuenta Corriente Vena"])
                    metodo_pago = st.selectbox("Método de Pago", options=["Transferencia", "Depósito", "Yape/Plin", "Letra"])
                
                obs_pago = st.text_input("Observaciones adicionales", placeholder="Ej. Pago parcial acordado")

                if st.button("💾 Registrar Pago en Sistema", use_container_width=True):
                    if not n_operacion:
                        st.warning("⚠️ Debe ingresar el número de operación.")
                    else:
                        try:
                            id_pago = f"PAG-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                            payload_pago = {
                                "id": id_pago,
                                "n_factura": info_d_sel["n_factura"],
                                "monto_pagado": float(monto_abono),
                                "f_pago": f_pago.strftime('%Y-%m-%d'),
                                "hora_pago": hora_pago,
                                "n_operacion": n_operacion.strip(),
                                "banco_destino": banco_destino,
                                "metodo_pago": metodo_pago,
                                "observacion": obs_pago,
                                "registrado_por": st.session_state.usuario_actual.get('nombre')
                            }
                            
                            supabase.table("pagos_facturas").insert(payload_pago).execute()
                            
                            nuevo_saldo = float(info_d_sel["saldo_pendiente"]) - float(monto_abono)
                            nuevo_estado = "Pagada" if nuevo_saldo <= 0 else "Por Cobrar"
                            
                            supabase.table("documentos_salida").update({
                                "saldo_pendiente": max(0.0, nuevo_saldo),
                                "estado_factura": nuevo_estado
                            }).eq("n_factura", info_d_sel["n_factura"]).execute()
                            
                            st.toast(f"¡Pago de S/ {monto_abono:.2f} registrado correctamente!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error al registrar el pago: {e}")
        else:
            st.success("🎉 ¡Excelente! No hay facturas pendientes de cobro en este momento.")

    else:
        st.subheader("Estado de Cuentas por Cobrar")
        try:
            docs_all = supabase.table("documentos_salida").select("*").execute()
            if docs_all.data:
                df_docs = pd.DataFrame(docs_all.data)
                
                total_por_cobrar = df_docs[df_docs["estado_factura"] == "Por Cobrar"]["saldo_pendiente"].sum()
                total_facturado = df_docs["importe_total"].sum()
                
                m1, m2 = st.columns(2)
                m1.metric("Total Facturado Histórico", f"S/ {total_facturado:,.2f}")
                m2.metric("Total Pendiente por Cobrar", f"S/ {total_por_cobrar:,.2f}")
                
                st.markdown("---")
                st.dataframe(df_docs, use_container_width=True)
            else:
                st.info("No hay documentos de salida registrados.")
        except Exception as e:
            st.error(f"Error al cargar cuentas por cobrar: {e}")
            
# ==========================================
# MÓDULO 2: CONTROL DE INVENTARIOS (LOTES)
# ==========================================
elif menu_logistica == "🏭 Control de Inventarios (Lotes)":
    st.subheader("Registro de Nuevos Lotes de Producto Terminado")
    
    try:
        prod_res = supabase.table("productos").select("codigo, producto").execute()
        lista_productos = prod_res.data if prod_res.data else []
    except:
        lista_productos = []

    with st.container(border=True):
        if lista_productos:
            prod_dict = {f"{p['codigo']} - {p['producto']}": p['codigo'] for p in lista_productos}
            prod_sel = st.selectbox("Seleccione el Producto", options=list(prod_dict.keys()), index=None, placeholder="-- Seleccione producto --")
            
            if prod_sel:
                codigo_elegido = prod_dict[prod_sel]
                
                col_l1, col_l2 = st.columns(2)
                with col_l1:
                    n_lote_input = st.text_input("Número de Lote", placeholder="Ej. LOTE-2026-001")
                    cantidad_lote = st.number_input("Cantidad Inicial Producida (Unidades)", min_value=1, value=100)
                with col_l2:
                    f_prod = st.date_input("Fecha de Producción", value=date.today())
                    f_venc = st.date_input("Fecha de Vencimiento", value=date.today())
                
                if st.button("💾 Registrar Lote en Almacén", use_container_width=True):
                    if not n_lote_input:
                        st.warning("⚠️ Ingrese el número de lote.")
                    else:
                        try:
                            id_lote_gen = f"LOT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                            payload_lote = {
                                "id": id_lote_gen,
                                "codigo_producto": codigo_elegido,
                                "n_lote": n_lote_input.strip(),
                                "cantidad_inicial": int(cantidad_lote),
                                "stock_actual": int(cantidad_lote),
                                "f_produccion": f_prod.strftime('%Y-%m-%d'),
                                "f_vencimiento": f_venc.strftime('%Y-%m-%d'),
                                "estado_lote": "Disponible"
                            }
                            supabase.table("lotes_inventario").insert(payload_lote).execute()
                            st.toast(f"¡Lote {n_lote_input} registrado con éxito!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error al guardar lote: {e}")
        else:
            st.warning("No hay productos cargados en la base de datos.")

    st.markdown("---")
    st.subheader("Inventario Actual de Lotes")
    try:
        lotes_res = supabase.table("lotes_inventario").select("*").execute()
        if lotes_res.data:
            st.dataframe(pd.DataFrame(lotes_res.data), use_container_width=True)
        else:
            st.info("No hay lotes registrados todavía.")
    except Exception as e:
        st.error(f"Error al cargar lotes: {e}")

# ==========================================
# MÓDULO 3: FACTURACIÓN Y COBRANZAS
# ==========================================
elif menu_logistica == "💳 Facturación y Cobranzas":
    st.subheader("Emisión de Facturas y Control de Créditos / Cobranzas")
    
    sub_op = st.radio("Seleccione opción de Finanzas", ["Emitir Factura / Guía", "Registrar Abono / Pago", "Estado de Cuentas por Cobrar"], horizontal=True)
    
    if sub_op == "Emitir Factura / Guía":
        with st.container(border=True):
            st.write("**Generar Comprobante de Salida**")
            
            try:
                ped_list_res = supabase.table("pedidos").select("n_pedido, nombre_cliente, total_pedido_importe").execute()
                pedidos_disponibles = ped_list_res.data if ped_list_res.data else []
            except:
                pedidos_disponibles = []

            if pedidos_disponibles:
                ped_dict_f = {f"{p['n_pedido']} - {p['nombre_cliente']} (S/ {p['total_pedido_importe']:.2f})": p for p in pedidos_disponibles}
                ped_sel_f = st.selectbox("Seleccione el Pedido Aprobado", options=list(ped_dict_f.keys()), index=None, placeholder="-- Seleccione pedido --")
                
                if ped_sel_f:
                    datos_p_sel = ped_dict_f[ped_sel_f]
                    
                    col_fac1, col_fac2 = st.columns(2)
                    with col_fac1:
                        n_factura_txt = st.text_input("Número de Factura", placeholder="Ej. F001-00001234")
                        n_guia_txt = st.text_input("Número de Guía de Remisión", placeholder="Ej. G001-00001234")
                        cond_credito = st.selectbox("Condición de Crédito", options=["Contado", "Crédito 30 días", "Crédito 45 días", "Crédito 60 días"])
                    with col_fac2:
                        transportista_txt = st.text_input("Empresa Transportista (Opcional)", placeholder="Ej. Transportes S.A.")
                        placa_txt = st.text_input("Placa de Vehículo (Opcional)", placeholder="Ej. ABC-123")
                        importe_doc = st.number_input("Importe Total (S/)", value=float(datos_p_sel["total_pedido_importe"]))

                    if st.button("💾 Emitir Documento y Registrar Cuentas por Cobrar", use_container_width=True):
                        if not n_factura_txt:
                            st.warning("⚠️ Debe ingresar el número de factura.")
                        else:
                            try:
                                dias = 0
                                if "30" in cond_credito: dias = 30
                                elif "45" in cond_credito: dias = 45
                                elif "60" in cond_credito: dias = 60
                                
                                f_emi = date.today()
                                from datetime import timedelta
                                f_venc = f_emi + timedelta(days=dias)
                                id_doc = f"DOC-{datetime.now().strftime('%Y%m%d%H%M%S')}"

                                payload_doc = {
                                    "id": id_doc,
                                    "n_pedido": datos_p_sel["n_pedido"],
                                    "n_factura": n_factura_txt.strip(),
                                    "n_guia_remision": n_guia_txt.strip() if n_guia_txt else None,
                                    "condicion_credito": cond_credito,
                                    "f_emision": f_emi.isoformat(),
                                    "f_vencimiento": f_venc.strftime('%Y-%m-%d'),
                                    "importe_total": float(importe_doc),
                                    "saldo_pendiente": float(importe_doc),
                                    "estado_factura": "Por Cobrar",
                                    "transportista": transportista_txt,
                                    "vehiculo_placa": placa_txt,
                                    "generado_por": st.session_state.usuario_actual.get('nombre')
                                }
                                
                                supabase.table("documentos_salida").insert(payload_doc).execute()
                                st.toast(f"¡Factura {n_factura_txt} emitida con éxito!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error al emitir factura: {e}")
            else:
                st.warning("No hay pedidos disponibles para facturar.")

    elif sub_op == "Registrar Abono / Pago":
        st.write("**Registrar Pago o Transferencia Bancaria**")
        
        try:
            doc_res = supabase.table("documentos_salida").select("n_factura, saldo_pendiente, importe_total").gt("saldo_pendiente", 0).execute()
            docs_pendientes = doc_res.data if doc_res.data else []
        except:
            docs_pendientes = []

        if docs_pendientes:
            doc_dict_p = {f"Factura: {d['n_factura']} (Saldo Pendiente: S/ {d['saldo_pendiente']:.2f})": d for d in docs_pendientes}
            doc_sel_p = st.selectbox("Seleccione la Factura", options=list(doc_dict_p.keys()), index=None, placeholder="-- Seleccione factura pendiente --")
            
            if doc_sel_p:
                info_d_sel = doc_dict_p[doc_sel_p]
                
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    monto_abono = st.number_input("Monto a Abonar (S/)", min_value=0.01, value=float(info_d_sel["saldo_pendiente"]), step=10.0)
                    f_pago = st.date_input("Fecha de Transferencia", value=date.today())
                    hora_pago = st.text_input("Hora de Operación (Opcional)", placeholder="Ej. 14:35")
                with col_p2:
                    n_operacion = st.text_input("Número de Operación / Código de Transferencia", placeholder="Ej. OP-987654321")
                    banco_destino = st.selectbox("Banco Destino", options=["BCP", "BBVA", "Interbank", "Scotiabank", "Cuenta Corriente Vena"])
                    metodo_pago = st.selectbox("Método de Pago", options=["Transferencia", "Depósito", "Yape/Plin", "Letra"])
                
                obs_pago = st.text_input("Observaciones adicionales", placeholder="Ej. Pago parcial acordado")

                if st.button("💾 Registrar Pago en Sistema", use_container_width=True):
                    if not n_operacion:
                        st.warning("⚠️ Debe ingresar el número de operación.")
                    else:
                        try:
                            id_pago = f"PAG-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                            payload_pago = {
                                "id": id_pago,
                                "n_factura": info_d_sel["n_factura"],
                                "monto_pagado": float(monto_abono),
                                "f_pago": f_pago.strftime('%Y-%m-%d'),
                                "hora_pago": hora_pago,
                                "n_operacion": n_operacion.strip(),
                                "banco_destino": banco_destino,
                                "metodo_pago": metodo_pago,
                                "observacion": obs_pago,
                                "registrado_por": st.session_state.usuario_actual.get('nombre')
                            }
                            
                            supabase.table("pagos_facturas").insert(payload_pago).execute()
                            
                            nuevo_saldo = float(info_d_sel["saldo_pendiente"]) - float(monto_abono)
                            nuevo_estado = "Pagada" if nuevo_saldo <= 0 else "Por Cobrar"
                            
                            supabase.table("documentos_salida").update({
                                "saldo_pendiente": max(0.0, nuevo_saldo),
                                "estado_factura": nuevo_estado
                            }).eq("n_factura", info_d_sel["n_factura"]).execute()
                            
                            st.toast(f"¡Pago de S/ {monto_abono:.2f} registrado correctamente!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error al registrar el pago: {e}")
        else:
            st.success("🎉 ¡Excelente! No hay facturas pendientes de cobro en este momento.")

    else:
        st.subheader("Estado de Cuentas por Cobrar")
        try:
            docs_all = supabase.table("documentos_salida").select("*").execute()
            if docs_all.data:
                df_docs = pd.DataFrame(docs_all.data)
                
                total_por_cobrar = df_docs[df_docs["estado_factura"] == "Por Cobrar"]["saldo_pendiente"].sum()
                total_facturado = df_docs["importe_total"].sum()
                
                m1, m2 = st.columns(2)
                m1.metric("Total Facturado Histórico", f"S/ {total_facturado:,.2f}")
                m2.metric("Total Pendiente por Cobrar", f"S/ {total_por_cobrar:,.2f}")
                
                st.markdown("---")
                st.dataframe(df_docs, use_container_width=True)
            else:
                st.info("No hay documentos de salida registrados.")
        except Exception as e:
            st.error(f"Error al cargar cuentas por cobrar: {e}")
