"""Discord bot Configuration."""

from os import getenv, path

from dotenv import load_dotenv

# Load values from .env
BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

# General config
ENVIRONMENT = getenv("ENVIRONMENT")
PROJECT_NAME = "discord-brobot"

# Discord
DISCORD_TOKEN = getenv("DISCORD_TOKEN")
DISCORD_CHANNEL = getenv("DISCORD_CHANNEL")

# Database
DATABASE_URI = getenv("DATABASE_URI")
