from typing import List
from profile import Profile
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters


class TelegramHandler:
    def __init__(self, profiles: List[Profile]):
        self._profiles: List[Profile] = profiles
        with open("telegram_api_key.txt", "r") as f:
            self.token = f.read()

        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        # add command handlers
        nc_handler = MessageHandler(Filters.text & (~Filters.command),
                                    self.no_command)
        self.dispatcher.add_handler(nc_handler)

        logon_handler = CommandHandler("logon", self.logon)
        self.dispatcher.add_handler(logon_handler)
        logoff_handler = CommandHandler("logoff", self.logoff)
        self.dispatcher.add_handler(logoff_handler)

    def no_command(self, update, context):
        text = "Sorry, I did not understand this command!"
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=text)

    def logon(self, update, context):
        if len(context.args) > 1 or len(context.args) == 0:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Please only give a name as argument.")
            return

        # check if user is logged on...
        for pr in self._profiles:
            if pr.get_user() == update.effective_chat.id:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="You are already logged on.")
                return

        logon_name = context.args[0]
        pr: Profile = None
        for pr in self._profiles:
            if pr.get_name() == logon_name:
                pr.set_user(update.effective_chat.id)
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="Logon succesful.")
                break
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Logon not succesful.")
    # end logon handler

    def logoff(self, update, context):
        for pr in self._profiles:
            if pr.get_user() == update.effective_chat.id:
                pr.set_user(None)
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="You have been logged off.")
                return
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Seems you are not logged in.")

    def run(self):
        self.updater.start_polling()
