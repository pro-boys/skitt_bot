import telegram
import importlib
from skitt_bot.modules import ALL_MODULES
from skitt_bot import dispatcher, logger, updater, TOKEN, WEBHOOK, LISTEN, CERT_PATH, PORT, URL, logger
from telegram import Update, Bot, ParseMode
from telegram.ext import CommandHandler, run_async

IMPORTED = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("skitt_bot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if not imported_module.__mod_name__.lower() in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

START_TEXT = """
കടന്നു വരണം മിഷ്ട്ടർ... ഞാനാണ് {}, ഒരു കാര്യവും ഇല്ലാത്ത കുറച്ച് features ആണ് എനിക്കുള്ളത്..!
അത് എന്തൊക്കെ ആണെന്ന് അറിയാൻ /help കൊടുത്താൽ മതിയാകും....
ഇനി ഞാൻ പ്രവർത്തിക്കുന്നത് എങ്ങനെ ആണെന്ന് അറിയണമെങ്കിൽ [ഇവിടെ ഞെക്കുക](https://github.com/skittles9823/skitt_bot)
""".format(dispatcher.bot.first_name)

HELP_TEXT = """
ഞാൻ എന്തൊക്കെ ചെയ്യുമെന്ന് അറിയാൻ വന്നതായിരിക്കും അല്ലെ....
എന്നാൽ കേട്ടോളു ഇതൊക്കെ ആണ് എനിക്ക് ചെയ്യാൻ പറ്റുന്നത്....

*കമാന്റുകൾ*
 _<reply> = reply to a message_
 _<args> = adding a message after the command_
 - `/🅱`: - _<reply>_ 
    *- replying to a message with replace a random character with the B emoji.*
 - `/👏`: - _<reply>_ 
    *- adds clap emojis at the begining, end, and in every space in a message.*
 - `/😂`: - _<reply>_ 
    *- a replica of mattatas copypasta command.*
 - `/deepfry`: - _<reply>_ 
    *- for when your images/stickers need to get a little fried.*
 - `/dllm`: - _<optional args>_ 
    *- sends a random chinese meme. if you add a number after the command, itll reply with a specific photo.*
 - `/forbes`: - _<reply>_ 
    *- turns a message into a Forbes headline.*
 - `me too`:
    *- Saying "me too" will have a small chance for the bot to make a remark.*
 - `/mock`: - _<reply>_ 
    *- mocks a replied message lick the spongebob meme.*
 - `/owo`: - _<reply>_ 
    *- OwO whats this? OwOfies a message.*
 - `/stretch`: - _<reply>_ 
    *- stretches vowels in a message a random number of times.*
 - `/thonkify`: - _<reply>/<args>_ 
    *- turns text into thonk text (only supports letters and none symbols for now).*
 - `/vapor`: - _<reply>/<args>_ 
    *- turns a message into vaporwave text.*
 - `/zalgofy`: - _<reply>_ 
    *- corrupts a message.*
"""

@run_async
def start(bot: Bot, update: Update):
    if update.effective_chat.type == "private":
        update.effective_message.reply_text(START_TEXT, parse_mode=ParseMode.MARKDOWN)
    else:
        update.effective_message.reply_text("Waow sur, you've UwU-ken me :3")

@run_async
def help(bot: Bot, update: Update):
    if update.effective_chat.type == "private":
        update.effective_message.reply_text(HELP_TEXT, parse_mode=ParseMode.MARKDOWN)
    else:
        update.effective_message.reply_text("Try this command again in a private message.")

def main():
    START_HANDLER = CommandHandler("start", start)
    HELP_HANDLER = CommandHandler("help", help)

    dispatcher.add_handler(START_HANDLER)
    dispatcher.add_handler(HELP_HANDLER)

    if WEBHOOK:
        logger.info("Using webhooks.")
        updater.start_webhook(listen=LISTEN,
                              port=PORT,
                              url_path=TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN,
                                    certificate=open(CERT_PATH, 'rb'))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)

    else:
        logger.info("Using long polling.")
        updater.start_polling(timeout=15, read_latency=4)

    updater.idle()

if __name__ == '__main__':
    logger.info("Successfully loaded modules: " + str(ALL_MODULES))
    main()
