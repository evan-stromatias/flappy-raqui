# Flappy Raqui — dev and packaging tasks.
#
# Standalone builds go through Nuitka, driven by uv so the compile sees the
# project's own dependencies (raylib, esper). Build tools live in the `build`
# dependency group; `uv run --group build` installs them on demand.

PKG    := src/flappy_raqui
ASSETS := $(PKG)/assets
ICON   := $(ASSETS)/images/player.png
OUT    := build
NAME   := flappy-raqui

NUITKA := uv run --group build python -m nuitka

# Flags shared by every platform. The data-dir target must stay
# `flappy_raqui/assets`, because game.py locates assets via
# Path(__file__).parent / "assets".
COMMON := --standalone \
          --python-flag=-m \
          --include-data-dir=./$(ASSETS)=flappy_raqui/assets \
          --output-dir=$(OUT)

# Extra flags appended to the Nuitka command line. CI sets
# `--assume-yes-for-downloads` so the build never stops on the prompt Nuitka
# shows before fetching ccache or the AppImage tooling.
NUITKA_FLAGS ?=

# ---------------------------------------------------------------------------
# Host detection. Nuitka is not a cross-compiler, so `make exe` only ever
# builds for the machine it runs on: the flags below are picked accordingly.
#
# macOS app bundles are standalone-only: Nuitka does not combine
# --macos-create-app-bundle with --onefile.
# ---------------------------------------------------------------------------
ifeq ($(OS),Windows_NT)
	HOST     := windows
	HOSTOPTS := --onefile \
	            --windows-icon-from-ico=$(ICON) \
	            --output-filename=$(NAME).exe
	ARTIFACT := $(OUT)/$(NAME).exe
else
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Linux)
		HOST     := linux
		HOSTOPTS := --onefile \
		            --linux-icon=$(ICON) \
		            --output-filename=$(NAME)
		ARTIFACT := $(OUT)/$(NAME)
	else ifeq ($(UNAME_S),Darwin)
		HOST     := macos
		HOSTOPTS := --macos-create-app-bundle \
		            --macos-app-icon=$(ICON) \
		            --macos-app-name="Flappy Raqui"
		ARTIFACT := $(OUT)/flappy_raqui.app
	else
		HOST := unknown
	endif
endif

.PHONY: help sync run exe clean distclean

help:
	@echo "Detected host: $(HOST)"
	@echo
	@echo "  make sync         Install runtime deps into .venv"
	@echo "  make run          Run the game from source"
	@echo "  make exe          Build a standalone binary for this host ($(HOST))"
	@echo "  make clean        Remove Nuitka intermediates, keep the artifact"
	@echo "  make distclean    Remove $(OUT)/ entirely"

sync:
	uv sync

run:
	uv run $(NAME)

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

exe:
ifeq ($(HOST),unknown)
	$(error Unsupported host '$(UNAME_S)' — build on Linux, macOS or Windows)
endif
	$(NUITKA) $(COMMON) $(HOSTOPTS) $(NUITKA_FLAGS) $(PKG)
	@echo "==> $(ARTIFACT)"

# ---------------------------------------------------------------------------

clean:
	rm -rf $(OUT)/*.build $(OUT)/*.dist $(OUT)/*.onefile-build

distclean:
	rm -rf $(OUT)
