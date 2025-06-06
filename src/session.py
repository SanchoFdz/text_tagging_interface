import streamlit as st
import pandas as pd
from src.preprocessing import preprocess_texts
from src.storage import load_texts

def init_session_state():
    """
    Inicializa el estado de la sesión si no está configurado.
    Carga los datos originales y genera los DataFrames para anotación.
    """
    # Datos originales (noticias)
    if "original_df" not in st.session_state:
        st.session_state.original_df = load_texts()

    # Preprocesamiento (solo si no existen)
    if "sentences_df" not in st.session_state or "paragraphs_df" not in st.session_state:
        sentences_df, paragraphs_df = preprocess_texts(st.session_state.original_df)
        st.session_state.sentences_df = sentences_df
        st.session_state.paragraphs_df = paragraphs_df

    # Progreso del usuario
    st.session_state.setdefault("total_tagged_items", 0)
    st.session_state.setdefault("total_tagged_words", 0)

    # Índice actual de anotación
    st.session_state.setdefault("current_row_index", None)

    # Modo de anotación (oraciones o párrafos)
    st.session_state.setdefault("annotation_mode", "sentences")

    # Usuario
    st.session_state.setdefault("username", "")

    # Indecisión (estado para mostrar inputs extra)
    st.session_state.setdefault("show_indeciso", False)

    st.session_state.setdefault("trigger_rerun", False)
