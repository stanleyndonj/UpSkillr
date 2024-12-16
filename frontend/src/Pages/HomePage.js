import React from 'react';
import './HomePage.css'; // Styling for the homepage
import logo from '/home/esther/UpSkillr/frontend/src/Pages/assets/UpSkillr Logo.png'; // Import the logo
import communityImage from '/home/esther/UpSkillr/frontend/src/Pages/assets/pexels-rdne-7551442.jpg'; // Add a community section image
import communityImage1 from '/home/esther/UpSkillr/frontend/src/Pages/assets/desola-lanre-ologun-IgUR1iX0mqM-unsplash.jpg'; // Add a community section image
import commmunityImage2 from '/home/esther/UpSkillr/frontend/src/Pages/assets/collaboration2.jpg';
import communityImage3 from '/home/esther/UpSkillr/frontend/src/Pages/assets/collaboration3.jpg';
import uniqueIcon1 from '/home/esther/UpSkillr/frontend/src/Pages/assets/profile.gif'; // Add icons for each unique feature
import uniqueIcon2 from '/home/esther/UpSkillr/frontend/src/Pages/assets/skills matching.png';
import uniqueIcon3 from '/home/esther/UpSkillr/frontend/src/Pages/assets/chat.gif';
import uniqueIcon4 from '/home/esther/UpSkillr/frontend/src/Pages/assets/trophy.gif';

const HomePage = () => {
    return (
        <div className="homepage-container">
            {/* Logo */}
            <header className="hero-section">
                <div className="logo-container">
                    <img src={logo} alt="UpSkillr Logo" className="logo" />
                </div>

                <h1>Learn, Teach, Thrive Together!</h1>
                <h2>Your go-to platform for skill sharing and collaboration.</h2>
                <a href="/signup" className="cta-button">Get Started</a>
            </header>

            {/* Unique Features */}
            <section className="unique-section">
                <h2>What Makes Us Unique</h2>
                <div className="unique-features">
                    <div className="feature">
                        <img src={uniqueIcon1} alt="User Profiles" className="feature-icon" />
                        <h3>User Profiles </h3>
                        <p>Showcase skills and learning goals.</p>
                    </div>
                    <div className="feature">
                        <img src={uniqueIcon2} alt="Skill Matching" className="feature-icon" />
                        <h3>Skill Matching</h3>
                        <p>Connects users with complementary needs.</p>
                    </div>
                    <div className="feature">
                        <img src={uniqueIcon3} alt="Chat & Collaboration" className="feature-icon" />
                        <h3>Chat & Collaboration</h3>
                        <p>Facilitates real-time interaction.</p>
                    </div>
                    <div className="feature">
                        <img src={uniqueIcon4} alt="Skill Badges" className="feature-icon" />
                        <h3>Skill Badges</h3>
                        <p>Recognize contributions and achievements.</p>
                    </div>
                </div>
            </section>

            {/* Community Section */}
            <section className="community-section">
                <h2>Our Community</h2>
                <div className="image-container">
                <div>
                    <img src={communityImage} alt="Community" className="community-image" />
                </div>
                <div>
                    <img src={communityImage1} alt="Community 1" className="community-image" />
                </div>
                <div>
                   <img src={commmunityImage2} alt="Community 1" className="community-image" />
                </div>
                <div>
                   <img src={communityImage3} alt="Community 1" className="community-image" />
                </div>
                </div>
            </section>

            {/* Testimonials */}
            <section className="testimonials">
            <h2>Testimonials</h2>
                <div className="testimonial-container">
                    <blockquote>
                        "UpSkillr has completely changed how I learn and share skills! 🎉" - Jane D.
                    </blockquote>
                    <blockquote>
                        "Connecting with like-minded people has been a game-changer. 🚀" - John S.
                    </blockquote>
                    <blockquote>
                        "UpSkillr has opened doors to new opportunities by allowing me to connect with people who share my interests and goals. The skill-sharing feature is fantastic! 🌟" - Sarah W.
                    </blockquote>
                    <blockquote>
                        "I love how easy it is to find people with the skills I need and vice versa. The community is supportive, and the platform is intuitive! 💡" - Michael T.
                    </blockquote>
                    <blockquote>
                       "UpSkillr helped me find a mentor for the exact skills I wanted to learn. It's a great way to grow personally and professionally. 🚀" - Emily F.
                    </blockquote>
                    <blockquote>
                        "I've met so many amazing people on UpSkillr. It's like having a personal learning network at your fingertips. Can't recommend it enough! 🌍" - David M.
                    </blockquote>
                </div>
                </section>

            {/* Contacts Section */}
            <section className="contacts-section">
                <h2>Contact Us</h2>
                <p>We’d love to hear from you! Reach out through any of the following channels:</p>
                <ul className="contacts-list">
                    <li>Email: <a href="mailto:support@upskillr.com">support@upskillr.com</a></li>
                    <li>Phone: <a href="tel:+1234567890">+254 705567-890</a></li>
                    <li>Follow us on:
                        <a href="https://www.facebook.com/UpSkillr" target="_blank" rel="noopener noreferrer"> Facebook</a>,
                        <a href="https://www.twitter.com/UpSkillr" target="_blank" rel="noopener noreferrer"> Twitter</a>,
                        <a href="https://www.linkedin.com/company/UpSkillr" target="_blank" rel="noopener noreferrer"> LinkedIn</a>
                    </li>
                    <li>Visit our Help Center: <a href="/help">Help Center</a></li>
                </ul>
            </section>
        </div>
    );
};

export default HomePage;
