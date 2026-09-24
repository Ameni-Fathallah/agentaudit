# AgentAudit

Plateforme multi-agents d'audit de sécurité et de fiabilité des agents IA.

AgentAudit teste automatiquement un agent IA avant sa mise en production :
injections de prompt, fuites de données, abus d'outils, hallucinations et
conformité à l'AI Act. Il produit un rapport d'audit avec un score de risque
et propose un garde-fou entraîné pour corriger les failles détectées.

## Statut

En cours de développement (sprint 0).

## Avertissement éthique

AgentAudit est conçu pour tester uniquement des agents dont vous êtes
propriétaire ou pour lesquels vous disposez d'une autorisation écrite.
Les agents cibles fournis dans `targets/` sont volontairement vulnérables
et utilisent exclusivement des données fictives.

## Stack technique

Python · LangGraph · FastAPI · Ollama · Docker · GitHub Actions
