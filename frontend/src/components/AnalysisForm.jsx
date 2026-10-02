import React, { useState } from 'react';
import { Send, RotateCcw, AlertCircle } from 'lucide-react';
import QuickSamples from './QuickSamples';

export default function AnalysisForm({ onAnalyze, loading, error }) {
  const [text, setText] = useState('');
  const [validationError, setValidationError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!text.trim()) {
      setValidationError('Please enter or paste news content before submitting.');
      return;
    }
    setValidationError('');
    onAnalyze(text);
  };

  const handleClear = () => {
    setText('');
    setValidationError('');
  };

  const handleSelectSample = (sampleText) => {
    setText(sampleText);
    setValidationError('');
  };

  return (
    <div className="glass-card">
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <div className="form-label">
            <span>News Article or Text</span>
            <span className="char-counter">{text.length} / 10000 chars</span>
          </div>
          <textarea
            id="news-input-textarea"
            className="news-textarea"
            placeholder="Paste your news article, headline, or paragraph here to evaluate authenticity and emotional sentiment..."
            value={text}
            onChange={(e) => {
              setText(e.target.value);
              if (validationError) setValidationError('');
            }}
            disabled={loading}
          />
        </div>

        {validationError && (
          <div className="alert-error" style={{ marginTop: '1rem' }}>
            <AlertCircle size={18} />
            <span>{validationError}</span>
          </div>
        )}

        {error && (
          <div className="alert-error" style={{ marginTop: '1rem' }}>
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        <QuickSamples onSelectSample={handleSelectSample} disabled={loading} />

        <div className="form-actions">
          {text && (
            <button
              type="button"
              className="btn btn-secondary"
              onClick={handleClear}
              disabled={loading}
            >
              <RotateCcw size={16} />
              Clear
            </button>
          )}
          <button
            type="submit"
            id="analyze-submit-btn"
            className="btn btn-primary"
            disabled={loading || !text.trim()}
          >
            {loading ? (
              <>
                <div className="spinner"></div>
                Analyzing...
              </>
            ) : (
              <>
                <Send size={16} />
                Analyze Text
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
