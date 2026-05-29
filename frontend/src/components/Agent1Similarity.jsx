import { useState } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001';

function App() {
  const [jdFile, setJdFile] = useState(null);
  const [resumeFile, setResumeFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(() => {
    const saved = sessionStorage.getItem('agent1_results');
    return saved ? JSON.parse(saved) : null;
  });
  const [error, setError] = useState(null);

  const handleEvaluate = async () => {
    if (!jdFile || !resumeFile) {
      setError('Please upload both Job Description and Resume files');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      // Create FormData to send files
      const formData = new FormData();
      formData.append('jd_file', jdFile);
      formData.append('resume_file', resumeFile);

      // Call backend API
      const response = await axios.post(`${API_BASE_URL}/agent1/evaluate`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResults(response.data);
      
      // Persist to sessionStorage (clears on browser close/refresh)
      sessionStorage.setItem('agent1_results', JSON.stringify(response.data));
    } catch (err) {
      console.error('Error:', err);
      setError(err.response?.data?.detail || err.message || 'An error occurred during evaluation');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setJdFile(null);
    setResumeFile(null);
    setResults(null);
    setError(null);
  };

  return (
    <div className="container">
      <div className="header">
        <h1 className="title">Interview Assistant</h1>
        <p className="subtitle">AI-powered JD-Resume Similarity Analysis</p>
      </div>

      <div className="upload-section">
        <div className="upload-grid">
          <FileUpload
            label="Job Description"
            selectedFile={jdFile}
            onFileSelect={setJdFile}
          />
          <FileUpload
            label="Resume"
            selectedFile={resumeFile}
            onFileSelect={setResumeFile}
          />
        </div>

        <div className="buttons">
          <button
            onClick={handleEvaluate}
            disabled={!jdFile || !resumeFile || loading}
            className="btn btn-primary"
          >
            {loading ? (
              <div className="loading">
                <div className="spinner"></div>
                <span>Analyzing...</span>
              </div>
            ) : (
              'Evaluate Similarity'
            )}
          </button>
          
          <button onClick={resetForm} className="btn btn-secondary">
            Reset
          </button>
        </div>
      </div>

      {error && (
        <div className="error">
          <div className="error-content">
            <div>
              <h3 className="error-title">Error</h3>
              <p className="error-message">{error}</p>
            </div>
          </div>
        </div>
      )}

      {results && <Results results={results} />}
    </div>
  );
}

const FileUpload = ({ label, selectedFile, onFileSelect }) => {
  const handleDrop = (e) => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      onFileSelect(files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files.length > 0) {
      onFileSelect(e.target.files[0]);
    }
  };

  const removeFile = (e) => {
    e.stopPropagation();
    onFileSelect(null);
  };

  return (
    <div className="file-upload">
      <label className="file-label">{label}</label>
      
      <div
        className={`dropzone ${selectedFile ? 'has-file' : ''}`}
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
        onClick={() => document.getElementById(`file-${label}`).click()}
      >
        <input
          id={`file-${label}`}
          type="file"
          accept=".pdf,.docx,.txt"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
        
        {selectedFile ? (
          <div className="file-info">
            <div className="file-details">
              <div>
                <p className="file-name">{selectedFile.name}</p>
                <p className="file-size">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>
            <button onClick={removeFile} className="remove-btn">
              ✕
            </button>
          </div>
        ) : (
          <div>
            <p>📄</p>
            <p>Drag & drop a file here, or click to select</p>
            <p style={{ fontSize: '0.75rem', color: '#6b7280', marginTop: '0.25rem' }}>
              Supports PDF, DOCX, TXT files
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

const Results = ({ results }) => {
  const [showMatches, setShowMatches] = useState(false);
  const [showMissing, setShowMissing] = useState(false);

  if (!results) return null;

  const { similarity_score, match_percentage, key_matches, missing_skills, recommendations, candidate_id, candidate_name, status } = results;
  const isGoodScore = match_percentage >= 70;

  return (
    <div className="results">
      {candidate_id && (
        <div className="candidate-info">
          <h3 className="candidate-info-title">Candidate Information</h3>
          <div className="candidate-details">
            <div className="candidate-field">
              <span className="candidate-label">Candidate ID:</span>
              <span className="candidate-value">{candidate_id}</span>
            </div>
            <div className="candidate-field">
              <span className="candidate-label">Name:</span>
              <span className="candidate-value">{candidate_name}</span>
            </div>
            <div className="candidate-field">
              <span className="candidate-label">Status:</span>
              <span className={`candidate-status ${status === 'shortlisted' ? 'shortlisted' : 'pending'}`}>
                {status === 'shortlisted' ? '✓ Shortlisted' : 'Pending'}
              </span>
            </div>
          </div>
        </div>
      )}
      
      <div className="results-header">
        <h2 className="results-title">Similarity Analysis</h2>
        
        <div className={`score-circle ${isGoodScore ? 'good' : 'bad'}`}>
          <span className={`score-text ${isGoodScore ? 'good' : 'bad'}`}>
            {match_percentage}%
          </span>
        </div>
        
        <p className={`status-text ${isGoodScore ? 'good' : 'bad'}`}>
          {isGoodScore ? 'Shortlisted (70%+)' : 'Not Shortlisted (<70%)'}
        </p>
      </div>

      <div className="results-grid">
        <div className="section">
          <button
            onClick={() => setShowMatches(!showMatches)}
            className="section-btn"
          >
            <span className="section-title">
              Key Matches ({key_matches?.length || 0})
            </span>
            <span>{showMatches ? '▲' : '▼'}</span>
          </button>
          
          {showMatches && (
            <div className="section-content">
              {key_matches?.length > 0 ? (
                key_matches.map((match, index) => (
                  <div key={index} className="match-item">
                    <p className="item-text">{match}</p>
                  </div>
                ))
              ) : (
                <p className="item-text" style={{ fontStyle: 'italic' }}>No key matches found</p>
              )}
            </div>
          )}
        </div>

        <div className="section">
          <button
            onClick={() => setShowMissing(!showMissing)}
            className="section-btn"
          >
            <span className="section-title">
              Missing Skills ({missing_skills?.length || 0})
            </span>
            <span>{showMissing ? '▲' : '▼'}</span>
          </button>
          
          {showMissing && (
            <div className="section-content">
              {missing_skills?.length > 0 ? (
                missing_skills.map((skill, index) => (
                  <div key={index} className="missing-item">
                    <p className="item-text" style={{ textTransform: 'capitalize' }}>{skill}</p>
                  </div>
                ))
              ) : (
                <p className="item-text" style={{ fontStyle: 'italic' }}>No missing skills identified</p>
              )}
            </div>
          )}
        </div>
      </div>

      <div className="recommendations">
        <h3 className="recommendations-title">Recommendations</h3>
        <p className="recommendations-text">{recommendations}</p>
      </div>
    </div>
  );
};

export default App;