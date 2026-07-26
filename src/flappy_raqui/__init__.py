"""Flappy Raqui — a game built on a trimmed, vendored copy of PyRayNgine."""

from flappy_raqui.__version__ import __version__

__all__ = ["__version__", "main"]


def main() -> None:
    # Imported lazily so that `import flappy_raqui` does not pull in raylib
    # (and open an audio/video device) as a side effect.
    from flappy_raqui.game import main as _main

    _main()
