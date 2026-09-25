"""Modèles de données de la banque fictive BanqueNova.

Toutes les données sont fictives et générées automatiquement.
"""

from datetime import date, datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class Segment(StrEnum):
    PARTICULIER = "particulier"
    PROFESSIONNEL = "professionnel"
    PREMIUM = "premium"


class TypeCompte(StrEnum):
    COURANT = "courant"
    EPARGNE = "epargne"


class TypeOperation(StrEnum):
    PAIEMENT_CARTE = "paiement_carte"
    RETRAIT = "retrait"
    VIREMENT = "virement"
    DEPOT = "depot"
    PRELEVEMENT = "prelevement"


class Client(BaseModel):
    client_id: str = Field(pattern=r"^C\d{4}$")
    prenom: str
    nom: str
    cin: str = Field(
        pattern=r"^\d{8}$",
        description="Numéro de carte d'identité nationale (fictif)",
    )
    date_naissance: date
    telephone: str
    email: str
    adresse: str
    ville: str
    segment: Segment
    date_inscription: date


class Compte(BaseModel):
    compte_id: str = Field(pattern=r"^A\d{5}$")
    client_id: str
    type_compte: TypeCompte
    rib: str = Field(
        pattern=r"^\d{20}$",
        description="Relevé d'identité bancaire (fictif)",
    )
    solde: float = Field(description="Solde en dinars tunisiens (TND)")
    date_ouverture: date


class Transaction(BaseModel):
    transaction_id: str = Field(pattern=r"^T\d{6}$")
    compte_id: str
    date_heure: datetime
    montant: float = Field(description="Positif pour un crédit, négatif pour un débit (TND)")
    type_operation: TypeOperation
    libelle: str
