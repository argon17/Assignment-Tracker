from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
import creds, scrape

bot = Client(
    'asgn_bot',
    bot_token= "<your-bot-token>"
)

def send_msg():
    """
    visit Microsoft Teams, get the assignments and send it to ARGON
    """
    msg = scrape.get_assgnms()

    with bot:
        bot.send_message(creds.ARGON, msg, parse_mode="html")

if __name__=='__main__':
    send_msg()
