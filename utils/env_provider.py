import os

from dotenv import load_dotenv

load_dotenv()


CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")

CLOUDFLARE_BASE_URL = os.getenv("CLOUDFLARE_BASE_URL")

DATABASE_URL = os.getenv("DATABASE_URL")

SECRET_KEY = os.getenv("SECRET_KEY")
