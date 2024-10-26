from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

load_dotenv()

app = FastAPI()
# llm = ChatOpenAI(model="gpt-4o-mini")

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

