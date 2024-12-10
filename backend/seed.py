import random
from faker import Faker
from models import db, User, Review, Message
from app import create_app

# Initialize the app and database
app = create_app()
fake = Faker()

# Number of records to generate
NUM_USERS = 50
NUM_REVIEWS = 100
NUM_MESSAGES = 200

def seed_users():
    """Seed the User table."""
    users = []
    for _ in range(NUM_USERS):
        skills_offered = ', '.join(fake.words(nb=3))  # Generate 3 random skills
        skills_requested = ', '.join(fake.words(nb=2))  # Generate 2 random skills
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password_hash=fake.password(),
            skills_offered=skills_offered,
            skills_requested=skills_requested,
        )
        users.append(user)
    db.session.bulk_save_objects(users)
    db.session.commit()
    print(f"Seeded {NUM_USERS} users.")

def seed_reviews():
    """Seed the Review table."""
    users = User.query.all()
    reviews = []
    for _ in range(NUM_REVIEWS):
        reviewer = random.choice(users)
        review = Review(
            user_id=reviewer.id,
            rating=random.randint(1, 5),  # Random rating between 1 and 5
            comment=fake.sentence(),
        )
        reviews.append(review)
    db.session.bulk_save_objects(reviews)
    db.session.commit()
    print(f"Seeded {NUM_REVIEWS} reviews.")

def seed_messages():
    """Seed the Message table."""
    users = User.query.all()
    messages = []
    for _ in range(NUM_MESSAGES):
        sender = random.choice(users)
        receiver = random.choice(users)
        while receiver.id == sender.id:  # Ensure sender and receiver are different
            receiver = random.choice(users)
        message = Message(
            sender_id=sender.id,
            receiver_id=receiver.id,
            content=fake.text(max_nb_chars=200),  # Message with up to 200 characters
        )
        messages.append(message)
    db.session.bulk_save_objects(messages)
    db.session.commit()
    print(f"Seeded {NUM_MESSAGES} messages.")

if __name__ == "__main__":
    with app.app_context():
        print("Seeding the database...")
        db.drop_all()  # Clear the database
        db.create_all()  # Create tables
        seed_users()
        seed_reviews()
        seed_messages()
        print("Database seeding completed.")
        print("App context active:", app.app_context().push())
