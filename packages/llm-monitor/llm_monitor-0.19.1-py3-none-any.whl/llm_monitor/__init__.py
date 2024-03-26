"""LLM Monitor"""

from warnings import warn

from llm_monitor.handlers import MonitorHandler
from llm_monitor.monitor import LLMMonitor
from llm_monitor.utils import __version__

__all__ = ["MonitorHandler", "LLMMonitor", "__version__"]

warn(
    "⚠️  'llm-monitor' is now deprecated. "
    "Please install and use the new package 'galileo-observe' instead. ⚠️",
    DeprecationWarning,
    stacklevel=2,
)
