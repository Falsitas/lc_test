from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool

from dotenv import load_dotenv

from apps.users.permission import is_aplha

load_dotenv()

class LangChainTest:
    def __init__(self, group):
        '''@param group: user groups to use for the model
            -"ALPHA": Can access tools
            -"BETA": Cannot access tools, default group
        '''
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite"
        )
        if group == "ALPHA":
            tools = [LangChainTest.pythonREPL, LangChainTest.runCommandOnShell]
        else:
            tools = []

        self.agent = create_agent(
            model=self.model,
            tools=tools,
            system_prompt="You are a helpful assistant"
        )

    def run_query(self, query: str) -> str:
        return self.agent.invoke({
            "messages": [{"role": "user", "content": query}]
        })
    
    # tools
    @tool
    def pythonREPL(code: str) -> str:
        """Execute Python code and return the output."""
        try:
            # Create a local namespace for executing the code
            local_namespace = {}
            exec(code, {}, local_namespace)
            return str(local_namespace.get("result", "No result variable found."))
        except Exception as e:
            return f"Error executing code: {e}"
        
    @tool
    def runCommandOnShell(command: str) -> str:
        """Execute a shell command and return the output."""
        import subprocess
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.stdout.decode('utf-8')
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e.stderr.decode('utf-8')}"

if __name__ == "__main__":
    agent = LangChainTest()
    query = "What is the capital of France?"
    response = agent.run_query(query)
    print(response)