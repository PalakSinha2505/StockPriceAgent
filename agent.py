import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools import get_stock_price, search_ticker

# Load environment variables from .env file
load_dotenv()

def create_stock_agent(model_name: str = "llama3-70b-8192", temperature: float = 0.0) -> AgentExecutor:
    """
    Initializes and returns the Stock Price Agent executor.
    
    Args:
        model_name: The name of the Groq LLM model to use (default: llama3-70b-8192)
        temperature: LLM temperature setting (default: 0.0)
        
    Returns:
        An instantiated AgentExecutor.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY environment variable is not set.\n"
            "Please create a '.env' file in the root of the project with 'GROQ_API_KEY=your_key_here'\n"
            "or set it directly in your shell environment."
        )
        
    # Initialize the LLM with Groq. ChatGroq automatically detects GROQ_API_KEY from environment,
    # but we pass it explicitly to be absolutely sure.
    llm = ChatGroq(
        model=model_name,
        temperature=temperature,
        api_key=api_key
    )
    
    # Bundle the tools the agent has access to
    tools = [search_ticker, get_stock_price]
    
    # Set up the chat prompt template
    prompt = ChatPromptTemplate.from_messages([
        (
            "system", 
            "You are a helpful and precise financial assistant specialized in retrieving stock and share prices.\n\n"
            "Guidelines:\n"
            "1. When asked about a company's share or stock price, if you do not know the exact ticker symbol, "
            "first call the `search_ticker` tool with the company name to find the correct symbol.\n"
            "2. Once you have the correct ticker symbol, retrieve the current price using the `get_stock_price` tool.\n"
            "3. Format your final answer clearly, stating the company name, ticker symbol, current price, currency, "
            "and daily performance percentage change if available.\n"
            "4. If a query is not related to stock prices or ticker searches, politely direct the user back to "
            "stock queries."
        ),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Construct the Tool Calling Agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # Create the Agent Executor
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, 
        handle_parsing_errors=True
    )
    
    return agent_executor
