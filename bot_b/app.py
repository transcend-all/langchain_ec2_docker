# app.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from langchain import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

app = FastAPI()

# Environment Variables
BOT_NAME = os.getenv("BOT_NAME")
OTHER_BOT_URL = os.getenv("OTHER_BOT_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize LangChain
llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.7)
prompt = PromptTemplate(
    input_variables=["message"],
    template="You are {bot_name}. Respond to the following message: {message}",
)
chain = LLMChain(llm=llm, prompt=prompt)

class Message(BaseModel):
    message: str

@app.post("/message")
def receive_message(msg: Message):
    print(f"Received message: {msg.message}")
    response = chain.run(message=msg.message, bot_name=BOT_NAME)
    print(f"Responding with: {response}")

    # Optionally, send the response to the other bot
    if OTHER_BOT_URL:
        try:
            payload = {"message": response}
            headers = {"Content-Type": "application/json"}
            res = requests.post(f"{OTHER_BOT_URL}/message", json=payload, headers=headers)
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error sending message to {OTHER_BOT_URL}: {e}")
    return {"response": response}

@app.get("/")
def read_root():
    return {"message": f"{BOT_NAME} is running."}
