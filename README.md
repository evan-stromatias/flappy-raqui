# Flappy Raqui

![Flappy Raqui](images/flappy-raqui.gif)

A small raylib game I made for my kid, nothing fancy but they had fun with it. It's inspired by [Flappy Bird](https://en.wikipedia.org/wiki/Flappy_Bird).


## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- A C compiler (`gcc`/`clang`) — only for building standalone executables

Runtime dependencies are just `raylib` and `esper`.

## Run

```
uv sync
uv run flappy-raqui
```

## Controls

| Key | Action |
| --- | --- |
| `Space` | Jump to avoid the lava and collect rainbow stars (and select in menus) |
| `Enter` | Throw popcorn to feed the hungry pigeons |
| `Up` / `Down` | Move between menu items |
| `P` | Pause |
| `D` | Toggle debug overlay (collision boxes, FPS, entity count) |
| `Esc` | Quit (press twice to confirm) |


## Layout

```
src/flappy_raqui/
├── game.py            # resource manager setup + entry point
├── ecs/               # components, systems, renderers, spawners (esper)
├── scenes/            # title, countdown, play
├── assets/            # audio, fonts, images
└── pyrayngine/        # vendored engine subset
    ├── engine.py             # main loop, render-texture scaling
    ├── configuration.py
    ├── animation/            # gif + spritesheet animators
    ├── collisions/           # AABB helpers, pixel-derived collision boxes
    ├── gui/                  # frame, box layout, button widget
    ├── resource_managers/    # texture, animated texture, font, audio
    ├── scenes/               # scene base + manager
    └── helpers/
```

Scenes are registered in `game.py`; the flow is `TitleScene → CountdownScene →
PlayScene`. Each scene owns its own `esper` world.

## Development

The dev tools (`ruff` + `pre-commit`) live in the `dev` dependency group, which
`uv sync` installs by default:

```
uv sync              # runtime + dev deps
uv sync --no-dev     # runtime only
```

`ruff` is used for import sorting (isort) and formatting (black), configured in
`pyproject.toml`. Enable the git hook so both run on staged files at commit time:

```
uv run pre-commit install
```

Run them manually — on the whole tree or via the hooks:

```
uv run ruff check --fix .          # sort imports
uv run ruff format .               # format code
uv run pre-commit run --all-files  # both, through pre-commit
```

## Packaging

Standalone builds go through [Nuitka](https://nuitka.net/), driven by `uv` so the
compile sees the project's own dependencies. Build tools live in the `build`
dependency group and are installed on demand, so a plain `uv sync` stays lean.

```
make exe          # build for the current OS
```

Nuitka is not a cross-compiler, so `make exe` always builds for the machine it
runs on, picking the right flags per host:

| Host    | Artifact                 |
| ------- | ------------------------ |
| Linux   | `build/flappy-raqui`     |
| macOS   | `build/flappy_raqui.app` |
| Windows | `build/flappy-raqui.exe` |

`make help` lists every target; `make clean` drops Nuitka's intermediates while
keeping the artifact.
