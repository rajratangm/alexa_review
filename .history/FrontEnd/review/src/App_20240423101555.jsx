import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [review, setReview] = useState('');
  const [prediction, setPrediction] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/predict', { review });
      setPrediction(response.data.prediction);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h1>Amazon Alexa Reviews Sentiment Analysis</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Enter your review:
          <textarea value={review} onChange={(e) => setReview(e.target.value)} />
        </label>
        <button type="submit">Predict</button>
      </form>
      {prediction !== null && (
        <div>
          <h2>Prediction: {prediction === 1 ? 'Positive' : 'Negative'}</h2>
        </div>
      )}
    </div>
  );
}

export default App;
