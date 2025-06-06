import streamlit as st

st.set_page_config(page_title="Criterios de Anotación")

st.title("Criterios de Anotación")

st.markdown("""
### **Instrucciones Generales**

- **Opinión**: Valoraciones personales, interpretaciones, lenguaje subjetivo.
- **Evidencia**: Datos, citas directas, hechos verificables.
- **Indeciso**: Fragmentos ambiguos, mal escritos o con falta de contexto claro.

📝 En caso de duda, marca *Indeciso* y deja un comentario explicando tu razonamiento.
""")