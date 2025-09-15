# Step 1 - Install
pip install langchain langchain-openai

# Step 2 - Define Tools
from langchain.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b

@tool
def reverse_string(text: str) -> str:
    """Reverse a string."""
    return text[::-1]

tools = [multiply, reverse_string]


# Step 3 - Setup the LLM
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# Step 4 - Create the Agent
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_openai_functions_agent, AgentExecutor

# Prompt template for guidance
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use tools if needed."),
    ("human", "{input}")
])

# Create the agent with tools + prompt
agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)

# AgentExecutor handles reasoning & tool calls
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Step 5 - Run It
result = agent_executor.invoke({"input": "Reverse 'LangChain' and then multiply 5 * 9"})
print(result["output"])
