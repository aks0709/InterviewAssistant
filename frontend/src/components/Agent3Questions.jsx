import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Agent3Questions = () => {
  const [candidateId, setCandidateId] = useState('');
  const [customRequirements, setCustomRequirements] = useState('');
  const [showCustomInput, setShowCustomInput] = useState(false);
  const [questions, setQuestions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const savedResults = sessionStorage.getItem('agent1Results');
    if (savedResults) {
      const results = JSON.parse(savedResults);
      if (results.candidate_id) {
        setCandidateId(results.candidate_id.toString());
      }
    }

    const savedQuestions = sessionStorage.getItem('agent3Questions');
    if (savedQuestions) {
      setQuestions(JSON.parse(savedQuestions));
    }
  }, []);

  const handleGenerate = async () => {
    if (!candidateId) {
      setError('Please enter a candidate ID');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:8001/agent3/questions', {
        candidate_id: parseInt(candidateId),
        custom_requirements: customRequirements || null
      });

      setQuestions(response.data);
      sessionStorage.setItem('agent3Questions', JSON.stringify(response.data));
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate questions');
      setQuestions(null);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadJSON = () => {
    if (!questions) return;

    const dataStr = JSON.stringify(questions, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `interview_questions_candidate_${questions.candidate_id}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const handleDownloadTXT = () => {
    if (!questions) return;

    let content = `Interview Questions for ${questions.candidate_name}\n`;
    content += `Candidate ID: ${questions.candidate_id}\n`;
    content += `Email: ${questions.candidate_email}\n`;
    content += `Skills: ${questions.skills.join(', ')}\n`;
    if (questions.custom_requirements) {
      content += `Custom Requirements: ${questions.custom_requirements}\n`;
    }
    content += `\n${'='.repeat(80)}\n\n`;

    content += `EASY QUESTIONS (5)\n${'='.repeat(80)}\n\n`;
    questions.questions.easy.forEach((q, i) => {
      content += `${i + 1}. ${q}\n\n`;
    });

    content += `\nMEDIUM QUESTIONS (5)\n${'='.repeat(80)}\n\n`;
    questions.questions.medium.forEach((q, i) => {
      content += `${i + 1}. ${q}\n\n`;
    });

    content += `\nHARD QUESTIONS (5)\n${'='.repeat(80)}\n\n`;
    questions.questions.hard.forEach((q, i) => {
      content += `${i + 1}. ${q}\n\n`;
    });

    const dataBlob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `interview_questions_candidate_${questions.candidate_id}.txt`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const handleReset = () => {
    setQuestions(null);
    setCustomRequirements('');
    setShowCustomInput(false);
    setError('');
    sessionStorage.removeItem('agent3Questions');
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="agent3-container">
      <div className="agent3-header">
        <h2>🎯 Interview Questions Generator</h2>
        <p>Generate tailored interview questions based on candidate skills</p>
      </div>

      <div className="agent3-form">
        <div className="form-group">
          <label>Candidate ID</label>
          <input
            type="number"
            value={candidateId}
            onChange={(e) => setCandidateId(e.target.value)}
            placeholder="Enter candidate ID"
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <div className="custom-toggle">
            <label>
              <input
                type="checkbox"
                checked={showCustomInput}
                onChange={(e) => setShowCustomInput(e.target.checked)}
                disabled={loading}
              />
              Add Custom Requirements
            </label>
          </div>
        </div>

        {showCustomInput && (
          <div className="form-group">
            <label>Custom Requirements (Optional)</label>
            <textarea
              value={customRequirements}
              onChange={(e) => setCustomRequirements(e.target.value)}
              placeholder="E.g., Focus on React hooks and state management, include system design questions..."
              rows="3"
              disabled={loading}
            />
          </div>
        )}

        <div className="form-actions">
          <button 
            onClick={handleGenerate} 
            disabled={loading || !candidateId}
            className="btn-primary"
          >
            {loading ? 'Generating...' : '✨ Generate Questions'}
          </button>
          {questions && (
            <button onClick={handleReset} className="btn-secondary">
              🔄 Reset
            </button>
          )}
        </div>

        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}
      </div>

      {questions && (
        <div className="questions-results">
          <div className="results-header">
            <div className="candidate-summary">
              <h3>📋 Questions for {questions.candidate_name}</h3>
              <div className="summary-details">
                <span className="detail-item">
                  <strong>ID:</strong> {questions.candidate_id}
                </span>
                <span className="detail-item">
                  <strong>Email:</strong> {questions.candidate_email}
                </span>
              </div>
            </div>

            <div className="action-buttons">
              <button onClick={handleDownloadJSON} className="btn-download">
                📥 Download JSON
              </button>
              <button onClick={handleDownloadTXT} className="btn-download">
                📄 Download TXT
              </button>
            </div>
          </div>

          <div className="skills-section">
            <h4>🎯 Skills Covered</h4>
            <div className="skills-tags">
              {questions.skills.map((skill, index) => (
                <span key={index} className="skill-tag">{skill}</span>
              ))}
            </div>
          </div>

          {questions.custom_requirements && (
            <div className="custom-requirements-display">
              <h4>📝 Custom Requirements Applied</h4>
              <p>{questions.custom_requirements}</p>
            </div>
          )}

          <div className="questions-grid">
            <div className="difficulty-section easy">
              <div className="difficulty-header">
                <h3>🟢 Easy Questions</h3>
                <span className="count">{questions.questions.easy.length} questions</span>
              </div>
              <div className="questions-list">
                {questions.questions.easy.map((question, index) => (
                  <div key={index} className="question-item">
                    <div className="question-number">{index + 1}</div>
                    <div className="question-text">{question}</div>
                    <button 
                      className="copy-btn"
                      onClick={() => copyToClipboard(question)}
                      title="Copy to clipboard"
                    >
                      📋
                    </button>
                  </div>
                ))}
              </div>
            </div>

            <div className="difficulty-section medium">
              <div className="difficulty-header">
                <h3>🟡 Medium Questions</h3>
                <span className="count">{questions.questions.medium.length} questions</span>
              </div>
              <div className="questions-list">
                {questions.questions.medium.map((question, index) => (
                  <div key={index} className="question-item">
                    <div className="question-number">{index + 1}</div>
                    <div className="question-text">{question}</div>
                    <button 
                      className="copy-btn"
                      onClick={() => copyToClipboard(question)}
                      title="Copy to clipboard"
                    >
                      📋
                    </button>
                  </div>
                ))}
              </div>
            </div>

            <div className="difficulty-section hard">
              <div className="difficulty-header">
                <h3>🔴 Hard Questions</h3>
                <span className="count">{questions.questions.hard.length} questions</span>
              </div>
              <div className="questions-list">
                {questions.questions.hard.map((question, index) => (
                  <div key={index} className="question-item">
                    <div className="question-number">{index + 1}</div>
                    <div className="question-text">{question}</div>
                    <button 
                      className="copy-btn"
                      onClick={() => copyToClipboard(question)}
                      title="Copy to clipboard"
                    >
                      📋
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="questions-summary">
            <div className="summary-card">
              <div className="summary-icon">📊</div>
              <div className="summary-content">
                <h4>Total Questions</h4>
                <p className="summary-value">15</p>
              </div>
            </div>
            <div className="summary-card">
              <div className="summary-icon">🎯</div>
              <div className="summary-content">
                <h4>Skills Covered</h4>
                <p className="summary-value">{questions.skills.length}</p>
              </div>
            </div>
            <div className="summary-card">
              <div className="summary-icon">⚡</div>
              <div className="summary-content">
                <h4>Difficulty Levels</h4>
                <p className="summary-value">3</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Agent3Questions;
