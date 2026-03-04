# Dashboard de Perfilamiento - MVP Crédito Economía Popular - ESAL

Dashboard para contrastar el perfil **"Invisible"** (tradicionalmente excluido) con su **potencial de pago real** mediante variables alternativas a las centrales de riesgo.

## Requisitos

- Python 3.9+
- Dependencias en `requirements.txt`

## Instalación y ejecución

```bash
pip install -r requirements.txt
streamlit run app.py
```

El dashboard se abre en el navegador (por defecto `http://localhost:8501`).

---

## Contenido del dashboard

- **KPIs:** Puntaje de Arraigo, Densidad de Red, Índice de Formalidad Relativa.
- **Radar:** Perfil bancarizado típico vs perfil economía popular - ESAL (historial crediticio, antigüedad oficio, respaldo comunitario, frecuencia ingresos, garantías líquidas).
- **Histograma y serie temporal:** Distribución y estacionalidad de ingresos (picos diarios/semanales).
- **Heatmap:** Participación en cooperativas vs tasa de cumplimiento de pagos (datos sintéticos).
- **Filtros:** Oficio, género, zona geográfica.
- **Diseño:** Paleta terrosa/verde/azul, sin rojo, orientada a gestores de fondos de economía social.

---

## Qué enfatizar al presentar el dashboard

Al mostrarlo al equipo, conviene destacar estos **tres puntos de valor analítico**:

### 1. La "Variable de Oro": Arraigo

En este MVP, el **Arraigo** (tiempo en el lugar y en la actividad) funciona como un **mejor predictor de pago** que el reporte de una central de riesgo tradicional. El dashboard lo refleja en el **Puntaje de Arraigo** y en la **Densidad de Red** (avales comunitarios). Son señales de estabilidad y compromiso que la banca clásica no suele usar.

### 2. Capacidad de pago dinámica

El dashboard incorpora **flujos de caja diarios**, no solo un ingreso mensual. Un feriante puede no tener $1.000.000 un lunes, pero generar $50.000 diarios de forma constante. La sección de **distribución y estacionalidad de ingresos** (histograma y serie temporal) muestra esa dinámica y permite evaluar capacidad de pago desde la caja diaria.

### 3. Reducción de sesgo: capital social como señal

El modelo **puntúa positivamente** la participación en redes (cooperativas, avales). El **mapa de calor** y la **correlación por oficio** entre participación en cooperativas y tasa de cumplimiento demuestran que el **capital social se traduce en mejor comportamiento de pago**, convirtiendo capital social en señal de crédito y reduciendo el sesgo contra quienes no tienen historial bancario formal.

---

## Estructura del proyecto

```
Externado/
├── app.py                 # Dashboard Streamlit
├── requirements.txt
├── README.md
└── data/
    ├── __init__.py
    └── synthetic_data.py  # Generación de datos sintéticos para el MVP
```

Los datos son **sintéticos** para el MVP; en producción se reemplazarán por datos reales de solicitantes y pagos.
# economia-popular
