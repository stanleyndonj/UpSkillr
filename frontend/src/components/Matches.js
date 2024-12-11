import React from 'react';

const Matches = () => {
  const matches = [
    { name: 'Mary', skill: 'Marketing' },
    { name: 'Sarah', skill: 'Cooking' },
  ];

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-4">Your Matches</h2>
      <div className="space-y-4">
        {/* Loop through the matches array and display each match */}
        {matches.map((match, index) => (
          <div key={index} className="p-4 bg-gray-100 rounded-md">
            <p><strong>{match.name}</strong></p>
            <p>Skills: {match.skill}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Matches;
