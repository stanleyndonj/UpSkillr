import React, { useEffect, useState } from 'react';
import axios from '../axiosConfig';  // Make sure path is correct
import { useAuth } from '../AuthContext';
import { useNavigate } from 'react-router-dom';

const Matches = () => {
  const [matches, setMatches] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const { isAuthenticated, user, isLoading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchMatches = async () => {
      try {
        // Check if authentication is still loading
        if (isLoading) return;

        // If not authenticated after loading, redirect to login
        if (!isAuthenticated) {
          navigate('/login');
          return;
        }

        // Make sure we have a user with an ID
        if (!user || !user.id) {
          throw new Error('User information not available');
        }

        const response = await axios.get(`/match/${user.id}`);
        
        if (response.data && response.data.matches) {
          setMatches(response.data.matches);
        } else {
          setMatches([]);
        }
        
      } catch (err) {
        setError(err.response?.data?.error || err.message);
        console.error('Error fetching matches:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchMatches();
  }, [isAuthenticated, user, isLoading, navigate]);

  // Show loading state while auth is being checked
  if (isLoading) {
    return <div>Loading...</div>;
  }

  // Show login prompt if not authenticated
  if (!isAuthenticated) {
    return <div>Please log in to see your matches</div>;
  }

  // Show loading state while fetching matches
  if (loading) {
    return <div>Loading matches...</div>;
  }

  // Show error if any
  if (error) {
    return <div>Error: {error}</div>;
  }

  // Show no matches message if array is empty
  if (matches.length === 0) {
    return <div>No matches found</div>;
  }

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Your Matches</h2>
      <div className="grid gap-4">
        {matches.map((match) => (
          <div key={match.id} className="border p-4 rounded-lg shadow">
            <h3 className="text-lg font-semibold">{match.username}</h3>
            <p className="mt-2">
              <span className="font-medium">Skills offered:</span>{' '}
              {match.skills_offered}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Matches;