from pyrogram import Client, filters

import yt_dlp

import os

token = ""

app = Client("bot", "26207265", "5b345259b15b8989f448ca7a2f78bac7", token)

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

