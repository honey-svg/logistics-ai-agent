from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
import os
from dotenv import load_dotenv
from typing import Dict, List
import json

load_dotenv()

app = FastAPI(title="Logistics Interview Chatbot", description="A stateful AI chatbot for logistics role interviews using Groq API.")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str


sessions: Dict[str, Dict] = {}

MAX_HISTORY_LENGTH = 10  
SUMMARY_PROMPT = "Summarize the following conversation history concisely, focusing on key user details for a logistics job interview:"

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    session_id = request.session_id
    user_message = request.message

    if session_id not in sessions:
        sessions[session_id] = {
            "history": [],
            "summary": ""
        }

    session = sessions[session_id]
    history = session["history"]
    summary = session["summary"]

    
    history.append({"role": "user", "content": user_message})

    messages = []
    if summary:
        messages.append({"role": "system", "content": f"Previous summary: {summary}"})
   
    messages.extend(history[-MAX_HISTORY_LENGTH:])

    
    system_prompt = "You are an AI interviewer for logistics roles. Ask relevant follow-up questions based on the user's responses. Keep responses professional and focused on logistics skills, experience, and AI knowledge."
    messages.insert(0, {"role": "system", "content": system_prompt})

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",  
            messages=messages,
            max_tokens=300
        )
        ai_response = response.choices[0].message.content

        
        history.append({"role": "assistant", "content": ai_response})

        
        if len(history) > MAX_HISTORY_LENGTH:
            
            history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
            summary_response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": f"{SUMMARY_PROMPT}\n{history_text}"}],
                max_tokens=200


            )
            new_summary = summary_response.choices[0].message.content
            session["summary"] = new_summary
            session["history"] = []  

        return ChatResponse(response=ai_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
