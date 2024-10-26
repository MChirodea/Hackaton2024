from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langchain_openai import ChatOpenAI
import json
import uvicorn

load_dotenv()

app = FastAPI()
@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}

@app.put("/send-ext-data")
async def send_data(jsonstring):
    data = json.load(jsonstring)

    # for k, v in data.items():
    #     print(k, v)
    return {"message": data}

def send_data_to_openai(data):
    llm = ChatOpenAI(model="gpt-4o-mini")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
