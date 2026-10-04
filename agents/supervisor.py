from typing import TypedDict,List,Literal
from pydantic import BaseModel,Field
from langchain_groq import ChatGroq
from langchain.messages import SystemMessage,HumanMessage,AIMessage
from dotenv import load_dotenv

load_dotenv()

class RoutingDecision(BaseModel):
    next_agent:List[Literal["rag","research","analysis","final"]]=Field(...,description="The next agent to route the query to. It can be one of 'rag', 'research', or 'analysis'.")



class State(TypedDict):
    user_request:str
    next_agent:str
    rag_result:str
    research_result:str
    analysis_result:str
    result:str
    final_context:str


base_llm=ChatGroq(
    model="openai/gpt-oss-120b",temperature=0)

router=base_llm.with_structured_output(RoutingDecision)

def supervisor(state: State):

    user_request = state["user_request"]
    rag_result = state["rag_result"]
    research_result = state["research_result"]
    analysis = state["analysis_result"]

    decision = router.invoke(
        f"""
You are the supervisor of a multi-agent AI system.

Your job is to decide which agent should execute next.

Available agents:

1. rag
Use the uploaded documents and internal knowledge base.

2. research
Search the internet when external or up-to-date information is required.

3. analysis
Analyze the information collected by the RAG and research agents.

4. final
Generate the final answer when enough information has been collected.

User request:
{user_request}

RAG result:
{rag_result}

Research result:
{research_result}

Analysis:
{analysis}

Choose ONLY the next agent.
"""
    )

    return {
        "next_agent": decision.next_agent
    }


def route_next_agent(state: State) -> str:
    return state["next_agent"]




