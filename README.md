# llm-injection-detector

Real-time prompt injection & jailbreak detection middleware for LLM applications.

## Le problème
Les applications basées sur des LLM sont exposées à des vulnérabilités propres à
l'IA. La prompt injection est classée n°1 du OWASP Top 10 for LLM Applications
(édition 2025, LLM01). Une attaque réussie peut entraîner une fuite de données
sensibles, un contournement des garde-fous ou une manipulation du comportement
de l'application.

## L'objectif
Construire un middleware défensif qui s'intercale entre l'utilisateur et le LLM,
et classe chaque entrée comme bénigne ou malveillante en temps réel — à la manière
d'un WAF, mais pour les LLM.

## Menaces couvertes
- Prompt injection directe et indirecte (LLM01:2025)
- Jailbreak / contournement de garde-fous
- Fuite de prompt système (LLM07:2025)

## Roadmap
- [ ] Phase 1 — Constitution et analyse du dataset
- [ ] Phase 2 — Détecteur baseline (embeddings + classifieur)
- [ ] Phase 3 — Middleware temps réel (API)
- [ ] Phase 4 — Robustesse adversariale
- [ ] Phase 5 — Packaging, benchmark, démo

## Stack
Python · HuggingFace · scikit-learn / PyTorch · FastAPI

## Statut
🚧 En cours de développement — projet d'études (2026-2028)