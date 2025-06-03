import re
from typing import List, Tuple
import pandas as pd
import uuid

# -------------------------------
# División en oraciones
# -------------------------------

def split_into_sentences(text: str) -> List[str]:
    """
    Divide un texto en oraciones usando signos de puntuación.
    Esta versión puede mejorarse usando NLP (nltk, spaCy).

    Args:
        text (str): Texto completo a dividir.

    Returns:
        List[str]: Lista de oraciones.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]

# -------------------------------
# Agrupación en chunks
# -------------------------------

def chunk_sentences(sentences: List[str], chunk_size: int = 3) -> List[str]:
    """
    Agrupa oraciones en bloques de tamaño fijo (chunks).

    Args:
        sentences (List[str]): Lista de oraciones.
        chunk_size (int): Número de oraciones por chunk.

    Returns:
        List[str]: Lista de chunks concatenados.
    """
    return [
        " ".join(sentences[i:i + chunk_size])
        for i in range(0, len(sentences), chunk_size)
    ]

# -------------------------------
# División en párrafos
# -------------------------------

def split_into_paragraphs(text: str) -> List[str]:
    """
    Divide un texto en párrafos usando doble salto de línea.

    Args:
        text (str): Texto completo.

    Returns:
        List[str]: Lista de párrafos.
    """
    paragraphs = text.split("\n\n")
    return [p.strip() for p in paragraphs if p.strip()]

# -------------------------------
# Preprocesamiento general
# -------------------------------

def preprocess_texts(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Procesa un DataFrame de textos en oraciones y párrafos.
    Genera dos DataFrames nuevos: uno por chunks de oraciones y otro por párrafos.

    Args:
        df (pd.DataFrame): DataFrame original con columnas: date, title, topic, text.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: (df_chunks, df_paragraphs)
    """
    sentence_records = []
    paragraph_records = []

    for _, row in df.iterrows():
        text_id = str(uuid.uuid4())
        date, title, topic, text = row["date"], row["title"], row["topic"], row["text"]

        # Chunks de oraciones
        sentences = split_into_sentences(text)
        for chunk in chunk_sentences(sentences):
            sentence_records.append({
                "id_text": text_id,
                "date": date,
                "title": title,
                "topic": topic,
                "chunk_text": chunk,
                "tagged": None,
                "comments": None,
                "educated_guess": None
            })

        # Párrafos
        paragraphs = split_into_paragraphs(text)
        for para in paragraphs:
            paragraph_records.append({
                "id_text": text_id,
                "date": date,
                "title": title,
                "topic": topic,
                "paragraph_text": para,
                "tagged": None,
                "comments": None,
                "educated_guess": None
            })

    return pd.DataFrame(sentence_records), pd.DataFrame(paragraph_records)
