import streamlit as st
import plotly.express as px
from pathlib import Path

from utils import update_plot, TC

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

with st.sidebar:
    st.title("Obsah")
    st.markdown("# [Mezní sklon](#mezni-sklon)")
    st.markdown("# [Veličiny celkové, průměrné a mezní](#veliciny)")
    
    

st.header("Mezní sklon", anchor="mezni-sklon")

col1, col2 = st.columns(2)

point = col1.slider("Sklon přímky", 10, 25, 10)
x_tangent = col2.slider("Tečna v bodě", 5, 15, 10)

x_values, y_values, f, tangent_line, slope_values = update_plot(point, x_tangent)

col1.write("🟢 **Funkce**")
subcol1, subcol2 = col2.columns(2)
subcol1.write("🔴 **Tečna**")
tecna = subcol2.toggle("Zobrazit tečnu",)

fig = px.line(
    x=x_values, y=y_values, labels={"x": "x", "y": "f(x)"}, template="simple_white"
)
fig.update_layout(xaxis=dict(range=[0, 20]), yaxis=dict(range=[0, 20]))
fig.update_traces(line_color="#3dd56d")


if tecna:
    fig.add_scatter(
        x=x_values,
        y=tangent_line,
        mode="lines",
        line=dict(color="#D53D59", width=2),
        showlegend=False,
    )
    fig.add_scatter(
        x=[x_tangent],
        y=[f(x_tangent)],
        mode="markers",
        marker=dict(color="#D53D59", size=10),
        showlegend=False,
    )

st.plotly_chart(fig, use_container_width=True, config={"staticPlot": True})

fig = px.line(
    x=x_values,
    y=slope_values,
    labels={"x": "x", "y": "f'(x)"},
    template="simple_white",
    title="Monotonnost sklonu",
)
fig.update_layout(xaxis=dict(range=[0, 20]), yaxis=dict(range=[0, 3]))
fig.update_traces(line_color="orange")

st.plotly_chart(fig, use_container_width=True, config={"staticPlot": True})

with st.expander("Pravidla pro poznávání mezního sklonu funkce"):
    st.markdown(
        """
                - Rostoucí funkce má sklon kladný.
                - Klesající funkce má sklon záporný.
                - Lineární funkce má konstantní sklon.
                - Konvexní funkce má rostoucí sklon.
                - Konkávní funkce má klesající sklon.
                """
    )

st.divider()

st.header("Veličiny celkové, průměrné a mezní", anchor="veliciny")

col1, col2, col3, col4 = st.columns(4)

a = col1.number_input("a", value=1)
b = col2.number_input("b", value=-10)
c = col3.number_input("c", value=50)
d = col4.number_input("d", value=100)

st.write("Celkové náklady jsou dány předpisem:")
st.latex(f"TC = {a}Q^3 + {b}Q^2 + {c}Q + {d}")

x, y, AC, min_ac, MC, min_mc, ac_x = TC(a, b, c, d, 10)

fig = px.line(
    x=x, y=y, labels={"x": "Q", "y": "TC(Q)"}, template="simple_white", title="Celkové náklady"
)
fig.update_layout(xaxis=dict(range=[0, 10]))
fig.update_traces(line_color="#3dd56d")

fig.add_scatter(x=x, y=AC, mode="lines", line=dict(color="orange", width=2), name="AC", showlegend=False)
fig.add_scatter(x=x, y=MC, mode="lines", line=dict(color="red", width=2), name="MC", showlegend=False)

fig.add_scatter(x=[ac_x[min_ac]], y=[AC[min_ac]], mode="markers", marker=dict(color="orange", size=10), name="min AC", showlegend=False)
fig.add_scatter(x=[ac_x[min_mc]], y=[MC[min_mc]], mode="markers", marker=dict(color="red", size=10), name="min MC", showlegend=False)

st.plotly_chart(fig, use_container_width=True, config={"staticPlot": True})