"""Generate traces.jsonl: simulated Langfuse traces, one per answer-quality case.

Run once; the output is committed. Each line is a trace as Langfuse exports it
(id, name, timestamp, input, output, metadata). The trace id is the case's
identity in qt-app. `output.answer` is the expected answer, `metadata.base_p` the
pass rate at full quality: about 60 % of cases always pass, 20 % almost always,
15 % are genuinely uncertain and 5 % (almost) always fail.
"""

import json
import random
from datetime import UTC, datetime, timedelta
from pathlib import Path

TOPICS = [
    "benefits", "deadlines", "documents", "eligibility", "fees",
    "forms", "housing", "income", "residence", "taxes",
]  # fmt: skip
PER_TOPIC = 20


def base_rate(rng: random.Random) -> float:
    r = rng.random()
    if r < 0.60:
        return 1.0
    if r < 0.80:
        return round(rng.uniform(0.95, 0.99), 2)
    if r < 0.95:
        return round(rng.uniform(0.05, 0.95), 2)
    return round(rng.uniform(0.0, 0.02), 2)


def main() -> None:
    rates = random.Random(20261106)  # the seed of qt-app's former cases.toml
    ids = random.Random(20261109)
    start = datetime(2026, 10, 1, tzinfo=UTC)
    lines = []
    for topic in TOPICS:
        for i in range(1, PER_TOPIC + 1):
            hrid = f"{topic}-{i:02d}"
            trace = {
                "id": f"{ids.getrandbits(128):032x}",
                "name": "answer",
                "timestamp": (start + timedelta(minutes=len(lines) * 7)).isoformat(),
                "input": {"question": f"Question {i} about {topic}?"},
                "output": {"answer": f"answer-{hrid}"},
                "metadata": {"topic": topic, "hrid": hrid, "base_p": base_rate(rates)},
            }
            lines.append(json.dumps(trace, sort_keys=True) + "\n")
    (Path(__file__).resolve().parents[1] / "traces.jsonl").write_text("".join(lines))


if __name__ == "__main__":
    main()
