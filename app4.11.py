import streamlit as st
import pandas as pd
import io
import plotly.graph_objects as go

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Tablero de Escenarios Comparativos", layout="wide")

# ==========================================
# 2. DEFINICIÓN DE DATOS (MATRIZ 21x21)
# ==========================================

INDICADORES = [
    "S-A-024", "S-A-026", "S-A-030", "S-A-031", "S-A-032", 
    "S-A-033", "S-A-037", "S-A-042", "S-A-047", "S-A-048", 
    "SR-A-A-01", "S-E-07", "S-E-014", "S-E-016", "S-E-020", 
    "S-S-03", "S-S-019", "S-S-021", "S-S-022", "S-S-034", 
    "S-S-041"
]

# --- VALORES BASE FIJOS (SITUACIÓN ACTUAL) ---
VALORES_BASE = {
    "S-A-024": 1, "S-A-026": 4, "S-A-030": 1, "S-A-031": 4,
    "S-A-032": 2, "S-A-033": 2, "S-A-037": 4, "S-A-042": 4, 
    "S-A-047": 2, "S-A-048": 2, "SR-A-A-01": 4, "S-E-07": 1, 
    "S-E-014": 5, "S-E-016": 1, "S-E-020": 1, "S-S-03": 1, 
    "S-S-019": 4, "S-S-021": 5, "S-S-022": 5, "S-S-034": 1, 
    "S-S-041": 1
}

# Matriz 21x21 (Valores numéricos + Signos integrados)
DATOS_MATRIZ_CSV = """
Origen,S-A-024,S-A-026,S-A-030,S-A-031,S-A-032,S-A-033,S-A-037,S-A-042,S-A-047,S-A-048,SR-A-A-01,S-E-07,S-E-014,S-E-016,S-E-020,S-S-03,S-S-019,S-S-021,S-S-022,S-S-034,S-S-041
S-A-024,0,-3,2,-2,-1,1,-1,-1,1,2,0,1,1,1,0,0,1,1,1,0,2
S-A-026,3,0,-1,2,1,-2,1,1,-1,2,0,1,1,1,0,0,2,0,1,0,-1
S-A-030,2,-1,0,-1,-1,2,-2,-1,1,2,0,1,0,0,0,0,0,0,0,0,1
S-A-031,2,2,-1,0,2,-1,0,2,-1,0,0,0,2,0,0,0,1,0,0,0,-1
S-A-032,-1,0,-1,2,0,0,0,2,-1,1,0,0,2,1,0,0,0,0,0,0,-1
S-A-033,2,-2,2,-1,0,0,-1,-1,1,0,1,1,0,0,0,0,0,0,0,0,1
S-A-037,-1,1,-2,0,0,-1,0,1,-1,1,0,1,0,0,0,-1,0,0,0,0,-1
S-A-042,-1,1,-1,2,2,0,1,0,-1,0,0,0,2,0,1,-1,0,0,0,0,-1
S-A-047,1,1,1,-1,-2,1,0,-1,0,0,0,0,1,0,0,0,0,0,0,0,1
S-A-048,1,0,-1,0,0,0,-1,0,0,0,0,0,1,1,1,-1,0,0,0,0,0
SR-A-A-01,1,-1,-1,0,-1,1,0,-1,1,0,0,2,1,1,1,0,0,0,0,0,1
S-E-07,0,1,0,1,1,0,0,-1,1,1,1,0,0,3,2,-3,1,0,0,1,1
S-E-014,0,0,0,0,0,0,0,0,0,0,1,0,1,0,2,3,1,0,0,1,1
S-E-016,0,0,0,0,0,0,0,0,0,0,1,2,2,0,2,0,0,0,0,0,0
S-E-020,0,0,0,0,-1,-1,0,1,1,1,1,2,3,2,0,1,1,1,1,1,1
S-S-03,2,-2,1,-1,-1,1,-1,-1,0,1,0,1,1,1,0,0,1,1,2,1,1
S-S-019,1,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,0,0,0,0,1
S-S-021,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,2,1,0
S-S-022,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,1,0
S-S-034,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1
S-S-041,2,-2,1,-2,-1,1,-1,-2,1,1,1,2,-1,1,1,1,1,1,1,1,0
"""

# ==========================================
# 3. LÓGICA MAUT (AJUSTADA PARA RECIBIR SLIDERS)
# ==========================================

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

class ModeloSemaforizacion:
    def __init__(self):
        self.color_map = {
            1: "#D32F2F", 2: "#F57C00", 3: "#FBC02D", 4: "#388E3C", 5: "#1B5E20"
        }

    def get_interpolated_color(self, value):
        value = max(1.0, min(5.0, value))
        lower_idx = int(value)
        upper_idx = min(lower_idx + 1, 5)
        
        if lower_idx == 5: return self.color_map[5]
            
        fraction = value - lower_idx 
        rgb1 = hex_to_rgb(self.color_map[lower_idx])
        rgb2 = hex_to_rgb(self.color_map[upper_idx])
        new_rgb = tuple(int(rgb1[i] + (rgb2[i] - rgb1[i]) * fraction) for i in range(3))
        return rgb_to_hex(new_rgb)

    def normalizar_desempeno(self, D_i):
        return (D_i - 3) / 2.0

    def normalizar_peso(self, I_ij):
        return I_ij / 3.0

    def calcular_Dj_final(self, S_j, min_val=1, max_val=5, es_binario=False):
        if es_binario: return 5.0 if S_j > 0 else 1.0
        val = (2 * S_j) + 3
        return max(float(min_val), min(float(max_val), val))

def cargar_relaciones_desde_csv(csv_str):
    try:
        df = pd.read_csv(io.StringIO(csv_str), index_col="Origen")
        relaciones = []
        for origen in df.index:
            for destino in df.columns:
                valor = df.loc[origen, destino]
                if valor != 0:
                    relaciones.append({
                        "origen": origen, "destino": destino,
                        "Iij": abs(valor), "signo": 1 if valor > 0 else -1
                    })
        return relaciones
    except Exception as e:
        st.error(f"Error al leer matriz: {e}")
        return []

RELACIONES = cargar_relaciones_desde_csv(DATOS_MATRIZ_CSV)
RESTRICCIONES_RANGO = {"S-A-031": (2, 4), "S-A-037": (2, 4),"S-R-A-A-01": (3, 4),}
INDICADORES_BINARIOS = [""]

# ==========================================
# 4. VISUALIZACIÓN
# ==========================================

def crear_grafico_lineas_comparativo(nombres, valores_base, valores_simulados):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=nombres, y=valores_base, name='Situación Actual (Fija)',
        mode='lines+markers', line=dict(color='gray', dash='dash', width=2),
        marker=dict(size=6), hovertemplate='%{y:.2f}'
    ))
    fig.add_trace(go.Scatter(
        x=nombres, y=valores_simulados, name='Escenario Simulado',
        mode='lines+markers', line=dict(color='#1E88E5', width=3),
        marker=dict(size=8), hovertemplate='%{y:.2f}'
    ))
    fig.update_layout(
        title="Comparativa: Actualidad vs. Simulación",
        # EJE Y CONFIGURADO PARA MOSTRAR SOLO 1, 2, 3, 4, 5
        yaxis=dict(
            title="Nivel (1-5)", 
            range=[0.9, 5.1],       # Rango ajustado para que no se vea el 0.5 ni el 5.5
            tickvals=[1, 2, 3, 4, 5], # Forzamos a que solo muestre enteros
            dtick=1
        ),
        legend=dict(orientation="h", y=1.15, x=0.5, xanchor="left"),
        height=600, margin=dict(l=20, r=20, t=140, b=100), xaxis=dict(tickangle=-45)
    )
    return fig

def crear_grafico_barras_horizontales(nombres, valores_simulados, colores):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=valores_simulados, y=nombres, orientation='h',
        marker=dict(color=colores, line=dict(color='rgba(0,0,0,0.1)', width=1)),
        text=valores_simulados, texttemplate='%{x:.2f}', textposition='auto'
    ))
    
    # LÍNEAS VERTICALES DE COLOR AZUL
    for i in range(1, 6):
        fig.add_shape(
            type="line", x0=i, y0=-0.5, x1=i, y1=len(nombres)-0.5,
            # Color azul (#1E88E5) con transparencia para el grid
            line=dict(color="rgba(30, 136, 229, 0.6)", width=2, dash="dot"), 
            layer="above"
        )
        
    fig.update_layout(
        title="Estado del Escenario",
        xaxis=dict(range=[0, 5.5], showgrid=False, title="Nivel",
            tickmode='array', tickvals=[0, 1, 2, 3, 4, 5], ticktext=['0', '1', '2', '3', '4', '5']),
        yaxis=dict(autorange="reversed"), height=600, margin=dict(l=10, r=10, t=50, b=50)
    )
    return fig

# ==========================================
# 5. GESTIÓN DE ESTADO (RESET Y LÓGICA)
# ==========================================

def reiniciar_sliders():
    st.session_state['slider_activo'] = None
    for ind in INDICADORES:
        if ind in VALORES_BASE:
            st.session_state[f"in_{ind}"] = VALORES_BASE[ind]

def bloquear_otros(nombre_indicador):
    st.session_state['slider_activo'] = nombre_indicador

# ==========================================
# 6. APP PRINCIPAL
# ==========================================

def main():
    st.title("📊 Simulador de Escenarios Estratégicos")
    modelo = ModeloSemaforizacion()

    # --- INICIALIZACIÓN DE ESTADO ---
    if 'init_done' not in st.session_state:
        for ind in INDICADORES:
            st.session_state[f"in_{ind}"] = VALORES_BASE.get(ind, 1)
        st.session_state['init_done'] = True
        st.session_state['slider_activo'] = None

    # --- SIDEBAR ---
    st.sidebar.header("🎚️ Controles")
    if st.sidebar.button("🔄 Reiniciar Escenario"):
        reiniciar_sliders()
        st.rerun()

    st.sidebar.info("Ajusta un indicador para simular su impacto.")
    
    valores_simulados_input = {}
    
    for indicador in INDICADORES:
        val = st.sidebar.slider(
            f"{indicador}", 1, 5, 
            key=f"in_{indicador}",
            on_change=bloquear_otros, args=(indicador,)
        )
        valores_simulados_input[indicador] = val

    # --- CÁLCULO DE PROPAGACIÓN ---
    lista_nombres = INDICADORES
    lista_base = [VALORES_BASE[k] for k in INDICADORES]
    lista_simulados = []
    lista_colores = []

    for destino in INDICADORES:
        base_val = VALORES_BASE[destino]
        base_norm = modelo.normalizar_desempeno(base_val)

        input_usuario = valores_simulados_input[destino]
        delta_propio = modelo.normalizar_desempeno(input_usuario) - base_norm

        impacto_red = 0.0
        entrantes = [r for r in RELACIONES if r['destino'] == destino]
        
        for r in entrantes:
            origen = r['origen']
            input_origen = valores_simulados_input[origen]
            base_origen = VALORES_BASE[origen]
            delta_origen = modelo.normalizar_desempeno(input_origen) - modelo.normalizar_desempeno(base_origen)
            
            if delta_origen != 0:
                w_ij = modelo.normalizar_peso(r['Iij'])
                impacto = delta_origen * w_ij * r['signo']
                impacto_red += impacto

        s_j_final = base_norm + delta_propio + impacto_red
        
        es_binario = destino in INDICADORES_BINARIOS
        r_min, r_max = RESTRICCIONES_RANGO.get(destino, (1, 5))
        
        val_final = modelo.calcular_Dj_final(s_j_final, r_min, r_max, es_binario)
        
        lista_simulados.append(val_final)
        lista_colores.append(modelo.get_interpolated_color(val_final))

    # --- VISUALIZACIÓN ---
    col_izq, col_der = st.columns([2, 1])

    with col_izq:
        st.subheader("Comparativa de Tendencias")
        fig_lineas = crear_grafico_lineas_comparativo(lista_nombres, lista_base, lista_simulados)
        st.plotly_chart(fig_lineas, width="stretch", config={'displayModeBar': False})

    with col_der:
        st.subheader("Detalle del Escenario")
        fig_barras = crear_grafico_barras_horizontales(lista_nombres, lista_simulados, lista_colores)
        st.plotly_chart(fig_barras, width="stretch", config={'displayModeBar': False})

    with st.expander("Ver Datos en Tabla"):
        df_resumen = pd.DataFrame({
            "Indicador": lista_nombres, "Base": lista_base, "Simulado": lista_simulados,
            "Diferencia": [s - b for s, b in zip(lista_simulados, lista_base)]
        })
        st.dataframe(df_resumen.style.map(lambda x: 'color: red' if x < 0 else ('color: green' if x > 0 else ''), subset=['Diferencia']))

if __name__ == "__main__":
    main()