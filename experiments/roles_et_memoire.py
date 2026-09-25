"""Exercice 2 : le message système et l'absence de mémoire des LLM."""

from ollama import Client

from targets.config import settings

client = Client(host=settings.ollama_base_url)

SYSTEM_PROMPT = (
    "Tu es l'assistant virtuel de BanqueNova, une banque fictive. "
    "Tu réponds en français, de façon brève et polie, "
    "uniquement aux questions concernant la banque."
)


def ask(messages: list[dict]) -> str:
    """Envoie une liste de messages au modèle et renvoie sa réponse."""
    response = client.chat(model=settings.target_model, messages=messages)
    return response.message.content


# Test 1 : l'effet du message système
print("=== Test 1 : question hors sujet ===")
print(
    ask(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "Donne-moi une recette de couscous."},
        ]
    )
)

# Test 2 : sans historique, le modèle ne se souvient de rien
print("\n=== Test 2 : sans historique ===")
ask(
    [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Bonjour, je m'appelle Ameni."},
    ]
)
print(
    ask(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "Comment je m'appelle ?"},
        ]
    )
)

# Test 3 : avec l'historique, il "se souvient"
print("\n=== Test 3 : avec historique ===")
history = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "Bonjour, je m'appelle Ameni."},
]
first_answer = ask(history)
history.append({"role": "assistant", "content": first_answer})
history.append({"role": "user", "content": "Comment je m'appelle ?"})
print(ask(history))
