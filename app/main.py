import streamlit as st
import os
from pathlib import Path
import importlib.util

st.set_page_config(
    page_title="KMA/MME",
    page_icon="💰",
    initial_sidebar_state="collapsed",
    layout="centered",
    menu_items={
        "Get Help": "https://www.kma-mme.com",
        "Report a bug": "https://www.kma-mme.com",
        "About": Path("About.md").read_text(),
    },
)

st.title("Matematika v mikroekonomii")

with st.sidebar:
    st.markdown("# [Mezní sklon](#sklon)")
    st.markdown("# [Veličiny celkové, průměrné a mezní](#veliciny)")
    st.markdown("# [Elasticita funkce](#elasticita)")
    st.markdown("# [Pavučinový model](#pavucina)")


directory = "app/exercises"
py_files = sorted(
    [filename for filename in os.listdir(directory) if filename.endswith(".py")]
)

for filename in py_files:
    module_name = filename[:-3]
    module_path = os.path.join(directory, filename)

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if hasattr(module, "page") and callable(module.page):
        module.page()
    st.divider()
