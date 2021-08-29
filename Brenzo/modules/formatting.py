from Brenzo.modules.helper_funcs.decorators import kigcallback
from telegram import (
    ParseMode,
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import run_async, CommandHandler, CallbackQueryHandler
from Brenzo.modules.tr_engine.strings import tld

def fmt_md_help(bot: Bot, update: Update):
    bot = context.bot
    update.effective_message.reply_text(
        tld(update.effective_chat.id, "md_help"),
        parse_mode=ParseMode.HTML,
    )


def fmt_filling_help(bot: Bot, update: Update):
    update.effective_message.reply_text(
        tld(update.effective_chat.id, "filling_help"),
        parse_mode=ParseMode.HTML,
    )



@kigcallback(pattern=r"fmt_help_")
def fmt_help(bot: Bot, update: Update):
    query = update.callback_query
    bot = context.bot
    help_info = query.data.split("fmt_help_")[1]
    if help_info == "md":
        help_text = tld(update.effective_chat.id, "md_help")
    elif help_info == "filling":
        help_text = tld(update.effective_chat.id, "filling_help") 
    query.message.edit_text(
        text=help_text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Back", callback_data=f"help_module({__mod_name__.lower()})"),
            InlineKeyboardButton(text='Report Error', url='https://t.me/YorkTownEagleUnion')]]
        ),
    )
    bot.answer_callback_query(query.id)

__help__ = True

def get_help(chat):
    return [gs(chat, "formt_help_bse"),
    [
        InlineKeyboardButton(text="Markdown", callback_data="fmt_help_md"),
        InlineKeyboardButton(text="Filling", callback_data="fmt_help_filling")
    ]
]
