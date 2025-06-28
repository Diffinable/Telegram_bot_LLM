from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import requests
import sqlite3
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")



@app.get("/", response_class=HTMLResponse)
async def read_messages(request: Request, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.status == 'new').all()

    return templates.TemplateResponse("messages.html", {
        "request": request, 
        "messages": messages
    })

@app.get("/message/{message_id}", response_class=HTMLResponse)
async def message_detail(request: Request, message_id: int, db: Sesison = Depends(get_db)):
    message = db.query(Messages).get(message_id)
    prompt = f"Пользователь написал: {message.text}. Сгенерируй ответ."
    llm_response = requests.post(
        "http://llm:11434/api/generate",
        json={"model": "tinyllama", "prompt": prompt}
    ).json["response"]

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
    message = query(Messages).get(message_id)
    if action == "approve":
        new_message = Messages(
            chat_id = message.chat_id,
            text = response_text,
            status = 'ready',
            is_from_user = False,
        )
        db.add(new_message)
        message.status = "processed"
    elif action == "regenerate":
        pass

    db.commit()
    return RedirectResponse("/", status_code=303)

