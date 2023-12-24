from ffmpeg.asyncio import FFmpeg
import audiosegment
import asyncio
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


async def ffmpeg_convert(audio, final_audio):
    ffmpeg = (FFmpeg().input(audio).output(final_audio))

    await ffmpeg.execute()
