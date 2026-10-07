from typing import TypedDict,List,Literal
from pydantic import BaseModel,Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import SystemMessage,HumanMessage,AIMessage
from dotenv import load_dotenv
from typing import Annotated 
import operator 
load_dotenv()

class RoutingDecision(BaseModel):
    next_agent:List[Literal["rag","research","analysis","final"]]=Field(...,description="The next agent to route the query to. It can be one of 'rag', 'research', or 'analysis'.")



class State(TypedDict):
    user_request:str
    next_agent:List[str]
    rag_result:str
    research_result:list[dict]
    analysis_result:str
    result:str
    final_context:str
    steps:int
    sources:Annotated[list[str],operator.add]

base_llm=ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",temperature=0,max_retries=5)

llm=ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite",temperature=0,reasoning_effort="low",max_retries=5)

router=llm.with_structured_output(RoutingDecision,method="json_schema")
MAX_STEPS=5

def supervisor(state: State):

    user_request = state["user_request"]
    rag_result = state.get("rag_result", "")
    research_result = state.get("research_result", "")
    analysis = state.get("analysis_result", "")
    steps=state.get("steps",0) + 1


    if steps > MAX_STEPS:
            return {"next_agent":["final"],"steps":steps}


    decision = router.invoke(
        f"""
You are the supervisor of a multi-agent AI system.

Your job is to decide which agent should execute next.

if the user request was on mars or space chech rag first and if you havenot any result then check others

Available agents:

1. rag
Use the uploaded documents and internal knowledge base. its about space and mars and this things only

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
        ,"steps":steps
    }


def route_next_agent(state: State) -> str:
    return state["next_agent"]




