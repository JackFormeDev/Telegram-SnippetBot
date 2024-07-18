from pyrogram import (Client, filters)
from pyrogram.handlers import (MessageHandler, CallbackQueryHandler)
from messages import MessagesHandler
from callback import CallbackHandler
from utils import Database

class Bot(Client):
    def __init__(self, name, id, hash, token):
        '''Core class'''
        super().__init__(name, id, hash, bot_token=token)
        self.messages_handler = MessagesHandler()
        self.callback_handler = CallbackHandler()
        self.database = Database()
        self.database.create_tables()
        self.add_handlers()

    def add_handlers(self):
        '''Handles messages and buttons'''
        self.add_handler(MessageHandler(self.messages_handler.get_message), 0)
        self.add_handler(CallbackQueryHandler(self.callback_handler.get_callback), 1)
        print("Running ...")

    def run_bot(self):
        '''Runs the bot'''
        self.run()


if __name__ == '__main__':
    API_ID = None
    API_HASH = None
    BOT_TOKEN = None
    bot = Bot('session', API_ID, API_HASH, BOT_TOKEN)
    bot.run_bot()