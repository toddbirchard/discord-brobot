"""Register bot commands."""

from datetime import datetime

import pytz
from discord.ext.commands import Bot

from log import LOGGER


def bot_commands(bot) -> Bot:
    """Register user-triggered commands to chatbot."""

    @bot.command(name="420", help="Get time remaining until that time of day.")
    async def time_remaining(ctx):
        """Get remaining time until target time."""
        LOGGER.info("Test")
        now = datetime.now(tz=pytz.timezone("America/New_York"))
        am_time = now.replace(hour=4, minute=20, second=0)
        pm_time = now.replace(hour=16, minute=20, second=0)
        if am_time > now:
            remaining = f"{am_time - now}"
        elif am_time < now < pm_time:
            remaining = f"{pm_time - now}"
        else:
            tomorrow_am_time = now.replace(day=now.day + 1, hour=4, minute=20, second=0)
            remaining = f"{tomorrow_am_time - now}"
        remaining = remaining.split(":")
        await ctx.send(
            f"{remaining[0]} hours, {remaining[1]} minutes, & {remaining[2]} seconds until 4:20"
        )

    return bot
