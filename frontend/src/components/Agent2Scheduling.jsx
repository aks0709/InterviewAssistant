import { useState } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001';

function Agent2Scheduling() {
  const [candidateId, setCandidateId] = useState(() => {
    const agent1Results = sessionStorage.getItem('agent1_results');
    if (agent1Results) {
      const data = JSON.parse(agent1Results);
      return data.candidate_id ? String(data.candidate_id) : '';
    }
    return '';
  });
  const [loading, setLoading] = useState(false);
  const [scheduledInterview, setScheduledInterview] = useState(() => {
    const saved = sessionStorage.getItem('agent2_scheduled');
    return saved ? JSON.parse(saved) : null;
  });
  const [error, setError] = useState(null);

  const handleSchedule = async () => {
    if (!candidateId) {
      setError('Please enter a candidate ID');
      return;
    }

    setLoading(true);
    setError(null);
    setScheduledInterview(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/agent2/schedule`, {
        candidate_id: parseInt(candidateId)
      });

      setScheduledInterview(response.data);
      sessionStorage.setItem('agent2_scheduled', JSON.stringify(response.data));
    } catch (err) {
      console.error('Error:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to schedule interview');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setCandidateId('');
    setScheduledInterview(null);
    setError(null);
    sessionStorage.removeItem('agent2_scheduled');
  };

  const formatDateTime = (isoString) => {
    const date = new Date(isoString);
    return {
      date: date.toLocaleDateString('en-US', { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      }),
      time: date.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: true 
      })
    };
  };

  return (
    <div className="container">
      <div className="header">
        <h1 className="title">Interview Scheduling</h1>
        <p className="subtitle">Schedule interviews for shortlisted candidates</p>
      </div>

      {!scheduledInterview ? (
        <div className="upload-section">
          <div className="input-group">
            <label className="file-label">Candidate ID</label>
            <input
              type="number"
              value={candidateId}
              onChange={(e) => setCandidateId(e.target.value)}
              placeholder="Enter candidate ID (e.g., 1)"
              className="input-field"
              disabled={loading}
            />
            <p className="input-hint">Enter the ID of a shortlisted candidate (auto-scheduled with available panel)</p>
          </div>

          <div className="buttons">
            <button
              onClick={handleSchedule}
              disabled={!candidateId || loading}
              className="btn btn-primary"
            >
              {loading ? (
                <div className="loading">
                  <div className="spinner"></div>
                  <span>Scheduling...</span>
                </div>
              ) : (
                'Schedule Interview'
              )}
            </button>
          </div>
        </div>
      ) : (
        <div className="results">
          <div className="success-icon">✓</div>
          <h2 className="success-title">Interview Scheduled Successfully!</h2>
          
          <div className="schedule-card">
            <div className="schedule-section">
              <div className="schedule-label">Candidate</div>
              <div className="schedule-value">{scheduledInterview.candidate_name}</div>
            </div>

            <div className="schedule-divider"></div>

            <div className="schedule-section">
              <div className="schedule-label">Interview Panel</div>
              <div className="schedule-value panel-name">{scheduledInterview.panel_name}</div>
            </div>

            <div className="schedule-divider"></div>

            <div className="schedule-section">
              <div className="schedule-label">Date</div>
              <div className="schedule-value">
                {formatDateTime(scheduledInterview.scheduled_time).date}
              </div>
            </div>

            <div className="schedule-divider"></div>

            <div className="schedule-section">
              <div className="schedule-label">Time</div>
              <div className="schedule-value time-value">
                {formatDateTime(scheduledInterview.scheduled_time).time}
              </div>
            </div>

            <div className="schedule-divider"></div>

            <div className="schedule-section">
              <div className="schedule-label">Duration</div>
              <div className="schedule-value">{scheduledInterview.duration_minutes} minutes</div>
            </div>

            {scheduledInterview.meeting_link && (
              <>
                <div className="schedule-divider"></div>
                <div className="schedule-section">
                  <div className="schedule-label">Meeting Link</div>
                  <a 
                    href={scheduledInterview.meeting_link} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="meeting-link"
                  >
                    Join Meeting →
                  </a>
                </div>
              </>
            )}
          </div>

          <div className="message-box">
            <p className="message-text">{scheduledInterview.message}</p>
          </div>

          <button onClick={resetForm} className="btn btn-secondary">
            Schedule Another Interview
          </button>
        </div>
      )}

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
    </div>
  );
}

export default Agent2Scheduling;