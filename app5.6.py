import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Dashboard Tesis", layout="wide")

# 2. ESTILOS CSS
st.markdown("""
    <style>
    .card-title {
        font-size: 16px !important; /* Un poco más pequeño para que entre bien en 2 columnas */
        font-weight: bold;
        color: #4A90E2; 
        margin-bottom: 10px;
        text-transform: uppercase;
        border-bottom: 2px solid #f0f2f6;
        padding-bottom: 5px;
    }
    .card-list {
        font-size: 13px !important;
        list-style-type: none; 
        padding-left: 0;
        line-height: 1.5;
    }
    .card-list li {
        margin-bottom: 5px;
        padding-left: 8px;
        border-left: 3px solid #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. INGRESO MANUAL DE DATOS
# ==========================================

# --- CASO 1 (25 Indicadores Fijos) ---
datos_c1 = [
    # --- DIMENSIÓN ECONÓMICA ---
    {"Codigo":"S-E-07", "Nombre": "Producción diaria ","Dimensión": "Económica",  "Tipo_Corto": "Relevo", "Tipo_Largo": "Dependientes", "Descripcion": "Este indicador mide la cantidad promedio de producto cosechado por día en una unidad productiva."},
    {"Codigo":"S-E-014","Nombre": "Entrada y salida monetaria","Dimensión": "Económica",  "Tipo_Corto": "Dependientes", "Tipo_Largo": "Excluidas", "Descripcion": "Este indicador evalúa el balance monetario entre los ingresos generados por las actividades productivas y los egresos."},
    {"Codigo":"S-E-016","Nombre": "Diversificación de ingresos","Dimensión": "Económica",  "Tipo_Corto": "Excluidas", "Tipo_Largo": "Excluidas", "Descripcion": "Este indicador mide el porcentaje de ingresos que una unidad productiva obtiene a partir de diversas fuentes."},
    {"Codigo":"S-E-019","Nombre": "Salario promedio","Dimensión": "Económica",  "Tipo_Corto": "Excluidas", "Tipo_Largo": "Excluidas", "Descripcion": "Este indicador estima el salario promedio mensual que reciben los trabajadores agrícolas contratados."},
    {"Codigo":"S-E-020","Nombre": "Ingresos por ventas", "Dimensión": "Económica", "Tipo_Corto": "Influencia / Clave","Tipo_Largo": "Influencia / Clave", "Descripcion": "Este indicador mide el total de ingresos brutos generados por la venta de productos agroalimentarios."},

    # --- DIMENSIÓN AMBIENTAL ---
    {"Codigo":"S-A-024","Nombre": "Conocimiento riesgos pesticidas","Dimensión": "Ambiental",  "Tipo_Corto": "Relevo", "Tipo_Largo": "Relevo", "Descripcion": "Este indicador mide el grado de conocimiento que tienen los trabajadores agrícolas sobre los riesgos asociados al uso de pesticidas."},
    {"Codigo":"S-A-026","Nombre": "Uso de pesticida persistente","Dimensión": "Ambiental", "Tipo_Corto": "Relevo", "Tipo_Largo": "Relevo", "Descripcion":"Este indicador evalúa si en la actividad agrícola se utilizan pesticidas con alta persistencia en el agua."},
    {"Codigo":"S-A-029","Nombre": "Eliminación de residuos","Dimensión": "Ambiental", "Tipo_Corto": "Relevo", "Tipo_Largo": "Relevo", "Descripcion":"Este indicador evalúa si la organización implementa prácticas adecuadas para la eliminación de residuos peligrosos."},
    {"Codigo":"S-A-030","Nombre": "Involucramiento ambiental","Dimensión": "Ambiental",  "Tipo_Corto": "Relevo", "Tipo_Largo": "Relevo", "Descripcion": "Este indicador mide el número de días en los que la organización participa activamente en iniciativas ambientales."},
    {"Codigo":"S-A-031","Nombre": "Uso de químicos crecimiento","Dimensión": "Ambiental", "Tipo_Corto": "Dependientes", "Tipo_Largo": "Relevo", "Descripcion": "Este indicador evalúa si en el proceso agrícola se utilizan o no reguladores de crecimiento sintéticos."},
    {"Codigo":"S-A-032","Nombre": "Cultivos híbridos","Dimensión": "Ambiental", "Tipo_Corto": "Excluidas", "Tipo_Largo": "Dependientes", "Descripcion": "Este indicador identifica si en la unidad productiva se utilizan semillas híbridas en los cultivos principales."},
    {"Codigo":"S-A-033","Nombre": "Manejo de franjas ribereñas","Dimensión": "Ambiental", "Tipo_Corto": "Excluidas", "Tipo_Largo": "Relevo", "Descripcion": "Este indicador evalúa si las franjas ribereñas zonas adyacentes a ríos están manejadas adecuadamente."},
    {"Codigo":"S-A-037","Nombre": "Quema de residuos","Dimensión": "Ambiental",  "Tipo_Corto": "Excluidas", "Tipo_Largo": "Influencia / Clave", "Descripcion": "Este indicador evalúa si la organización agroproductiva realiza prácticas de quema de residuos."},
    {"Codigo":"S-A-042","Nombre": "Cultivos transgénicos","Dimensión": "Ambiental", "Tipo_Corto": "Dependientes", "Tipo_Largo": "Relevo", "Descripcion": "Este indicador determina si dentro de las parcelas agrícolas se cultivan especies transgénicas."},
    {"Codigo":"S-A-047","Nombre": "Promoción organismos benef.","Dimensión": "Ambiental", "Tipo_Corto": "Dependientes", "Tipo_Largo": "Dependientes", "Descripcion": "Este indicador evalúa si se implementan prácticas para promover la presencia de organismos beneficiosos."},
    {"Codigo":"S-A-048","Nombre": "Materiales reutilizables","Dimensión": "Ambiental", "Tipo_Corto": "Excluidas", "Tipo_Largo": "Excluidas", "Descripcion": "Este indicador evalúa si la organización agroindustrial utiliza materiales de embalaje reutilizables."},
    {"Codigo":"S-A-053","Nombre": "Conciencia cambio climático","Dimensión": "Ambiental", "Tipo_Corto": "Relevo", "Tipo_Largo": "Relevo", "Descripcion": "Este indicador mide el nivel de conciencia que tienen los agricultores respecto al cambio climático."},
    {"Codigo":"SR-A-A-01","Nombre": "Riego baja energía","Dimensión": "Ambiental", "Tipo_Corto": "Excluidas", "Tipo_Largo": "Influencia / Clave", "Descripcion": "Este indicador permite identificar si la unidad productiva emplea tecnologías de riego de bajo consumo."},

    # --- DIMENSIÓN SOCIAL ---
    {"Codigo":"S-S-03","Nombre": "Capacitación seguridad","Dimensión": "Social", "Tipo_Corto": "Influencia / Clave", "Tipo_Largo": "Influencia / Clave", "Descripcion": "Este indicador mide el porcentaje del personal que ha recibido capacitación en seguridad industrial."},
    {"Codigo":"S-S-06","Nombre": "Descansos regulares","Dimensión": "Social", "Tipo_Corto": "Excluidas", "Tipo_Largo": "Excluidas", "Descripcion": "Este indicador evalúa la existencia de pausas regulares durante la jornada laboral."},
    {"Codigo":"S-S-019","Nombre": "Acceso a medios electrónicos","Dimensión": "Social",  "Tipo_Corto": "Excluidas", "Tipo_Largo": "Excluidas", "Descripcion": "Este indicador mide el nivel de acceso que tienen los agricultores a medios electrónicos."},
    {"Codigo":"S-S-021","Nombre": "Disponibilidad tratamiento","Dimensión": "Social", "Tipo_Corto": "Excluidas", "Tipo_Largo": "Excluidas", "Descripcion": "Este indicador mide el porcentaje de agricultores que tienen acceso efectivo a servicios médicos."},
    {"Codigo":"S-S-022","Nombre": "Instalaciones sanitarias","Dimensión": "Social", "Tipo_Corto": "Excluidas", "Tipo_Largo": "Excluidas", "Descripcion": "Este indicador mide el porcentaje de agricultores que disponen de acceso regular a instalaciones sanitarias."},
    {"Codigo":"S-S-034","Nombre": "Apoyo vulnerables","Dimensión": "Social",  "Tipo_Corto": "Excluidas", "Tipo_Largo": "Excluidas", "Descripcion": "Este indicador evalúa si la agroindustria implementa programas que beneficien a personas vulnerables."},
    {"Codigo":"S-S-041","Nombre": "Capacitación agrícola","Dimensión": "Social",  "Tipo_Corto": "Relevo", "Tipo_Largo": "Relevo", "Descripcion": "Este indicador mide el porcentaje de agricultores que han recibido capacitación técnica agrícola."},
]

# --- CASO 2 (21 Indicadores Fijos) ---
datos_c2 = [
   # --- DIMENSIÓN ECONÓMICA ---
    {"Codigo":"S-E-07", "Nombre": "Producción diaria ","Dimensión": "Económica",  "Tipo_Corto": "Relevo", "Tipo_Largo": "Relevo", "Descripcion": "Este indicador mide la cantidad promedio de producto cosechado por día en una unidad productiva."},
    {"Codigo":"S-E-014","Nombre": "Entrada y salida monetaria","Dimensión": "Económica",  "Tipo_Corto": "Dependientes", "Tipo_Largo": "Dependientes", "Descripcion": "Este indicador evalúa el balance monetario entre los ingresos generados por las actividades productivas y los egresos."},
    {"Codigo":"S-E-016","Nombre": "Diversificación de ingresos","Dimensión": "Económica",  "Tipo_Corto": "Excluidas", "Tipo_Largo": "Excluidas", "Descripcion": "Este indicador mide el porcentaje de ingresos que una unidad productiva obtiene a partir de diversas fuentes."},
    {"Codigo":"S-E-020","Nombre": "Ingresos por ventas", "Dimensión": "Económica", "Tipo_Corto": "Influencia / Clave","Tipo_Largo": "Influencia / Clave", "Descripcion": "Este indicador mide el total de ingresos brutos generados por la venta de productos agroalimentarios."},

    # --- DIMENSIÓN AMBIENTAL ---
    {"Codigo":"S-A-024","Nombre": "Conocimiento riesgos pesticidas","Dimensión": "Ambiental",  "Tipo_Corto": "Relevo", "Tipo_Largo": "Relevo", "Descripcion": "Este indicador mide el grado de conocimiento que tienen los trabajadores agrícolas sobre los riesgos asociados al uso de pesticidas."},
    {"Codigo":"S-A-026","Nombre": "Uso de pesticida persistente","Dimensión": "Ambiental", "Tipo_Corto": "Relevo", "Tipo_Largo": "Relevo", "Descripcion":"Este indicador evalúa si en la actividad agrícola se utilizan pesticidas con alta persistencia en el agua."},
    {"Codigo":"S-A-030","Nombre": "Involucramiento ambiental","Dimensión": "Ambiental",  "Tipo_Corto": "Dependientes", "Tipo_Largo": "Relevo", "Descripcion": "Este indicador mide el número de días en los que la organización participa activamente en iniciativas ambientales."},
    {"Codigo":"S-A-031","Nombre": "Uso de químicos crecimiento","Dimensión": "Ambiental", "Tipo_Corto": "Dependientes", "Tipo_Largo": "Relevo", "Descripcion": "Este indicador evalúa si en el proceso agrícola se utilizan o no reguladores de crecimiento sintéticos."},
    {"Codigo":"S-A-032","Nombre": "Cultivos híbridos","Dimensión": "Ambiental", "Tipo_Corto": "Excluidas", "Tipo_Largo": "Dependientes", "Descripcion": "Este indicador identifica si en la unidad productiva se utilizan semillas híbridas en los cultivos principales."},
    {"Codigo":"S-A-033","Nombre": "Manejo de franjas ribereñas","Dimensión": "Ambiental", "Tipo_Corto": "Excluidas", "Tipo_Largo": "Influencia / Clave", "Descripcion": "Este indicador evalúa si las franjas ribereñas zonas adyacentes a ríos están manejadas adecuadamente."},
    {"Codigo":"S-A-037","Nombre": "Quema de residuos","Dimensión": "Ambiental",  "Tipo_Corto": "Excluidas", "Tipo_Largo": "Excluidas", "Descripcion": "Este indicador evalúa si la organización agroproductiva realiza prácticas de quema de residuos."},
    {"Codigo":"S-A-042","Nombre": "Cultivos transgénicos","Dimensión": "Ambiental", "Tipo_Corto": "Dependientes", "Tipo_Largo": "Relevo", "Descripcion": "Este indicador determina si dentro de las parcelas agrícolas se cultivan especies transgénicas."},
    {"Codigo":"S-A-047","Nombre": "Promoción organismos benef.","Dimensión": "Ambiental", "Tipo_Corto": "Excluidas", "Tipo_Largo": "Dependientes", "Descripcion": "Este indicador evalúa si se implementan prácticas para promover la presencia de organismos beneficiosos."},
    {"Codigo":"S-A-048","Nombre": "Materiales reutilizables","Dimensión": "Ambiental", "Tipo_Corto": "Excluidas", "Tipo_Largo": "Excluidas", "Descripcion": "Este indicador evalúa si la organización agroindustrial utiliza materiales de embalaje reutilizables."},
    {"Codigo":"SR-A-A-01","Nombre": "Riego baja energía","Dimensión": "Ambiental", "Tipo_Corto": "Excluidas", "Tipo_Largo": "Influencia / Clave", "Descripcion": "Este indicador permite identificar si la unidad productiva emplea tecnologías de riego de bajo consumo."},

    # --- DIMENSIÓN SOCIAL ---
    {"Codigo":"S-S-03","Nombre": "Capacitación seguridad","Dimensión": "Social", "Tipo_Corto": "Influencia / Clave", "Tipo_Largo": "Influencia / Clave", "Descripcion": "Este indicador mide el porcentaje del personal que ha recibido capacitación en seguridad industrial."},
    {"Codigo":"S-S-019","Nombre": "Acceso a medios electrónicos","Dimensión": "Social",  "Tipo_Corto": "Excluidas", "Tipo_Largo": "Excluidas", "Descripcion": "Este indicador mide el nivel de acceso que tienen los agricultores a medios electrónicos."},
    {"Codigo":"S-S-021","Nombre": "Disponibilidad tratamiento","Dimensión": "Social", "Tipo_Corto": "Excluidas", "Tipo_Largo": "Excluidas", "Descripcion": "Este indicador mide el porcentaje de agricultores que tienen acceso efectivo a servicios médicos."},
    {"Codigo":"S-S-022","Nombre": "Instalaciones sanitarias","Dimensión": "Social", "Tipo_Corto": "Excluidas", "Tipo_Largo": "Excluidas", "Descripcion": "Este indicador mide el porcentaje de agricultores que disponen de acceso regular a instalaciones sanitarias."},
    {"Codigo":"S-S-034","Nombre": "Apoyo vulnerables","Dimensión": "Social",  "Tipo_Corto": "Excluidas", "Tipo_Largo": "Excluidas", "Descripcion": "Este indicador evalúa si la agroindustria implementa programas que beneficien a personas vulnerables."},
    {"Codigo":"S-S-041","Nombre": "Capacitación agrícola","Dimensión": "Social",  "Tipo_Corto": "Relevo", "Tipo_Largo": "Relevo", "Descripcion": "Este indicador mide el porcentaje de agricultores que han recibido capacitación técnica agrícola."},
]

# Configuración Maestra (Asegúrate de tener las imágenes en la carpeta)
DB_CASOS = {
    "Nivel Básico": {"imagenes": ["MICMAC_map1.png", "MICMAC_graph1.png", "MICMAC_graph2.png"], "data": datos_c1},
    "Caso de Estudio": {"imagenes": ["MICMAC_map2.png", "MICMAC_graph21.png", "MICMAC_graph22.png"], "data": datos_c2}
}

# ==========================================
# 4. LÓGICA DE APLICACIÓN
# ==========================================

# Sidebar
st.sidebar.title("Menú")
seleccion_caso = st.sidebar.radio("Seleccione Caso:", list(DB_CASOS.keys()))

# Carga de datos base
caso_actual = DB_CASOS[seleccion_caso]
df = pd.DataFrame(caso_actual["data"])

# Creamos las columnas de texto para visualización
df["Texto_Tarjeta"] = "<b>" + df["Codigo"] + "</b> " + df["Nombre"]
df["Texto_Tabla"] = df["Codigo"] + " " + df["Nombre"]


# --- CUERPO PRINCIPAL ---
st.title(f"Análisis Estructural: {seleccion_caso}")

# >>> CAMBIO DE LAYOUT AQUÍ <<<
# Dividimos la pantalla: 
# Columna Izquierda (im_col) para imágenes (30% ancho)
# Columna Derecha (data_col) para los cuadros (70% ancho)
im_col, data_col = st.columns([2.5, 2.5], gap="large")

# --- COLUMNA IZQUIERDA: IMÁGENES VERTICALES ---
with im_col:
    st.markdown("### Mapas / Gráficos")
    # Iteramos sobre las 3 imágenes configuradas en DB_CASOS
    for ruta in caso_actual["imagenes"]:
        if os.path.exists(ruta):
            st.image(ruta, width="stretch")
            st.write("") # Espacio pequeño entre imágenes
        else:
            with st.container(border=True):
                st.warning(f"Falta imagen:\n{ruta}")

# --- COLUMNA DERECHA: SELECTOR Y CUADROS ---
with data_col:
    st.subheader("Tablero de Variables Agrupadas (MICMAC)")
    
    # Selector de Tiempo
    plazo = st.selectbox("Seleccione Horizonte:", ["Corto Plazo", "Largo Plazo"])
    columna_filtro = "Tipo_Corto" if plazo == "Corto Plazo" else "Tipo_Largo"
    
    st.markdown("---")

    # GRID DE CUADROS (2x2)
    # Al estar en una columna lateral, 4 en fila es muy estrecho.
    # Hacemos 2 filas de 2 columnas cada una.
    
    tipos_micmac = ["Influencia / Clave", "Relevo", "Dependientes", "Excluidas"]
    
    # Fila 1 (Motrices y Enlace)
    row1 = st.columns(2)
    # Fila 2 (Dependientes y Autónomas)
    row2 = st.columns(2)
    
    # Unimos las columnas en una sola lista para iterar fácil
    all_cols = row1 + row2 

    for col, tipo in zip(all_cols, tipos_micmac):
        with col:
            with st.container(border=True):
                # Filtramos datos
                items = df[df[columna_filtro] == tipo]["Texto_Tarjeta"].tolist()
                count = len(items)
                
                # Título
                st.markdown(f'<div class="card-title">{tipo} ({count})</div>', unsafe_allow_html=True)
                
                # Lista con Scroll si es muy larga (opcional, aquí es lista normal)
                if count > 0:
                    lista_html = "".join([f"<li>{item}</li>" for item in items])
                    st.markdown(f'<ul class="card-list">{lista_html}</ul>', unsafe_allow_html=True)
                else:
                    st.markdown('<p style="font-size:12px; color:gray; padding-left:10px">-</p>', unsafe_allow_html=True)


# --- TABLA DETALLADA (ABAJO DEL TODO) ---
st.markdown("---")

# Definimos los datos
df_tabla = df[["Dimensión", "Texto_Tabla", "Descripcion"]].copy()
df_tabla.columns = ["Dimensión", "Indicador", "Descripción"]

# Estilos CSS
st.markdown("""
<style>
    table.customTable {
        width: 100%;
        background-color: transparent;
        border-collapse: collapse;
        border-width: 0px;
        color: inherit; 
    }
    table.customTable td, table.customTable th {
        border-width: 0px;
        border-bottom: 1px solid #444; 
        padding: 10px;
        vertical-align: top;
        font-size: 14px;
    }
    table.customTable td:nth-child(1), table.customTable th:nth-child(1) { width: 15%; font-weight: bold; }
    table.customTable td:nth-child(2), table.customTable th:nth-child(2) { width: 25%; font-weight: 600; }
    table.customTable td:nth-child(3), table.customTable th:nth-child(3) { width: 60%; }
    
    table.customTable thead {
        background-color: transparent;
        border-bottom: 2px solid #4A90E2;
    }
    table.customTable th {
        text-transform: uppercase;
        font-size: 15px;
        color: #4A90E2;
        text-align: left;
    }
</style>
""", unsafe_allow_html=True)

st.subheader(f"Inventario de Indicadores (Total: {len(df)})")
with st.expander("Ver Tabla de Datos Detallada", expanded=True):
    html = df_tabla.to_html(index=False, classes="customTable", escape=False)
    st.markdown(html, unsafe_allow_html=True)