import ollama
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from datetime import datetime
import os


# Initialize database connection

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'chat_memory.db'))
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# 🔐 Ensure chat_history table exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp TEXT NOT NULL
)
''')
conn.commit()

app = FastAPI()

# Enable CORS so frontend can access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# System prompt to instruct Mistral on how to behave
# SYSTEM_PROMPT = """
# You are MIMI, a friendly, empathetic, and knowledgeable AI parenting assistant. 
# Your purpose is to support and reassure parents by offering practical advice, emotional encouragement, 
# and reliable information on child care, sleep routines, feeding, educational activities, child health, 
# and cognitive development. Always respond in a supportive, compassionate, and understanding tone. 
# Use simple, clear language suitable for all parents.
# """

# Romanian system prompt
SYSTEM_PROMPT = """
Ești MIMI, un asistent virtual inteligent, empatic și prietenos, specializat în sprijinul părinților. 
Scopul tău este să oferi sfaturi practice și încurajare emoțională cu privire la îngrijirea copilului, 
rutine de somn, alimentație sănătoasă, activități educative, sănătatea copilului și dezvoltarea cognitivă. 
Răspunde întotdeauna în limba română, folosind un limbaj simplu, concis, relevant, clar, empatic și încurajator, 
potrivit pentru toți părinții. Ai grija ca limbajul sa fie unul corect gramatical.
"""

model_selected = "llama3.1" # llama3.1 , deepseek-llm, openhermes, mistral

class ChatInput(BaseModel):
    query: str

# POST Endpoint
@app.post("/chat")
def chat_post(payload: ChatInput):

    # Save user message to DB
    cursor.execute("INSERT INTO chat_history (role, content, timestamp) VALUES (?, ?, ?)",
                ("user", payload.query, datetime.now().isoformat()))

    # Build full message history (system prompt + saved chat)
    history = [{"role": "system", "content": SYSTEM_PROMPT}] + get_chat_history()

    # Send to Ollama
    response = ollama.chat(
        model=model_selected,
        messages=history
    )

    # Extract and save AI response
    ai_message = response.get("message", {}).get("content", "").strip()
    cursor.execute("INSERT INTO chat_history (role, content, timestamp) VALUES (?, ?, ?)",
                ("assistant", ai_message, datetime.now().isoformat()))
    conn.commit()

    # Format output
    ai_message = ai_message.replace("**", "<strong>").replace("* ", "• ").replace("\n", "<br>")

    return {"response": ai_message}



# # GET Endpoint
# @app.get("/")
# def home():
#     return {"message": "Welcome to Mimi - Your AI Parenting Assistant!"}

# @app.get("/chat")
# def chat(query: str):
#     """Trimite mesajul utilizatorului către Mistral/Llama/DeepSeek etc și returnează un răspuns clar în limba română."""
#     response = ollama.chat(
#         model=model_selected,
#         messages=[
#             {"role": "system", "content": SYSTEM_PROMPT},
#             {"role": "user", "content": query}])

#     # Extract the content properly
#     ai_response = response.get("message", {}).get("content", "").strip()

#     # Replace markdown bold (`**text**`) with HTML `<strong>text</strong>`
#     ai_response = ai_response.replace("**", "<strong>")

#     # Replace asterisks (`* `) with HTML bullet points (`• `)
#     ai_response = ai_response.replace("* ", "• ")

#     # Replace newline characters with HTML `<br>` for proper line breaks
#     ai_response = ai_response.replace("\n", "<br>")

#     return {"response": ai_response}

def get_chat_history():
    cursor.execute("SELECT role, content FROM chat_history ORDER BY id")
    return [{"role": role, "content": content} for role, content in cursor.fetchall()]

@app.get("/reset")
def reset_chat():
    cursor.execute("DELETE FROM chat_history")
    conn.commit()
    return {"message": "MIMI's memory has been reset."}





# Go to backend CD with:  cd /Users/diana/Documents/parenting_app/backend
# Activate env with: 
# python3 -m venv venv 
# source venv/bin/activate 

# Run the server with: uvicorn app.main:app --reload




