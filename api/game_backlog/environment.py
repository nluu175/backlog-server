import environ
import os
from pathlib import Path

env = environ.Env(DEBUG=(bool, False))
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# env vars
STEAM_API_KEY = env("STEAM_API_KEY")
GEMINI_API_KEY = env("GEMINI_API_KEY")
DB_USERNAME = env("DB_USERNAME")
DB_PASSWORD = env("DB_PASSWORD")
