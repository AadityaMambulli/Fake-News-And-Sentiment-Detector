import React from 'react';
import { ShieldCheck, AlertTriangle, Smile, Frown, Meh } from 'lucide-react';

export default function ResultCard({ fakeNews, sentiment }) {
  if (!fakeNews || !sentiment) return null;

  const fakePercentage = Math.round((fakeNews.confidence || 0) * 100);
  const sentimentPercentage = Math.round((sentiment.confidence || 0) * 100);

  const getFakeNewsBadgeClass = (label) => {
    return label === 'FAKE' ? 'badge-fake' : 'badge-real';
  };

  const getSentimentBadgeClass = (label) => {
    if (label === 'POSITIVE') return 'badge-positive';
    if (label === 'NEGATIVE') return 'badge-negative';
    return 'badge-neutral';
  };

  const renderSentimentIcon = (label) => {
    if (label === 'POSITIVE') return <Smile size={18} />;
    if (label === 'NEGATIVE') return <Frown size={18} />;
    return <Meh size={18} />;
  };

  return (
    <div className="results-grid">
      {/* Fake News Prediction Card */}
      <div className="result-card">
        <div className="result-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            {fakeNews.label === 'FAKE' ? (
              <AlertTriangle color="#fb7185" size={20} />
            ) : (
              <ShieldCheck color="#34d399" size={20} />
            )}
            <span className="result-type">Verification Status</span>
          </div>
          <span className={`badge ${getFakeNewsBadgeClass(fakeNews.label)}`}>
            {fakeNews.label}
          </span>
        </div>

        <div className="confidence-section">
          <div className="confidence-meta">
            <span>Model Confidence</span>
            <span className="confidence-value">{fakePercentage}%</span>
          </div>
          <div className="progress-bar-bg">
            <div
              className={`progress-bar-fill ${fakeNews.label === 'FAKE' ? 'bg-fake' : 'bg-real'}`}
              style={{ width: `${fakePercentage}%` }}
            />
          </div>
        </div>
      </div>

      {/* Sentiment Prediction Card */}
      <div className="result-card">
        <div className="result-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            {renderSentimentIcon(sentiment.label)}
            <span className="result-type">Sentiment Score</span>
          </div>
          <span className={`badge ${getSentimentBadgeClass(sentiment.label)}`}>
            {sentiment.label}
          </span>
        </div>

        <div className="confidence-section">
          <div className="confidence-meta">
            <span>Model Confidence</span>
            <span className="confidence-value">{sentimentPercentage}%</span>
          </div>
          <div className="progress-bar-bg">
            <div
              className={`progress-bar-fill ${
                sentiment.label === 'POSITIVE'
                  ? 'bg-positive'
                  : sentiment.label === 'NEGATIVE'
                  ? 'bg-negative'
                  : 'bg-neutral'
              }`}
              style={{ width: `${sentimentPercentage}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
