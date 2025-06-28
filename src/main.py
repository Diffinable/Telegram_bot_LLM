from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
import sqlite3
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_messages():
    return [
        {"id": 1, "user_id": "user123", "text": "Привет! Помогите с заказом", "status": "new", "created_at": "2025-06-27 10:00"},
        {"id": 2, "user_id": "user456", "text": "Не работает приложение", "status": "new", "created_at": "2025-06-27 10:15"},
        {"id": 3, "user_id": "user789", "text": "Вопрос по оплате", "status": "pending", "created_at": "2025-06-27 10:30"},
    ]

def get_generated_response(message_id):
    responses = {
        1: "Здравствуйте! Я помогу вам с заказом. Уточните, пожалуйста, номер заказа.",
        2: "Попробуйте перезапустить приложение. Если проблема остается, обновите до последней версии.",
        3: "По вопросам оплаты обращайтесь в службу биллинга по телефону +7-800-xxx-xx-xx"
    }
    return responses.get(message_id, "Спасибо за обраение!")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    messages = get_messages()  
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "messages": messages
    })

@app.get_messages("/message/")

@app.post("/approve/{message_id}")
async def approve_message(message_id: int):
    # логика одобрения
    return {"status": "success"}