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

    input_tokens: int
    output_tokens: int
    total_tokens: int

    response_time: float


class AgentLogger:

    @staticmethod
    def log_execution(
        query: str,
        agent: str,
        model: str,
        needs_search: bool,
        response_time: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        total_tokens: int = 0
    ) -> None:

        LOG_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        log_entry = AgentLog(
            timestamp=time.strftime(
                "%Y-%m-%dT%H:%M:%SZ",
                time.gmtime()
            ),

            query=query,
            agent=agent,
            model=model,
            needs_search=needs_search,

            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,

            response_time=round(
                response_time,
                2
            )
        )

        logs = []

        if LOG_FILE.exists():
            try:
                with open(LOG_FILE, "r") as f:
                    logs = json.load(f)
            except Exception:
                logs = []

        logs.append(asdict(log_entry))

        with open(LOG_FILE, "w") as f:
            json.dump(
                logs,
                f,
                indent=4
            )