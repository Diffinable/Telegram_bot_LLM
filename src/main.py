from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import requests
from src.models import Messages, Responses
from src.database import get_db
from datetime import datetime
from dotenv import load_dotenv
import os




load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="templates")

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")




@app.get("/", response_class=HTMLResponse)
async def read_messages(request: Request, db: Session = Depends(get_db)):
    messages = db.query(Messages).filter(Messages.status == 'new').all()
    responses = db.query(Responses).filter(Responses.status == "pending").all()
    return templates.TemplateResponse("messages.html", {
        "request": request, 
        "messages": messages,
        "responses": responses,
    })

@app.get("/message/{message_id}", response_class=HTMLResponse)
async def message_detail(request: Request, message_id: int, db: Session = Depends(get_db)):
    message = db.query(Messages).get(message_id)
    if not message:
        return {"error": "Message not found"}
    

    prompt = f"Пользователь написал: {message.text}. Сгенерируй ответ."
    
    response = db.query(Responses).filter_by(message_id==message_id, status="pending").first()


    llm_response = response.text if response else "Not response yet"
    
    return templates.TemplateResponse("message_detail.html", {
        "request": request,
        "message": message,
        "llm_response": llm_response,
    })

@app.post("/message/{message_id}/action")
async def handle_action(
    message_id: int,
    action: str = Form(...),
    response_text: str = Form(...),
    db: Session = Depends(get_db),
):
    message = db.query(Messages).get(message_id)
    if not message:
        return {"error": "Message not found"}
    response = db.query(Responses).filter_by(message_id, status="pending").first()
    if action == "approve":
        response = db.query(Responses).filter_by(message_id=message_id, status='pending').first()
        if response:
            response.text = response_text
            response.status = 'ready'
        else:
            response = Responses(
                chat_id=message.chat_id,
                message_id=message.id,
                text=response_text,
                status='ready',
            )
            db.add(response)
        message.status = "processed"
        db.commit()
    elif action == "regenerate":
        pass

    return RedirectResponse("/", status_code=303)




def add_test_message():
    try:
        db = next(get_db())
        message = Messages(chat_id=123, user_id=567, text="Text message", status="new")
        db.add(message)
        db.commit()
        print("Тестовое сообщение успешно добавлено")
    except Exception as e:
        print(f"Ошибка при добавлении сообщения {str(e)}")
    finally:
        db.close()



if __name__ == "__main__":
    add_test_message()




