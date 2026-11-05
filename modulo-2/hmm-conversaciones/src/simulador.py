"""Supuestos sintéticos compartidos con el navegador mediante modelos.json."""
import json
from pathlib import Path
from modelo_hmm import HMM
ROOT=Path(__file__).resolve().parents[1]
def load_models():
    d=json.loads((ROOT/'modelos.json').read_text())
    return {k:HMM(v,d['B'],d['pi']) for k,v in d['A'].items()}
