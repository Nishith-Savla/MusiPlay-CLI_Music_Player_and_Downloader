import pathlib
import shutil
from time import sleep

import keyboard
import pyglet
import stopit
from youtube_dl import YoutubeDL


def get_partial_audio(url: str, add_suffix=False, timeout=None):
    with stopit.ThreadingTimeout(timeout):
        options = {
            "format": "m4a",
            "outtmpl": f"downloaded/%(title)s-%(id)s{' (1)' if add_suffix else ''}.%(ext)s",
            "nopart": True,
        }

        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
            file_path = ydl.prepare_filename(info)
            ydl.process_info(info)

    return file_path


def play_audio(filepath: str, timestamp=1):
    media: pyglet.media.codecs.Source = pyglet.resource.media(pathlib.Path(filepath).as_posix())

    media.seek(timestamp)
    return media.play()


def toggle_playback(player):
    if player.playing:
        player.pause()
    else:
        player.play()


def handle_resume_swap(player, filepath, timestamp):
    player.pause()
    player = play_audio(filepath, timestamp)
    player.play()


def play_song(url):
    filepath = get_partial_audio(url, False, 10).replace('\\', '/')
    player = play_audio(filepath)

    shutil.copy(filepath, f'downloaded/{pathlib.Path(filepath).stem} (1){pathlib.Path(filepath).suffix}')
    sleep(1)
    filepath = get_partial_audio(url, add_suffix=True, timeout=30).replace('\\', '/')

    keyboard.add_hotkey('ctrl+space', lambda: toggle_playback(player))
    keyboard.add_hotkey('r', lambda: handle_resume_swap(player, filepath, player.time))


def main():
    # url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    url = input("Enter the url to download the audio: ")
    play_song(url)

    keyboard.wait()


if __name__ == '__main__':
    main()
