import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

cwd = Path().cwd()

BASE_URL = os.getenv("WEBHOOK_HOST", "https://example.com")
