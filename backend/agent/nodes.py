from .state import AgentState
from app.services.agent_service import extract_claim, generate_queries, score_sources, determine_verdict
from agent.mcp_client import mcp_search
import random


def node_extract_claim(state: AgentState) -> AgentState:
    state.claim = extract_claim(state.text)
    state.reasoning.append("Claim extracted.")
    return state


def node_generate_queries(state: AgentState) -> AgentState:
    state.queries = generate_queries(state.claim)
    state.reasoning.append("Queries generated.")
    return state


def node_search(state: AgentState) -> AgentState:
    """
    Perform MCP search for each query. Collect all results.
    THIS VERSION GUARANTEES THAT mcp_search() IS CALLED.
    """
    all_results = []
    queries = state.queries or []

    for q in queries:
        print("DEBUG: calling MCP search for query:", q)
        res = mcp_search(q)
        print("DEBUG: MCP returned:", res)
        if res:
            all_results.extend(res)

    state.sources = all_results
    state.reasoning.append(f"Searched {len(all_results)} sources via MCP.")
    return state


def node_score_evidence(state: AgentState) -> AgentState:
    scored = score_sources(state.sources or [], (state.claim or "").split()[:8])
    state.sources = scored
    state.reasoning.append(f"Scored {len(scored)} sources.")
    return state


def node_determine_verdict(state: AgentState) -> AgentState:
    verdict, confidence = determine_verdict(state.sources or [])
    state.verdict = verdict
    state.confidence = float(confidence or 0.0)
    state.reasoning.append(f"Determined verdict: {verdict} (conf={state.confidence:.2f}).")
    return state


# --- Reflection / Retry nodes ---


def _refine_query_variations(base: str) -> list:
    """
    Produce several refined query variants from a base claim.
    """
    # deterministic but varied refinements
    seeds = [
        f"{base} official statement",
        f"{base} statement from government",
        f"{base} fact check",
        f"{base} analysis",
        f"{base} reported by news",
        f"{base} Reuters",
        f"{base} BBC",
        f"{base} The Hindu",
        f"{base} clarification",
    ]
    # randomize order but keep deterministic by shuffle with seed from base
    r = random.Random(hash(base) & 0xFFFFFFFF)
    r.shuffle(seeds)
    return seeds


def node_check_reflect(state: AgentState) -> AgentState:
    """
    Decide whether to reflect and retry or finish.
    If confidence is below threshold and attempts < max_attempts  prepare to reflect.
    """
    # if no sources or low confidence, consider reflecting
    conf = state.confidence or 0.0
    if (not state.sources or len(state.sources) < 2) and state.attempts < state.max_attempts:
        state.reasoning.append("Reflection triggered: insufficient evidence.")
        state.last_action = "reflect"
    elif conf < state.confidence_target and state.attempts < state.max_attempts:
        state.reasoning.append(f"Reflection triggered: low confidence ({conf:.2f} < {state.confidence_target}).")
        state.last_action = "reflect"
    else:
        state.reasoning.append("No reflection needed; finishing.")
        state.last_action = "finish"
    return state


def node_reflect(state: AgentState) -> AgentState:
    """
    Produce refined queries and increment attempt counter.
    """
    state.attempts += 1
    base = state.claim or state.text
    refined = _refine_query_variations(base)
    # merge with existing queries but prefer refined first
    state.queries = refined + (state.queries or [])
    state.reasoning.append(f"Reflection pass {state.attempts}: generated {len(refined)} refined queries.")
    return state
