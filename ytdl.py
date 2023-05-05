from pyrogram import Client, filters
import pytube
import os


api_id = '26207265'
app_hash = "5b345259b15b8989f448ca7a2f78bac7"
token = ""
app = Client("bot", api_id, api_hash, token)


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

from pyrogram import Client, filters

import yt_dlp

import os

app = Client("my_bot")

@app.on_message(filters.regex(r"https?://(www\.)?youtube\.com/watch\?v=.+") & filters.private)

async def download_video(client, message):

    url = message.text.strip()

    ytdl = yt_dlp.YoutubeDL({})

    info = ytdl.extract_info(url, download=False)

    if message.text.endswith("a"):

        # download audio

        options = {

            "format": "bestaudio/best",

            "outtmpl": "%(title)s.%(ext)s",

            "postprocessors": [{

                "key": "FFmpegExtractAudio",

                "preferredcodec": "mp3",

                "preferredquality": "192"

            }]

        }

        filename = ytdl.prepare_filename(info)

        ytdl.process_info(info, options=options)

        audio_file = filename.replace(".webm", ".mp3")

        os.rename(filename, audio_file)

        await client.send_audio(message.chat.id, audio_file)

    else:

        # download video

        options = {

            "format": "bestvideo+bestaudio/best",

            "outtmpl": "%(title)s.%(ext)s",

        }

        filename = ytdl.prepare_filename(info)

        ytdl.process_info(info, options=options)

        await client.send_video(message.chat.id, filename)

app.run()
