"""
Interface d'appel au LLM.

Version actuelle : mock (simulation) pour développer sans coût.
Pour brancher un vrai LLM plus tard, il suffit de remplacer le corps
de la fonction `call_llm` par un appel API réel (Mistral, OpenAI, Anthropic...).
"""
def call_llm(message: str) -> str:
    """
    Simule un appel à un LLM.
    Renvoie une réponse factice mais réaliste.
    """
    return (
        f"[LLM SIMULÉ] J'ai bien reçu votre message : « {message[:100]} ». "
        f"Voici une réponse générée par le modèle."
    )