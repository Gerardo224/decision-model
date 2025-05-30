import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

def run_avanzado():
    st.header("🚀 Perfil Avanzado – AHP Dinámico")

    # Llista de criteris negatius (menys és millor)
    criterios_negativos = ["Riesgo", "Comisiones", "Horizonte"]

    # Selección de criterios y alternativas
    todos_crit = ["Rentabilidad","Riesgo","Liquidez","Comisiones","Horizonte"]
    criterios = st.multiselect("Elige tus criterios (al menos 2):", todos_crit)
    todas_alt = ["Acciones","Bonos","ETFs","Criptomonedas","Fondos indexados","Bienes raíces"]
    alternativas = st.multiselect("Elige tus alternativas (al menos 2):", todas_alt)

    if len(criterios) < 2 or len(alternativas) < 2:
        st.warning("Selecciona al menos 2 criterios y 2 alternativas para continuar.")
        return

    # 1) Comparación AHP de criterios
    st.subheader("1) Comparación de criterios")
    n = len(criterios)
    Mc = np.ones((n, n))
    for i in range(n):
        for j in range(i+1, n):
            c_i, c_j = criterios[i], criterios[j]
            st.markdown(f"**{c_i} vs {c_j}**")
            choice = st.radio("¿Qué criterio es más importante?", [c_i, c_j], key=f"crit_pref_{i}_{j}", horizontal=True)
            intensidad = st.slider("Indique la intensidad de la preferencia (1=igual, 9=muy fuerte)", 1, 9, 1, key=f"crit_int_{i}_{j}")
            if choice == c_i:
                Mc[i, j], Mc[j, i] = intensidad, 1/intensidad
            else:
                Mc[i, j], Mc[j, i] = 1/intensidad, intensidad

    # Cálculo de pesos de criterios
    pesos_crit = (Mc / Mc.sum(axis=0)).mean(axis=1)

    # 2) Comparación AHP de alternativas
    st.subheader("2) Comparación de alternativas")
    m = len(alternativas)
    pesos_alt = {}
    for ci, crit in enumerate(criterios):
        st.markdown(f"### {crit}")
        Ma = np.ones((m, m))
        for i in range(m):
            for j in range(i+1, m):
                a_i, a_j = alternativas[i], alternativas[j]
                st.markdown(f"**{a_i} vs {a_j}**")
                choice_a = st.radio("¿Cuál alternativa es mejor?", [a_i, a_j], key=f"alt_pref_{crit}_{i}_{j}", horizontal=True)
                val = st.slider("Indique la intensidad de la preferencia (1-9)", 1, 9, 1, key=f"alt_int_{crit}_{i}_{j}")

                if crit in criterios_negativos:
                    # Invertir la lògica per criteris negatius
                    if choice_a == a_i:
                        Ma[i, j], Ma[j, i] = 1/val, val
                    else:
                        Ma[i, j], Ma[j, i] = val, 1/val
                else:
                    # Criteri positiu (com Rentabilitat o Liquiditat)
                    if choice_a == a_i:
                        Ma[i, j], Ma[j, i] = val, 1/val
                    else:
                        Ma[i, j], Ma[j, i] = 1/val, val

        # Pesos locals
        pesos_alt[crit] = (Ma / Ma.sum(axis=0)).mean(axis=1)

    # 3) Agregación y puntuación final
    st.subheader("3) Ranking final de alternativas")
    df_final = pd.DataFrame({"Alternativa": alternativas})
    total_score = np.zeros(m)
    for ci, crit in enumerate(criterios):
        df_final[crit] = pesos_alt[crit]
        total_score += pesos_crit[ci] * pesos_alt[crit]
    df_final["Score"] = total_score
    df_final = df_final.set_index("Alternativa")

    # Mostrar resultado y gráficos
    mejor = df_final['Score'].idxmax()
    valor = df_final['Score'].max()
    st.success(f"La mejor alternativa es **{mejor}** con score {valor:.4f}")

    # Visualización en columnas
    col1, col2 = st.columns(2)

    fig_bar = px.bar(
        df_final.sort_values("Score", ascending=False).reset_index(),
        x="Alternativa", y="Score", title="Ranking final de alternativas", text_auto=".4f", template="plotly_white"
    )
    fig_bar.update_layout(
        paper_bgcolor='white', plot_bgcolor='white', font=dict(color='black'), title_font=dict(color='black')
    )
    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)

    fig_pie = px.pie(
        df_final.reset_index(), names="Alternativa", values="Score", title="Distribución de Score", template="plotly_white"
    )
    fig_pie.update_layout(
        paper_bgcolor='white', plot_bgcolor='white', font=dict(color='black'), title_font=dict(color='black')
    )
    with col2:
        st.plotly_chart(fig_pie, use_container_width=True)
