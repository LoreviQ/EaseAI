import logging

from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from src.database import MessagesAdapter

from ..state import OverallState

logger = logging.getLogger("easeai")


@tool
def create_presentation_tool(topic: str) -> str:
    """Creates a presentation for the user on the given topic."""
    logger.info(f"create_presentation_tool called with topic: {topic}")
    return f"Presentation created successfully for topic: {topic}"


def chat_node(state: OverallState, config: RunnableConfig) -> OverallState:
    # Initialize Gemini model
    gemini_llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
    )

    # Create custom prompt template for the agent
    tools = [create_presentation_tool]
    prompt = PromptTemplate(
        template="""You are EaseAI, an AI assistant helping users create presentations.

        You have access to the following tools:
        {tools}

        IMPORTANT: You must ALWAYS follow this exact format. Do not deviate from it:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question

        If you don't need to use a tool, still follow the format but skip 
        Action/Action Input/Observation.

        # Chat History:
        {chat_history}

        Question: {input}
        Thought: {agent_scratchpad}""",
        input_variables=[
            "chat_history",
            "input",
            "agent_scratchpad",
            "tools",
            "tool_names",
        ],
    )
    agent = create_react_agent(gemini_llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
    )

    # Execute agent with full message history
    user_input = state["messages"][-1].content
    chat_history = "\n".join(
        [f"{msg.type}: {msg.content}" for msg in state["messages"][:-1]]
    )
    result = agent_executor.invoke({"input": user_input, "chat_history": chat_history})
    response = result["output"]

    # Save the response to the database
    project_id = config["configurable"]["project_id"]
    db_session = config["configurable"]["db_session"]
    MessagesAdapter(db_session).create_message(
        project_id=project_id,
        role="ai",
        content=response,
    )
    return {"messages": [AIMessage(content=response)]}
