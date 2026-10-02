from flask import Blueprint, request, jsonify
from app.ml.preprocessing import validate_input
from app.ml.classifier import predict_fake_news
from app.ml.sentiment import predict_sentiment
from app.database.db import save_analysis

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify backend status."""
    return jsonify({"status": "ok"}), 200

@api_bp.route('/analyze', methods=['POST'])
def analyze_text():
    """
    Main analysis endpoint. Accepts text in JSON body, runs classification
    and sentiment models, and returns structured predictions.
    """
    try:
        data = request.get_json(silent=True)
        is_valid, text_or_error = validate_input(data)
        
        if not is_valid:
            return jsonify({
                "success": False,
                "error": text_or_error
            }), 400
        
        cleaned_text = text_or_error
        
        # 1. Run Fake-News Model Inference
        fake_news_res = predict_fake_news(cleaned_text)
        
        # 2. Run Sentiment Model Inference
        sentiment_res = predict_sentiment(cleaned_text)
        
        # 3. Optional DB Persistence
        saved_id = save_analysis(cleaned_text, fake_news_res, sentiment_res)
        
        return jsonify({
            "success": True,
            "fake_news": fake_news_res,
            "sentiment": sentiment_res,
            "record_id": saved_id
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"An unexpected error occurred during processing: {str(e)}"
        }), 500
