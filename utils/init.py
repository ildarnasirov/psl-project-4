import streamlit as st
from utils.movies import load_movies
from utils.constants import MOVIES_STATE, REVIEW_STATE

def config_page(init_cache = True):
    st.set_page_config(
        layout="wide", 
        initial_sidebar_state="collapsed"
    )

    if not init_cache:
        return

    if MOVIES_STATE not in st.session_state:
        st.session_state[MOVIES_STATE] = load_movies()
    if REVIEW_STATE not in st.session_state:
        st.session_state[REVIEW_STATE] = {}
