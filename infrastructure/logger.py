import json
import time
from pathlib import Path
from dataclasses import dataclass, asdict

LOG_FILE = Path("logs/agent_logs.json")

@dataclass
class AgentLog:
    timestamp: str
    query: str
    agent: str
    model: str
    needs_search: bool
    response_time: float

class AgentLogger:
    @staticmethod
    def log_execution(query: str, agent: str, model: str, needs_search: bool, response_time: float) -> None:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        log_entry = AgentLog(
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            query=query,
            agent=agent,
            model=model,
            needs_search=needs_search,
            response_time=round(response_time, 2)
        )
        
        logs = []
        if LOG_FILE.exists():
            try:
                with open(LOG_FILE, "r") as f:
                    logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
                
        logs.append(asdict(log_entry))
        
        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)