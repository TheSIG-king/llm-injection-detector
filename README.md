# 🛡️ LLM Injection Detector

**Real-time prompt injection & jailbreak detection middleware for LLM applications.**

*Read this in [French / Français](README.fr.md).*

<!-- Once your HuggingFace Space is live, replace the URL below -->
[![Live Demo](https://img.shields.io/badge/🤗_Live_Demo-HuggingFace_Spaces-yellow)](https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

Prompt injection is ranked **#1 in the OWASP Top 10 for LLM Applications (2025, LLM01)**.
This project builds a defensive middleware that sits between the user and the LLM and
classifies every input as benign or malicious in real time — like a WAF, but for LLMs.

---

## 📊 Key result: adversarial hardening

Adversarial training reduced the evasion rate on **unseen** obfuscated attacks
from **33.3% to 2.8%** — a 30-point improvement — by adding just 48 adversarial
examples (1.5% of the dataset).

![Adversarial hardening results](adversarial_hardening.png)

*Tested on 36 attacks generated from base phrases absent from the training set (no leakage).*

---

## Results at a glance

| Metric | Value |
|--------|-------|
| Detection F1 (hardened model) | 0.97 |
| Evasion rate — before hardening | 33.3% |
| Evasion rate — after hardening | **2.8%** |
| Adversarial examples added | 48 (1.5% of dataset) |
| Non-regression on legitimate inputs | 6/6 ✅ |

### Robustness map (3 attack surfaces)

| Attack category | Evasion rate | Real weakness |
|-----------------|--------------|---------------|
| Obfuscation (surface) | 28.6% | Most vulnerable — fixed by hardening |
| Semantic (meaning) | 14.3% | Robust: embeddings capture intent |
| Multilingual | 12.5% | Fragile on non-Latin scripts |

---

## How it works

The middleware intercepts each message, runs it through the detector, and either
blocks it or forwards it to the LLM:

```
user message
     │
     ▼
[ detector ]  ──malicious?──►  YES  →  block, return a refusal
     │
     NO
     │
     ▼
[ LLM ]  →  return the response
```

**Pipeline:** text → sentence embeddings (`all-MiniLM-L6-v2`) → logistic-regression
classifier → verdict + confidence score.

---

## Quick start

```bash
# 1. Clone and set up
git clone https://github.com/TheSIG-king/llm-injection-detector.git
cd llm-injection-detector
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Run the interactive demo (compares v2 vs v3 side by side)
python demo.py

# 3. Or run the API
uvicorn app.main:app --reload
# Interactive docs at http://127.0.0.1:8000/docs
```

### API endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /detect` | Analyze a text → verdict (benign/malicious) + confidence |
| `POST /chat` | Full middleware: detect, then block or forward to the LLM |

---

## Project journey

Built in five phases, each ending with a concrete deliverable:

1. **Dataset** — unified & balanced 3,120 examples from 3 heterogeneous public sources.
2. **Baseline detector** — embeddings + classifier; diagnosed and fixed a register bias (F1 0.95 → 0.97).
3. **Middleware** — FastAPI service with detection, decision logic, and logging.
4. **Adversarial robustness** — attack mapping + hardening via adversarial training (33.3% → 2.8% evasion).
5. **Packaging** — interactive demo, benchmark, documentation.

---

## Known limitations

Honest about what this does *not* solve:

- **Multilingual coverage is uneven** — Latin scripts are handled well; non-Latin scripts (Arabic, and Chinese at low confidence) remain fragile. A multilingual embedding model would be the fix.
- **The confidence "grey zone"** — very polite/indirect phrasings can push confidence toward 0.5. A graded response (allow / flag / block) would handle this better than a binary threshold.
- **Adversarial hardening is a moving target** — this neutralizes known obfuscation techniques, but new ones can be crafted. It raises the cost of attack; it does not "solve" it.

---

## Tech stack

Python · HuggingFace Sentence Transformers · scikit-learn · FastAPI · Gradio

## License

MIT