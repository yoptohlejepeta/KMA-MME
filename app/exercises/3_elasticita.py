import streamlit as st
import plotly.express as px
import numpy as np
import sympy as sp

from utils import alpha_a, alhpa_m, tangent


def page():
    st.header("Elasticita funkce", anchor="elasticita")
    
    col1, col2, col3 = st.columns(3)
    
    a = col1.number_input("a", value=-1, key="a")
    b = col2.number_input("b", value=1, key="b")
    c = col3.number_input("c", value=4, key="c")

    st.latex(f"f(x) = {a}x^2 + {b}x + {c}")
    
    def f(x):
        return a * x**2 + b * x + c

    roots = np.roots([a, b, c])
    solutions = [root.real for root in roots if np.isreal(root) and root > 0]
    
    if not solutions:
        st.warning("Funkce nemá reálné kořeny v kladných hodnotách.")
        return
    
    x = np.linspace(0, solutions[-1], 10000)
    y = f(x)

    point = st.number_input("Bod", min_value=0.0, max_value=solutions[-1], value=2.0, step=0.1)

    line = tangent(point, x, f)[0]

    fig = px.line(x=x, y=y, labels={"x": "P", "y": "Q"}, template="simple_white")
    fig.update_layout(xaxis=dict(range=[0, solutions[-1]]), yaxis=dict(range=[0, np.max(y) + 1]))
    fig.update_traces(line_color="#3dd56d")

    # alfa a
    fig.add_scatter(x=x, y=line, mode='lines', line=dict(color="orange", width=2), name="Tečna", showlegend=False)
    
    fig.add_scatter(x=[0, point], y=[0, f(point)], mode='lines', line=dict(color="red", width=2), name="Paprsek z počátku", showlegend=False)

    # y=0
    fig.add_hline(y=0, line_width=1, line_color="white", showlegend=False)
    
    st.plotly_chart(fig, use_container_width=True, config={"staticPlot": True})
    
    col1, col2 = st.columns(2)
    
    a_a = alpha_a(point, f)
    a_m = alhpa_m(point, f)
    
    col1.latex(f"\\alpha_a = {round(a_a, 3)}")
    col1.latex(f"\\alpha_m = {round(a_m, 3)}")
    
    if a_a > a_m:
        col2.latex("\\alpha_a > \\alpha_m")
        col2.info("Funkce je v tomto bodě neelastická.")
    elif a_a < a_m:
        col2.latex("\\alpha_a < \\alpha_m")
        col2.info("Funkce je v tomto bodě elastická.")
    else:
        col2.latex("\\alpha_a = \\alpha_m")
        col2.info("Funkce je v tomto bodě jednotkově elastická.")
    
    with st.expander("Elasticita funkce"):
        st.latex("E_f = \\frac{Mf(x)}{Af(x)} = \\frac{f'(x)}{\\frac{f(x)}{x}} = \\frac{f'(x)}{f(x)} \\cdot x")