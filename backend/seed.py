import random
from faker import Faker
from models import db, User, Review, Message, Skill, SkillRequest
from app import create_app
from sqlalchemy.exc import IntegrityError

# Initialize Faker
fake = Faker()

# Number of records to generate
NUM_USERS = 50
NUM_REVIEWS = 100
NUM_MESSAGES = 200
COMMON_SKILLS = ["Python", "React", "Flask", "JavaScript", "Node.js", "Data Analysis", "UI/UX Design"]

def seed_users():
    users = []
    for _ in range(NUM_USERS):
        user = User(
            username=fake.unique.user_name(),
            email=fake.unique.email(),
        )
        user.set_password(fake.password())
        
        db.session.add(user)
        try:
            db.session.flush()  # Ensure user has an ID
        except IntegrityError:
            db.session.rollback()
            continue
        
        users.append(user)

    db.session.commit()
    print(f"Seeded {len(users)} users.")
    return users

def seed_skills(users):
    skills = []
    for user in users:
        # Assign common skills to ensure overlap
        offered_skills = random.sample(COMMON_SKILLS, random.randint(1, 5))
        for skill_name in offered_skills:
            skill = Skill(
                name=skill_name,
                user_id=user.id
            )
            skills.append(skill)
    
    db.session.add_all(skills)
    db.session.commit()
    print(f"Seeded {len(skills)} skills.")
    return skills

def seed_skill_requests(users, skills):
    skill_requests = []
    for user in users:
        user_skills = [skill for skill in skills if skill.user_id != user.id]  # Avoid self-referencing skills
        
        # Create 1-3 skill requests per user
        for _ in range(random.randint(1, 3)):
            if user_skills:
                skill = random.choice(user_skills)  # Pick a skill from another user
                skill_request = SkillRequest(
                    user_id=user.id,
                    skill_id=skill.id,  # Assign a valid skill ID
                    description=fake.sentence()
                )
                skill_requests.append(skill_request)
    
    db.session.add_all(skill_requests)
    db.session.commit()
    print(f"Seeded {len(skill_requests)} skill requests.")

def seed_reviews(users):
    reviews = []
    for _ in range(NUM_REVIEWS):
        reviewer = random.choice(users)
        reviewed = random.choice(users)
        
        while reviewer.id == reviewed.id:
            reviewed = random.choice(users)
        
        review = Review(
            user_id=reviewed.id,
            rating=random.randint(1, 5),
            comment=fake.sentence(),
        )
        reviews.append(review)
    
    db.session.bulk_save_objects(reviews)
    db.session.commit()
    print(f"Seeded {NUM_REVIEWS} reviews.")

def seed_messages(users):
    messages = []
    for _ in range(NUM_MESSAGES):
        sender = random.choice(users)
        receiver = random.choice(users)
        
        while receiver.id == sender.id:
            receiver = random.choice(users)
        
        message = Message(
            sender_id=sender.id,
            receiver_id=receiver.id,
            content=fake.text(max_nb_chars=200),
        )
        messages.append(message)
    
    db.session.bulk_save_objects(messages)
    db.session.commit()
    print(f"Seeded {NUM_MESSAGES} messages.")

def main():
    app = create_app()
    with app.app_context():
        print("Seeding the database...")
        db.drop_all()  # Clear the database
        db.create_all()  # Create tables
        
        # Seed in a logical order
        users = seed_users()
        skills = seed_skills(users)  # Generate skills for the users
        seed_skill_requests(users, skills)  # Pass both users and skills here
        seed_reviews(users)
        seed_messages(users)
        
        print("Database seeding completed.")


if __name__ == "__main__":
    main()
