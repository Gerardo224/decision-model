# app.py
import streamlit as st
from perfil_basico import run_basico
from perfil_avanzado import run_avanzado

# Configuración de la página
st.set_page_config(page_title="SafeInvest", layout="wide")

# Inyectar CSS personalizado para fondo, textos, botones y recuadros
st.markdown(
    """
    <style>
    /* Fondo de la app */
    .stApp {
        background-color: #f0f2f6;
    }
    /* Colores de textos generales */
    h1, h2, h3, h4, h5, h6, p, label, div {
        color: #333333;
    }
    /* Estilo de los recuadros de perfiles */
    .perfil-caja {
        border: none;
        border-radius: 8px;
        padding: 16px;
        background-color: #ffffff;
        box-shadow: 6px 6px 16px rgba(0, 0, 0, 0.25);
    }
    /* Estilo de los botones */
    .stButton > button {
        background-color: #3b82f6 !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 8px 16px !important;
        font-weight: bold !important;
        cursor: pointer !important;
    }
    .stButton > button:hover {
        background-color: #2563eb !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicializar página en sesión
if "page" not in st.session_state:
    st.session_state.page = "Inicio"

# Página de inicio (landing)
def pagina_inicio():
    # Encabezado principal
    st.markdown(
        "<div style='background:#3b82f6;padding:20px;border-radius:8px;text-align:center'>"
        "<h1 style='color:white;font-family:Arial'>SafeInvest</h1>"
        "<p style='color:white;font-size:16px'>Una aplicación web para definir tu perfil inversor usando el método AHP.</p>"
        "</div><br>",
        unsafe_allow_html=True
    )

    # Descripción general
    st.markdown(
        "SafeInvest te ayuda a conocer tu perfil inversor a través de dos modos:\n"
        "- **Perfil Básico**: Compara criterios fijos y utiliza datos históricos para recomendar inversiones.\n"
        "- **Perfil Avanzado**: Selecciona criterios y alternativas dinámicamente y realiza comparaciones AHP completas."
    )
    st.markdown("---")

    # Contenedores para cada perfil
    col1, col2 = st.columns(2)

    # Perfil Básico
    with col1:
        st.markdown(
            "<div class='perfil-caja'>"
            "<h3 style='text-align:center;'>Perfil Básico</h3>"
            "<p>En este modo, compararás cuatro criterios fijos (Rentabilidad, Riesgo, Liquidez y Comisiones) y obtendrás recomendaciones basadas en datos históricos pre-cargados.</p>"
            "</div><br>",
            unsafe_allow_html=True
        )
        if st.button("Seleccionar Perfil Básico", key="btn_basico_landing"):
            st.session_state.page = "Perfil Básico"

    # Perfil Avanzado
    with col2:
        st.markdown(
            "<div class='perfil-caja'>"
            "<h3 style='text-align:center;'>Perfil Avanzado</h3>"
            "<p>En este modo, podrás seleccionar dinámicamente tus propios criterios y alternativas, realizando comparaciones AHP completas para obtener un ranking personalizado de inversiones.</p>"
            "</div><br>",
            unsafe_allow_html=True
        )
        if st.button("Seleccionar Perfil Avanzado", key="btn_avanzado_landing"):
            st.session_state.page = "Perfil Avanzado"

# Navegación interna entre secciones
def nav_buttons():
    if st.button("🔙 Volver al inicio", key="btn_volver_inicio"):
        st.session_state.page = "Inicio"
    st.markdown("---")

# Renderizado según página seleccionada
if st.session_state.page == "Inicio":
    pagina_inicio()
elif st.session_state.page == "Perfil Básico":
    nav_buttons()
    run_basico()
elif st.session_state.page == "Perfil Avanzado":
    nav_buttons()
    run_avanzado()