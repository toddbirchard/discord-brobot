"""Room events."""

from discord.ext.commands import Bot

from log import LOGGER


def bot_events(bot: Bot) -> Bot:
    """Register actions to be taken upon room actions."""

    @bot.event
    async def on_error(event, *args, **kwargs) -> None:
        """Log unhandled errors raised by event handlers."""
        LOGGER.exception(
            f"Unhandled error in event `{event}` | args: {', '.join(repr(arg) for arg in args)}"
        )

    return bot
