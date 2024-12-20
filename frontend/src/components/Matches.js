import React, { useEffect, useState } from 'react';
import axios from '../axiosConfig';
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
        if (isLoading) return;

        if (!isAuthenticated) {
          navigate('/login');
          return;
        }

        if (!user || !user.id) {
          throw new Error('User information not available');
        }

        const response = await axios.get(`/match/${user.id}`);
        setMatches(response.data.matches || []);
      } catch (err) {
        setError(err.response?.data?.error || err.message);
        console.error('Error fetching matches:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchMatches();
  }, [isAuthenticated, user, isLoading, navigate]);

  if (isLoading) return <div>Loading...</div>;
  if (!isAuthenticated) return <div>Please log in to see your matches</div>;
  if (loading) return <div>Loading matches...</div>;
  if (error) return <div>Error: {error}</div>;
  if (matches.length === 0) return <div>No matches found</div>;

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Your Matches</h2>
      <div className="grid gap-4">
        {matches.map((match) => (
          <div key={match.id} className="border p-4 rounded-lg shadow">
            <h3 className="text-lg font-semibold">{match.username}</h3>
            <p className="mt-2">
              <span className="font-medium">Skills offered:</span> {match.skills_offered}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Matches;
