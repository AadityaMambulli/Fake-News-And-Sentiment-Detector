import React from 'react';
import { ShieldAlert, Sparkles } from 'lucide-react';

export default function Header() {
  return (
    <header className="app-header">
      <div className="app-badge">
        <Sparkles size={14} />
        <span>Hugging Face Neural Pipeline</span>
      </div>
      <h1 className="app-title">Fake News & Sentiment Detector</h1>
      <p className="app-subtitle">
        Real-time NLP classification engine powered by pretrained BERT Transformer models.
      </p>
    </header>
  );
}
