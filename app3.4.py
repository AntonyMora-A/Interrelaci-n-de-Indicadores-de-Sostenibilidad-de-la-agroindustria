import streamlit as st
import pandas as pd
import altair as alt

# ---------------------------------------------------------
# 1. CONFIGURACIÓN Y DATOS
# ---------------------------------------------------------
st.set_page_config(page_title="Dashboard DSS - Evaluación de Sostenibilidad", layout="wide")

def get_complete_data():
    """
    Devuelve un DataFrame con los 21 indicadores y sus VALORES FIJOS.
    Datos actualizados por el usuario.
    """
    fixed_data = [
        # --- DIMENSIÓN ECONÓMICA ---
        {"Dimensión": "Económica", "Indicador": "S-E-07 Producción diaria ", "ValorOriginal": -2, "Descripcion": "Este indicador mide la cantidad promedio de producto cosechado por día en una unidad productiva, considerando cultivos propios de la sierra andina como papa, quinua, cebada o leguminosas. Permite analizar la capacidad productiva diaria y evaluar la eficiencia operativa del sistema agrícola en función de la frecuencia y regularidad de cosecha."},
        {"Dimensión": "Económica", "Indicador": "S-E-014 Entrada y salida monetaria", "ValorOriginal": 2, "Descripcion": "Este indicador evalúa el balance monetario entre los ingresos generados por las actividades productivas del agroecosistema y los egresos asociados a los costos operativos. Permite valorar la eficiencia económica general del sistema agrícola en un periodo determinado. "},
        {"Dimensión": "Económica", "Indicador": "S-E-16 Diversificación de ingresos", "ValorOriginal": 1, "Descripcion": "Este indicador mide el porcentaje de ingresos que una unidad productiva obtiene a partir de diversas fuentes, como múltiples productos, servicios complementarios, turismo rural u otras actividades económicas. Una mayor diversificación reduce la vulnerabilidad financiera y mejora la resiliencia económica. "},
        {"Dimensión": "Económica", "Indicador": "S-E-20 Ingresos por ventas", "ValorOriginal": -2, "Descripcion": "Este indicador mide el total de ingresos brutos generados por la venta de productos agroalimentarios durante un periodo definido. El cálculo se basa en los precios unitarios y las cantidades comercializadas, sin deducir devoluciones ni descuentos. Refleja la capacidad comercial directa de la unidad productiva y constituye una métrica base de rendimiento financiero bruto. "},
     

        # --- DIMENSIÓN AMBIENTAL ---
        {"Dimensión": "Ambiental", "Indicador": "S-A-024 Conocimiento riesgos pesticidas", "ValorOriginal": -2, "Descripcion": "Este indicador mide el grado de conocimiento que tienen los trabajadores agrícolas y administradores sobre los riesgos asociados al uso de pesticidas. Evalúa si se comprende adecuadamente la toxicidad, vías de exposición, medidas preventivas y efectos en la salud humana y ambiental. Refleja el nivel de formación y sensibilización en el uso responsable de agroquímicos. "},
        {"Dimensión": "Ambiental", "Indicador": "S-A-026 Uso de pesticida persistente", "ValorOriginal": 1, "Descripcion":"Este indicador evalúa si en la actividad agrícola se utilizan pesticidas con alta persistencia en el agua, definidos como aquellos cuya vida media en medio acuático es superior a 60 días. La presencia de este tipo de compuestos implica riesgos significativos para la salud humana, los organismos acuáticos y la calidad ambiental. "},
        {"Dimensión": "Ambiental", "Indicador": "S-A-030 Involucramiento ambiental", "ValorOriginal": -2, "Descripcion": "Este indicador mide el número de días en los que la organización participa activamente en iniciativas ambientales fuera de sus instalaciones, tales como reforestación, limpieza de ríos, educación ambiental o restauración ecológica. Evalúa el compromiso externo de la empresa con la sostenibilidad territorial. "},
        {"Dimensión": "Ambiental", "Indicador": "S-A-031 Uso de químicos crecimiento", "ValorOriginal": 1, "Descripcion": "Este indicador evalúa si en el proceso agrícola se utilizan o no reguladores de crecimiento sintéticos, como hormonas artificiales o estimulantes químicos. Su objetivo es promover prácticas agronómicas que respeten el equilibrio fisiológico natural de los cultivos. "},
        {"Dimensión": "Ambiental", "Indicador": "S-A-032 Cultivos híbridos", "ValorOriginal": -1, "Descripcion": "Este indicador identifica si en la unidad productiva se utilizan semillas híbridas en los cultivos principales. El uso de híbridos puede incrementar el rendimiento, pero también implica dependencia tecnológica y pérdida de diversidad genética en los agroecosistemas andinos. "},
        {"Dimensión": "Ambiental", "Indicador": "S-A-033 Manejo de franjas ribereñas", "ValorOriginal": -1, "Descripcion": "Este indicador evalúa si las franjas ribereñas zonas adyacentes a ríos, quebradas o canales están manejadas adecuadamente, sin intervención agrícola directa ni uso de fertilizantes o pesticidas. El objetivo es mantener su función ecológica como barreras naturales que protegen la calidad del agua y la biodiversidad. "},
        {"Dimensión": "Ambiental", "Indicador": "S-A-037 Quema de residuos", "ValorOriginal": 2, "Descripcion": "Este indicador evalúa si la organización agroproductiva realiza prácticas de quema de residuos, tanto agrícolas (rastrojos, podas, desechos de cosecha) como domésticos (plásticos, papel, restos orgánicos). La quema no controlada afecta negativamente la calidad del aire, el suelo y la salud humana, por lo cual se considera una práctica ambientalmente inadecuada."},
        {"Dimensión": "Ambiental", "Indicador": "S-A-042 Cultivos transgénicos", "ValorOriginal": 1, "Descripcion": "Este indicador determina si dentro de las parcelas agrícolas se cultivan especies transgénicas, es decir, organismos modificados genéticamente (OGM) mediante técnicas de ingeniería genética. Permite identificar el grado de adopción de tecnologías de alto impacto ecológico y normativo. "},
        {"Dimensión": "Ambiental", "Indicador": "S-A-047 Promoción organismos beneficiosos", "ValorOriginal": -1, "Descripcion": "Este indicador evalúa si en la unidad productiva se implementan prácticas para promover la presencia de organismos beneficiosos como insectos polinizadores, depredadores naturales de plagas, microorganismos del suelo, entre otros. Estas prácticas incluyen siembras asociadas, refugios naturales, reducción de pesticidas, y son clave para la sostenibilidad del agroecosistema."},
        {"Dimensión": "Ambiental", "Indicador": "S-A-048 Materiales reutilizables", "ValorOriginal": -1, "Descripcion": "Este indicador evalúa si la organización agroindustrial utiliza materiales de embalaje que pueden ser reutilizados múltiples veces, como cajas plásticas, canastillas retornables o recipientes reutilizables. El uso de este tipo de embalajes busca reducir los residuos sólidos, especialmente los plásticos de un solo uso, y avanzar hacia una producción más sostenible. "},
        {"Dimensión": "Ambiental", "Indicador": "SR-A-A-01 Tecnologías riego baja energía", "ValorOriginal": 1, "Descripcion": "Este indicador permite identificar si la unidad productiva emplea tecnologías de riego que requieren un bajo consumo energético, como sistemas por goteo o microaspersión. Su implementación mejora la eficiencia en el uso del agua y reduce la dependencia de fuentes energéticas convencionales, contribuyendo así a una producción más resiliente y sostenible. "},

        # --- DIMENSIÓN SOCIAL ---
        {"Dimensión": "Social", "Indicador": "S-S-03 Capacitación seguridad y salud", "ValorOriginal": -2, "Descripcion": "Este indicador mide el porcentaje del personal operativo y técnico de planta que ha recibido capacitación formal en temas de seguridad industrial y salud ocupacional durante el último año. Evalúa el compromiso de la organización con la prevención de riesgos laborales y el cumplimiento de normativas en ambientes agroindustriales. "},
        {"Dimensión": "Social", "Indicador": "S-S-019 Acceso a medios electrónicos", "ValorOriginal": 1, "Descripcion": "Este indicador mide el nivel de acceso que tienen los agricultores a medios electrónicos como celulares, computadoras, tabletas u otros dispositivos conectados, necesarios para acceder a información técnica, comercial o climática. Su monitoreo permite identificar brechas digitales que afectan la inclusión tecnológica del sector rural. "},
        {"Dimensión": "Social", "Indicador": "S-S-021 Disponibilidad tratamiento médico", "ValorOriginal": 2, "Descripcion": "Este indicador mide el porcentaje de agricultores que tienen acceso efectivo a servicios médicos o tratamiento en caso de enfermedad. Refleja la capacidad del entorno rural para responder a problemas de salud y representa un componente clave del bienestar social y la resiliencia familiar."},
        {"Dimensión": "Social", "Indicador": "S-S-022 Instalaciones sanitarias", "ValorOriginal": 2, "Descripcion": "Este indicador mide el porcentaje de agricultores que disponen de acceso regular a instalaciones sanitarias seguras, tales como baños conectados a red, letrinas mejoradas o unidades de saneamiento ecológico. Permite evaluar condiciones básicas de higiene en el entorno productivo rural. "},
        {"Dimensión": "Social", "Indicador": "S-S-034 Apoyo personas vulnerables", "ValorOriginal": -1, "Descripcion": "Este indicador evalúa si la agroindustria implementa o participa activamente en programas, proyectos o acciones que beneficien directamente a personas o grupos vulnerables de la comunidad (personas con discapacidad, adultos mayores, hogares monoparentales, migrantes, etc.). Se considera un componente clave de la inclusión social y la responsabilidad territorial. "},
        {"Dimensión": "Social", "Indicador": "S-S-041 Capacitación agrícola", "ValorOriginal": -2, "Descripcion": "Este indicador mide el porcentaje de agricultores que han recibido capacitación técnica agrícola durante el último año. Refleja el nivel de acceso a procesos formativos sobre buenas prácticas, tecnologías sostenibles, manejo agroecológico u otros conocimientos que fortalecen la capacidad productiva y la resiliencia del sistema agrícola. "},
    ]
    
    # Crear DataFrame
    df = pd.DataFrame(fixed_data)
    
    # Agregar la columna para el gráfico (Escala visual 1-5)
    df['ValorGrafico'] = df['ValorOriginal'] + 3
    
    return df

# Cargar datos
df_full = get_complete_data()

# ---------------------------------------------------------
# 2. BARRA LATERAL (FILTROS Y LEYENDA)
# ---------------------------------------------------------
st.sidebar.title('Panel de Control')

# Filtros
st.sidebar.header('Filtros')
dimension_options = ['Todas'] + list(df_full['Dimensión'].unique())
selected_dimension = st.sidebar.selectbox('Seleccionar Dimensión:', dimension_options)

if selected_dimension == 'Todas':
    df_filtered = df_full.copy()
    chart_title = "Visión General: Todas las Dimensiones"
else:
    df_filtered = df_full[df_full['Dimensión'] == selected_dimension].copy()
    chart_title = f"Análisis Detallado: Dimensión {selected_dimension}"

st.sidebar.markdown("---")

# Leyenda
st.sidebar.header('Leyenda de Evaluación')
legend_data = [
    {"Nivel": "Excelente", "Valor": 2, "Color": "ForestGreen"},
    {"Nivel": "Bueno", "Valor": 1, "Color": "LightGreen"},
    {"Nivel": "Estándar", "Valor": 0, "Color": "Yellow"},
    {"Nivel": "Bajo", "Valor": -1, "Color": "Orange"},
    {"Nivel": "Crítico", "Valor": -2, "Color": "Red"}
]

for item in legend_data:
    st.sidebar.markdown(
        f"""<div style="padding:4px; border-radius:4px; color:black; background-color:{item['Color']}; margin-bottom:4px; text-align:center; font-size:0.9em;">
            <strong>{item['Nivel']} ({item['Valor']})</strong>
        </div>""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. ÁREA PRINCIPAL
# ---------------------------------------------------------
st.title(f'📊 Estado del Caso de Estudio')
st.markdown(f"**Vista Actual:** {chart_title}")

# Métricas
m1, m2, m3 = st.columns(3)
promedio = df_filtered['ValorOriginal'].mean()
conteo_criticos = len(df_filtered[df_filtered['ValorOriginal'] <= -1])
mejor_ind_val = df_filtered.loc[df_filtered['ValorOriginal'].idxmax()]['Indicador']

#m2.metric("Promedio de Nivel", f"{promedio:.2f}")
m1.metric("Indicadores en Alerta", conteo_criticos)
#m3.metric("Mejor Desempeño", mejor_ind_val if len(mejor_ind_val) < 20 else mejor_ind_val[:17]+"...")

st.markdown("---")

col_charts_1, col_charts_2 = st.columns([2, 1])

# Escala de colores
color_scale = alt.Scale(
    domain=[-2, -1, 0, 1, 2],
    range=['Red', 'Orange', 'Yellow', 'LightGreen', 'ForestGreen']
)

with col_charts_1:
    st.subheader("Desempeño por Indicador")
    bar_chart = alt.Chart(df_filtered).mark_bar().encode(
        y=alt.Y('Indicador', sort=None, title=None),
        x=alt.X('ValorGrafico', title='Nivel (Escala 1-5)', scale=alt.Scale(domain=[0, 5])),
        color=alt.Color('ValorOriginal:N', scale=color_scale, legend=None),
        tooltip=['Dimensión', 'Indicador', 'ValorOriginal']
    ).properties(height=500)
    st.altair_chart(bar_chart, width="stretch")

with col_charts_2:
    st.subheader("Porcentaje de Desempeño")
    
    # 1. Preparar datos para el gráfico de pastel (Calcular %)
    pie_data = df_filtered['ValorOriginal'].value_counts().reset_index()
    pie_data.columns = ['ValorOriginal', 'Conteo']
    pie_data['Porcentaje'] = pie_data['Conteo'] / pie_data['Conteo'].sum()
    
    # 2. Base del gráfico con ORDEN explícito
    base = alt.Chart(pie_data).encode(
        theta=alt.Theta("Conteo", stack=True),
        # IMPORTANTE: Ordenar explícitamente por el valor para que coincida con el texto
        order=alt.Order("ValorOriginal", sort="descending"), 
        color=alt.Color("ValorOriginal:N", scale=color_scale, legend=alt.Legend(title="Nivel", orient="bottom"))
    )
    
    # 3. Arcos (Donut)
    pie = base.mark_arc(innerRadius=60) # Radio interno un poco más grande
    
    # 4. Texto con Porcentaje
    text = base.mark_text(radius=100,size=16).encode( # Radio ajustado para que quede dentro
        text=alt.Text("Porcentaje", format=".1%"), # Formato de porcentaje (ej: 25.0%)
        color=alt.value("black"),  # Negro para mejor contraste en amarillo/verde claro
        order=alt.Order("ValorOriginal", sort="descending") # EL MISMO ORDEN que el arco
    )
    
    # Tooltip para ver el conteo absoluto al pasar el mouse
    chart_final = (pie + text).encode(
        tooltip=["ValorOriginal", "Conteo", alt.Tooltip("Porcentaje", format=".1%")]
    )
    
    st.altair_chart(chart_final, width="stretch")


# ---------------------------------------------------------
# 4. TABLA DE DETALLES (Diseño Personalizado HTML/CSS)
# ---------------------------------------------------------
st.markdown("---")
st.subheader(f"Inventario de Indicadores (Mostrando: {len(df_filtered)})")

# 1. Preparar datos (Respetando filtros de la barra lateral)
# Seleccionamos las columnas de 'df_filtered'
# 'Descripcion' viene sin tilde en tus datos originales
df_tabla = df_filtered[["Dimensión", "Indicador", "Descripcion"]].copy()

# Renombramos para que el encabezado se vea bien (con tilde)
df_tabla.columns = ["Dimensión", "Indicador", "Descripción"]

# 2. Inyectar CSS (El estilo limpio que te gustó)
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
        border-bottom: 1px solid #444; /* Línea sutil separadora */
        padding: 10px;
        vertical-align: top; /* Texto alineado arriba */
        font-size: 14px;
    }
    /* Estilos Específicos por Columna (Anchos Fijos) */
    /* Columna 1 (Dimensión): 15% */
    table.customTable td:nth-child(1), table.customTable th:nth-child(1) { width: 15%; font-weight: bold; }
    /* Columna 2 (Indicador): 25% */
    table.customTable td:nth-child(2), table.customTable th:nth-child(2) { width: 25%; font-weight: 600; }
    /* Columna 3 (Descripción): 60% */
    table.customTable td:nth-child(3), table.customTable th:nth-child(3) { width: 60%; }
    
    /* Encabezado */
    table.customTable thead {
        background-color: transparent;
        border-bottom: 2px solid #4A90E2; /* Línea azul bajo titulos */
    }
    table.customTable th {
        text-transform: uppercase;
        font-size: 15px;
        color: #4A90E2;
        text-align: left;
    }
</style>
""", unsafe_allow_html=True)

# 3. Renderizar la tabla como HTML puro dentro del Expander
with st.expander("Ver Tabla de Datos Detallada", expanded=True):
    # Convertimos DF a HTML sin el índice molesto y aplicamos la clase 'customTable'
    html = df_tabla.to_html(index=False, classes="customTable", escape=False)
    st.markdown(html, unsafe_allow_html=True)
    