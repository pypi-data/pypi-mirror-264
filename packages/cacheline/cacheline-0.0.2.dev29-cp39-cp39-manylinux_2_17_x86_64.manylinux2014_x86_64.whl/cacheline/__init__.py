from ._debug import enable_debugger_mode
from .apm import Bot
from .typed import unwrap


def is_in_jupyter_interactive_mode():
    """Check if the current process is running in a Jupyter notebook.

    Returns:
        bool: True if the current process is running in a Jupyter notebook, False otherwise.
    """
    try:
        from IPython import get_ipython

        return get_ipython() is not None
    except Exception:  # pylint: disable=broad-except
        return False

__all__ = ["enable_debugger_mode", "Bot", "unwrap", "is_in_jupyter_interactive_mode" ]
