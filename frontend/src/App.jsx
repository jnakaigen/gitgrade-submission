import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // IMPORTANT: This points to your local Python backend
const API_URL = "http://localhost:8000/analyze";
  const handleAnalyze = async () => {
    if (!url) return;
    
    setLoading(true);
    setError('');
    setData(null);

    try {
      // Send the URL to your backend
      const response = await axios.post(API_URL, { url });
      setData(response.data);
    } catch (err) {
      console.error(err);
      setError("Failed to connect. Is your Python backend running?");
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <div className="card">
        <h1>GitGrade</h1>
        <p>AI-Powered Repository Evaluator</p>
        
        <div className="input-group">
          <input 
            type="text" 
            placeholder="Paste GitHub Repository URL..." 
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <button onClick={handleAnalyze} disabled={loading}>
            {loading ? "Analyzing..." : "Grade It"}
          </button>
        </div>

        {error && <p className="error-msg">{error}</p>}

        {data && (
          <div className="results fade-in">
            <div className="score-box">
              <h2>{data.score}</h2>
              <span>/ 100</span>
            </div>
            
            <div className="info-box">
              <h3>Summary</h3>
              <p>{data.summary}</p>
            </div>

            <div className="info-box">
              <h3>Personalized Roadmap</h3>
              <ul>
                {data.roadmap.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;