import { useState } from 'react';
import Agent1Similarity from './components/Agent1Similarity';
import Agent2Scheduling from './components/Agent2Scheduling';
import Agent3Questions from './components/Agent3Questions';

function App() {
  const [activeAgent, setActiveAgent] = useState('agent1');

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="nav-bar">
        <div className="nav-container">
          <h1 className="nav-title">Interview Assistant</h1>
          <div className="nav-tabs">
            <button
              onClick={() => setActiveAgent('agent1')}
              className={`nav-tab ${activeAgent === 'agent1' ? 'active' : ''}`}
            >
              Agent 1: Similarity Analysis
            </button>
            <button
              onClick={() => setActiveAgent('agent2')}
              className={`nav-tab ${activeAgent === 'agent2' ? 'active' : ''}`}
            >
              Agent 2: Interview Scheduling
            </button>
            <button
              onClick={() => setActiveAgent('agent3')}
              className={`nav-tab ${activeAgent === 'agent3' ? 'active' : ''}`}
            >
              Agent 3: Question Generator
            </button>
          </div>
        </div>
      </nav>

      {/* Content */}
      <div className="content">
        {activeAgent === 'agent1' && <Agent1Similarity />}
        {activeAgent === 'agent2' && <Agent2Scheduling />}
        {activeAgent === 'agent3' && <Agent3Questions />}
      </div>
    </div>
  );
}

export default App;