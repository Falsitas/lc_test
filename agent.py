from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool

from dotenv import load_dotenv

load_dotenv()

class LangChainTest:
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite"
        )
        self.agent = create_agent(
            model=self.model,
            tools=[LangChainTest.pythonREPL, LangChainTest.runCommandOnShell],
            system_prompt="You are a helpful assistant"
        )

    def run_query(self, query: str) -> str:
        return self.agent.invoke({
            "messages": [{"role": "user", "content": query}]
        })
        
if __name__ == "__main__":
    agent = LangChainTest()
    query = "What is the capital of France?"
    response = agent.run_query(query)
    print(response)