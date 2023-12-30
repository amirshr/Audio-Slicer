from ffmpeg.asyncio import FFmpeg
import audiosegment
import asyncio
import os
import argparse

dir_path = os.path.dirname(os.path.realpath(__file__))


async def ffmpeg_convert(audio, final_audio):
    ffmpeg = (FFmpeg().input(audio).output(final_audio))
    await ffmpeg.execute()


async def slice_audio(input_path, chunk_size, output_format):
    directory, base_filename = os.path.split(input_path)
    filename, extension = os.path.splitext(base_filename)
    final_audio = os.path.join(directory, f"segment.{output_format}")
    if extension != '.' + output_format:
        try:
            await asyncio.wait_for(ffmpeg_convert(input_path, final_audio), timeout=10)
        except Exception as e:
            print(f"Error processing audio: {e}")
            pass

    segment_duration = chunk_size
    offset = 0
    segment_index = 0
    segment_paths = []
    audio = audiosegment.from_file(final_audio)
    audio_duration = audio.seg.duration_seconds
    while offset < audio_duration:
        segment_duration = min(segment_duration, audio_duration - offset)
        segment_end = min(offset + segment_duration, audio_duration)

        segment = audio[round(offset * 1000):round(segment_end * 1000)]

        segment_file = f"{filename}_segment_{segment_index}.{output_format}"
        segment_path = os.path.join(dir_path, segment_file)

        segment.export(segment_path, format=output_format)
        segment_paths.append(segment_path)
        segment_index += 1
        offset = segment_end


async def main():
    parser = argparse.ArgumentParser(description='Audio Slicer')
    parser.add_argument('-p', '--path', help='Path to audio file', required=True)
    parser.add_argument('-c', '--chunk-size', type=int, help='Chunk size in seconds', required=True)
    parser.add_argument('-f', '--format', help='Output format', required=True)

    args = parser.parse_args()
    await slice_audio(args.path, args.chunk_size, args.format)


if __name__ == "__main__":
    asyncio.run(main())
