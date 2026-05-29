import { useState } from 'react';
import { ChevronDownIcon, ChevronUpIcon } from '@heroicons/react/24/outline';

const Results = ({ results }) => {
  const [showMatches, setShowMatches] = useState(false);
  const [showMissing, setShowMissing] = useState(false);

  if (!results) return null;

  const { similarity_score, match_percentage, key_matches, missing_skills, recommendations } = results;
  
  const getScoreColor = (percentage) => {
    return percentage >= 80 ? 'text-green-600' : 'text-red-600';
  };

  const getScoreBg = (percentage) => {
    return percentage >= 80 ? 'bg-green-100' : 'bg-red-100';
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Similarity Analysis</h2>
        
        <div className={`inline-flex items-center justify-center w-32 h-32 rounded-full ${getScoreBg(match_percentage)} mb-4`}>
          <span className={`text-4xl font-bold ${getScoreColor(match_percentage)}`}>
            {match_percentage}%
          </span>
        </div>
        
        <p className={`text-lg font-semibold ${getScoreColor(match_percentage)}`}>
          {match_percentage >= 80 ? 'Strong Match' : 'Needs Improvement'}
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Key Matches */}
        <div className="space-y-3">
          <button
            onClick={() => setShowMatches(!showMatches)}
            className="flex items-center justify-between w-full p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <span className="font-medium text-gray-900">
              Key Matches ({key_matches?.length || 0})
            </span>
            {showMatches ? (
              <ChevronUpIcon className="h-5 w-5 text-gray-500" />
            ) : (
              <ChevronDownIcon className="h-5 w-5 text-gray-500" />
            )}
          </button>
          
          {showMatches && (
            <div className="space-y-2 pl-4">
              {key_matches?.length > 0 ? (
                key_matches.map((match, index) => (
                  <div key={index} className="p-2 bg-green-50 rounded border-l-4 border-green-400">
                    <p className="text-sm text-gray-700">{match}</p>
                  </div>
                ))
              ) : (
                <p className="text-sm text-gray-500 italic">No key matches found</p>
              )}
            </div>
          )}
        </div>

        {/* Missing Skills */}
        <div className="space-y-3">
          <button
            onClick={() => setShowMissing(!showMissing)}
            className="flex items-center justify-between w-full p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <span className="font-medium text-gray-900">
              Missing Skills ({missing_skills?.length || 0})
            </span>
            {showMissing ? (
              <ChevronUpIcon className="h-5 w-5 text-gray-500" />
            ) : (
              <ChevronDownIcon className="h-5 w-5 text-gray-500" />
            )}
          </button>
          
          {showMissing && (
            <div className="space-y-2 pl-4">
              {missing_skills?.length > 0 ? (
                missing_skills.map((skill, index) => (
                  <div key={index} className="p-2 bg-red-50 rounded border-l-4 border-red-400">
                    <p className="text-sm text-gray-700 capitalize">{skill}</p>
                  </div>
                ))
              ) : (
                <p className="text-sm text-gray-500 italic">No missing skills identified</p>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Recommendations */}
      <div className="bg-blue-50 rounded-lg p-4">
        <h3 className="font-semibold text-blue-900 mb-2">Recommendations</h3>
        <p className="text-blue-800">{recommendations}</p>
      </div>
    </div>
  );
};

export default Results;