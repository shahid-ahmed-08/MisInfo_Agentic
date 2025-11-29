from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import (
    node_extract_claim,
    node_generate_queries,
    node_search,
    node_score_evidence,
    node_determine_verdict,
    node_check_reflect,
    node_reflect,
)


def build_agent_graph():
    """ 
    Graph flow:
    extract_claim -> generate_queries -> search -> score_evidence -> determine_verdict -> check_reflect
    if check_reflect sets last_action == 'reflect' -> reflect -> search -> score -> determine_verdict -> check_reflect...
    else -> END
    """
    graph = StateGraph(AgentState)

    graph.add_node("extract_claim", node_extract_claim)
    graph.add_node("generate_queries", node_generate_queries)
    graph.add_node("search", node_search)
    graph.add_node("score_evidence", node_score_evidence)
    graph.add_node("determine_verdict", node_determine_verdict)
    graph.add_node("check_reflect", node_check_reflect)
    graph.add_node("reflect", node_reflect)

    graph.set_entry_point("extract_claim")

    graph.add_edge("extract_claim", "generate_queries")
    graph.add_edge("generate_queries", "search")
    graph.add_edge("search", "score_evidence")
    graph.add_edge("score_evidence", "determine_verdict")
    graph.add_edge("determine_verdict", "check_reflect")

    # reflection loop: check_reflect -> reflect -> search
    graph.add_edge("check_reflect", "reflect")
    graph.add_edge("reflect", "search")

    # if no reflection, allow check_reflect -> END
    graph.add_edge("check_reflect", END)

    # after reflection loop, continue normal path (edges already create loops)
    graph.add_edge("determine_verdict", END)

    return graph.compile()
