# from telegram.ext import (
#     ApplicationBuilder, CommandHandler, MessageHandler,
#     filters, ConversationHandler, ContextTypes, CallbackQueryHandler
# )
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
# import asyncio
# import json
# import os

# YOUR_USER_ID = 612202903  # твой Telegram ID
# DATA_FILE = "data.json"

# Q1, Q2, Q3 = range(3)

# employees = {}
# answers = {}

# questions = [
#     "Вопрос 1: Как дела?",
#     "Вопрос 2: Что делаешь?",
#     "Вопрос 3: Когда закончишь?"
# ]

# # === Загрузка и сохранение ===
# def load_data():
#     global employees, answers
#     if os.path.exists(DATA_FILE):
#         with open(DATA_FILE, "r", encoding="utf-8") as f:
#             data = json.load(f)
#             employees = {int(k): v for k, v in data.get("employees", {}).items()}
#             answers = data.get("answers", {})
#     else:
#         employees = {}
#         answers = {}

# def save_data():
#     with open(DATA_FILE, "w", encoding="utf-8") as f:
#         json.dump({
#             "employees": employees,
#             "answers": answers
#         }, f, ensure_ascii=False, indent=2)

# # === Опрос ===
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.effective_user
#     if user.id not in employees:
#         await update.message.reply_text("Ты не в списке сотрудников для опроса.")
#         return ConversationHandler.END

#     answers[user.id] = {
#         'username': user.username or user.full_name or str(user.id),
#         'responses': []
#     }
#     await update.message.reply_text(questions[0])
#     return Q1

# async def answer_q1(update, context):
#     user_id = update.effective_user.id
#     answers[user_id]['responses'].append(update.message.text)
#     await update.message.reply_text(questions[1])
#     return Q2

# async def answer_q2(update, context):
#     user_id = update.effective_user.id
#     answers[user_id]['responses'].append(update.message.text)
#     await update.message.reply_text(questions[2])
#     return Q3

# async def answer_q3(update, context):
#     user_id = update.effective_user.id
#     answers[user_id]['responses'].append(update.message.text)
#     await update.message.reply_text("Спасибо за ответы!")
#     save_data()
#     return ConversationHandler.END

# # === Проверка ответов ===
# async def check_non_responders(context):
#     non_responders = [uid for uid in employees if uid not in answers or len(answers[uid]['responses']) < 3]
#     responders = [uid for uid in employees if uid in answers and len(answers[uid]['responses']) == 3]

#     msg = ""
#     if non_responders:
#         msg += "❌ Не ответили:\n"
#         for uid in non_responders:
#             name = employees.get(uid, f"ID {uid}")
#             msg += f"- {name} ({uid})\n"

#     if responders:
#         msg += "\n✅ Ответы сотрудников:\n"
#         for uid in responders:
#             name = employees.get(uid, f"ID {uid}")
#             user_answers = answers[uid]['responses']
#             msg += f"{name} ответил:\n"
#             for i, ans in enumerate(user_answers, start=1):
#                 msg += f"  Вопрос {i}: {ans}\n"
#             msg += "\n"

#     if not msg:
#         msg = "Все ответили!"

#     await context.bot.send_message(chat_id=YOUR_USER_ID, text=msg)

# async def trigger_check(update, context):
#     await check_non_responders(context)

# # === /id команда ===
# async def send_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.effective_user
#     user_id = user.id
#     username = user.username or "Без username"
#     full_name = user.full_name

#     await update.message.reply_text(f"Твой Telegram ID: {user_id}")

#     keyboard = [
#         [InlineKeyboardButton("➕ Добавить в список", callback_data=f"add:{user_id}:{full_name}")]
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

# # === Обработка добавления сотрудника ===
# async def handle_add_employee(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()
#     data = query.data

#     if data.startswith("add:"):
#         parts = data.split(":")
#         user_id = int(parts[1])
#         full_name = parts[2]

#         if user_id not in employees:
#             employees[user_id] = full_name
#             save_data()
#             await query.edit_message_text(f"✅ Пользователь {full_name} добавлен в список сотрудников.")
#         else:
#             await query.edit_message_text(f"⚠️ {employees[user_id]} уже в списке.")

# # === Основной запуск ===
# def main():
#     load_data()

#     app = ApplicationBuilder().token("8016723771:AAHwDSI1MoEAd4f6QwaIQmKBevpq30qAu40").build()

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
#     app.add_handler(CallbackQueryHandler(handle_add_employee))

#     app.run_polling()

# if __name__ == "__main__":
#     main()

import os
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ConversationHandler, ContextTypes, CallbackQueryHandler
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

YOUR_USER_ID = 612202903  # твой Telegram ID

Q1, Q2, Q3 = range(3)

employees = [464421030, 612202903, 818831952, 983099743]  # список сотрудников
answers = {}

questions = [
    "Вопрос 1: Как дела?",
    "Вопрос 2: Что делаешь?",
    "Вопрос 3: Когда закончишь?"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in employees:
        await update.message.reply_text("Ты не в списке сотрудников для опроса.")
        return ConversationHandler.END

    answers[user.id] = {
        'username': user.username or user.full_name or str(user.id),
        'responses': []
    }
    await update.message.reply_text(questions[0])
    return Q1

async def answer_q1(update, context):
    user_id = update.effective_user.id
    answers[user_id]['responses'].append(update.message.text)
    await update.message.reply_text(questions[1])
    return Q2

async def answer_q2(update, context):
    user_id = update.effective_user.id
    answers[user_id]['responses'].append(update.message.text)
    await update.message.reply_text(questions[2])
    return Q3

async def answer_q3(update, context):
    user_id = update.effective_user.id
    answers[user_id]['responses'].append(update.message.text)
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
    TOKEN = os.getenv("BOT_TOKEN")
    PORT = int(os.getenv("PORT", "8443"))
    HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME")

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

    # Запуск webhook, URL формируем автоматически с https://
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"https://{HOST}/webhook"
    )

if __name__ == "__main__":
    main()
