from agent.graph import build_agent_graph
from agent.state import AgentState
import json


def test():
    agent = build_agent_graph()
    input_state = AgentState(text="India-China tensions over Arunachal Pradesh")
    result = agent.invoke(input_state)

    print("\n--- AGENT OUTPUT ---")
    print("Claim:", result.get("claim"))
    print("Queries (top 6):", json.dumps((result.get("queries") or [])[:6], indent=2))
    print("Sources (count):", len(result.get("sources") or []))
    print("Verdict:", result.get("verdict"))
    print("Confidence:", result.get("confidence"))
    print("Attempts:", result.get("attempts"))
    print("Reasoning:", json.dumps(result.get("reasoning"), indent=2))


if __name__ == "__main__":
    test()
