"""
Datos sintéticos para MVP de crédito en economía popular - ESAL.
Simula perfiles 'Invisible' vs potencial de pago con variables alternativas.
"""
import numpy as np
import pandas as pd
from datetime import datetime

# Semilla para reproducibilidad
np.random.seed(42)

OFICIOS = ["Reciclador", "Feriante", "Costurero", "Vendedor ambulante", "Panadero", "Peluquero", "Otro"]
GENEROS = ["Mujer", "Hombre", "No binario"]
ZONAS = ["Soacha", "Ciudad Bolívar", "Kennedy", "Suba", "Bosa", "Usme", "Rafael Uribe"]


def generar_solicitantes(n: int = 500) -> pd.DataFrame:
    """Genera DataFrame de solicitantes con variables para perfilamiento."""
    oficios = np.random.choice(OFICIOS, n, p=[0.15, 0.25, 0.20, 0.18, 0.08, 0.07, 0.07])
    generos = np.random.choice(GENEROS, n, p=[0.55, 0.42, 0.03])
    zonas = np.random.choice(ZONAS, n, p=[0.18, 0.15, 0.14, 0.14, 0.13, 0.13, 0.13])

    # Arraigo: años en actividad (economía popular - ESAL suele tener más antigüedad en el oficio)
    anos_actividad = np.clip(np.random.exponential(6, n) + np.random.randint(0, 4, n), 1, 25).astype(int)
    anos_vivienda = np.clip(anos_actividad + np.random.randint(-2, 5, n), 1, 30).astype(int)
    arraigo_puntaje = (anos_actividad * 0.5 + anos_vivienda * 0.5)

    # Densidad de red: avales comunitarios (1-5)
    avales = np.random.choice([1, 2, 3, 4, 5], n, p=[0.15, 0.25, 0.35, 0.18, 0.07])

    # Formalidad relativa: servicios a nombre o billetera digital
    tiene_servicios = np.random.binomial(1, 0.35 + (avales / 10), n)
    tiene_billetera = np.random.binomial(1, 0.55 + (avales / 15), n)
    formalidad_relativa = ((tiene_servicios + tiene_billetera) / 2 * 100).round(1)

    # Participación en cooperativas (0-100%)
    participacion_coop = np.clip(np.random.beta(2, 3, n) * 100, 5, 95).round(1)

    # Tasa de cumplimiento sintética: correlacionada con arraigo y cooperativas
    base_cumplimiento = 0.6 + (arraigo_puntaje / 50) * 0.15 + (participacion_coop / 100) * 0.25
    base_cumplimiento += np.random.normal(0, 0.08, n)
    tasa_cumplimiento = np.clip(base_cumplimiento * 100, 25, 98).round(1)

    return pd.DataFrame({
        "id": range(1, n + 1),
        "oficio": oficios,
        "genero": generos,
        "zona": zonas,
        "anos_actividad": anos_actividad,
        "anos_vivienda": anos_vivienda,
        "puntaje_arraigo": np.round(arraigo_puntaje, 1),
        "avales_comunitarios": avales,
        "tiene_servicios_nombre": tiene_servicios,
        "tiene_billetera_digital": tiene_billetera,
        "formalidad_relativa_pct": formalidad_relativa,
        "participacion_cooperativas_pct": participacion_coop,
        "tasa_cumplimiento_pagos_pct": tasa_cumplimiento,
    })


def generar_ingresos_estacionales(n_dias: int = 90) -> pd.DataFrame:
    """
    Simula ingresos con estacionalidad de economía popular - ESAL:
    picos diarios/semanales vs mensual tradicional.
    """
    fechas = pd.date_range(end=datetime.now(), periods=n_dias, freq="D")
    # Base diaria con picos los fines de semana y quincena
    base = 35000 + np.random.lognormal(0, 0.4, n_dias) * 15000
    dia_semana = fechas.dayofweek  # 5,6 = fin de semana
    quincena = (fechas.day <= 7) | (fechas.day >= 25)
    pico_fin_semana = 1 + (dia_semana >= 5) * 0.4
    pico_quincena = 1 + quincena * 0.25
    ingresos = (base * pico_fin_semana * pico_quincena).round(0)
    return pd.DataFrame({"fecha": fechas, "ingreso_diario": ingresos})


def datos_radar_perfiles() -> dict:
    """
    Valores normalizados (0-100) para Radar: Bancarizado típico vs Economía popular - ESAL.
    Variables: Historial crediticio, Antigüedad oficio, Respaldo comunitario,
    Frecuencia ingresos (caja diaria), Garantías líquidas.
    """
    return {
        "variables": [
            "Historial crediticio",
            "Antigüedad en el oficio",
            "Respaldo comunitario",
            "Frecuencia ingresos (caja diaria)",
            "Garantías líquidas",
        ],
        "perfil_bancarizado": [85, 45, 20, 30, 75],
        "perfil_economia_popular": [25, 72, 88, 90, 18],
    }


def matriz_correlacion_coop_cumplimiento(df: pd.DataFrame) -> pd.DataFrame:
    """Prepara matriz de correlación Cooperativas vs Cumplimiento por segmentos."""
    segmentos = []
    for oficio in OFICIOS:
        sub = df[df["oficio"] == oficio]
        if len(sub) >= 10:
            corr = sub["participacion_cooperativas_pct"].corr(sub["tasa_cumplimiento_pagos_pct"])
            segmentos.append({"Oficio": oficio, "Correlación": round(corr, 3), "n": len(sub)})
    return pd.DataFrame(segmentos)
