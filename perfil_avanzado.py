# perfil_avanzado.py
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px


def run_avanzado():
    st.header("🚀 Perfil Avanzado – AHP Dinámico con Detalles de Cálculo")

    # Selección de criterios y alternativas
    todos_crit = ["Rentabilidad","Riesgo","Liquidez","Comisiones","Horizonte"]
    criterios = st.multiselect("Elige tus criterios (al menos 2):", todos_crit)
    todas_alt = ["Acciones","Bonos","ETFs","Criptomonedas","Fondos indexados","Bienes raíces"]
    alternativas = st.multiselect("Elige tus alternativas (al menos 2):", todas_alt)

    if len(criterios) < 2 or len(alternativas) < 2:
        st.warning("Selecciona al menos 2 criterios y 2 alternativas para continuar.")
        return

    # -------------------------
    # 1) Comparación AHP de criterios
    # -------------------------
    st.subheader("1) Matriz de comparación de criterios")
    n = len(criterios)
    Mc = np.ones((n, n))

    # Rellenar la parte superior de la matriz con inputs
    for i in range(n):
        for j in range(i+1, n):
            c_i, c_j = criterios[i], criterios[j]
            st.markdown(f"**Criterio {i+1} vs {j+1}: {c_i} vs {c_j}**")
            choice = st.radio("¿Qué criterio es más importante?", [c_i, c_j], key=f"crit_pref_{i}_{j}", horizontal=True)
            intensidad = st.slider("Intensidad (1=igual, 9=muy fuerte)", 1, 9, 1, key=f"crit_int_{i}_{j}")
            if choice == c_i:
                Mc[i, j], Mc[j, i] = intensidad, 1/intensidad
            else:
                Mc[i, j], Mc[j, i] = 1/intensidad, intensidad

    # Mostrar matriz cruda
    df_Mc = pd.DataFrame(Mc, index=criterios, columns=criterios)
    st.write("**Matriz comparativa de criterios**")
    st.dataframe(df_Mc)

    # Normalización por columnas y cálculo de pesos
    col_sum = Mc.sum(axis=0)
    Mc_norm = Mc / col_sum
    df_Mc_norm = pd.DataFrame(Mc_norm, index=criterios, columns=criterios)
    st.write("**Matriz de criterios normalizada (dividiendo por suma de columnas)**")
    st.dataframe(df_Mc_norm)

    pesos_crit = Mc_norm.mean(axis=1)
    df_pesos_crit = pd.DataFrame({"Peso criterio": pesos_crit}, index=criterios)
    st.write("**Pesos de cada criterio (promedio de filas)**")
    st.dataframe(df_pesos_crit)

    # -------------------------
    # 2) Comparación AHP de alternativas para cada criterio
    # -------------------------
    st.subheader("2) Matrices AHP de alternativas por criterio")
    m = len(alternativas)
    pesos_alt = {}

    for ci, crit in enumerate(criterios):
        st.markdown(f"---\n### Matriz para el criterio: {crit}")
        Ma = np.ones((m, m))
        for i in range(m):
            for j in range(i+1, m):
                a_i, a_j = alternativas[i], alternativas[j]
                st.markdown(f"**{a_i} vs {a_j}**")
                choice_a = st.radio("¿Cuál alternativa es mejor?", [a_i, a_j], key=f"alt_pref_{crit}_{i}_{j}", horizontal=True)
                val = st.slider("Intensidad (1-9)", 1, 9, 1, key=f"alt_int_{crit}_{i}_{j}")
                if choice_a == a_i:
                    Ma[i, j], Ma[j, i] = val, 1/val
                else:
                    Ma[i, j], Ma[j, i] = 1/val, val

        # Mostrar matriz cruda de alternativas
        df_Ma = pd.DataFrame(Ma, index=alternativas, columns=alternativas)
        st.write(f"**Matriz comparativa cruda para {crit}**")
        st.dataframe(df_Ma)

        # Normalizar por columnas y pesos locales
        sum_cols = Ma.sum(axis=0)
        Ma_norm = Ma / sum_cols
        df_Ma_norm = pd.DataFrame(Ma_norm, index=alternativas, columns=alternativas)
        st.write(f"**Matriz normalizada para {crit}**")
        st.dataframe(df_Ma_norm)

        pesos_loc = Ma_norm.mean(axis=1)
        pesos_alt[crit] = pesos_loc
        df_pesos_loc = pd.DataFrame({f"Peso local ({crit})": pesos_loc}, index=alternativas)
        st.write(f"**Pesos locales para {crit} (promedio de filas)**")
        st.dataframe(df_pesos_loc)

    # -------------------------
    # 3) Agregación de resultados y puntuación final
    # -------------------------
    st.subheader("3) Agregación y score final de alternativas")
    df_final = pd.DataFrame({"Alternativa": alternativas})
    total_score = np.zeros(m)
    for ci, crit in enumerate(criterios):
        df_final[crit] = pesos_alt[crit]
        total_score += pesos_crit[ci] * pesos_alt[crit]

    df_final["Score"] = total_score
    df_final = df_final.set_index("Alternativa")[ [*criterios, "Score"] ]
    st.write("**Tabla final con scores and desglose de pesos**")
    st.dataframe(df_final)

    # Mostrar ranking
    st.success(f"La mejor alternativa es **{df_final['Score'].idxmax()}** con score {df_final['Score'].max():.4f}")
    fig = px.bar(df_final.sort_values("Score", ascending=False).reset_index(), x="Alternativa", y="Score", title="Ranking final de alternativas", text_auto=".4f")
    st.plotly_chart(fig, use_container_width=True)