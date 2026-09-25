"""Exercice 1 : premier appel à un LLM local avec Ollama."""

from ollama import Client

from targets.config import settings

client = Client(host=settings.ollama_base_url)

response = client.chat(
    model=settings.target_model,
    messages=[
        {"role": "user", "content": "Explique en deux phrases ce qu'est une banque."},
    ],
)

print("Réponse du modèle :")
print(response.message.content)
print()
print(f"Tokens envoyés (prompt)   : {response.prompt_eval_count}")
print(f"Tokens générés (réponse)  : {response.eval_count}")
print(f"Durée totale              : {response.total_duration / 1e9:.2f} secondes")
