import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Watson Discovery Configurations
WD_API_KEY = os.getenv("WD_API_KEY")
WD_BASE_URL = os.getenv("WD_BASE_URL")
WD_PROJECT_ID = os.getenv("WD_PROJECT_ID")

# watsonx Configurations
WX_API_KEY = os.getenv("WX_API_KEY")
WX_BASE_URL = os.getenv("WX_BASE_URL")
WX_PROJECT_ID = os.getenv("WX_PROJECT_ID")
