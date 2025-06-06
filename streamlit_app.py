import streamlit as st
from src.session import init_session_state
from src.anotador import render_annotation_interface

def main():
    st.set_page_config(page_title="Etiquetador de Opinión vs Evidencia", layout="wide")

    # Inicializar estado
    init_session_state()

    # Login + Modo
    with st.sidebar:
        st.subheader("Login")
        st.session_state["username"] = st.text_input("Usuario:", value=st.session_state["username"])

        st.session_state["annotation_mode"] = st.radio(
            "Modo de anotación",
            options=["sentences", "paragraphs"],
            format_func=lambda x: "Oraciones" if x == "sentences" else "Párrafos",
            index=0 if st.session_state["annotation_mode"] == "sentences" else 1
        )

    # Tabs principales
    tab1, tab2 = st.tabs(["Anotaciones", "Criterios de Anotación"])

    with tab2:
        st.header("Guía / Criterios de Anotación")
        st.markdown("""
        **Instrucciones Básicas**  
        - **Opinión**: Juicios, conjeturas o valoraciones personales.  
        - **Evidencia**: Hechos verificables, datos, citas.  
        - **Indeciso**: No queda claro con la información provista.  
        """)

    with tab1:
        render_annotation_interface()

if __name__ == "__main__":
    main()
