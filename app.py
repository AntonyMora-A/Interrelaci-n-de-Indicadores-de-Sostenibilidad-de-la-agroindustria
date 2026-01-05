import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Mi Super App Unificada", layout="wide")

# Definir las páginas apuntando a tus archivos existentes
pg1 = st.Page("app5.6.py", title="Análisis MICMAC", icon="📈")
pg2 = st.Page("app3.4.py", title="Estado Actual", icon="⚙️")
pg3 = st.Page("app4.11.py", title="Simulación de Escenarios", icon="💰")

# Crear la navegación
pg = st.navigation([pg1, pg2, pg3])

# Ejecutar la navegación
pg.run()
