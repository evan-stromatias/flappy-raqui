from pathlib import Path

from flappy_raqui.pyrayngine.configuration import EngineConfig
from flappy_raqui.pyrayngine.engine import PyRayNgine
from flappy_raqui.pyrayngine.resource_managers.audio_manager import AudioManager
from flappy_raqui.pyrayngine.resource_managers.font_manager import FontManager
from flappy_raqui.pyrayngine.resource_managers.texture_manager import (
    AnimatedTextureManager,
    TextureManager,
)
from flappy_raqui.pyrayngine.scenes.scene_manager import SceneManager
from flappy_raqui.scenes.countdown_scene import CountdownScene
from flappy_raqui.scenes.play_scene import PlayScene
from flappy_raqui.scenes.title_scene import TitleScene

P = Path(__file__).parent

TITLE = "Flappy Raqui"
WIDTH = 1280
HEIGHT = 570
FULL_SCREEN = True
HIDE_MOUSE = False
DEBUG = False


def create_font_manager() -> FontManager:
    font_manager = FontManager()
    font_manager.add_font("huge", P / Path("./assets/fonts/flappy.ttf"))
    font_manager.add_font("font", P / Path("./assets/fonts/font.ttf"))
    return font_manager


def create_audio_manager() -> AudioManager:
    audio_manager = AudioManager()
    audio_manager.add_audio("are_you_sure", P / Path("./assets/audio/are_you_sure.mp3"))
    audio_manager.add_audio(
        "i_didnt_think_so", P / Path("./assets/audio/i_didnt_think_so.mp3")
    )
    audio_manager.add_audio("jump", P / Path("./assets/audio/jump.wav"))
    audio_manager.add_audio("score", P / Path("./assets/audio/score.wav"))
    audio_manager.add_audio(
        "bist_du_mein_freund", P / Path("./assets/audio/bist_du_mein_freund.mp3")
    )
    audio_manager.add_audio("bird1", P / Path("./assets/audio/bird1.mp3"))
    audio_manager.add_audio("bird2", P / Path("./assets/audio/bird2.mp3"))
    audio_manager.add_audio("bird3", P / Path("./assets/audio/bird3.mp3"))
    audio_manager.add_audio("feed_bird1", P / Path("./assets/audio/feed_bird1.mp3"))
    audio_manager.add_audio("feed_bird2", P / Path("./assets/audio/feed_bird2.mp3"))
    audio_manager.add_audio("raq", P / Path("./assets/audio/schwarz.mp3"))
    audio_manager.add_audio("hurt", P / Path("./assets/audio/hurt.wav"))
    audio_manager.add_audio("explosion", P / Path("./assets/audio/explosion.wav"))
    audio_manager.add_audio("intro_voice", P / Path("./assets/audio/intro_voice.mp3"))
    return audio_manager


def create_texture_manager() -> TextureManager:
    texture_manager = TextureManager()

    texture_manager.add_texture("popcorn1", P / Path("assets/images/popcorn1.png"))
    texture_manager.add_texture("title", P / Path("./assets/images/intro_text.png"))

    texture_manager.add_texture("cloud1", P / Path("./assets/images/cloud1.png"))
    texture_manager.add_texture("cloud2", P / Path("./assets/images/cloud2.png"))
    texture_manager.add_texture("cloud3", P / Path("./assets/images/cloud3.png"))
    texture_manager.add_texture("cloud4", P / Path("./assets/images/cloud4.png"))
    texture_manager.add_texture("background", P / Path("./assets/images/city.png"))
    texture_manager.add_texture("ground", P / Path("./assets/images/ground.png"))
    texture_manager.add_texture("player", P / Path("./assets/images/player.png"))
    texture_manager.add_texture("birdy", P / Path("./assets/images/birdy.png"))

    return texture_manager


def create_animated_texture_manager() -> AnimatedTextureManager:
    a_texture_manager = AnimatedTextureManager()
    a_texture_manager.add_texture(
        "star", P / Path("./assets/images/Magical rainbow star.gif")
    )
    a_texture_manager.add_texture(
        "star-big", P / Path("./assets/images/Magical rainbow star 128px.gif")
    )
    a_texture_manager.add_texture("lava", P / Path("./assets/images/lava.gif"))
    a_texture_manager.add_texture("smoke", P / Path("./assets/images/smoke2.gif"))
    return a_texture_manager


def create_scene_manager() -> SceneManager:
    scene_manager = SceneManager()
    scene_manager.add_scene("TitleScene", TitleScene(width=WIDTH, height=HEIGHT))
    scene_manager.add_scene(
        "CountdownScene", CountdownScene(width=WIDTH, height=HEIGHT)
    )
    scene_manager.add_scene("PlayScene", PlayScene(width=WIDTH, height=HEIGHT))
    scene_manager.set_current_scene("TitleScene")
    scene_manager.load_current_scene()
    return scene_manager


def main():
    config = EngineConfig(
        window_title=TITLE,
        window_width=WIDTH,
        window_height=HEIGHT,
        full_screen=FULL_SCREEN,
        hide_mouse=HIDE_MOUSE,
        debug=DEBUG,
    )

    engine = PyRayNgine(config=config)

    engine.textures_manager = create_texture_manager()
    engine.animimated_textures_manager = create_animated_texture_manager()
    engine.font_manager = create_font_manager()
    engine.audio_manager = create_audio_manager()

    engine.run(scene_manager=create_scene_manager())


if __name__ == "__main__":
    main()
