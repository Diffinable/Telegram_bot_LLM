from telegram.ext import Application, MessageHandler, filters
from telegram import Update
from src.database import get_db
import requests
from src.models import Messages, Responses
from telegram_bot.ollama_api import generate_response
import os
from dotenv import load_dotenv


load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def handle_message(update: Update, context):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    text = update.message.text
    message_id = update.message.message_id
    
    await update.message.reply_text(            
    "Подождите оператор скоро ответит",
    reply_to_message_id=message_id,
    )


    db = next(get_db())
    message = Messages(chat_id=chat_id,
                        user_id=user_id,
                        text=text,
                        status="new",
                        id=message_id
                    )
                              
    db.add(message)
    db.commit()
    
    prompt = f"{text}"
    llm_response = generate_response(prompt)

    response = Responses(chat_id=chat_id, message_id=message.id, text=llm_response, status="pending")
    db.add(response)
    db.commit()
    db.close()


    # await update.message.reply_text(f"{llm_response}")

def send_telegram_message(chat_id: int, text: str, reply_to_message_id: int = None):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "reply_to_message_id":reply_to_message_id,
    }
    response = requests.post(url, json=payload)
    return response.json()



def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()