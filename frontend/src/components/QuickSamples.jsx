import React from 'react';

const SAMPLES = [
  {
    label: "Genuine Tech News",
    text: "Tech giant announces a breakthrough in quantum computing power, drastically reducing energy consumption by 40% in initial lab benchmarks."
  },
  {
    label: "Suspicious Clickbait",
    text: "SHOCKING SECRET! Scientists discover 100% cure for aging hidden in basic kitchen ingredient. Big pharma doesn't want you to know this!"
  },
  {
    label: "Negative Market Report",
    text: "Global stock markets experienced a sharp downturn today as rising inflation concerns and supply chain disruptions spooked investors."
  }
];

export default function QuickSamples({ onSelectSample, disabled }) {
  return (
    <div className="samples-container">
      <div className="samples-title">Try Example Headlines:</div>
      <div className="sample-chips">
        {SAMPLES.map((sample, idx) => (
          <button
            key={idx}
            type="button"
            className="chip"
            disabled={disabled}
            onClick={() => onSelectSample(sample.text)}
          >
            {sample.label}
          </button>
        ))}
      </div>
    </div>
  );
}
