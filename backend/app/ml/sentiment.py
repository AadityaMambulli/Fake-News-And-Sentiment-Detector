import os
import logging
from transformers import pipeline

_sentiment_pipeline = None
_model_name = None

def get_sentiment_pipeline():
    global _sentiment_pipeline, _model_name
    if _sentiment_pipeline is None:
        _model_name = os.getenv("SENTIMENT_MODEL", "distilbert/distilbert-base-uncased-finetuned-sst-2-english")
        logging.info(f"Loading Sentiment Analysis model: {_model_name}")
        try:
            _sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model=_model_name,
                tokenizer=_model_name
            )
            logging.info("Sentiment model loaded successfully.")
        except Exception as e:
            logging.warning(f"Could not load Hugging Face sentiment model '{_model_name}': {e}. Using fallback sentiment analysis.")
            _sentiment_pipeline = "FALLBACK"
            
    return _sentiment_pipeline

def predict_sentiment(text: str) -> dict:
    """
    Predicts sentiment of text: POSITIVE, NEGATIVE, or NEUTRAL.
    Returns: {"label": "POSITIVE" | "NEGATIVE" | "NEUTRAL", "confidence": float}
    """
    pipe = get_sentiment_pipeline()
    
    if pipe == "FALLBACK":
        lowered = text.lower()
        pos_words = ["great", "good", "amazing", "success", "optimistic", "growth", "positive", "win", "victory"]
        neg_words = ["bad", "terrible", "disaster", "crisis", "corrupt", "death", "fail", "scam", "loss"]
        
        pos_count = sum(1 for w in pos_words if w in lowered)
        neg_count = sum(1 for w in neg_words if w in lowered)
        
        if pos_count > neg_count:
            return {"label": "POSITIVE", "confidence": 0.80}
        elif neg_count > pos_count:
            return {"label": "NEGATIVE", "confidence": 0.80}
        else:
            return {"label": "NEUTRAL", "confidence": 0.70}

    try:
        truncated_text = text[:1500]
        results = pipe(truncated_text)
        
        if isinstance(results, list) and len(results) > 0:
            top_pred = results[0]
            raw_label = str(top_pred.get('label', '')).upper()
            score = round(float(top_pred.get('score', 0.5)), 4)
            
            if "POS" in raw_label:
                final_label = "POSITIVE"
            elif "NEG" in raw_label:
                final_label = "NEGATIVE"
            elif "NEU" in raw_label:
                final_label = "NEUTRAL"
            else:
                final_label = raw_label
                
            return {"label": final_label, "confidence": score}
    except Exception as e:
        logging.error(f"Error during sentiment model inference: {e}")
        return {"label": "NEUTRAL", "confidence": 0.50}

    return {"label": "NEUTRAL", "confidence": 0.50}
