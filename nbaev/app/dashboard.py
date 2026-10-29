"""Dashboard opcional en Streamlit: streamlit run nbaev/app/dashboard.py

Filtros por fecha, mercado, partido y jugador sobre las tablas que exporta `python -m nbaev diario`, más el
registro de apuestas, la banca y el estado de validación de cada mercado.
"""
from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st

RAIZ = Path(__file__).resolve().parents[2]
CARPETA = RAIZ / "reportes" / "diario"
DB = RAIZ / "data" / "nbaev.duckdb"

st.set_page_config(page_title="Props NBA", layout="wide")
st.title("Props NBA: probabilidad, valor y banca")
st.caption("Solo los mercados validados por el backtest reciben monto. Las apuestas implican riesgo de perder dinero.")

archivos = sorted(CARPETA.glob("*.csv"), reverse=True)
if not archivos:
    st.info("Aún no hay tablas diarias: ejecuta `python -m nbaev diario`.")
    st.stop()

fecha = st.sidebar.selectbox("Fecha", [a.stem for a in archivos])
t = pd.read_csv(CARPETA / f"{fecha}.csv")
mercados = st.sidebar.multiselect("Mercado", sorted(t["mercado"].unique()))
partidos = st.sidebar.multiselect("Partido", sorted(t["partido"].dropna().unique()))
jugador = st.sidebar.text_input("Jugador contiene")
solo_picks = st.sidebar.checkbox("Solo picks", value=False)
ev_min = st.sidebar.slider("EV mínimo", -0.2, 0.3, 0.0, 0.01)

f = t[t["EV"] >= ev_min]
if mercados:
    f = f[f["mercado"].isin(mercados)]
if partidos:
    f = f[f["partido"].isin(partidos)]
if jugador:
    f = f[f["jugador"].str.contains(jugador, case=False, na=False)]
if solo_picks:
    f = f[f["pick"]]

c1, c2, c3 = st.columns(3)
c1.metric("Líneas", len(f))
c2.metric("Picks", int(f["pick"].sum()))
c3.metric("Monto sugerido total", f"{f['monto sugerido'].sum():,.2f}")
st.dataframe(f.sort_values("EV", ascending=False), width="stretch", hide_index=True)

if DB.exists():
    try:
        con = duckdb.connect(str(DB), read_only=True)
        st.subheader("Estado de los mercados")
        st.dataframe(con.execute("SELECT * FROM market_validation").df(), hide_index=True)
        st.subheader("Registro de apuestas")
        ap = con.execute("SELECT * FROM apuestas ORDER BY id DESC").df()
        st.dataframe(ap, hide_index=True)
        conf = ap[(ap["estado"] == "confirmada") & (ap["resultado"] != "pendiente")].sort_values("liquidada_at")
        if not conf.empty:
            st.line_chart(conf.set_index("liquidada_at")["ganancia"].cumsum(), y_label="ganancia acumulada")
    except duckdb.IOException:
        st.warning("La base está en uso por otro proceso; vuelve a cargar en unos segundos.")
