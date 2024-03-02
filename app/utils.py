import numpy as np
import sympy as sp
import streamlit as st
from scipy.interpolate import lagrange


def tangent(x, x_values, f):
    y = f(x)
    diff = sp.diff(f(sp.Symbol("x")), sp.Symbol("x"))
    f_prime = sp.lambdify(sp.Symbol("x"), diff)
    slope = f_prime(x)

    line = slope * (x_values - x) + y
    slope_values = [f_prime(x) for x in x_values]

    return line, slope_values


@st.cache_data(ttl=600, max_entries=10, show_spinner=True)
def update_plot(y_third, x_tangent):
    x_points = [0, 3, 15]
    y_points = [0, 3]

    y_points = y_points + [y_third]

    interp_func = lagrange(x_points, y_points)

    x_values = np.linspace(0, 20, 100)
    y_values = interp_func(x_values)

    tangent_line, slope_values = tangent(x_tangent, x_values, interp_func)

    return x_values, y_values, interp_func, tangent_line, slope_values


@st.cache_data(ttl=600, max_entries=10, show_spinner=True)
def TC(a: float, b: float, c: float, d: float, x_max: int):
    def f(x):
        return a * x ** 3 + b * x ** 2 + c * x + d
    
    x = np.linspace(0, x_max, 100)
    y = f(x)
    _x = np.linspace(1, x_max, 100)
    
    AC = f(_x)/_x
    min_ac = AC.argmin()
    
    diff = sp.diff(f(sp.Symbol("x")), sp.Symbol("x"))
    f_prime = sp.lambdify(sp.Symbol("x"), diff)
    MC = f_prime(_x)
    min_mc = MC.argmin()
    
    return x, y, AC, min_ac, MC, min_mc, _x
    