"""Register bot commands."""

from datetime import datetime, timedelta

import pytz
from discord.ext.commands import Bot

from log import LOGGER


def bot_commands(bot: Bot) -> Bot:
    """Register user-triggered commands to chatbot."""

    @bot.command(name="420", help="Get time remaining until that time of day.")
    async def time_remaining(ctx) -> None:
        """Get remaining time until target time."""
        now = datetime.now(tz=pytz.timezone("America/New_York"))
        am_time = now.replace(hour=4, minute=20, second=0, microsecond=0)
        pm_time = now.replace(hour=16, minute=20, second=0, microsecond=0)
        if now < am_time:
            target = am_time
        elif now < pm_time:
            target = pm_time
        else:
            target = am_time + timedelta(days=1)
        remaining = target - now
        hours, seconds = divmod(int(remaining.total_seconds()), 3600)
        minutes, seconds = divmod(seconds, 60)
        LOGGER.info(f"`420` requested by {ctx.author}; {remaining} remaining.")
        await ctx.send(
            f"{hours} hours, {minutes} minutes, & {seconds} seconds until 4:20"
        )

    return bot
