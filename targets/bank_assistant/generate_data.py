"""Génère les fausses données de BanqueNova : clients, comptes et transactions.

Les données sont entièrement fictives et reproductibles grâce à une graine fixe.
Usage : uv run python -m targets.bank_assistant.generate_data
"""

import json
import unicodedata
from datetime import date, datetime, time, timedelta
from itertools import count
from pathlib import Path

from faker import Faker
from pydantic import BaseModel

from targets.bank_assistant.data_models import (
    Client,
    Compte,
    Segment,
    Transaction,
    TypeCompte,
    TypeOperation,
)

SEED = 42
NB_CLIENTS = 50
# Date de référence fixe : les données ne changent pas selon le jour d'exécution.
REFERENCE_DATE = date(2026, 9, 1)
OUTPUT_DIR = Path("data/generated/bank")

PRENOMS = [
    "Ahmed",
    "Mohamed",
    "Youssef",
    "Karim",
    "Sami",
    "Walid",
    "Hamza",
    "Amine",
    "Fatma",
    "Amira",
    "Salma",
    "Ines",
    "Mariem",
    "Rania",
    "Nour",
    "Yasmine",
]
NOMS = [
    "Ben Salah",
    "Gharbi",
    "Jlassi",
    "Mejri",
    "Hammami",
    "Chaabane",
    "Khelifi",
    "Mansouri",
    "Ayari",
    "Sassi",
    "Dridi",
    "Ben Amor",
    "Zouari",
    "Feki",
    "Abidi",
]
VILLES = [
    "Tunis",
    "Ariana",
    "Ben Arous",
    "La Marsa",
    "Sfax",
    "Sousse",
    "Monastir",
    "Nabeul",
    "Bizerte",
    "Gabès",
    "Kairouan",
]
RUES = [
    "Avenue Habib Bourguiba",
    "Rue de Marseille",
    "Avenue de la Liberté",
    "Rue Ibn Khaldoun",
    "Avenue Hédi Chaker",
    "Rue de Palestine",
    "Avenue de Carthage",
    "Rue Mongi Slim",
]
# Domaines réservés aux exemples : ils n'appartiendront jamais à personne.
DOMAINES_EMAIL = ["example.com", "example.org", "example.net"]
FACTURES = ["Facture électricité", "Facture eau", "Abonnement téléphone", "Assurance habitation"]
MULTIPLICATEUR_SOLDE = {Segment.PARTICULIER: 1, Segment.PROFESSIONNEL: 4, Segment.PREMIUM: 10}


def sans_accents(texte: str) -> str:
    """Supprime les accents et les espaces, pour construire une adresse email."""
    texte = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode()
    return texte.lower().replace(" ", "")


def date_avant_reference(fake: Faker, min_jours: int, max_jours: int) -> date:
    """Tire une date entre min_jours et max_jours avant la date de référence."""
    return REFERENCE_DATE - timedelta(days=fake.random_int(min_jours, max_jours))


def generer_client(fake: Faker, numero: int) -> Client:
    prenom = fake.random_element(PRENOMS)
    nom = fake.random_element(NOMS)
    email = (
        f"{sans_accents(prenom)}.{sans_accents(nom)}{fake.random_int(1, 99)}"
        f"@{fake.random_element(DOMAINES_EMAIL)}"
    )
    return Client(
        client_id=f"C{numero:04d}",
        prenom=prenom,
        nom=nom,
        cin=fake.random_element(["0", "1"]) + fake.numerify("#######"),
        date_naissance=date_avant_reference(fake, 18 * 365, 80 * 365),
        telephone="+216 " + fake.random_element(["2", "5", "9"]) + fake.numerify("# ### ###"),
        email=email,
        adresse=f"{fake.random_int(1, 150)}, {fake.random_element(RUES)}",
        ville=fake.random_element(VILLES),
        segment=fake.random.choices(list(Segment), weights=[70, 20, 10])[0],
        date_inscription=date_avant_reference(fake, 365, 10 * 365),
    )


def montant_et_libelle(fake: Faker, type_op: TypeOperation, ville: str) -> tuple[float, str]:
    """Renvoie un montant (négatif pour un débit) et un libellé réalistes."""
    match type_op:
        case TypeOperation.PAIEMENT_CARTE:
            return -round(fake.random.uniform(5, 400), 3), f"Paiement carte {fake.company()}"
        case TypeOperation.RETRAIT:
            montant = fake.random_element([20, 50, 100, 200, 300, 500])
            return -float(montant), f"Retrait DAB {ville}"
        case TypeOperation.VIREMENT:
            beneficiaire = f"{fake.random_element(PRENOMS)} {fake.random_element(NOMS)}"
            return -round(fake.random.uniform(50, 3000), 3), f"Virement vers {beneficiaire}"
        case TypeOperation.DEPOT:
            return round(fake.random.uniform(100, 5000), 3), f"Dépôt espèces agence {ville}"
        case TypeOperation.PRELEVEMENT:
            libelle = f"Prélèvement {fake.random_element(FACTURES)}"
            return -round(fake.random.uniform(20, 250), 3), libelle
        case _:
            raise ValueError(f"Type d'opération inconnu : {type_op}")


def generer_transactions(
    fake: Faker, compte: Compte, ville: str, compteur: count
) -> list[Transaction]:
    if compte.type_compte == TypeCompte.COURANT:
        nombre = fake.random_int(15, 40)
        types = list(TypeOperation)
        poids = [40, 20, 15, 15, 10]
    else:
        nombre = fake.random_int(2, 8)
        types = [TypeOperation.DEPOT, TypeOperation.VIREMENT]
        poids = [70, 30]

    transactions = []
    for _ in range(nombre):
        type_op = fake.random.choices(types, weights=poids)[0]
        montant, libelle = montant_et_libelle(fake, type_op, ville)
        minutes = fake.random_int(0, 180 * 24 * 60)  # sur les 180 jours précédents
        date_heure = datetime.combine(REFERENCE_DATE, time()) - timedelta(minutes=minutes)
        transactions.append(
            Transaction(
                transaction_id=f"T{next(compteur):06d}",
                compte_id=compte.compte_id,
                date_heure=date_heure,
                montant=montant,
                type_operation=type_op,
                libelle=libelle,
            )
        )
    return sorted(transactions, key=lambda t: t.date_heure)


def sauvegarder(nom_fichier: str, objets: list[BaseModel]) -> None:
    chemin = OUTPUT_DIR / nom_fichier
    donnees = [objet.model_dump(mode="json") for objet in objets]
    chemin.write_text(json.dumps(donnees, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    fake = Faker("fr_FR")
    fake.seed_instance(SEED)
    compteur_comptes = count(1)
    compteur_transactions = count(1)

    clients: list[Client] = []
    comptes: list[Compte] = []
    transactions: list[Transaction] = []

    for numero in range(1, NB_CLIENTS + 1):
        client = generer_client(fake, numero)
        clients.append(client)

        types_comptes = [TypeCompte.COURANT]
        if fake.boolean(chance_of_getting_true=50):
            types_comptes.append(TypeCompte.EPARGNE)

        for type_compte in types_comptes:
            compte = Compte(
                compte_id=f"A{next(compteur_comptes):05d}",
                client_id=client.client_id,
                type_compte=type_compte,
                rib="99" + fake.numerify("#" * 18),
                solde=0.0,
                date_ouverture=client.date_inscription + timedelta(days=fake.random_int(0, 30)),
            )
            operations = generer_transactions(fake, compte, client.ville, compteur_transactions)
            solde_initial = fake.random.uniform(500, 5000) * MULTIPLICATEUR_SOLDE[client.segment]
            compte.solde = round(solde_initial + sum(t.montant for t in operations), 3)
            comptes.append(compte)
            transactions.extend(operations)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sauvegarder("clients.json", clients)
    sauvegarder("comptes.json", comptes)
    sauvegarder("transactions.json", transactions)

    print(f"{len(clients)} clients, {len(comptes)} comptes, {len(transactions)} transactions")
    print(f"Fichiers enregistrés dans {OUTPUT_DIR}/")
    print("\nExemple de client :")
    print(json.dumps(clients[0].model_dump(mode="json"), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
