from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import FileResponse
from agent import LangChainTest

# uvicorn main:app --reload

app = FastAPI()
agent = LangChainTest()

class QueryRequest(BaseModel):
    query: str

@app.get("/")
async def root():
    return FileResponse("index.html")

@app.post("/chat")
async def run_chat(request: QueryRequest):
    response = agent.run_query(request.query)
    # print(response)
    # print("----")
    # print(response["messages"][1].content)
    return {"response": response["messages"][1].content}
