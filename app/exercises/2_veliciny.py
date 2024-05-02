import streamlit as st
import plotly.express as px

from utils import TC, TR


def page():
    st.header("Veličiny celkové, průměrné a mezní", anchor="veliciny")
    st.subheader("Celkové náklady")

    col1, col2, col3, col4 = st.columns(4)

    a_tc = col1.number_input("$a$", value=1, key="a_tc")
    b_tc = col2.number_input("$b$", value=-10, key="b_tc")
    c_tc = col3.number_input("$c$", value=50, key="c_tc")
    d_tc = col4.number_input("$d$", value=100, key="d_tc", help="fixní náklady")

    st.write("Celkové náklady jsou dány předpisem:")
    st.latex(f"TC = {a_tc}Q^3 + {b_tc}Q^2 + {c_tc}Q + {d_tc}")
    
    x_max1 = st.slider("Vykreslit graf do", min_value=1, max_value=100, value=10, key="x_max1")

    x, y, AC, min_ac, MC, min_mc, ac_x = TC(a_tc, b_tc, c_tc, d_tc, x_max=x_max1)

    fig = px.line(x=x, y=y, labels={"x": "Q", "y": "TC(Q)"}, template="simple_white")
    # fig.update_layout(xaxis=dict(range=[0, 10]))
    fig.update_traces(line_color="#3dd56d")

    # AC
    fig.add_scatter(
        x=x,
        y=AC,
        mode="lines",
        line=dict(color="orange", width=2),
        name="AC",
        showlegend=False,
    )
    fig.add_scatter(
        x=[ac_x[min_ac]],
        y=[AC[min_ac]],
        mode="markers",
        marker=dict(color="orange", size=10),
        name="min AC",
        showlegend=False,
    )
    fig.add_vline(
        x=ac_x[min_ac],
        line_width=1,
        line_dash="dash",
        line_color="orange",
        showlegend=False,
    )

    # MC
    fig.add_scatter(
        x=x,
        y=MC,
        mode="lines",
        line=dict(color="red", width=2),
        name="MC",
        showlegend=False,
    )
    fig.add_scatter(
        x=[ac_x[min_mc]],
        y=[MC[min_mc]],
        mode="markers",
        marker=dict(color="red", size=10),
        name="min MC",
        showlegend=False,
    )
    fig.add_vline(
        x=ac_x[min_mc],
        line_width=1,
        line_dash="dash",
        line_color="red",
        showlegend=False,
    )

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
    
    x_max2 = st.slider("Vykreslit graf do", min_value=1, max_value=100, value=10, key="x_max2")

    x, y, AR, max_ar, MR, max_mr, _x = TR(a_tr, b_tr, c_tr, x_max=x_max2)

    fig = px.line(x=x, y=y, labels={"x": "Q", "y": "TR(Q)"}, template="simple_white")
    # fig.update_layout(xaxis=dict(range=[0, 10]))
    fig.update_traces(line_color="#3dd56d")

    # AR
    fig.add_scatter(
        x=_x,
        y=AR,
        mode="lines",
        line=dict(color="orange", width=2),
        name="AR",
        showlegend=False,
    )
    fig.add_scatter(
        x=[_x[max_ar]],
        y=[AR[max_ar]],
        mode="markers",
        marker=dict(color="orange", size=10),
        name="max AR",
        showlegend=False,
    )
    fig.add_vline(
        x=_x[max_ar],
        line_width=1,
        line_dash="dash",
        line_color="orange",
        showlegend=False,
    )

    # MR
    fig.add_scatter(
        x=_x,
        y=MR,
        mode="lines",
        line=dict(color="red", width=2),
        name="MR",
        showlegend=False,
    )
    fig.add_scatter(
        x=[_x[max_mr]],
        y=[MR[max_mr]],
        mode="markers",
        marker=dict(color="red", size=10),
        name="max MR",
        showlegend=False,
    )
    fig.add_vline(
        x=_x[max_mr], line_width=1, line_dash="dash", line_color="red", showlegend=False
    )

    # y=0
    fig.add_hline(y=0, line_width=1, line_color="white", showlegend=False)

    # max TR
    fig.add_vline(
        x=x[y.argmax()],
        line_width=1,
        line_dash="dash",
        line_color="#3dd56d",
        showlegend=False,
    )
    fig.add_scatter(
        x=[x[y.argmax()]],
        y=[y.max()],
        mode="markers",
        marker=dict(color="#3dd56d", size=10),
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True, config={"staticPlot": True})
