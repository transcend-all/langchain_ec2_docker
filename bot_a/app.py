# app.py
import os
import threading
import time
import random
from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

# Environment Variables
BOT_NAME = os.getenv("BOT_NAME", "Bot A")
OTHER_BOT_URL = os.getenv("OTHER_BOT_URL")

# Simulated response generator
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

# Function to send a message to the other bot
def send_message_to_other_bot(message: str):
    if OTHER_BOT_URL:
        try:
            payload = {"message": message}
            headers = {"Content-Type": "application/json"}
            res = requests.post(f"{OTHER_BOT_URL}/message", json=payload, headers=headers)
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error sending message to {OTHER_BOT_URL}: {e}")

@app.post("/message")
def receive_message(msg: Message):
    print(f"[{BOT_NAME}] Received message: {msg.message}")

    # Create a response
    response = simulate_response(msg.message, BOT_NAME)
    print(f"[{BOT_NAME}] Responding with: {response}")

    # Send the response back to the other bot in a background thread
    if OTHER_BOT_URL:
        threading.Thread(target=delayed_send, args=(response,)).start()

    return {"response": response}

def delayed_send(message: str):
    time.sleep(1)  # Small delay to simulate "thinking"
    send_message_to_other_bot(message)

@app.get("/")
def read_root():
    return {"message": f"{BOT_NAME} is running."}
