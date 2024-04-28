import numpy as np
import sympy as sp
import streamlit as st
import pandas as pd
from scipy.interpolate import lagrange


def tangent(
    x: float, x_values: np.ndarray, f: callable
) -> tuple[np.ndarray, np.ndarray]:
    """Tečna v bodě x.

    Args:
    -----
        x (float): bod, ve kterém chceme tečnu
        x_values (np.ndarray): hodnoty x
        f (callable): funkce

    Returns:
    --------
        line (np.ndarray): tečna
        slope_values (np.ndarray): hodnoty sklonu
    """
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
        return a * x**3 + b * x**2 + c * x + d

    x = np.linspace(0, x_max, 10000)
    y = f(x)
    _x = np.linspace(1, x_max, 10000)

    AC = f(_x) / _x
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

    x = np.linspace(0, x_max, 10000)
    _x = np.linspace(1, x_max, 10000)
    y = f(x)

    AR = f(_x) / _x
    max_ar = np.argmax(AR)

    diff = sp.diff(f(sp.Symbol("x")), sp.Symbol("x"))
    f_prime = sp.lambdify(sp.Symbol("x"), diff)
    MR = f_prime(_x)
    max_mr = np.argmax(MR)

    return x, y, AR, max_ar, MR, max_mr, _x


def alhpa_m(x_point: float, f: callable) -> float:
    """Úhel mezi tečnou a osou x.

    Args:
        x_point (float): bod, ve kterém chceme tečnu
        f (callable): funkce

    Returns:
        float: úhel v radiánech
    """
    x = sp.Symbol("x")
    f = f(x)

    f_prime = sp.diff(f, x)
    slope_at_point = f_prime.subs(x, x_point)

    angle_radians = np.arctan2(abs(float(slope_at_point)), 1)

    return angle_radians


def alpha_a(x_point: float, f: callable) -> float:
    """Úhel mezi spojnicí bodu x_point s počátkem a osou x.

    Args:
        x_point (float): bod, do kterého vedeme spojnici
        f (callable): funkce

    Returns:
        float: úhel v radiánech
    """
    y_point = f(x_point)
    radians = np.arctan2(y_point, x_point)

    return radians


def cobweb(Q_dt, Q_st, p_0, a, b, c, d, y):
    """Diskrétní pavučinový model.

    Args:
        Q_dt: Funkce pro poptávku
        Q_st: Funkce pro nabídku
        p_0: _description_
        a: parametr funkce poptávky
        b: parametr funkce poptávky
        c: parametr funkce nabídky
        d: parametr funkce nabídky
        y

    Returns:
        DataFrame: hodnoty p a q
    """
    q_0 = Q_dt(a, b, p_0)

    q = []
    p = [p_0]

    for i in range(1, len(y)):
        q_0 = Q_dt(a, b, p[-1])
        q_1 = Q_st(c, d, p[-1])
        q.append(q_0)
        q.append(q_1)
        p.append(p[-1])
        if i == len(y) - 1:
            break
        p.append((q_1 - a) / -b)

    df = pd.DataFrame({"P": p, "Q": q})

    return df
