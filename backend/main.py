from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import Optional
import json
import ollama
import re

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class ChatMessage(BaseModel):
    message: str

chat_history = []

# English system prompt
SYSTEM_PROMPT_EN = """You are MIMI, an AI parenting assistant. You MUST ALWAYS respond in English, regardless of the input language.

### Main Answer
🎯 [Your direct answer in 1-2 sentences]

### Key Points
📝 [List 2-3 key points with proper spacing]
- [First point]
- [Second point]
- [Third point if needed]

### Action Steps
🔔 [Clear, numbered steps]
1. [First step]
2. [Second step]
3. [Third step if needed]

**Safety Note:** [Add safety reminder if relevant]

Remember: ALWAYS respond in English. Keep responses under 200 words."""

# Romanian system prompt
SYSTEM_PROMPT_RO = """Ești MIMI, un asistent virtual pentru părinți. TREBUIE să răspunzi ÎNTOTDEAUNA în limba română, indiferent de limba în care este pusă întrebarea.

### Răspuns Principal
🎯 Răspuns scurt și clar (1-2 propoziții)

### Puncte Cheie
📝 Enumeră 2-3 puncte cheie:
- Punct 1: Explicație scurtă
- Punct 2: Explicație scurtă
- Punct 3: Explicație scurtă (dacă este necesar)

### Pași de Urmat
🔔 Oferă pași clari:
1. Primul pas cu detalii scurte
2. Al doilea pas cu detalii scurte
3. Al treilea pas (dacă este necesar)

**Notă de Siguranță:** Dacă este relevant, adaugă un scurt memento despre siguranță.

Ține minte: Răspunde ÎNTOTDEAUNA în română. Păstrează răspunsurile sub 200 de cuvinte."""

def format_response(text: str) -> str:
    """Format the response for better readability"""
    # Add newlines before and after headers
    text = re.sub(r'(?<!\\n)###', '\n\n###', text)
    text = re.sub(r'###([^\n]+)', r'###\1\n', text)
    
    # Format bullet points
    text = re.sub(r'(?<!\\n)- ', '\n- ', text)
    
    # Format numbered lists
    text = re.sub(r'(?<!\\n)(\d+\.) ', r'\n\1 ', text)
    
    # Add spacing after sections
    text = re.sub(r'([.!?])(\s*)([A-Z])', r'\1\n\n\3', text)
    
    # Ensure proper spacing around bold text
    text = re.sub(r'(?<!\*)\*\*(?!\*)', ' **', text)
    text = re.sub(r'(?<!\*)\*\*(?!\*)', '** ', text)
    
    # Clean up multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Ensure proper spacing around emojis
    text = re.sub(r'([^\s])([🌟💡🎯🔔📝])', r'\1 \2', text)
    text = re.sub(r'([🌟💡🎯🔔📝])([^\s])', r'\1 \2', text)
    
    return text.strip()

@app.get("/")
async def root():
    return {"message": "MIMI AI Parenting Assistant API"}

@app.post("/chat")
async def chat(message: ChatMessage, accept_language: str = Header(default="en")):
    try:
        # Normalize language code
        language = "ro" if accept_language.lower().startswith("ro") else "en"
        
        # Select system prompt based on language
        system_prompt = SYSTEM_PROMPT_RO if language == "ro" else SYSTEM_PROMPT_EN
        
        # Format the conversation context
        conversation = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"Remember: You MUST respond in {'Romanian' if language == 'ro' else 'English'} ONLY."}
        ]
        
        # Add chat history for context
        for msg in chat_history[-4:]:
            conversation.append(msg)
            
        # Add the new user message
        conversation.append({"role": "user", "content": message.message})
        
        # Get response from Ollama
        response = ollama.chat(model='mistral', 
                             messages=[{"role": m["role"], "content": m["content"]} for m in conversation])
        
        # Format the response
        assistant_message = format_response(response['message']['content'])
        
        # Store both user message and response in chat history
        chat_history.append({"role": "user", "content": message.message})
        chat_history.append({"role": "assistant", "content": assistant_message})
        
        return {"response": assistant_message}
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reset")
async def reset_chat():
    chat_history.clear()
    return {"message": "Chat history has been reset."} 