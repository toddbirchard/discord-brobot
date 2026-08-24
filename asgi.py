"""Application entry point."""

from config import DISCORD_TOKEN
from discord_brobot import init_bot

bot = init_bot()


def main() -> None:
    """Connect the bot to Discord and block until disconnected."""
    if not DISCORD_TOKEN:
        raise RuntimeError(
            "`DISCORD_TOKEN` is unset. Add it to your `.env` file or environment before starting the bot."
        )
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
