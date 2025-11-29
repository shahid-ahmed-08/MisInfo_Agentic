from typing import List, Optional
from pydantic import BaseModel

class AgentState(BaseModel):
    text: str
    claim: Optional[str] = None
    queries: Optional[List[str]] = None
    sources: Optional[List[dict]] = None
    verdict: Optional[str] = None
    confidence: Optional[float] = None
    reasoning: Optional[List[str]] = []
    # reflection / loop control
    attempts: int = 0
    max_attempts: int = 3
    confidence_target: float = 0.60
    last_action: Optional[str] = None
