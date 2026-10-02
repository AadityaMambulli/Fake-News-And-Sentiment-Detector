import React, { useState } from 'react';
import Header from './components/Header';
import AnalysisForm from './components/AnalysisForm';
import ResultCard from './components/ResultCard';
import { analyzeText } from './services/api';

export default function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const handleAnalyze = async (text) => {
    setLoading(true);
    setError(null);
    try {
      const data = await analyzeText(text);
      setResult(data);
    } catch (err) {
      setError(err.message || 'Failed to analyze text. Ensure backend service is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <Header />
      
      <main>
        <AnalysisForm
          onAnalyze={handleAnalyze}
          loading={loading}
          error={error}
        />

        {result && (
          <ResultCard
            fakeNews={result.fake_news}
            sentiment={result.sentiment}
          />
        )}
      </main>

      <footer className="footer">
        Fake News & Sentiment Detector — Built with React, Flask & Hugging Face Transformers
      </footer>
    </div>
  );
}
