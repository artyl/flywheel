import sys, queue, threading, re, traceback
import telebot
import flywheel
from ui_level import UiOperations

MSG_QUEUE = queue.Queue()
API_TOKEN = sys.argv[1]
IDS = sys.argv[2].strip().split(',')
chat_id = IDS[0]

bot = telebot.TeleBot(API_TOKEN)

def exception_text():
    return "".join(traceback.format_exception(*sys.exc_info())).encode('cp1251', 'ignore').decode('cp1251', 'ignore')

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def input_message(message):
    if chat_id != message.chat.id:
        print(f'Unknown chat_id {message.chat.id}')
    print(f'queue.put: {message.text}')
    MSG_QUEUE.put(message.text)

def tg_print(text, end='\n'):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    print(f'tg_print: {text}')
    text = ansi_escape.sub('', text)
    try:
        if len(text.strip()) > 0:
            bot.send_message(chat_id, text, disable_notification=True)
    except Exception:
        print(exception_text())

def tg_input(text):
    tg_print(text)    
    print(f'tg_input: {text}')
    msg = MSG_QUEUE.get()
    print(f'queue.get: {msg}')
    return msg

if __name__ == '__main__':
    # bot.send_message(chat_id, 'text _text_ text', disable_notification=True, parse_mode='MarkdownV2')
    threading.Thread(target=bot.infinity_polling, name='bot_polling', daemon=True).start()
    uop = UiOperations(tg_print, tg_input, colorize='md')
    flywheel.main(uop)
