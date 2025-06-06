import pandas as pd
import os

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = "data"
ORIGINAL_FILE = os.path.join(BASE_DIR, "../textos_completos.xlsx")
SENTENCE_FILE = os.path.join(DATA_DIR, "sentences_untagged.xlsx")
PARAGRAPH_FILE = os.path.join(DATA_DIR, "paragraphs_untagged.xlsx")

def load_texts():
    # Datos (noticios) : ahorita esta funcion solo carga unos datos sinteticos de prubea que saqué de la biblioteca nltk
    # TODO : tenemos que conectarnos al API de LexisNexis, pero no me queda claro co´omo o si lo pagamos. Si no, pues tendremos que
    # echarnos la talacha de bajar chunks manualmente o en una de esas scrappear
    return pd.read_excel(ORIGINAL_FILE)

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
