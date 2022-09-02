#!/usr/bin/env python

import logging
import os
from telegram import __version__ as TG_VER
import yt_dlp
import re
import time

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

API_Hash =os.environ.get('BOT_TOKEN')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def downloader(links):
    for URL in links:
        with yt_dlp.YoutubeDL({'max_filesize':50*1024*1024}) as ydl:
            error_code = ydl.download(URL)

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Dear {user.mention_html()}, Bot is active and will download videos now onwards.",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("There's No help available here. Call 911.")


async def developer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """About the Bot Developer!"""
    await update.message.reply_text("Bot is developed by @PrabeshAryalNP on Telegram.")


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Deletes the Tiktok/Yt URL."""
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Downloader."""
    string = update.message.text
    pattern = '([^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})'
    URLS = re.findall(pattern, string)
    downloader(URLS)
    time.sleep(2)
    downloaded_files = os.listdir('./')
    for files in downloaded_files:
        size =int((os.path.getsize(files))/(1024*1024))
        if os.path.isdir(files):
            print("Skipping Check for Directory. \n")
        elif size < 50:
            if files.endswith(('avi', 'flv', 'mkv', 'mov', 'mp4', 'webm', '3g2', '3gp', 'f4v', 'mk3d', 'divx', 'mpg', 'ogv', 'm4v', 'wmv')):
                print("Found Short Video")
                await context.bot.send_video(chat_id=update.message.chat_id, video=open(files, 'rb'), supports_streaming=True)
                print("Video {} was Sent Successfully!".format(files))
                os.remove(files)
                try:
                    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
                except BaseException:
                    print("Message was already deleted.")

            elif files.endswith(('aiff', 'alac', 'flac', 'm4a', 'mka', 'mp3', 'ogg', 'opus', 'wav','aac', 'ape', 'asf', 'f4a', 'f4b', 'm4b', 'm4p', 'm4r', 'oga', 'ogx', 'spx', 'vorbis', 'wma')):
                print("Found Short Audio")
                await context.bot.send_audio(chat_id=update.message.chat_id, audio=open(files, 'rb'))
                print("Audio {} was Sent Successfully!".format(files))
                os.remove(files)
                try:
                    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
                except BaseException:
                    print("Message was already deleted. \n \n")    

            elif files.endswith(('py','json','Procfile','txt','text','pip', 'md','git','pycache','cache'))==False:
                os.remove(files)
            time.sleep(1)
        else:
            print(files + "is "+str(size)+" MB."+"\n"+"Which is greater than 50 MB, So removing it !!")
            os.remove(files)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(API_Hash).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("developerinfoPA", developer))

    #For other links
    application.add_handler(MessageHandler(filters.Regex('([^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})') & ~filters.COMMAND, download))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()