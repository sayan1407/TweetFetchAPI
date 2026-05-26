from fastapi import FastAPI
import httpx
import os
from dotenv import load_dotenv
from urllib.parse import unquote
from pydantic import BaseModel
import json
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
#BEARER_TOKEN = BEARER_TOKEN.strip()


class Data(BaseModel):
    id: str
    name: str
    username: str

@app.get("/twitter/user/{username}")
async def get_user(username: str,start_time: str , end_time: str):
    try:
        url = f"https://api.x.com/2/users/by/username/{username}"

        headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }

        async with httpx.AsyncClient() as client:
           response = await client.get(url, headers=headers)
        if "data" not in response.json():
           return {"error": "User not found"}
        return_data = json.loads(json.dumps(response.json()["data"]))
        data = Data(**return_data)
        id = data.id
        url = f"https://api.x.com/2/users/{id}/tweets?max_results=5&start_time={start_time}&end_time={end_time}"
        async with httpx.AsyncClient() as client:
           response = await client.get(url, headers=headers)
    

        return response.json()
    except Exception as e:
        return {"error": str(e)}

    