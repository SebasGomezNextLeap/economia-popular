"""
Dashboard de Perfilamiento de Clientes - MVP Crédito Economía Popular - ESAL
Contrasta perfil 'Invisible' con potencial de pago mediante variables alternativas.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

from data.synthetic_data import (
    generar_solicitantes,
    generar_ingresos_estacionales,
    datos_radar_perfiles,
    OFICIOS,
    GENEROS,
    ZONAS,
)

# ============ CONFIGURACIÓN Y TEMA ============
# Paleta: terrosos, verdes, azules (sin rojo para no estigmatizar)
COLORES = {
    "terroso_oscuro": "#5C4033",
    "terroso_medio": "#8B7355",
    "terroso_claro": "#C4A77D",
    "verde_oscuro": "#2D5A27",
    "verde_medio": "#4A7C59",
    "verde_claro": "#6B8E6B",
    "azul_oscuro": "#2C5282",
    "azul_medio": "#3182CE",
    "azul_claro": "#63B3ED",
    "fondo_claro": "#F5F0E8",
    "texto": "#2D3748",
}

st.set_page_config(
    page_title="Perfilamiento Economía Popular - ESAL",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    /* Tema cálido y profesional */
    .stApp { background-color: #F5F0E8; }
    h1, h2, h3 { color: #2D5A27; font-family: 'Segoe UI', sans-serif; }
    .kpi-card {
        background: linear-gradient(135deg, #F5F0E8 0%, #E8E0D5 100%);
        border: 1px solid #C4A77D;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(92, 64, 51, 0.08);
    }
    .kpi-val { font-size: 1.8rem; font-weight: 700; color: #2C5282; }
    .kpi-label { font-size: 0.85rem; color: #5C4033; margin-top: 0.25rem; }
    .stMetric label { color: #5C4033 !important; }
    div[data-testid="stSidebar"] { background-color: #EDE8E0; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============ CARGA DE DATOS ============
@st.cache_data
def cargar_datos():
    df = generar_solicitantes(500)
    ingresos = generar_ingresos_estacionales(90)
    return df, ingresos

df_raw, df_ingresos = cargar_datos()

# ============ SIDEBAR - FILTROS ============
st.sidebar.header("🔍 Segmentación")
st.sidebar.markdown("Filtre por perfil para análisis detallado.")

oficio_sel = st.sidebar.multiselect("Oficio", options=OFICIOS, default=OFICIOS)
genero_sel = st.sidebar.multiselect("Género", options=GENEROS, default=GENEROS)
zona_sel = st.sidebar.multiselect("Zona geográfica", options=ZONAS, default=ZONAS)

df = df_raw[
    df_raw["oficio"].isin(oficio_sel)
    & df_raw["genero"].isin(genero_sel)
    & df_raw["zona"].isin(zona_sel)
].copy()

if df.empty:
    st.warning("No hay registros con los filtros seleccionados. Ajuste criterios.")
    st.stop()

# ============ KPIs PRINCIPALES ============
st.title("📊 Dashboard de Perfilamiento - Economía Popular - ESAL")
st.caption("Contraste perfil 'Invisible' vs potencial de pago con variables alternativas")

k1, k2, k3 = st.columns(3)
with k1:
    arraigo_prom = df["puntaje_arraigo"].mean()
    st.metric(
        label="Puntaje de Arraigo",
        value=f"{arraigo_prom:.1f} años",
        delta="Promedio años en actividad/vivienda",
        help="Indicador clave: tiempo en el lugar como predictor de pago.",
    )
with k2:
    densidad_red = df["avales_comunitarios"].mean()
    st.metric(
        label="Densidad de Red",
        value=f"{densidad_red:.1f}",
        delta="Avales comunitarios por solicitante",
        help="Respaldo social y capital comunitario.",
    )
with k3:
    formalidad = df["formalidad_relativa_pct"].mean()
    st.metric(
        label="Índice de Formalidad Relativa",
        value=f"{formalidad:.1f}%",
        delta="Servicios a nombre o billetera digital",
        help="Trazabilidad de ingresos y compromisos.",
    )

st.divider()

# ============ RADAR: BANCARIZADO vs ECONOMÍA POPULAR ============
st.subheader("Perfil Bancarizado vs Economía Popular - ESAL")
radar_data = datos_radar_perfiles()

fig_radar = go.Figure()
fig_radar.add_trace(
    go.Scatterpolar(
        r=radar_data["perfil_bancarizado"],
        theta=radar_data["variables"],
        fill="toself",
        name="Perfil bancarizado típico",
        line_color=COLORES["azul_medio"],
        fillcolor="rgba(49, 130, 206, 0.3)",
    )
)
fig_radar.add_trace(
    go.Scatterpolar(
        r=radar_data["perfil_economia_popular"],
        theta=radar_data["variables"],
        fill="toself",
        name="Perfil economía popular - ESAL",
        line_color=COLORES["verde_medio"],
        fillcolor="rgba(74, 124, 89, 0.3)",
    )
)
fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(color=COLORES["texto"]))),
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=COLORES["texto"], size=12),
    margin=dict(t=80, b=60),
    height=420,
)
st.plotly_chart(fig_radar, use_container_width=True)

st.info(
    "**Variables del radar:** Historial crediticio, antigüedad en el oficio, respaldo comunitario, "
    "frecuencia de ingresos (caja diaria) y garantías líquidas. El perfil de economía popular - ESAL destaca en arraigo y red."
)

st.divider()

# ============ HISTOGRAMA INGRESOS - ESTACIONALIDAD ============
st.subheader("Distribución y estacionalidad de ingresos")
st.caption("Picos diarios/semanales vs flujo mensual tradicional (datos sintéticos)")

# Histograma de ingresos diarios
fig_hist = go.Figure()
fig_hist.add_trace(
    go.Histogram(
        x=df_ingresos["ingreso_diario"],
        nbinsx=35,
        name="Frecuencia",
        marker_color=COLORES["verde_medio"],
        opacity=0.85,
    )
)
fig_hist.update_layout(
    xaxis_title="Ingreso diario (simulado)",
    yaxis_title="Frecuencia (días)",
    bargap=0.15,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=COLORES["texto"]),
    showlegend=False,
    height=360,
)
st.plotly_chart(fig_hist, use_container_width=True)

# Serie temporal para ver picos semanales/quincenales
fig_ts = go.Figure()
fig_ts.add_trace(
    go.Scatter(
        x=df_ingresos["fecha"],
        y=df_ingresos["ingreso_diario"],
        mode="lines",
        line=dict(color=COLORES["azul_medio"], width=1.5),
        name="Ingreso diario",
    )
)
fig_ts.update_layout(
    title="Flujo de caja diario (estacionalidad semanal y quincenal)",
    xaxis_title="Fecha",
    yaxis_title="Ingreso diario",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=COLORES["texto"]),
    height=320,
)
st.plotly_chart(fig_ts, use_container_width=True)

st.info(
    "**Capacidad de pago dinámica:** Un feriante puede no tener un monto único alto un lunes, "
    "pero genera flujos diarios constantes. El dashboard captura esta caja diaria."
)

st.divider()

# ============ MAPA DE CALOR: COOPERATIVAS vs CUMPLIMIENTO ============
st.subheader("Participación en cooperativas vs cumplimiento de pagos")

# Heatmap: bins de participación vs bins de cumplimiento (conteo)
part_bins = pd.cut(df["participacion_cooperativas_pct"], bins=5, labels=["0-20%", "20-40%", "40-60%", "60-80%", "80-100%"])
cump_bins = pd.cut(df["tasa_cumplimiento_pagos_pct"], bins=5, labels=["25-40%", "40-55%", "55-70%", "70-85%", "85-100%"])
heatmap_df = pd.crosstab(part_bins, cump_bins)

fig_heat = go.Figure(
    data=go.Heatmap(
        z=heatmap_df.values,
        x=heatmap_df.columns.astype(str),
        y=heatmap_df.index.astype(str),
        colorscale=[[0, "#F5F0E8"], [0.5, COLORES["verde_claro"]], [1, COLORES["verde_oscuro"]]],
        text=heatmap_df.values,
        texttemplate="%{text}",
        textfont={"size": 12},
        hoverongaps=False,
    )
)
fig_heat.update_layout(
    title="Concentración: Participación en cooperativas (eje Y) vs Tasa de cumplimiento (eje X)",
    xaxis_title="Tasa de cumplimiento de pagos",
    yaxis_title="Participación en cooperativas",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=COLORES["texto"]),
    height=400,
)
st.plotly_chart(fig_heat, use_container_width=True)

corr_global = df["participacion_cooperativas_pct"].corr(df["tasa_cumplimiento_pagos_pct"])
st.metric("Correlación global (muestra filtrada)", f"{corr_global:.2f}", help="Valor positivo: más participación en cooperativas se asocia a mayor cumplimiento.")

# Correlación por oficio (refuerzo analítico)
corr_oficio = df.groupby("oficio").apply(
    lambda g: g["participacion_cooperativas_pct"].corr(g["tasa_cumplimiento_pagos_pct"]) if len(g) >= 10 else np.nan
).dropna()
if len(corr_oficio) > 0:
    fig_corr = go.Figure(go.Bar(x=corr_oficio.index, y=corr_oficio.values, marker_color=COLORES["verde_medio"]))
    fig_corr.update_layout(title="Correlación Cooperativas–Cumplimiento por oficio", xaxis_title="Oficio", yaxis_title="Correlación", height=280, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=COLORES["texto"]))
    st.plotly_chart(fig_corr, use_container_width=True)

st.info(
    "**Reducción de sesgo:** El modelo puntúa positivamente la participación en redes (cooperativas), "
    "convirtiendo capital social en señal de crédito."
)

st.divider()

# ============ TABLA POR SEGMENTO (OPCIONAL) ============
st.subheader("Resumen por oficio y género")
resumen = (
    df.groupby(["oficio", "genero"], as_index=False)
    .agg(
        solicitantes=("id", "count"),
        arraigo_prom=("puntaje_arraigo", "mean"),
        formalidad_prom=("formalidad_relativa_pct", "mean"),
        cumplimiento_prom=("tasa_cumplimiento_pagos_pct", "mean"),
    )
    .round(1)
)
st.dataframe(resumen, use_container_width=True, hide_index=True)

# ============ PIE DE PÁGINA - MENSAJES DE VALOR ============
st.divider()
with st.expander("💡 Tres puntos de valor analítico para presentar al equipo"):
    st.markdown("""
    1. **Variable de Oro (Arraigo):** En este MVP, el **Arraigo** (tiempo en el lugar y en la actividad) 
    es un mejor predictor de pago que el reporte de una central de riesgo tradicional. Los KPIs de 
    Puntaje de Arraigo y Densidad de Red capturan este comportamiento.

    2. **Capacidad de pago dinámica:** El dashboard captura **flujos de caja diarios**. Un feriante 
    puede no tener $1.000.000 un lunes, pero genera montos diarios constantes (ej. $50.000/día). 
    La sección de distribución y estacionalidad de ingresos visualiza esta dinámica.

    3. **Reducción de sesgo:** El modelo **puntúa positivamente** la participación en redes sociales 
    (cooperativas). El heatmap Cooperativas vs Cumplimiento demuestra cómo el capital social se 
    traduce en mayor tasa de cumplimiento, convirtiendo capital social en capital financiero.
    """)
