import logging

from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI

from src.database import MessagesAdapter

from ..state import OverallState
from ..tools import create_update_plan_tool

logger = logging.getLogger("easeai")


def planner_node(state: OverallState, config: RunnableConfig) -> OverallState:
    # Initialize Gemini model
    gemini_llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
    )

    # Create custom prompt template for the agent
    presentation_plan = state.get("presentation_plan")
    plan_container = {"plan": presentation_plan}
    tools = [create_update_plan_tool(plan_container)]
    prompt = PromptTemplate(
        template="""You are EaseAI, an AI assistant helping users create presentations.

        You have access to the following tools:
        {tools}

        Your goal is to help users build and refine their presentation plan through conversation.
        Ask the user questions about their desired presentation to help build the presentation plan.
        Use the update_plan tool to create or update the presentation plan based on user input.

        # Response format
        Follow this exact format. Do not deviate from it.

        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the respose to the user after completing the necessary actions

        If you don't need to use a tool, still follow the format but skip Action/Action Input/Observation.

        IMPORTANT: You must include the relevant prefix in every response.
        'Final Answer:' must be included before your response to the user.

        # Current Presentation Plan:
        {current_plan}

        # Chat History:
        {chat_history}

        Question: {input}
        Thought: {agent_scratchpad}""",
        input_variables=[
            "input",
            "chat_history",
            "current_plan",
            "agent_scratchpad",
            "tools",
            "tool_names",
        ],
    )
    agent = create_react_agent(gemini_llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
    )

    # Execute agent
    user_input = state["messages"][-1].content
    chat_history = "\n".join(
        [f"{msg.type}: {msg.content}" for msg in state["messages"][:-1]]
    )
    plan_str = (
        presentation_plan.model_dump_json(indent=2)
        if presentation_plan
        else "No plan created yet"
    )
    result = agent_executor.invoke(
        {"input": user_input, "chat_history": chat_history, "current_plan": plan_str}
    )
    response = result["output"]

    # Save the response to the database
    project_id = config["configurable"]["project_id"]
    db_session = config["configurable"]["db_session"]
    MessagesAdapter(db_session).create_message(
        project_id=project_id,
        role="ai",
        content=response,
    )
    return {
        "messages": [AIMessage(content=response)],
        "presentation_plan": plan_container["plan"],
    }
