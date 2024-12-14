import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import styles from './Navbar.module.css';

const Navbar = () => {
  const { isAuthenticated, logout } = useAuth();

  return (
    <nav className={styles.navbar}>
      <h1 className={styles.logo}>UpSkillr</h1>
      <div className={styles.navLinks}>
        <Link to="/">Home</Link>
        {!isAuthenticated ? (
          <>
            <Link to="/login">Login</Link>
            <Link to="/signup">Sign Up</Link>
          </>
        ) : (
          <>
            <Link to="/profile">Profile</Link>
            <Link to="/matches">Matches</Link>
            <Link to="/chat">Chats</Link>
            <Link to="/reviews">Reviews</Link>
            <button onClick={logout}>Logout</button>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
