from typing import TypedDict


class AgentState(TypedDict, total=False):

    question: str

    video_id: str | None

    intent: str

    answer: str

    sources: list

    summary: str