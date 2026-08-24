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

# Uvicorn server options.
#
# `reload` is intentionally absent: reloading restarts the gateway connection on
# every file save, and Discord rate-limits repeated logins.
#
# `workers` is intentionally absent: the ASGI app owns a Discord gateway
# connection, and every extra worker is a *separate* connection that would
# answer each command an extra time. This process must stay single-worker.
if ENVIRONMENT == "production":
    UVICORN_OPTIONS = {
        "uds": path.join(BASE_DIR, "bot.sock"),
        "log_level": "info",
    }
elif ENVIRONMENT == "development" or ENVIRONMENT is None:
    UVICORN_OPTIONS = {
        "host": "127.0.0.1",
        "port": 8000,
        "log_level": "debug",
    }
else:
    raise ValueError(
        f"Unknown environment provided: `{ENVIRONMENT}`. Must be `development` or `production`."
    )
