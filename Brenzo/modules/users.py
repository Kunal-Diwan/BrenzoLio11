from io import BytesIO
from time import sleep

from telegram import Bot, Update, TelegramError
from telegram.error import BadRequest
from telegram.ext import CommandHandler, MessageHandler, Filters, run_async

import Brenzo.modules.sql.users_sql as sql

from Brenzo import dispatcher, OWNER_ID, LOGGER, DEV_USERS
from Brenzo.modules.helper_funcs.chat_status import sudo_plus, dev_plus

USERS_GROUP = 4
DEV_AND_MORE = DEV_USERS.append(int(OWNER_ID))
CHAT_GROUP = 10


def get_user_id(username):
    # ensure valid userid
    if len(username) <= 5:
        return None

    if username.startswith('@'):
        username = username[1:]

    users = sql.get_userid_by_name(username)

    if not users:
        return None

    elif len(users) == 1:
        return users[0].user_id

    else:
        for user_obj in users:
            try:
                userdat = dispatcher.bot.get_chat(user_obj.user_id)
                if userdat.username == username:
                    return userdat.id

            except BadRequest as excp:
                if excp.message == 'Chat not found':
                    pass
                else:
                    LOGGER.exception("Error extracting user ID")

    return None


@run_async
@dev_plus
def broadcast(bot: Bot, update: Update):

    to_send = update.effective_message.text.split(None, 1)

    if len(to_send) >= 2:
        chats = sql.get_all_chats() or []
        failed = 0
        for chat in chats:
            try:
                bot.sendMessage(int(chat.chat_id), to_send[1])
                sleep(0.1)
            except TelegramError:
                failed += 1
                LOGGER.warning("Couldn't send broadcast to %s, group name %s", str(chat.chat_id), str(chat.chat_name))

        update.effective_message.reply_text(
            f"Broadcast complete. {failed} groups failed to receive the message, probably due to being kicked.")


@run_async
def log_user(bot: Bot, update: Update):
    chat = update.effective_chat
    msg = update.effective_message

    sql.update_user(msg.from_user.id,
                    msg.from_user.username,
                    chat.id,
                    chat.title)

    if msg.reply_to_message:
        sql.update_user(msg.reply_to_message.from_user.id,
                        msg.reply_to_message.from_user.username,
                        chat.id,
                        chat.title)

    if msg.forward_from:
        sql.update_user(msg.forward_from.id,
                        msg.forward_from.username)


@run_async
def snipe(bot: Bot, update: Update, args: List[str]):
    try:
        chat_id = str(args[0])
        del args[0]
    except TypeError as excp:
        update.effective_message.reply_text(
            "Please give me a chat to echo to!")
    to_send = " ".join(args)
    if len(to_send) >= 2:
        try:
            bot.sendMessage(int(chat_id), str(to_send))
        except TelegramError:
            LOGGER.warning("Couldn't send to group %s", str(chat_id))
            update.effective_message.reply_text(
                "Couldn't send the message. Perhaps I'm not part of that group?"
            )


@run_async
@bot_admin
def getlink(bot: Bot, update: Update, args: List[int]):
    message = update.effective_message
    if args:
        pattern = re.compile(r'-\d+')
    else:
        message.reply_text("You don't seem to be referring to any chats.")
    links = "Invite link(s):\n"
    for chat_id in pattern.findall(message.text):
        try:
            chat = bot.getChat(chat_id)
            bot_member = chat.get_member(bot.id)
            if bot_member.can_invite_users:
                invitelink = bot.exportChatInviteLink(chat_id)
                links += str(chat_id) + ":\n" + invitelink + "\n"
            else:
                links += str(
                    chat_id
                ) + ":\nI don't have access to the invite link." + "\n"
        except BadRequest as excp:
            links += str(chat_id) + ":\n" + excp.message + "\n"
        except TelegramError as excp:
            links += str(chat_id) + ":\n" + excp.message + "\n"

    message.reply_text(links)


@bot_admin
def leavechat(bot: Bot, update: Update, args: List[int]):
    if args:
        chat_id = int(args[0])
    else:
        try:
            chat = update.effective_chat
            if chat.type == "private":
                update.effective_message.reply_text(
                    "You do not seem to be referring to a chat!")
                return
            chat_id = chat.id
            reply_text = "`I'll leave this group`"
            bot.send_message(chat_id,
                             reply_text,
                             parse_mode='Markdown',
                             disable_web_page_preview=True)
            bot.leaveChat(chat_id)
        except BadRequest as excp:
            if excp.message == "Chat not found":
                update.effective_message.reply_text(
                    "It looks like I've been kicked out of the group :p")
            else:
                return

    try:
        chat = bot.getChat(chat_id)
        titlechat = bot.get_chat(chat_id).title
        reply_text = "`I'll Go Away!`"
        bot.send_message(chat_id,
                         reply_text,
                         parse_mode='Markdown',
                         disable_web_page_preview=True)
        bot.leaveChat(chat_id)
        update.effective_message.reply_text(
            "I'll left group {}".format(titlechat))

    except BadRequest as excp:
        if excp.message == "Chat not found":
            update.effective_message.reply_text(
                "It looks like I've been kicked out of the group :p")
        else:
            return


@run_async
@sudo_plus
def chats(bot: Bot, update: Update):

    all_chats = sql.get_all_chats() or []
    chatfile = 'List of chats.\n'
    for chat in all_chats:
        chatfile += f"{chat.chat_name} - ({chat.chat_id})\n"

    with BytesIO(str.encode(chatfile)) as output:
        output.name = "chatlist.txt"
        update.effective_message.reply_document(document=output, filename="chatlist.txt",
                                                caption="Here is the list of chats in my Hit List.")


def __user_info__(user_id, chat_id):
    if user_id == dispatcher.bot.id:
        return tld(chat_id, "users_seen_is_bot")
    num_chats = sql.get_user_num_chats(user_id)
    return tld(chat_id, "users_seen").format(num_chats)


def __stats__():
    return "`{}` users, across `{}` chats".format(sql.num_users(),
                                                    sql.num_chats())


def __gdpr__(user_id):
    sql.del_user(user_id)


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


__help__ = ""  # no help string

BROADCAST_HANDLER = CommandHandler("broadcast", broadcast)
USER_HANDLER = MessageHandler(Filters.all & Filters.group, log_user)
SNIPE_HANDLER = CommandHandler("snipe",
                               snipe,
                               pass_args=True,
                               filters=Filters.user(OWNER_ID))
GETLINK_HANDLER = CommandHandler("getlink",
                                 getlink,
                                 pass_args=True,
                                 filters=Filters.user(OWNER_ID))
LEAVECHAT_HANDLER = CommandHandler("leavechat",
                                   leavechat,
                                   pass_args=True,
                                   filters=Filters.user(OWNER_ID))
CHATLIST_HANDLER = CommandHandler("chatlist", chats)

dispatcher.add_handler(USER_HANDLER, USERS_GROUP)
dispatcher.add_handler(BROADCAST_HANDLER)
dispatcher.add_handler(CHATLIST_HANDLER)

__mod_name__ = "Users"
__handlers__ = [(USER_HANDLER, USERS_GROUP), BROADCAST_HANDLER, CHATLIST_HANDLER]
