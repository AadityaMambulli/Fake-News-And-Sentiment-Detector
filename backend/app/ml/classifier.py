import os
import logging
from transformers import pipeline

_fake_news_pipeline = None
_model_name = None

# Candidate labels used for zero-shot classification.
# The model scores text against these two hypotheses.
_FAKE_LABEL = "fake news"
_REAL_LABEL = "real news"

def get_fake_news_pipeline():
    """
    Loads and caches a zero-shot classification pipeline.
    We use zero-shot because it lets us explicitly define what 'fake' and 'real' mean,
    avoiding the ambiguous LABEL_0/LABEL_1 problem of fine-tuned classifiers with no
    named output labels.
    """
    global _fake_news_pipeline, _model_name
    if _fake_news_pipeline is None:
        _model_name = os.getenv("FAKE_NEWS_MODEL", "typeform/distilbert-base-uncased-mnli")
        logging.info(f"Loading Fake News zero-shot model: {_model_name}")
        try:
            _fake_news_pipeline = pipeline(
                "zero-shot-classification",
                model=_model_name,
            )
            logging.info("Fake News model loaded successfully.")
        except Exception as e:
            logging.warning(
                f"Could not load Hugging Face model '{_model_name}': {e}. Using fallback classifier."
            )
            _fake_news_pipeline = "FALLBACK"

    return _fake_news_pipeline


def predict_fake_news(text: str) -> dict:
    """
    Predicts if input news text is FAKE or REAL using zero-shot classification.
    Returns: {"label": "FAKE" | "REAL", "confidence": float}
    """
    pipe = get_fake_news_pipeline()

    if pipe == "FALLBACK":
        # Simple keyword-based fallback when model is unavailable
        lowered = text.lower()
        fake_keywords = [
            "shocking truth", "conspiracy", "secret cured",
            "they don't want you to know", "miracle cure",
            "click here", "unbelievable", "cover-up", "hidden truth",
        ]
        fake_score = sum(1 for kw in fake_keywords if kw in lowered)
        if fake_score > 0:
            return {"label": "FAKE", "confidence": min(0.60 + (fake_score * 0.1), 0.95)}
        return {"label": "REAL", "confidence": 0.75}

    try:
        # Truncate to a reasonable length for the transformer token limit
        truncated_text = text[:1000]
        result = pipe(truncated_text, candidate_labels=[_FAKE_LABEL, _REAL_LABEL])

        # result structure: {"labels": ["fake news", "real news"], "scores": [0.87, 0.13], ...}
        top_label = result["labels"][0]
        top_score = round(float(result["scores"][0]), 4)

        final_label = "FAKE" if top_label == _FAKE_LABEL else "REAL"
        return {"label": final_label, "confidence": top_score}

    except Exception as e:
        logging.error(f"Error during fake news model inference: {e}")
        return {"label": "REAL", "confidence": 0.50}
