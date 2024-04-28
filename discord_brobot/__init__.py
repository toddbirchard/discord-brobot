"""Initalize Discord chat bot."""

from discord import Intents
from discord.ext.commands import Bot
from discord.ext.commands.help import HelpCommand

from config import DISCORD_TOKEN
from discord_brobot.commands import bot_commands
from discord_brobot.events import bot_events
from log import LOGGER


class DiscordBot(Bot):
    """Discord Bot."""

    async def on_ready(self):
        """Log successful login."""
        LOGGER.success(f"Logged on as {self.user}!")

    async def on_message(self, message):
        """Log chat messages."""
        LOGGER.info(f"Message from {message.author}: {message.content}")


def init_bot():
    """Initialize bot, register all commands & events."""
    intents = Intents.default()
    intents.members = True
    intents.message_content = True
    help = HelpCommand()

    bot = DiscordBot(
        command_prefix="!",
        intents=intents,
        description="Generic Chat Bot",
        help_command=help,
    )
    bot = bot_events(bot)
    bot = bot_commands(bot)

    LOGGER.info(f"Bot initialized: {bot.user.name}")
    bot.run(DISCORD_TOKEN)
