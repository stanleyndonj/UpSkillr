import os

from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///upskillr.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Add OpenAI configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    if not OPENAI_API_KEY:
        raise ValueError("No OpenAI API key found. Please add it to .env file")