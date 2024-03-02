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
    """

    Args:
    -----
        a (float): _description_
        b (float): _description_
        c (float): _description_
        d (float): fixní náklady
        x_max (int): kam az vzkreslovat graf na ose x
    
    Returns:
    --------
        x (np.ndarray): Q (od 0 do x_max)
        y (np.ndarray): TC
        AC (np.ndarray): průměrné náklady
        min_ac (int): minimum průměrných nákladů
        MC (np.ndarray): mezní náklady
        min_mc (int): minimum mezních nákladů
        _x (np.ndarray): Q (omezené od 1 do x_max)
    """
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


@st.cache_data(ttl=600, max_entries=10, show_spinner=True)
def TR(a: float, b: float, c: float, x_max: int):
    """

    Args:
    -----
        a (float): _description_
        b (float): _description_
        c (float): _description_
        x_max (int): kam az vzkreslovat graf na ose x
    
    Returns:
    --------
        x (np.ndarray): Q (od 0 do x_max)
        y (np.ndarray): TR
        AR (np.ndarray): průměrné výnosy
        max_ar (int): maximum průměrných výnosů
        MR (np.ndarray): mezní výnosy
        max_mr (int): maximum mezních výnosů
        _x (np.ndarray): Q (omezené od 1 do x_max)
    """
    def f(x):
        return a * x**3 + b * x**2 + c * x

    x = np.linspace(0, x_max, 1000)
    _x = np.linspace(1, x_max, 1000)
    y = f(x)

    AR = f(_x) / _x
    max_ar = np.argmax(AR)

    diff = sp.diff(f(sp.Symbol("x")), sp.Symbol("x"))
    f_prime = sp.lambdify(sp.Symbol("x"), diff)
    MR = f_prime(_x)
    max_mr = np.argmax(MR)
    
    return x, y, AR, max_ar, MR, max_mr, _x