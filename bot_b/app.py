import os
import random
import time
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

BOT_NAME = os.getenv("BOT_NAME", "Bot")

def simulate_response(message: str, bot_name: str) -> str:
    responses = [
        f"{bot_name} says: Got your message!",
        f"{bot_name} replies: How interesting!",
        f"{bot_name} says: Tell me more!",
        f"{bot_name} says: Haha, that's funny.",
        f"{bot_name} says: I see. Let's continue!"
    ]
    return random.choice(responses)

class Message(BaseModel):
    message: str

@app.post("/message")
def receive_message(msg: Message):
    print(f"[{BOT_NAME}] Received message: {msg.message}")
    response = simulate_response(msg.message, BOT_NAME)
    print(f"[{BOT_NAME}] Responding with: {response}")
    return {"response": response}

@app.get("/")
def read_root():
    return {"message": f"{BOT_NAME} is running."}
