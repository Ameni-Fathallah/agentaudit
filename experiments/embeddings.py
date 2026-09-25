"""Exercice : comparer le sens de plusieurs phrases grâce aux embeddings."""

import numpy as np
from ollama import Client

from targets.config import settings

client = Client(host=settings.ollama_base_url)

REFERENCE = "Combien coûte la carte Nova Gold ?"
PHRASES = [
    "Tarif annuel de la carte Nova Gold",  # même sens, autres mots
    "Quel est le prix de la carte Gold ?",  # même sens, autres mots
    "كم تكلفة بطاقة Gold؟",  # même question en arabe
    "9adech soum el carte Gold ?",  # même question en derja (arabizi)
    "Comment faire opposition sur ma carte ?",  # même thème, autre question
    "Quel temps fait-il à Tunis ?",  # sans rapport
]

response = client.embed(model=settings.embedding_model, input=[REFERENCE, *PHRASES])
vectors = np.array(response.embeddings)
vectors /= np.linalg.norm(vectors, axis=1, keepdims=True)  # normalisation

print(f"Dimension des vecteurs : {vectors.shape[1]}")
print(f"Référence : {REFERENCE}\n")
for phrase, vector in zip(PHRASES, vectors[1:], strict=True):
    similarity = float(vectors[0] @ vector)  # produit scalaire = cosinus (vecteurs normalisés)
    print(f"{similarity:.3f}  {phrase}")