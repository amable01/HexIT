# src/utils/env.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Export environment variables
user = os.getenv('SERVICENOW_USER')
pwd = os.getenv('SERVICENOW_PWD')
endpoint = "https://hexawaretechnologiesincdemo8.service-now.com"
db_path = os.getenv('DATABASE_PATH')