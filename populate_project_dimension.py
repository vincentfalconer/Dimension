from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the token
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
