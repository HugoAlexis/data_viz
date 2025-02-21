import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import re
import time

st.markdown("""<style>
    .stMainBlockContainer {
        max-width: 1280px;
        }</style>""",
            unsafe_allow_html=True
            )

pattern_dt = re.compile('(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)')
pattern_t1 = re.compile(r'Core 0:\s*\+([\d.]+)\s*°C')
pattern_t2 = re.compile(r'Core 1:\s*\+([\d.]+)\s*°C')
pattern_t3 = re.compile(r'Core 2:\s*\+([\d.]+)\s*°C')
pattern_t4 = re.compile(r'Core 3:\s*\+([\d.]+)\s*°C')


with open('../../Downloads/cpu_temp_log_full.txt') as f:
    file_content = ''.join(f.read()).strip()
items = file_content.split('---------------------------------')


def extract_info(item_text):
    dt = pattern_dt.findall(item_text)
    t1 = pattern_t1.findall(item_text)
    t2 = pattern_t2.findall(item_text)
    t3 = pattern_t3.findall(item_text)
    t4 = pattern_t4.findall(item_text)

    try:
        return {
            'datetime': time.strftime(dt[0]),
            'Core 0': float(t1[0]),
            'Core 1': float(t2[0]),
            'Core 2': float(t3[0]),
            'Core 3': float(t4[0])
        }
    except:
        print(item_text)

data = [extract_info(item) for item in items if extract_info(item)]
df_data = pd.DataFrame(data)
df_data['datetime'] = pd.to_datetime(df_data['datetime'])

# Crea la figura con subplots (4 filas, 1 columna)
fig = make_subplots(rows=4, cols=1, shared_xaxes=True)

# Añade los trazos a cada subplot
fig.add_trace(go.Scatter(x=df_data['datetime'], y=df_data['Core 0'], mode='lines', name='Core 0', marker=dict(color='Crimson')), row=1, col=1)
fig.add_trace(go.Scatter(x=df_data['datetime'], y=df_data['Core 1'], mode='lines', name='Core 1', marker=dict(color='MediumSeaGreen')), row=2, col=1)
fig.add_trace(go.Scatter(x=df_data['datetime'], y=df_data['Core 2'], mode='lines', name='Core 2', marker=dict(color='Goldenrod')), row=3, col=1)
fig.add_trace(go.Scatter(x=df_data['datetime'], y=df_data['Core 3'], mode='lines', name='Core 3', marker=dict(color='DodgerBlue')), row=4, col=1)

# Actualiza el layout para mejorar la presentación
fig.update_layout(
    xaxis_title="Datetime",
    yaxis_title="Value (°C)",  # Añade el símbolo de grado centígrado
    title="Core Usage",
    plot_bgcolor='White',
    paper_bgcolor='White',
    height=800  # Ajusta la altura para que los subplots se vean bien
)

# Formatea el eje Y con el símbolo de grado centígrado
fig.update_yaxes(ticksuffix="°C")  # ticksuffix añade el sufijo a las etiquetas del eje Y

# Muestra el gráfico en Streamlit
st.plotly_chart(fig)
