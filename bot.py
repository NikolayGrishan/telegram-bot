# import os
# import json
# from telegram.ext import (
#     ApplicationBuilder, CommandHandler, MessageHandler,
#     filters, ConversationHandler, ContextTypes, CallbackQueryHandler
# )
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

# YOUR_USER_ID = 612202903  # твой Telegram ID

# Q1, Q2, Q3 = range(3)

# employees = [464421030, 612202903, 818831952, 983099743]  # список сотрудников
# answers = {}

# questions = [
#     "Вопрос 1: Как дела?",
#     "Вопрос 2: Что делаешь?",
#     "Вопрос 3: Когда закончишь?"
# ]

# def load_answers():
#     global answers
#     try:
#         with open("data.json", "r", encoding="utf-8") as f:
#             answers.update(json.load(f))
#     except FileNotFoundError:
#         pass

# def save_answers():
#     with open("data.json", "w", encoding="utf-8") as f:
#         json.dump(answers, f, ensure_ascii=False, indent=4)

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.effective_user
#     if user.id not in employees:
#         await update.message.reply_text("Ты не в списке сотрудников для опроса.")
#         return ConversationHandler.END

#     answers[user.id] = {
#         'username': user.username or user.full_name or str(user.id),
#         'responses': []
#     }
#     save_answers()
#     await update.message.reply_text(questions[0])
#     return Q1

# async def answer_q1(update, context):
#     user_id = update.effective_user.id
#     answers[user_id]['responses'].append(update.message.text)
#     save_answers()
#     await update.message.reply_text(questions[1])
#     return Q2

# async def answer_q2(update, context):
#     user_id = update.effective_user.id
#     answers[user_id]['responses'].append(update.message.text)
#     save_answers()
#     await update.message.reply_text(questions[2])
#     return Q3

# async def answer_q3(update, context):
#     user_id = update.effective_user.id
#     answers[user_id]['responses'].append(update.message.text)
#     save_answers()
#     await update.message.reply_text("Спасибо за ответы!")
#     return ConversationHandler.END

# async def check_non_responders(context):
#     non_responders = [uid for uid in employees if uid not in answers or len(answers[uid]['responses']) < 3]
#     responders = [uid for uid in employees if uid in answers and len(answers[uid]['responses']) == 3]

#     msg = ""
#     if non_responders:
#         msg += "❌ Не ответили:\n"
#         for uid in non_responders:
#             msg += f"- {uid}\n"

#     if responders:
#         msg += "\n✅ Ответы сотрудников:\n"
#         for uid in responders:
#             username = answers[uid]['username']
#             user_answers = answers[uid]['responses']
#             msg += f"@{username} ответил:\n"
#             for i, ans in enumerate(user_answers, start=1):
#                 msg += f"  Вопрос {i}: {ans}\n"
#             msg += "\n"

#     if not msg:
#         msg = "Все ответили!"

#     await context.bot.send_message(chat_id=YOUR_USER_ID, text=msg)

# async def trigger_check(update, context):
#     await check_non_responders(context)

# async def send_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.effective_user
#     user_id = user.id
#     username = user.username or "Без username"
#     full_name = user.full_name

#     await update.message.reply_text(f"Твой Telegram ID: {user_id}")

#     keyboard = [
#         [InlineKeyboardButton("➕ Добавить в список", callback_data=f"add:{user_id}")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)

#     await context.bot.send_message(
#         chat_id=YOUR_USER_ID,
#         text=f"🔔 Новый пользователь:\n"
#              f"Имя: {full_name}\n"
#              f"Username: @{username}\n"
#              f"ID: {user_id}",
#         reply_markup=reply_markup
#     )

# async def handle_add_employee(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()
#     data = query.data

#     if data.startswith("add:"):
#         user_id = int(data.split(":")[1])
#         if user_id not in employees:
#             employees.append(user_id)
#             await query.edit_message_text(f"✅ Пользователь {user_id} добавлен в список сотрудников.")
#         else:
#             await query.edit_message_text("⚠️ Этот пользователь уже в списке сотрудников.")

# def main():
#     load_answers()

#     TOKEN = os.getenv("BOT_TOKEN")
#     PORT = int(os.getenv("PORT", "8443"))
#     HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME")

#     app = ApplicationBuilder().token(TOKEN).build()

#     conv_handler = ConversationHandler(
#         entry_points=[CommandHandler("start", start)],
#         states={
#             Q1: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_q1)],
#             Q2: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_q2)],
#             Q3: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_q3)],
#         },
#         fallbacks=[]
#     )

#     app.add_handler(conv_handler)
#     app.add_handler(CommandHandler("check", trigger_check))
#     app.add_handler(CommandHandler("id", send_user_id))
#     app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, send_user_id))
#     app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^/id$"), send_user_id))
#     app.add_handler(CallbackQueryHandler(handle_add_employee))

#     # Запуск webhook, URL формируем автоматически с https://
#     app.run_webhook(
#         listen="0.0.0.0",
#         port=PORT,
#         url_path="webhook",
#         webhook_url=f"https://{HOST}/webhook"
#     )

# if __name__ == "__main__":
#     main()

import os
import json
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ConversationHandler, ContextTypes, CallbackQueryHandler
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

YOUR_USER_ID = 612202903  # твой Telegram ID

Q1, Q2, Q3 = range(3)

employees = [464421030, 612202903, 818831952, 983099743]  # список сотрудников
answers = {}

DATA_FILE = 'data.json'

questions = [
    "Вопрос 1: Как дела?",
    "Вопрос 2: Что делаешь?",
    "Вопрос 3: Когда закончишь?"
]

def load_answers():
    global answers
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            answers.update(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        answers.clear()

def save_answers():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(answers, f, ensure_ascii=False, indent=4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in employees:
        await update.message.reply_text("Ты не в списке сотрудников для опроса.")
        return ConversationHandler.END

    answers[user.id] = {
        'username': user.username or user.full_name or str(user.id),
        'responses': []
    }
    save_answers()
    await update.message.reply_text(questions[0])
    return Q1

async def answer_q1(update, context):
    user_id = update.effective_user.id
    answers[user_id]['responses'].append(update.message.text)
    save_answers()
    await update.message.reply_text(questions[1])
    return Q2

async def answer_q2(update, context):
    user_id = update.effective_user.id
    answers[user_id]['responses'].append(update.message.text)
    save_answers()
    await update.message.reply_text(questions[2])
    return Q3

async def answer_q3(update, context):
    user_id = update.effective_user.id
    answers[user_id]['responses'].append(update.message.text)
    save_answers()
    await update.message.reply_text("Спасибо за ответы!")
    return ConversationHandler.END

async def check_non_responders(context):
    non_responders = [uid for uid in employees if uid not in answers or len(answers[uid]['responses']) < 3]
    responders = [uid for uid in employees if uid in answers and len(answers[uid]['responses']) == 3]

    msg = ""
    if non_responders:
        msg += "❌ Не ответили:\n"
        for uid in non_responders:
            msg += f"- {uid}\n"

    if responders:
        msg += "\n✅ Ответы сотрудников:\n"
        for uid in responders:
            username = answers[uid]['username']
            user_answers = answers[uid]['responses']
            msg += f"@{username} ответил:\n"
            for i, ans in enumerate(user_answers, start=1):
                msg += f"  Вопрос {i}: {ans}\n"
            msg += "\n"

    if not msg:
        msg = "Все ответили!"

    await context.bot.send_message(chat_id=YOUR_USER_ID, text=msg)

async def trigger_check(update, context):
    await check_non_responders(context)

async def send_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    username = user.username or "Без username"
    full_name = user.full_name

    await update.message.reply_text(f"Твой Telegram ID: {user_id}")

    keyboard = [
        [InlineKeyboardButton("➕ Добавить в список", callback_data=f"add:{user_id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=YOUR_USER_ID,
        text=f"🔔 Новый пользователь:\n"
             f"Имя: {full_name}\n"
             f"Username: @{username}\n"
             f"ID: {user_id}",
        reply_markup=reply_markup
    )

async def handle_add_employee(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("add:"):
        user_id = int(data.split(":")[1])
        if user_id not in employees:
            employees.append(user_id)
            await query.edit_message_text(f"✅ Пользователь {user_id} добавлен в список сотрудников.")
        else:
            await query.edit_message_text("⚠️ Этот пользователь уже в списке сотрудников.")

def main():
    global answers
    TOKEN = os.getenv("BOT_TOKEN")
    PORT = int(os.getenv("PORT", "8443"))
    HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME")

    load_answers()

    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            Q1: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_q1)],
            Q2: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_q2)],
            Q3: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_q3)],
        },
        fallbacks=[]
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("check", trigger_check))
    app.add_handler(CommandHandler("id", send_user_id))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, send_user_id))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^/id$"), send_user_id))
    app.add_handler(CallbackQueryHandler(handle_add_employee))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="webhook",
        webhook_url=f"https://{HOST}/webhook"
    )

if __name__ == "__main__":
    main()
