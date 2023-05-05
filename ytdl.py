from pyrogram import Client, filters
import pytube
import os


app = Client("my_bot")


@app.on_message(filters.regex(r"https?://(www\.)?youtube\.com/watch\?v=.+") & filters.private)

async def download_video(client, message):

    url = message.text.strip()

    yt = pytube.YouTube(url)

    video = yt.streams.get_highest_resolution()

    video_file = await client.download_media(video.url)

    if message.text.endswith("a"):

        # convert video to audio

        audio_file = video_file.replace(".mp4", ".mp3")

        os.system(f"ffmpeg -i {video_file} {audio_file}")

        await client.send_audio(message.chat.id, audio_file)

    else:

        # send video

        await client.send_video(message.chat.id, video_file)

app.run()

