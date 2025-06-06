import streamlit as st
import pandas as pd
from src.storage import save_dataframe

"""
Módulo para inicializar la sección de etiquetado.
"""

def render_annotation_interface():
    """
    Renderiza la interfaz principal de anotación de texto.
    """

    st.subheader("Anotaciones")
    st.session_state.setdefault("trigger_rerun", False)

    # Mostrar progreso del usuario
    total_tagged = st.session_state["total_tagged_items"]
    progress = (total_tagged % 100) / 100.0 # TODO : Definir esto dinámicamente; cuando lo deployemos que? Cuántos como base es razonable? Como hacemos para reiniciar el contador? 
    st.progress(progress)
    st.write(f"**Total Anotados**: {total_tagged}")
    st.write(f"**Total Palabras Anotadas**: {st.session_state['total_tagged_words']}")

    # Determinar modo y columnas
    if st.session_state["annotation_mode"] == "sentences": # Creo que hay que etiquetar oraciones y párrafos, va a servir al entrenar
        df = st.session_state["sentences_df"]
        text_column = "chunk_text"
        mode = "sentences"
    else:
        df = st.session_state["paragraphs_df"]
        text_column = "paragraph_text"
        mode = "paragraphs"

    # Revisar si se solicitó explícitamente nuevo fragmento
    if st.session_state.get("next_text_ready", False):
        st.session_state["current_row_index"] = None
        st.session_state["next_text_ready"] = False

    # Seleccionar fragmento actual o uno nuevo si ya fue etiquetado
    if (
        st.session_state["current_row_index"] is None or
        pd.notna(df.at[st.session_state["current_row_index"], "tagged"])
    ):
        untagged = df[df["tagged"].isna()]
        if untagged.empty:
            st.success("No quedan fragmentos sin anotar. ¡Felicidades!")
            return
        row = untagged.sample(1).iloc[0]
        st.session_state["current_row_index"] = row.name
    else:
        row = df.loc[st.session_state["current_row_index"]]

    # Mostrar metadata y texto
    st.write(f"**Fecha**: {row['date']}")
    st.write(f"**Título**: {row['title']}")
    st.write(f"**Tema**: {row['topic']}")
    st.markdown(f"**Texto a anotar**:\n\n{row[text_column]}")

    # Selección de etiqueta con estado persistente (#TODO: aquí le pongo un key que es igual que una concatenacion de la fila;
    #  me da cosa que esto termine jugando en contra. Por ahora no encuentro mejor solución)
    st.write("Seleccione la etiqueta:")
    tag_to_save = st.radio(
        "Seleccione etiqueta",
        ["opinión", "evidencia", "indeciso"],
        index=None,
        key=f"selected_label_{st.session_state['current_row_index']}",
        format_func=lambda x: x.capitalize()
    )

    reason = None
    guess_value = None

    # Inputs adicionales si es "indeciso"
    if tag_to_save == "indeciso":
        reason = st.selectbox(
            "¿Qué te tiene indeciso?",
            ["Falta contexto", "Contradictorio", "Otra", "Falta claridad en criterios", "Ninguna de las dos"],
            key="indecision_reason"
        )
        st.write("0=Opinión; 1=Evidencia")
        guess_value = st.slider(
            "¿Hacia dónde te inclinas?",
            min_value=0.0, max_value=1.0, value=0.5, step=0.1,
            key="educated_guess"
        )

    # Botón para guardar y avanzar
    if st.button("Siguiente"):
        if tag_to_save is None:
            st.warning("Por favor seleccione una categoría antes de continuar.")
        else:
            # Si se seleccionó "indeciso", obtener los valores guardados
            if tag_to_save == "indeciso":
                reason = st.session_state.get("indecision_reason", None)
                guess_value = st.session_state.get("educated_guess", None)

            # Guardar en el DataFrame
            df.at[st.session_state["current_row_index"], "tagged"] = tag_to_save
            df.at[st.session_state["current_row_index"], "comments"] = reason
            df.at[st.session_state["current_row_index"], "educated_guess"] = guess_value

            # Contadores
            
            st.session_state["total_tagged_items"] += 1
            st.session_state["total_tagged_words"] += len(row[text_column].split())

            # Guardar en disco
            save_dataframe(df, mode=mode)

            # Limpieza del estado
            st.session_state["current_row_index"] = None
            st.session_state["show_indeciso"] = False
            st.session_state.pop("selected_label", None)
            st.session_state.pop("indecision_reason", None)
            st.session_state.pop("educated_guess", 0.5)

            # Forzar cambio para re-render
            st.session_state["trigger_rerun"] = not st.session_state["trigger_rerun"]
            st.session_state.selected_label = "opinión"
            st.write("Gracias")
            st.button("Actualizar") # TODO : Aquí no sñ que más hacer para  ue se actualice y re-renderice 

