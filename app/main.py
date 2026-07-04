from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from app.llm import call_llm
import joblib
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("detections.log"),  # écrit dans un fichier
        logging.StreamHandler(),                 # affiche aussi dans le terminal
    ],
)
logger = logging.getLogger("detector")
# Réduire le bruit des bibliothèques tierces
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("sentence_transformers").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Chargement des modèles (une seule fois, au démarrage) 
print("Chargement de l'encodeur d'embeddings...")
encoder = SentenceTransformer("all-MiniLM-L6-v2")

print("Chargement du classifieur...")
classifier = joblib.load("models/baseline_logreg_v2.joblib")

print("Prêt.")

# L'application 
app=FastAPI(title="LLM Injection Detector", version="0.1.0")

#  Schéma de la requête entrante 
class DetectionRequest(BaseModel):
    text: str

# Schéma de la réponse 
class DetectionResponse(BaseModel):
    text: str
    is_malicious: bool
    confidence: float
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    blocked: bool
    detection_confidence: float
    response: str
# Route de santé (vérifier que l'API tourne) 
@app.get("/")
def health():
    return {"status": "ok", "service": "llm-injection-detector"}

# Route de détection 
@app.post("/detect", response_model=DetectionResponse)
def detect(request: DetectionRequest):
    # 1. Encoder le texte en embedding
    embedding = encoder.encode([request.text])
    # 2. Prédire
    prediction = classifier.predict(embedding)[0]
    proba = classifier.predict_proba(embedding)[0]
    # 3. Log de la détection
    logger.info(
        f"detection | malicious={bool(prediction == 1)} | "
        f"confidence={float(proba[prediction]):.3f} | "
        f"text={request.text[:80]!r}"
    )
    # 4. Construire la réponse
    return DetectionResponse(
        text=request.text,
        is_malicious=bool(prediction == 1),
        confidence=float(proba[prediction]),
    )

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # 1. Passer le message au détecteur
    embedding = encoder.encode([request.message])
    prediction = classifier.predict(embedding)[0]
    proba = classifier.predict_proba(embedding)[0]
    is_malicious = bool(prediction == 1)
    confidence = float(proba[prediction])

    # 2. Décision du middleware
    if is_malicious:
        logger.warning(
            f"BLOCKED | confidence={confidence:.3f} | message={request.message[:80]!r}"
        )
        return ChatResponse(
            blocked=True,
            detection_confidence=confidence,
            response="Requête bloquée : contenu potentiellement malveillant détecté.",
        )

    # 3. Si bénin, transmettre au LLM
    logger.info(
        f"ALLOWED | confidence={confidence:.3f} | message={request.message[:80]!r}"
    )
    llm_response = call_llm(request.message)
    return ChatResponse(
        blocked=False,
        detection_confidence=confidence,
        response=llm_response,
    )