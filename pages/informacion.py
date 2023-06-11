import streamlit as st
with open("README.md", "r") as f:
    mkdown = f.read()
    st.markdown(mkdown, True)