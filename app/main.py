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

point = col1.slider("Vyber bod", 10, 25, 10)
x_tangent = col2.slider("Vyber bod pro tečnu", 5, 15, 10)

x_values, y_values, tangent_line = update_plot(point, x_tangent)

fig = px.line(x=x_values, y=y_values, labels={"x": "x", "y": "f(x)"}, template="simple_white")
fig.update_layout(xaxis=dict(range=[0, 20]), yaxis=dict(range=[0, 20]))
fig.update_traces(line_color="#3dd56d")
fig.add_scatter(
    x=x_values, y=tangent_line, mode="lines", line=dict(color="#D53D59", width=2), showlegend=False
)

st.plotly_chart(fig, )
