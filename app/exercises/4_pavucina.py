import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from utils import cobweb


def page():
    st.header("Pavučinový model", anchor="pavucina")
    
    st.subheader("Diskrétní model")

    def Q_dt(a, b, p_t):
        return a - b * p_t

    def Q_st(c, d, p_t_minus_1):
        return -c + d * p_t_minus_1

    col1, col2, col3, col4 = st.columns(4)
    a = col1.number_input("$a$", value=24, min_value=1)
    b = col2.number_input("$b$", value=3, min_value=1)
    c = col3.number_input("$c$", value=1, min_value=1)
    d = col4.number_input("$d$", value=2, min_value=1)
    p_0 = st.number_input("$P_0$", value=3, key="p_0_1", min_value=1)

    opt_p = (a + c) / (b + d)
    opt_q = a - b * opt_p
    lbda = -(d / b)
    k = p_0 - opt_p

    st.latex(f"Q_{{D_t}} = {a} - {b}P_t")
    st.latex(f"Q_{{S_t}} = -{c} + {d}P_{{t-1}}")

    st.latex(f"P_0 = {p_0}")
    # st.latex(f"P_t = k \cdot \lambda^t + P^*")
    # opt values
    # st.latex(f"""
    #          Rovnovážný bod:
    #          P^* = {opt_p}, Q^* = {opt_q}
    #          """)
    st.markdown(
        f"""
        Rovnovážný bod: $[P^*, Q^*] = [{opt_p}, {opt_q}]$
        """
    )
    

    def p_t(k, lbd, opt_p, t):
        return k * lbd**t + opt_p

    t = np.linspace(0, 10, 11)
    y = p_t(k, lbda, opt_p, t)

    fig = px.scatter(x=t, y=y, template="simple_white", labels={"x": "t", "y": "P"})
    fig.update_layout(xaxis=dict(range=[0, 10]))
    fig.update_traces(marker=dict(color="#3dd56d", size=10))
    fig.add_hline(y=opt_p, line_width=1, line_color="white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True, config={"staticPlot": True})

    if np.abs(lbda) > 1:
        st.info("Posloupnost diverguje.")
    elif np.abs(lbda) == 1:
        st.info("Posloupnost osciluje.")
    else:
        st.info("Posloupnost konverguje.")

    st.subheader("Pavučina")

    df = cobweb(Q_dt, Q_st, p_0, a, b, c, d, y)

    st.table(df.drop_duplicates(subset=["P"]).reset_index(drop=True).T)
    fig = px.line(df, x="P", y="Q", template="simple_white")
    fig.update_layout(
        xaxis=dict(title="P", tickmode="array"),
        yaxis=dict(title="Q"),
    )
    fig.update_traces(line_color="#3dd56d")

    fig.add_scatter(
        x=[opt_p], y=[opt_q], mode="markers", marker=dict(color="red"), showlegend=False
    )

    # for i in range(int(len(df)/2)):
    #     fig.add_hline(y=df["Q"].iloc[i], line_width=1, line_color="orange", showlegend=False, line_dash="dash")
    #     fig.add_annotation(
    #         x=df["P"].iloc[i],
    #         y=df["Q"].iloc[i],
    #         text=f"Q{i}",
    #         showarrow=True,
    #         font=dict(size=15),
    #     )
    #     fig.add_vline(x=df["P"].iloc[i], line_width=1, line_color="orange", showlegend=False, line_dash="dash")
    #     fig.add_annotation(
    #         x=df["P"].iloc[i],
    #         y=df["Q"].iloc[i],
    #         text=f"P{i}",
    #         showarrow=True,
    #         font=dict(size=15),
    #     )
    st.plotly_chart(fig, use_container_width=True, config={"staticPlot": True})
    
    with st.expander("Řešení"):
        st.write("Zadání:")
        st.latex(r"""
        \begin{align*}
        Q_{D_t} &= a - bP_t \\
        Q_{S_t} &= -c + dP_{t-1} \\
        P_0 &= 3
        \end{align*}
        """)
        st.write("Rovnovážný bod:")
        st.latex(r"""
        \begin{align*}
        a - bP^* &= -c + dP^* \\
        P^* &= \frac{a + c}{b + d} \\
        Q^* &= a - bP^*
        \end{align*}
        """)
        
        st.write("Obecné řešení:")
        st.latex(r"""
        \begin{align*}
        P_t &= k \cdot \lambda^t + P^* \\
        \lambda &= -\frac{d}{b} \\
        k &= P_0 - P^* \\
        P_t &= (P_0 - P^*) \cdot \left(-\frac{d}{b}\right)^t + P^*
        \end{align*}
        """)
    
    st.subheader("Spojitý model")
    
    def Q_d_t(m, n, p_t):
        return m - n*p_t

    col1, col2, col3, col4, col5 = st.columns(5)
    m = col1.number_input("$m$", value=24, min_value=1)
    n = col2.number_input("$n$", value=3, min_value=1)
    alpha = col3.number_input(r"$\alpha$", value=3, min_value=1)
    r = col4.number_input("$r$", value=1, min_value=1)
    s = col5.number_input("$s$", value=2, min_value=1)
    
    p0 = st.number_input("$P_0$", value=3, key="p_0_2", min_value=1)
    

    p_opt = (m + r) / (n + s)
    q_opt = Q_d_t(m, n, p_opt)

    t = np.linspace(0, 10, 1000)

    lbda = - ((s + n) / alpha)
    k = p0 - p_opt

    def Pt(k, lbda, p_opt, t):
        return k * np.exp(lbda * t) + p_opt
    
    fig = px.line(x=t, y=Pt(k, lbda, p_opt, t), template="simple_white", labels={"x": "t", "y": "P"})
    fig.update_traces(line=dict(color="#3dd56d"))
    fig.add_hline(y=p_opt, line_width=1, line_color="white", showlegend=False)
    
    st.latex(f"Q_D(t) = {m} - {n}P(t) \pm {alpha} * \\frac{{dP(t)}}{{dt}}")
    st.latex(f"Q_S(t) = -{r} + {s}P(t)")
    st.latex(f"P_0 = {p0}")
    
    st.markdown(
        f"""
        Rovnovážný bod: $[P^*, Q^*] = [{p_opt}, {q_opt}]$
        """
    )

    st.plotly_chart(fig, use_container_width=True, config={"staticPlot": True})
