# perfil_basico.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def run_basico():
    # Header estilitzat amb ombra
    with st.container():
        st.markdown(
            """
            <div style='background-color: #f9f9f9; padding: 1rem; border-radius: 0.5rem;
                        box-shadow: 4px 4px 10px rgba(0,0,0,0.25);'>
                <h2 style='text-align:center; font-family: "Segoe UI", sans-serif;'>📊 Perfil Básico - AHP con Datos Históricos</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Espai abans de la primera pregunta
    st.markdown("<br>", unsafe_allow_html=True)

    # 1. Comparación fija de criterios
    criterios = ["Rentabilidad", "Riesgo", "Liquidez", "Horizonte temporal"]
    pares = [(criterios[i], criterios[j]) for i in range(len(criterios)) for j in range(i+1, len(criterios))]
    prefs, ints = {}, {}
    for idx, (a, b) in enumerate(pares, 1):
        st.markdown(f"**{idx}. {a} vs {b}**")
        prefs[(a, b)] = st.radio("¿Cuál pesa más?", [a, b], key=f"b_pref_{idx}", horizontal=True)
        ints[(a, b)] = st.slider("Intensidad (1-9)", 1, 9, 1, key=f"b_int_{idx}")
        st.markdown("---")  # Separador visual entre preguntas

    # Botón para calcular
    if st.button("Mostrar resultados"):
        # 2. Construir matriz
        M = np.ones((4, 4))
        idx_map = {c: i for i, c in enumerate(criterios)}
        for (a, b), pref in prefs.items():
            i, j = idx_map[a], idx_map[b]
            v = ints[(a, b)]
            if pref == a:
                M[i, j], M[j, i] = v, 1 / v
            else:
                M[i, j], M[j, i] = 1 / v, v

        # 3. Normalizar y pesos
        col_sum = M.sum(axis=0)
        norm = M / col_sum
        pesos = norm.mean(axis=1)
        st.write("### Pesos de criterios", dict(zip(criterios, np.round(pesos, 3))))

        # 4. Datos históricos y score
        df = pd.read_csv("data/inversiones.csv")
        df["rent_norm"] = df["Rentabilidad"] / df["Rentabilidad"].max()
        df["risk_norm"] = df["Riesgo"].min() / df["Riesgo"]
        df["liq_norm"] = df["Liquidez"] / df["Liquidez"].max()
        df["horiz_norm"] = df["Horizonte temporal"] / df["Horizonte temporal"].max()

        df["score"] = (
            df["rent_norm"] * pesos[idx_map["Rentabilidad"]] +
            df["risk_norm"] * pesos[idx_map["Riesgo"]] +
            df["liq_norm"] * pesos[idx_map["Liquidez"]] +
            df["horiz_norm"] * pesos[idx_map["Horizonte temporal"]]
        )
        best = df.loc[df["score"].idxmax()]

        # 5. Guardar y mostrar resultados
        st.session_state.df_resultados = df
        st.session_state.pesos_criterios = dict(zip(criterios, pesos))

        # 💡 Recomanació estilitzada
        st.markdown(
            f"""
            <div style='
                background-color: #d4edda;
                color: #155724;
                padding: 1rem;
                border-radius: 0.5rem;
                font-family: "Segoe UI", sans-serif;
                font-size: 18px;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
                margin-top: 1rem;
            '>
                <strong>✅ Recomendación:</strong> {best['Nombre']} (score {best['score']:.3f})
            </div>
            """,
            unsafe_allow_html=True
        )

        # 6. Gráficos visuales
        col1, col2 = st.columns(2)

        with col1:
            fig_bar = px.bar(
                df.sort_values("score", ascending=False),
                x="Nombre", y="score", title="Ranking de Inversiones",
                text_auto=".3f", template="plotly_white"
            )
            fig_bar.update_layout(
                paper_bgcolor='white',
                plot_bgcolor='white',
                font=dict(color='black'),
                title_font=dict(color='black')
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            fig_pie = px.pie(
                df, names="Nombre", values="score",
                title="Distribución de Score", template="plotly_white"
            )
            fig_pie.update_layout(
                paper_bgcolor='white',
                plot_bgcolor='white',
                font=dict(color='black'),
                title_font=dict(color='black')
            )
            st.plotly_chart(fig_pie, use_container_width=True)
