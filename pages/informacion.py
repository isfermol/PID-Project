import streamlit as st
with open("/PID-ProyectoFinal/README.md", "r") as f:
    mkdown = f.read()
    st.markdown(mkdown, True)