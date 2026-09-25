"""Exercice 3 : l'effet de la température sur la variabilité des réponses."""

from ollama import Client

from targets.config import settings

client = Client(host=settings.ollama_base_url)

QUESTION = "Invente un slogan court pour une banque."

for temperature in (0.0, 1.2):
    print(f"\n=== Température {temperature} ===")
    for essai in range(1, 4):
        response = client.chat(
            model=settings.target_model,
            messages=[{"role": "user", "content": QUESTION}],
            options={"temperature": temperature},
        )
        print(f"Essai {essai} : {response.message.content.strip()}")
