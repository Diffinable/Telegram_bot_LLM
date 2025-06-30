from telegram.ext import Application, MessageHandler, filters
from telegram import Update
from src.database import get_db
from src.models import Messages, Responses
from llm import TinyLlame
import os
from dotenv import load_dotenv


load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
llm = TinyLlame()

async def handle_message(update: Update, context):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    text = update.message.text

    db = next(get_db())
    message = Messages(chat_id=chat_id, user_id=user_id, text=text, status="new")
    db.add(message)
    db.commit()
    
    prompt = f"Пользователь написал: {text}. Сгенерируй ответ"
    llm_response = llm.generate_response(prompt)

    response = Responses(chat_id=chat_id, message_id=message.id, text=llm_response, status="pending")
    db.add(response)
    db.commit()
    db.close()


    await update.message.reply_text("Ваше сообщение принято. Оператор скоро ответит")



def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()