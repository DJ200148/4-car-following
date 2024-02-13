from dotenv import load_dotenv
import os

load_dotenv()  # Loads the .env file

api_key = os.getenv('GOOGLE_API_KEY')

print(api_key)