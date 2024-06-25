from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

async def start(update, context):
    dialog.mode = "main"
    text = load_message("main")
    await send_photo(update, context, "main")
    await send_text(update, context, text)

    await show_main_menu(update,context,  {
        "start": "Запустить",
        "gpt": "задать вопрос чату GPT 🧠",
        "profile": "генерация Tinder-профля😎",
        "opener": "сообщение для знакомства 🥰",
        "message": "переписка от вашего имени 😈",
        "date": "переписка со звездами 🔥"

    })

async def gpt(update, context):
    dialog.mode = "gpt"
    text = load_message("gpt")
    await send_photo(update, context, "gpt")
    await send_text(update, context, text)


async def gpt_dialog(update, context):
    text = update.message.text
    prompt = load_prompt("gpt")
    answer = await chatgpt.send_question(prompt, text)
    await send_text(update, context, answer)

async def date(update, context):
    dialog.mode = "date"
    text = load_message("date")
    await send_photo(update, context, "date")
    await send_text_buttons(update, context, text, {
        "date_grande": " Ариана Гранде",
        "date_robbie": "Марго Робби",
        "date_zendaya": "Зендея",
        "date_gosling": "Райан Гослинг",
        "date_hardy": "Том Харди",

    })

async def date_dialog(update, context):
    text = update.message.text
    my_message = await send_text(update, context, "Набирает текст...")
    answer = await chatgpt.add_message(text)
    await my_message.edit_text(answer)

async def date_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()

    await send_photo(update, context,query)
    await send_text(update, context, "кликнул по кнопке " + query, parse_mode=ParseMode.HTML)
    prompt = load_prompt(query)
    chatgpt.set_prompt(prompt)






async def message(update, context):
    dialog.mode = "message"
    text = load_message("message")
    await send_photo(update, context, "message")
    await send_text_buttons(update, context, text, {
        "message_next": "Написать сообщение",
        "message_date": "Пригласить на свидание",
    })
    dialog.list.clear()


async def message_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()

    prompt = load_prompt(query)
    user_chat_history = "\n\n".join(dialog.list)
    my_message = await send_text(update, context, "ChatGPT думает над вариантами ответа...")
    answer = await chatgpt.send_question(prompt, user_chat_history)
    await my_message.edit_text(answer)

async def message_dialog(update, context):
    text = update.message.text
    dialog.list.append(text)
async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update,context)
    if dialog.mode == "date":
        await date_dialog(update, context)
    if dialog.mode == "message":
        await message_dialog(update, context)
    else:
        await send_text(update, context, "Твоя очередь ответчать...")





async def hello_buttons(update, context):
    query = update.callback_query.data
    if query == "start":
        await send_text(update,context, "Процесс запущен")
    else:
        await send_text(update, context, "Процесс остановлен")

dialog = Dialog
dialog.mode = None
dialog.list = []
chatgpt = ChatGptService(token="chat token")

app = ApplicationBuilder().token("your token").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(CommandHandler("date", date))
app.add_handler(CommandHandler("message", message))


app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(date_button, pattern="^date_.*"))
app.add_handler(CallbackQueryHandler(message_button, pattern="^message_.*"))

app.add_handler(CallbackQueryHandler(hello_buttons))

app.run_polling()
