import React, { useEffect, useState } from 'react';
//import axios from '../axiosConfig'; //refused to work a couple of times so i opted for sample sata for now
import { useAuth } from '../AuthContext';
import { useNavigate } from 'react-router-dom';

// Example matches data
const exampleMatches = [
  {
    id: 1,
    username: "Sarah Johnson",
    skills_offered: "JavaScript, React, Node.js",
    match_percentage: 95,
    experience_level: "Senior",
    last_active: "2024-12-19"
  },
  {
    id: 2,
    username: "Michael Chen",
    skills_offered: "Python, Django, AWS",
    match_percentage: 88,
    experience_level: "Mid-Level",
    last_active: "2024-12-20"
  },
  {
    id: 3,
    username: "Emma Rodriguez",
    skills_offered: "UI/UX Design, Figma, Adobe XD",
    match_percentage: 92,
    experience_level: "Senior",
    last_active: "2024-12-18"
  },
  {
    id: 4,
    username: "Alex Kumar",
    skills_offered: "DevOps, Docker, Kubernetes",
    match_percentage: 85,
    experience_level: "Senior",
    last_active: "2024-12-19"
  },
  {
    id: 5,
    username: "Jessica Taylor",
    skills_offered: "Product Management, Agile, Scrum",
    match_percentage: 90,
    experience_level: "Lead",
    last_active: "2024-12-20"
  },
  {
    id: 6,
    username: "David Wilson",
    skills_offered: "Data Science, Machine Learning, TensorFlow",
    match_percentage: 87,
    experience_level: "Mid-Level",
    last_active: "2024-12-17"
  },
  {
    id: 7,
    username: "Maria Garcia",
    skills_offered: "Flutter, Mobile Development, Firebase",
    match_percentage: 83,
    experience_level: "Senior",
    last_active: "2024-12-19"
  },
  {
    id: 8,
    username: "Thomas Anderson",
    skills_offered: "C++, Systems Programming, Linux",
    match_percentage: 89,
    experience_level: "Principal",
    last_active: "2024-12-20"
  },
  {
    id: 9,
    username: "Lisa Wang",
    skills_offered: "Ruby on Rails, PostgreSQL, Redis",
    match_percentage: 86,
    experience_level: "Senior",
    last_active: "2024-12-18"
  },
  {
    id: 10,
    username: "James Mitchell",
    skills_offered: "Cybersecurity, Network Security, Penetration Testing",
    match_percentage: 91,
    experience_level: "Lead",
    last_active: "2024-12-19"
  }
];

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

        // Simulate API call with example data
        // In production, use this instead:
        // const response = await axios.get(`/match/${user.id}`);
        // setMatches(response.data.matches || []);
        
        // Simulated API delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        setMatches(exampleMatches);
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
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {matches.map((match) => (
          <div key={match.id} className="border p-4 rounded-lg shadow hover:shadow-md transition-shadow">
            <div className="flex justify-between items-start">
              <h3 className="text-lg font-semibold">{match.username}</h3>
              <span className="text-green-600 font-medium">{match.match_percentage}% Match</span>
            </div>
            <p className="mt-2 text-gray-600">{match.experience_level}</p>
            <p className="mt-2">
              <span className="font-medium">Skills:</span> {match.skills_offered}
            </p>
            <p className="mt-2 text-sm text-gray-500">
              Last active: {new Date(match.last_active).toLocaleDateString()}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Matches;