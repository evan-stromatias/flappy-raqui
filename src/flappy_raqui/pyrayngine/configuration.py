from dataclasses import dataclass


@dataclass
class EngineConfig:
    window_width: int = 300
    window_height: int = 300
    full_screen: bool = False
    virtual_window_width: int | None = None
    virtual_window_height: int | None = None
    target_fps: int | None = None
    window_title: str = "PyRayNgine"
    debug: bool = False
    hide_mouse: bool = False
