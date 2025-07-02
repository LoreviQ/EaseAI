import logging
from typing import Optional

from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from src.database import MessagesAdapter
from src.types import PresentationPlan

from ..state import OverallState

logger = logging.getLogger("easeai")


def create_set_plan_tool(state: OverallState):
    @tool
    def set_plan(
        title: str,
        objective: Optional[str] = None,
        target_audience: Optional[str] = None,
        tone: Optional[str] = None,
        duration: Optional[str] = None,
        research_summary: Optional[str] = None,
    ) -> str:
        """Sets or updates the presentation plan with the provided details.

        Args:
            title: The title of the presentation. Create a relevant title if the user doesn't provide one (required)
            objective: The main objective or goal of the presentation
            target_audience: Who the presentation is intended for
            tone: The desired tone (e.g., formal, casual, humorous)
            duration: How long the presentation should be
            research_summary: Summary of research findings
        """
        try:
            plan = PresentationPlan(
                title=title,
                objective=objective,
                target_audience=target_audience,
                tone=tone,
                duration=duration,
                research_summary=research_summary,
            )
            state["presentation_plan"] = plan
            logger.info(f"Plan updated: {plan.title}")
            return f"Presentation plan updated successfully: {plan.title}"
        except Exception as e:
            logger.error(f"Error updating plan: {e}")
            return f"Error updating plan: {str(e)}"

    return set_plan


def chat_node(state: OverallState, config: RunnableConfig) -> OverallState:
    # Initialize Gemini model
    gemini_llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
    )

    # Create custom prompt template for the agent
    set_plan_tool = create_set_plan_tool(state)
    tools = [set_plan_tool]
    prompt = PromptTemplate(
        template="""You are EaseAI, an AI assistant helping users create presentations.

        You have access to the following tools:
        {tools}

        Your goal is to help users build and refine their presentation plan through conversation.
        Ask the user questions about their desired presentation to help build the presentation plan.
        Use the set_plan tool to create or update the presentation plan based on user input.

        IMPORTANT: You must ALWAYS follow this exact format. Do not deviate from it:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the respose to the user after completing the necessary actions

        If you don't need to use a tool, still follow the format but skip Action/Action Input/Observation.

        # Current Presentation Plan:
        {current_plan}

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
            "current_plan",
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
    current_plan = state.get("presentation_plan")
    plan_str = (
        current_plan.model_dump_json(indent=2)
        if current_plan
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
    return {"messages": [AIMessage(content=response)]}
