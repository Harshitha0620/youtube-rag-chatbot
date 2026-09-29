from app.agents.state import AgentState

from app.llm.ollama_llm import (
    get_llm
)

from app.rag.rag_service import (
    answer_question,
    generate_video_summary
)


def classify_query(
    state: AgentState
) -> AgentState:

    question = state["question"]

    prompt = f"""
Classify the following user query.

Return exactly one value:

CHAT
SUMMARY

Query:
{question}
"""

    response = get_llm().invoke(
        prompt
    )

    intent = response.content.strip().upper()

    if "SUMMARY" in intent:
        intent = "SUMMARY"
    else:
        intent = "CHAT"

    return {
        **state,
        "intent": intent
    }


def chat_node(
    state: AgentState
) -> AgentState:

    result = answer_question(
        question=state["question"],
        video_id=state.get(
            "video_id"
        )
    )

    return {
        **state,
        "answer": result["answer"],
        "sources": result["sources"]
    }


def summary_node(
    state: AgentState
) -> AgentState:

    summary = generate_video_summary(
        state["video_id"]
    )

    return {
        **state,
        "answer": summary,
        "summary": summary,
        "sources": []
    }


def route_intent(
    state: AgentState
):

    if state.get("intent") == "SUMMARY":
        return "summary"

    return "chat"