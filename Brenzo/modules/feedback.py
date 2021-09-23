import html
from telegram import Update, Bot, ParseMode
from telegram.ext import run_async
from Brenzo.modules.disable import DisableAbleCommandHandler
from Brenzo import dispatcher
from requests import get
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from Brenzo.modules.tr_engine.strings import tld

@run_async
def feedback(bot: Bot, update: Update):
  name = update.effective_message.from_user.first_name
  message = update.effective_message
  userid=message.from_user.id
  text = message.text[len('/feedback '):]
   

  feed_text = f"Brenzo's *New* feedback from [{name}](tg://user?id={userid})\n\nfeed: {text}"
  

  bot.send_message(-1001513232985, feed_text, parse_mode=ParseMode.MARKDOWN)
 
  chat = update.effective_chat
  text = html.escape(text)
  reply_text = tld(chat.id, 'thanks_feedback')
  message.reply_text(reply_text, reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(text=tld(chat.id, 'see_feedback'),url="https://t.me/BrenzoFeedback")]]))
                                               
  

  



feed_handle = DisableAbleCommandHandler("feedback", feedback)

dispatcher.add_handler(feed_handle)
