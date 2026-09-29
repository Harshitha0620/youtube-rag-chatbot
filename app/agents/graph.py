from langgraph.graph import (
    StateGraph,
    START,
    END
)

from app.agents.state import (
    AgentState
)

from app.agents.nodes import (
    classify_query,
    chat_node,
    summary_node,
    route_intent
)


def build_graph():

    graph_builder = StateGraph(
        AgentState
    )

    graph_builder.add_node(
        "classify",
        classify_query
    )

    graph_builder.add_node(
        "chat",
        chat_node
    )

    graph_builder.add_node(
        "summary",
        summary_node
    )

    graph_builder.add_edge(
        START,
        "classify"
    )

    graph_builder.add_conditional_edges(
        "classify",
        route_intent,
        {
            "chat": "chat",
            "summary": "summary"
        }
    )

    graph_builder.add_edge(
        "chat",
        END
    )

    graph_builder.add_edge(
        "summary",
        END
    )

    return graph_builder.compile()


agent_graph = build_graph()


def run_agent(
    question: str,
    video_id: str | None = None
):

    result = agent_graph.invoke(
        {
            "question": question,
            "video_id": video_id
        }
    )

    return {
        "answer": result.get(
            "answer",
            ""
        ),
        "sources": result.get(
            "sources",
            []
        )
    }