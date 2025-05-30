import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Predicción de Partidos", layout="centered")

st.title("🔮 Predicción de Resultados de Fútbol")
st.write("Simulación por modelo Poisson y Monte Carlo (10,000 repeticiones)")

# Inputs
team_home = st.text_input("Equipo Local", "Real Madrid")
team_away = st.text_input("Equipo Visitante", "Girona")

avg_home = st.slider("Promedio de goles esperados del local", 0.0, 5.0, 2.1)
avg_away = st.slider("Promedio de goles esperados del visitante", 0.0, 5.0, 1.3)

if st.button("Predecir"):
    # Simulación
    sim_home = np.random.poisson(avg_home, 10000)
    sim_away = np.random.poisson(avg_away, 10000)
    df = pd.DataFrame({"Local": sim_home, "Visitante": sim_away})

    # Resultados
    home_win = (df["Local"] > df["Visitante"]).mean()
    away_win = (df["Visitante"] > df["Local"]).mean()
    draw = (df["Local"] == df["Visitante"]).mean()
    over_2_5 = (df["Local"] + df["Visitante"] > 2.5).mean()
    btts = ((df["Local"] > 0) & (df["Visitante"] > 0)).mean()
    avg_score_home = df["Local"].mean()
    avg_score_away = df["Visitante"].mean()

    # Mostrar resultados
    st.subheader("📊 Resultados de la Simulación")
    st.markdown(f"""
    - ⚽ **Promedio de goles esperados:** {team_home} {avg_score_home:.2f} - {avg_score_away:.2f} {team_away}  
    - 🏆 **Probabilidad de victoria local ({team_home}):** {home_win:.2%}  
    - 🤝 **Probabilidad de empate:** {draw:.2%}  
    - 🚩 **Probabilidad de victoria visitante ({team_away}):** {away_win:.2%}  
    - 🔥 **Probabilidad +2.5 goles:** {over_2_5:.2%}  
    - 🎯 **Probabilidad ambos marcan (BTTS):** {btts:.2%}
    """)

    # Cuotas justas
    st.subheader("💰 Cuotas Justas (Fair Odds)")
    def fair_odds(prob):
        return round(1 / prob, 2) if prob > 0 else "-"

    st.write(f"🏆 1 (local): {fair_odds(home_win)}")
    st.write(f"🤝 X (empate): {fair_odds(draw)}")
    st.write(f"🚩 2 (visita): {fair_odds(away_win)}")
    st.write(f"🔥 +2.5 goles: {fair_odds(over_2_5)}")
    st.write(f"🎯 Ambos marcan: {fair_odds(btts)}")
