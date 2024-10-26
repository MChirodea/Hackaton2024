from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

load_dotenv()

app = FastAPI()
# llm = ChatOpenAI(model="gpt-4o-mini")

@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
