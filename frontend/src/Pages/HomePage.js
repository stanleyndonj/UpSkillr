import React from 'react';
import './HomePage.css'; // Styling for the homepage

const HomePage = () => {
return (
    <div className="homepage-container">
        <h1>Welcome to UpSkillr</h1>
        <p>Your go-to platform for learning and connections.</p>
        <a href="/signup" className="cta-button">Get Started</a>
    </div>
    );
};

export default HomePage;
