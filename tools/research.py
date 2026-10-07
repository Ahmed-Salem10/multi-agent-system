from langchain_core.tools import tool 
from langchain_tavily import TavilySearch


tavily=TavilySearch()
@tool
def research_tool(query:str)->str:
    """search web for relevant information """
    try:
        raw=tavily.invoke(query)
        trimmed=[{"title":r.get("title",""),
                  "url":r.get("url",""),
                  "content":r.get("content","")}
                    for r in raw.get("results",[])]
        return trimmed
    except Exception as e:
        return f"Error occurred during Tavily search: {str(e)}"
    