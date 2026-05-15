from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware, AgentState, wrap_model_call, ModelRequest, ModelResponse
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from typing import Callable

from dotenv import load_dotenv

from apps.users.permission import is_aplha
from security.context import security_context

load_dotenv()

@wrap_model_call
def attribute_based_tool(request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
    """Select tools based on user attributes."""
    print("Middleware invoked")
    ctx = security_context.get()
    user = ctx.get("user")
    ip = ctx.get("ip")
    time = ctx.get("time")
    state = request.state

    print(f"User: {user}")
    print(f"IP: {ip}")
    print(f"Time: {time}")

    if not user.groups.filter(name='ALPHA').exists() or ip != "127.0.0.1" or time.hour < 9 or time.hour > 15:
        print("tool access denied")
        request = request.override(tools=[])
    else:        print("tool access granted")

    return handler(request)

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
            self.agent = create_agent(
                model=self.model,
                tools=tools,
                system_prompt="You are a helpful assistant",
                middleware=[attribute_based_tool]
            )
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