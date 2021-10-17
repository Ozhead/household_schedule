from typing import List
import profile
import telegram
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters
from task import Task

g_telegram_handler = None


class ProfileNotFoundException(Exception):
    def __init__(self, id):
        self.message = "There was no profile found for ID " + str(id) + "."

    def __str__(self):
        return self.message


class TelegramHandler:
    def __init__(self):
        self._profiles: List[profile.Profile] = []
        with open("telegram_api_key.txt", "r") as f:
            self.token = f.read()

        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        # add command handlers
        logon_handler = CommandHandler("logon", self.logon)
        self.dispatcher.add_handler(logon_handler)
        logoff_handler = CommandHandler("logoff", self.logoff)
        self.dispatcher.add_handler(logoff_handler)

        nc_handler = MessageHandler(Filters.text & (~Filters.command),
                                    self.no_command)
        self.dispatcher.add_handler(nc_handler)

    def set_profiles(self, profiles: List[profile.Profile]):
        self._profiles: List[profile.Profile] = profiles

    def _get_profile_by_id(self, id):
        for pr in self._profiles:
            if pr.get_user() == id:
                return pr
        else:
            raise ProfileNotFoundException(id)

    def no_command(self, update, context):
        msg = update.message.text.lower()
        try:
            if msg == "done":
                pr = self._get_profile_by_id(update.effective_chat.id)
                pr.on_msg_done()
            elif msg == "no":
                pr = self._get_profile_by_id(update.effective_chat.id)
                pr.on_msg_no()
            elif msg == "next":
                pr = self._get_profile_by_id(update.effective_chat.id)
                pr.on_msg_next()
            else:
                text = "Sorry, I did not understand this command!"
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=text)
        except ProfileNotFoundException:
            text = "You don't have an active session. Please use /logon first."
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=text)

    # executed by /logon <id>
    def logon(self, update, context):
        if len(context.args) > 1 or len(context.args) == 0:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Pls only give a name as argument.")
            return

        # check if user is logged on...
        for pr in self._profiles:
            if pr.get_user() == update.effective_chat.id:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="You are already logged on.")
                return

        logon_name = context.args[0]
        pr: profile.Profile = None
        for pr in self._profiles:
            if pr.get_name() == logon_name:
                if pr.get_user() is None:
                    pr.logon(update.effective_chat.id)
                    update.message.reply_text(text="Logon succesful.")
                    pr.update()
                    break
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id,
                                             text="This profile is already being used.")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Logon not succesful.")
    # end logon handler

    # method that is executed via /logoff
    def logoff(self, update, context):
        for pr in self._profiles:
            if pr.get_user() == update.effective_chat.id:
                pr.logoff()
                update.message.reply_text(text="You have been logged off.")
                return
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Seems you are not logged in.")

    # singleton pattern
    @staticmethod
    def the():
        global g_telegram_handler
        if g_telegram_handler is None:
            return TelegramHandler()

        return g_telegram_handler

    @staticmethod
    def announce_task(pr: profile.Profile, task: Task):
        txt = ("The next task is \n\n" +
               "                 '<b>" + task.get_name() + "</b>'.\n\n" +
               "Please write 'done' if you have finished the task.\n" +
               "If you are not going to do the task, please write 'no'.\n" +
               "If the day is over, the task will count as failed.")
        TelegramHandler.the().updater.bot.send_message(chat_id=pr.get_user(),
                                                       text=txt,
                                                       parse_mode=(telegram.
                                                                   ParseMode.
                                                                   HTML))

    @staticmethod
    def send_msg(pr: profile.Profile, msg: str):
        TelegramHandler.the().updater.bot.send_message(chat_id=pr.get_user(),
                                                       text=msg,
                                                       parse_mode=(telegram.
                                                                   ParseMode.
                                                                   HTML))

    def run(self):
        self.updater.start_polling()
