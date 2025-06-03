import pandas as pd
import os

DATA_DIR = "data"
ORIGINAL_FILE = os.path.join(DATA_DIR, "textos_completos.xlsx")
SENTENCE_FILE = os.path.join(DATA_DIR, "sentences_untagged.xlsx")
PARAGRAPH_FILE = os.path.join(DATA_DIR, "paragraphs_untagged.xlsx")

def load_texts() -> pd.DataFrame:
    """
    Carga el archivo de noticias originales.

    Returns:
        pd.DataFrame: DataFrame con columnas: date, title, topic, text
    """
    try:
        return pd.read_excel(ORIGINAL_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["date", "title", "topic", "text"])

def save_dataframe(df: pd.DataFrame, mode: str):
    """
    Guarda un DataFrame anotado en archivo Excel.

    Args:
        df (pd.DataFrame): DataFrame a guardar.
        mode (str): 'sentences' o 'paragraphs'
    """
    if mode == "sentences":
        df.to_excel(SENTENCE_FILE, index=False)
    elif mode == "paragraphs":
        df.to_excel(PARAGRAPH_FILE, index=False)
    else:
        raise ValueError("Modo de guardado no válido: debe ser 'sentences' o 'paragraphs'")
