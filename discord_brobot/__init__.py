"""Initalize Discord chat bot."""

from discord import Intents, Message
from discord.ext.commands import Bot, DefaultHelpCommand

from discord_brobot.commands import bot_commands
from discord_brobot.events import bot_events
from log import LOGGER


class DiscordBot(Bot):
    """Discord Bot."""

    async def on_ready(self) -> None:
        """Log successful login."""
        LOGGER.success(f"Logged on as {self.user} (id: {self.user.id})")

    async def on_message(self, message: Message) -> None:
        """Log chat messages & dispatch registered commands."""
        if message.author == self.user:
            return
        LOGGER.info(f"Message from {message.author}: {message.content}")
        await self.process_commands(message)


def init_bot() -> DiscordBot:
    """Initialize bot, register all commands & events."""
    intents = Intents.default()
    intents.members = True
    intents.message_content = True

    bot = DiscordBot(
        command_prefix="!",
        intents=intents,
        description="Generic Chat Bot",
        help_command=DefaultHelpCommand(),
    )
    bot = bot_events(bot)
    bot = bot_commands(bot)

    LOGGER.info("Bot initialized; connecting to Discord...")
    return bot
