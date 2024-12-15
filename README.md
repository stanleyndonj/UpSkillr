## UpSkillr

UpSkillr is a skill-sharing platform. It helps connect people having different talents who want to teach and learn. For example, you can learn graphic design by teaching Spanish or share cooking tips in return for marketing strategies. UpSkillr makes it simple to connect, work together, and grow without using money.

---

## What the Project Will Cover

UpSkillr aims at building the most user-friendly skill-swapping platform. Here's what the app does:

**Managing Users:**

People sign up and fill out profiles showing the skills they possess and those they would like to acquire. Profiles include ratings and reviews, which establish trust and credibility.

**Skill Matching:**

Users can search for others by skills they want to learn from or share with them. Smart matching finds the best skill partners.

**Talking and Communication:**

Having real-time chat functionality built in allows users to communicate directly, plan sessions, and discuss details.

**Comments and Reviews:**

After users share their skills, they can write reviews and give ratings for one another, building a reputation system.

**Authentication and Authorization:**

Secure user authentication (signup/login) with protected routes for profile and chat pages.

**Responsive Design:**

A user-friendly design that works well on computers, tablets, and phones.

---

## Features

- Secure authentication for user registration/login.
  
- Create and manage profiles with skill offerings and requests.

- Pair users who have the same skills.

- Instant messaging to arrange swaps.

- Inspect and rate partners after a deal.

## Stretch Features

- Create a "Skills Marketplace" to highlight trending skills.

- Facilitate group skill exchanges (e.g., small classes).

- Apply entertaining features like badges for regular traders.

- Add video call features for online learning sessions.

---

### Technologies Used

*Frontend*

- React for building a responsive and interactive user interface.

- Next.js for server-side rendering and efficient routing.

- Modern, clean and flexible design with Tailwind CSS.

*Backend*

- Flask - a backend tool for API creation.

- SQLAlchemy for object-relational mapping.

- Flask-Migrate for handling database migrations.

---

### Project Structure

*Frontend*
```
css
src/
├── parts/
│   ├── Navbar.js
│   ├── Profile.js
│   ├── Matches.js
│   ├── Chat.js
│   ├── Review.js
├── pages/
│   ├── homepage.js
│   ├── Loginpage.js
│   ├── SignupPage.js
│   ├── profilepage.js
├── app.js
├── index.js
```

*Backend*
```
backend
├── app.py
├── config.py
├── models.py
├── database.py
├── migrations/
├── paths/
│   ├── auth_routes.py
│   ├── user_routes.py
│   ├── match_routes.py
│   ├── review_routes.py
```

## Installation Instructions

*Frontend Setup*

1. Enter the frontend folder:

    `cd frontend`

2. Install dependencies:
   
    `npm install`

3. Start the development server:

   `npm start`

4. Go to http://localhost:3000 to open the application.


*Setup Backend*

1. Move to the backend folder:

   `cd backend`

2. Create a virtual environment:

   `python3 -m venv UpSkillr`

   `source UpSkillr/bin/activate`

3. Install all backend dependencies:

   `pip install -r requirements.txt`

4. Run the application setup by setting up the database:

   `flask db init`  
   
   `flask db migrate`  

   `flask db upgrade` 

5. Start the Flask server:

   `flask run` 

6. Go to the backend API at http://localhost:5000.

---

## Usage

- **Frontend:** Browse the app, find matching skills, and chat with other users.

- **Backend:** RESTful APIs for authentication, user management, and skill matching. --- ## License This project is licensed under the MIT License. See the LICENSE file for details.

---

## Deploying

*1. Set Up Render*

For simple integration, create an account on Render and link your GitHub account.

*2. Create a Web Service*

Then select New > Web Service from the Render dashboard.

Select your GitHub repository and name the service.

*3. Deployment*

Your project will be built automatically by Render. After finishing, you will receive a live URL, such as https://your-service.onrender.com.

*4. Update Changes*

Updates should be pushed to GitHub

---

## License
This project is licensed under the MIT License.




