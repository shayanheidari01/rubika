import tempfile
import mutagen
import os


class AudioResult:
    def __init__(self, duration=1, performer='') -> None:
        self.duration = duration
        self.performer = performer


class Audio:
    @classmethod
    def get_audio_info(cls, audio: bytes) -> AudioResult:
        with tempfile.NamedTemporaryFile('wb', suffix='.rpa', delete=False, dir='./temps/') as file:
            file.write(audio)
            filename = file.name

        audio = mutagen.File(filename, easy=True)
        performer = ''

        try:
            performer = audio.tags.get('artist')[0]

        except Exception:
            pass

        os.remove(filename)

        return AudioResult(audio.info.length, performer)