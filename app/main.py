import streamlit as st
import plotly.express as px
from pathlib import Path

from utils import update_plot, tangent

st.set_page_config(
    page_title="KMA/MME",
    page_icon="💰",
    layout="centered",
    menu_items={
        "Get Help": "https://www.kma-mme.com",
        "Report a bug": "https://www.kma-mme.com",
        "About": Path("README.md").read_text(),
    },
)

st.title("Matematika v mikroekonomii")

st.header("Mezní sklon", anchor="mezní-sklon")

col1, col2 = st.columns(2)

point = col1.slider("Sklon přímky", 10, 25, 10)
x_tangent = col2.slider("Tečna v bodě", 5, 15, 10)

x_values, y_values, f, tangent_line, slope_values = update_plot(point, x_tangent)

col1.write("🟢 **Funkce**")
col2.write("🔴 **Tečna**")

fig = px.line(x=x_values, y=y_values, labels={"x": "x", "y": "f(x)"}, template="simple_white")
fig.update_layout(xaxis=dict(range=[0, 20]), yaxis=dict(range=[0, 20]))
fig.update_traces(line_color="#3dd56d")
fig.add_scatter(
    x=x_values, y=tangent_line, mode="lines", line=dict(color="#D53D59", width=2), showlegend=False
)
fig.add_scatter(x=[x_tangent], y=[f(x_tangent)], mode="markers", marker=dict(color="#D53D59", size=10), showlegend=False)

st.plotly_chart(fig, use_container_width=True, config={"staticPlot": True})

fig = px.line(x=x_values, y=slope_values, labels={"x": "x", "y": "f'(x)"}, template="simple_white", title="Monotonnost sklonu")
fig.update_layout(xaxis=dict(range=[0, 20]), yaxis=dict(range=[0, 3]))
fig.update_traces(line_color="orange")

st.plotly_chart(fig, use_container_width=True, config={"staticPlot": True})

with st.expander("Pravidla pro poznávání mezního sklonu funkce"):
    st.markdown("""
                - Rostoucí funkce má sklon kladný.
                - Klesající funkce má sklon záporný.
                - Lineární funkce má konstantní sklon.
                - Konvexní funkce má rostoucí sklon.
                - Konkávní funkce má klesající sklon.
                """)
