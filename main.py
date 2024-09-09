from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Allow CORS (for frontend to communicate with backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request validation
class CodeRequest(BaseModel):
    prompt: str
    language: str
    api_key_type: str = "default"  # Optional: 'default' or specific key name (e.g., "key1")

# Function to get the appropriate API key based on user input or default
def get_openai_api_key(api_key_type: str):
    # Default to the key in the .env file or choose specific key
    if api_key_type == "key1":
        return os.getenv("OPENAI_API_KEY_1")
    elif api_key_type == "key2":
        return os.getenv("OPENAI_API_KEY_2")
    elif api_key_type == "key3":
        return os.getenv("OPENAI_API_KEY_3")
    else:
        # Use default key
        default_key = os.getenv("DEFAULT_KEY")
        return os.getenv(default_key)

# Function to generate code using OpenAI Codex
def generate_code(prompt, language, api_key):
    # Set the API key
    openai.api_key = api_key
    
    # Language specific prompt adjustments if needed
    code_prompt = f"### Generate {language} code:\n\n{prompt}"
    
    response = openai.Completion.create(
        engine="code-davinci-002",  # Codex engine
        prompt=code_prompt,
        max_tokens=150,  # Adjust max tokens as necessary
        temperature=0,  # Lower temperature for more deterministic output
        top_p=1,
        n=1,
        stop=None
    )
    
    return response.choices[0].text.strip()

# Route to handle POST requests for code generation
@app.post("/generate")
async def generate_code_endpoint(request: CodeRequest):
    # Fetch the correct API key based on user input or default
    api_key = get_openai_api_key(request.api_key_type)
    
    if not api_key:
        raise HTTPException(status_code=400, detail="Invalid or missing API key.")
    
    # Generate the code using OpenAI Codex
    code_output = generate_code(request.prompt, request.language, api_key)
    return {"response": code_output}

# Basic route for health check
@app.get("/")
def read_root():
    return {"message": "Code Generation API is running"}
