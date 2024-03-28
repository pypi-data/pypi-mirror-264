"""CAU."""
import rich.logging

from .timer import timer
from .wrappers import Conan, Coverage, Git, Tidy

rich_handler = rich.logging.RichHandler(enable_link_path=False, show_path=False, show_time=False)

logger = rich.logging.logging.getLogger("CAU")
logger.addHandler(rich_handler)
logger.setLevel(rich.logging.logging.INFO)

__all__ = (
    "Conan",
    "Coverage",
    "Git",
    "Tidy",
    "timer",
)
