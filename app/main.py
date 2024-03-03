import streamlit as st
import plotly.express as px
from pathlib import Path

from utils import update_plot, TC, TR

st.set_page_config(
    page_title="KMA/MME",
    page_icon="💰",
    initial_sidebar_state="collapsed",
    layout="centered",
    menu_items={
        "Get Help": "https://www.kma-mme.com",
        "Report a bug": "https://www.kma-mme.com",
        "About": Path("README.md").read_text(),
    },
)

st.title("Matematika v mikroekonomii")

with st.sidebar:
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
st.subheader("Celkové náklady")

col1, col2, col3, col4 = st.columns(4)

a_tc = col1.number_input("$a$", value=1, key="a_tc")
b_tc = col2.number_input("$b$", value=-10, key="b_tc")
c_tc = col3.number_input("$c$", value=50, key="c_tc")
d_tc = col4.number_input("$d$", value=100, key="d_tc", help="fixní náklady")

st.write("Celkové náklady jsou dány předpisem:")
st.latex(f"TC = {a_tc}Q^3 + {b_tc}Q^2 + {c_tc}Q + {d_tc}")

x, y, AC, min_ac, MC, min_mc, ac_x = TC(a_tc, b_tc, c_tc, d_tc, 10)

fig = px.line(
    x=x, y=y, labels={"x": "Q", "y": "TC(Q)"}, template="simple_white"
)
fig.update_layout(xaxis=dict(range=[0, 10]))
fig.update_traces(line_color="#3dd56d")

# AC
fig.add_scatter(x=x, y=AC, mode="lines", line=dict(color="orange", width=2), name="AC", showlegend=False)
fig.add_scatter(x=[ac_x[min_ac]], y=[AC[min_ac]], mode="markers", marker=dict(color="orange", size=10), name="min AC", showlegend=False)
fig.add_vline(x=ac_x[min_ac], line_width=1, line_dash="dash", line_color="orange", showlegend=False)

# MC
fig.add_scatter(x=x, y=MC, mode="lines", line=dict(color="red", width=2), name="MC", showlegend=False)
fig.add_scatter(x=[ac_x[min_mc]], y=[MC[min_mc]], mode="markers", marker=dict(color="red", size=10), name="min MC", showlegend=False)
fig.add_vline(x=ac_x[min_mc], line_width=1, line_dash="dash", line_color="red", showlegend=False)

# y=0
fig.add_hline(y=0, line_width=1, line_color="white", showlegend=False)

st.plotly_chart(fig, use_container_width=True, config={"staticPlot": True})

st.subheader("Celkové příjmy")

col1, col2, col3 = st.columns(3)

a_tr = col1.number_input("$a$", value=-5, key="a_tr")
b_tr = col2.number_input("$b$", value=50, key="b_tr")
c_tr = col3.number_input("$c$", value=100, key="c_tr")

st.write("Celkové příjmy jsou dány předpisem:")
st.latex(f"TR = {a_tr}Q^3 + {b_tr}Q^2 + {c_tr}Q")

x, y, AR, max_ar, MR, max_mr, _x = TR(a_tr, b_tr, c_tr, 10)

fig = px.line(
    x=x, y=y, labels={"x": "Q", "y": "TR(Q)"}, template="simple_white"
)
fig.update_layout(xaxis=dict(range=[0, 10]))
fig.update_traces(line_color="#3dd56d")

# AR
fig.add_scatter(x=_x, y=AR, mode="lines", line=dict(color="orange", width=2), name="AR", showlegend=False)
fig.add_scatter(x=[_x[max_ar]], y=[AR[max_ar]], mode="markers", marker=dict(color="orange", size=10), name="max AR", showlegend=False)
fig.add_vline(x=_x[max_ar], line_width=1, line_dash="dash", line_color="orange", showlegend=False)

# MR
fig.add_scatter(x=_x, y=MR, mode="lines", line=dict(color="red", width=2), name="MR", showlegend=False)
fig.add_scatter(x=[_x[max_mr]], y=[MR[max_mr]], mode="markers", marker=dict(color="red", size=10), name="max MR", showlegend=False)
fig.add_vline(x=_x[max_mr], line_width=1, line_dash="dash", line_color="red", showlegend=False)

# y=0
fig.add_hline(y=0, line_width=1, line_color="white", showlegend=False)

# max TR
fig.add_vline(x=x[y.argmax()], line_width=1, line_dash="dash", line_color="#3dd56d", showlegend=False)
fig.add_scatter(x=[x[y.argmax()]], y=[y.max()], mode="markers", marker=dict(color="#3dd56d", size=10), showlegend=False)

st.plotly_chart(fig, use_container_width=True, config={"staticPlot": True})

st.divider()