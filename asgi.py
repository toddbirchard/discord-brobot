"""Application entry point.

Exposes `app`, an ASGI application served by uvicorn. Uvicorn is an HTTP
server and a Discord bot is an outbound gateway client, so the bot is not
itself an ASGI app; it is started as a background task on uvicorn's event
loop via the ASGI lifespan protocol, and the HTTP surface serves a health
check reporting the gateway connection's state.
"""

import asyncio
import json
from typing import Any, Awaitable, Callable, MutableMapping, Optional

from config import DISCORD_TOKEN, UVICORN_OPTIONS
from discord_brobot import init_bot
from log import LOGGER

Scope = MutableMapping[str, Any]
Message = MutableMapping[str, Any]
Receive = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]

bot = init_bot()

# Seconds to wait for the gateway task to unwind before cancelling it.
SHUTDOWN_TIMEOUT = 10

_bot_task: Optional[asyncio.Task] = None


def _require_token() -> str:
    """Fetch the bot token, failing loudly when it is unset."""
    if not DISCORD_TOKEN:
        raise RuntimeError(
            "`DISCORD_TOKEN` is unset. Add it to your `.env` file or environment before starting the bot."
        )
    return DISCORD_TOKEN


def _log_bot_exit(task: asyncio.Task) -> None:
    """Surface a gateway task that died on its own, rather than failing silently."""
    if task.cancelled():
        return
    error = task.exception()
    if error is not None:
        LOGGER.opt(exception=error).error("Discord gateway task stopped unexpectedly.")


async def _start_bot() -> None:
    """Connect to the Discord gateway as a background task."""
    global _bot_task
    token = _require_token()
    _bot_task = asyncio.create_task(bot.start(token), name="discord-gateway")
    _bot_task.add_done_callback(_log_bot_exit)


async def _stop_bot() -> None:
    """Close the gateway connection and wait for the task to unwind."""
    if not bot.is_closed():
        await bot.close()
    if _bot_task is not None:
        _, pending = await asyncio.wait({_bot_task}, timeout=SHUTDOWN_TIMEOUT)
        if pending:
            LOGGER.warning(
                f"Gateway task still running {SHUTDOWN_TIMEOUT}s after close; cancelling it."
            )
            _bot_task.cancel()
        await asyncio.gather(_bot_task, return_exceptions=True)
    LOGGER.info("Discord gateway connection closed.")


async def _lifespan(receive: Receive, send: Send) -> None:
    """Tie the bot's connection lifetime to the server's."""
    while True:
        message = await receive()
        if message["type"] == "lifespan.startup":
            try:
                await _start_bot()
            except Exception as error:  # noqa: BLE001 - reported to the server
                LOGGER.opt(exception=error).critical("Bot failed to start.")
                await send({"type": "lifespan.startup.failed", "message": str(error)})
                return
            await send({"type": "lifespan.startup.complete"})
        elif message["type"] == "lifespan.shutdown":
            await _stop_bot()
            await send({"type": "lifespan.shutdown.complete"})
            return


async def _http(scope: Scope, send: Send) -> None:
    """Serve a health check describing the gateway connection."""
    if scope["path"].rstrip("/") not in ("", "/health"):
        status, payload = 404, {"detail": "Not Found"}
    elif bot.is_ready():
        status, payload = 200, {
            "status": "ok",
            "bot": str(bot.user),
            "guilds": len(bot.guilds),
            "latency_ms": round(bot.latency * 1000, 2),
        }
    else:
        status, payload = 503, {"status": "connecting", "bot": None}
    body = json.dumps(payload).encode()
    await send(
        {
            "type": "http.response.start",
            "status": status,
            "headers": [
                (b"content-type", b"application/json"),
                (b"content-length", str(len(body)).encode()),
            ],
        }
    )
    await send({"type": "http.response.body", "body": body})


async def app(scope: Scope, receive: Receive, send: Send) -> None:
    """ASGI entry point."""
    if scope["type"] == "lifespan":
        await _lifespan(receive, send)
    elif scope["type"] == "http":
        await _http(scope, send)


def main() -> None:
    """Run the bot under uvicorn."""
    import uvicorn

    _require_token()
    uvicorn.run(app, **UVICORN_OPTIONS)


if __name__ == "__main__":
    main()
