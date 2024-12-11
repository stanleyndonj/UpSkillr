import React from 'react';

const Review = () => {
  return (
    <div className="p-6 max-w-md mx-auto bg-white rounded-xl shadow-md">
      <h2 className="text-xl font-semibold mb-4">Review Your Matches</h2>
      
      {/* Example Review Cards */}
      <div className="space-y-4">
        <div className="flex items-center space-x-2">
          <p><strong>John</strong></p>
          <div className="flex space-x-1">
            <span>⭐⭐⭐⭐</span> {/* 4-star rating */}
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <p><strong>Sarah</strong></p>
          <div className="flex space-x-1">
            <span>⭐⭐⭐⭐⭐</span> {/* 5-star rating */}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Review;
