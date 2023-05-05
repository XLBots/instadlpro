from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto, InputMediaVideo
import instaloader

app = Client('your_bot_token')


@app.on_message(filters.private)
def handle_message(client, message):
    url = message.text
    
if url.startswith('https://www.instagram.com/'):
        # Extract the username from the Instagram URL
        username = url.split('/')[3]
        
        # Create an Instaloader instance
        L = instaloader.Instaloader()
        
        # Download the most recent post from the user's profile
        post = None
        for p in instaloader.Profile.from_username(L.context, username).get_posts():
            post = p
            break
        
        # Download the photo or video file
        if post.is_video:
            filename = L.download_video(post, f'{username}_post')
            media = InputMediaVideo(filename)
        else:
            filename = L.download_pic(post, f'{username}_post')
            media = InputMediaPhoto(filename)
        
        # Send the file to the user
        message.reply_media(media=media)
        
        # Delete the file from the local directory
        os.remove(filename)
    else:
        # Send a message to the user asking for an Instagram URL
        message.reply_text('Please enter a valid Instagram URL.')

app.run()
