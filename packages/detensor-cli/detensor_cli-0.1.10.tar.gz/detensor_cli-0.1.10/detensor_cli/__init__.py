import sys

from cashews import Cache

from .i18n import _ as _

if sys.version_info < (3, 10):
    from importlib_metadata import EntryPoint, version, entry_points
else:
    from importlib.metadata import EntryPoint, version, entry_points

try:
    __version__ = version("detensor-cli")
except Exception:
    __version__ = None

cache = Cache("mpcc")
cache.setup("mem://")

from .cli import run_sync
from .cli import cli as cli_sync
from .consts import PLUGINS_GROUP
from .handlers import install_signal_handler


async def cli_main(*args, **kwargs):
    install_signal_handler()
    return await run_sync(cli_sync)(*args, **kwargs)
