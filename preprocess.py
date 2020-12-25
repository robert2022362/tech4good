from pydub import AudioSegment
from pydub.playback import play

audio = AudioSegment.from_file("test.m4a", "aac")
play(audio)