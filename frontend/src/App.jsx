import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // IMPORTANT: Points to your Python backend
  const API_URL = "http://localhost:8000/analyze"; 

  const handleAnalyze = async () => {
    if (!url) return;
    
    setLoading(true);
    setError('');
    setData(null);

    try {
      const response = await axios.post(API_URL, { url });
      setData(response.data);
    } catch (err) {
      console.error(err);
      setError("CONNECTION ERROR: Backend not found or API Limit Reached.");
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <div className="card">
        <h1>GitGrade_AI</h1>
        <p className="subtitle">SYSTEM STATUS: ONLINE</p>
        
        <div className="input-group">
          <input 
            type="text" 
            placeholder="ENTER REPOSITORY URL..." 
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <button onClick={handleAnalyze} disabled={loading}>
            {loading ? "SCANNING..." : "INITIATE"}
          </button>
        </div>

        {error && <p style={{color: '#ff4444', fontFamily: 'Orbitron'}}>{error}</p>}

        {loading && (
           <div className="scanning-bar"></div>
        )}

        {data && (
          <div className="results">
            <div className="score-container">
              <div className="score-circle">
                <div className="score-text">
                  <h2>{data.score}</h2>
                  <span>QUALITY INDEX</span>
                </div>
              </div>
            </div>
            
            <div className="info-box">
              <h3>// EXECUTIVE SUMMARY</h3>
              <p>{data.summary}</p>
            </div>

            <div className="info-box">
              <h3>// OPTIMIZATION PROTOCOLS</h3>
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