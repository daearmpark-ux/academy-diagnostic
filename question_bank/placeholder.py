"""Temporary fallback questions for sets not yet available."""

PLACEHOLDER_QUESTIONS = [
    {
        "id": "DEMO-01",
        "text": "다음 중 알맞은 답을 골라주세요.",
        "choices": [
            "① 첫 번째 보기", "② 두 번째 보기", "③ 세 번째 보기",
            "④ 네 번째 보기", "⑤ 다섯 번째 보기",
        ],
        "answer": "② 두 번째 보기",
        "area": "기초 개념",
        "recommended_sec": 30,
    },
    {
        "id": "DEMO-02",
        "text": "문제를 읽고 가장 알맞은 답을 선택해주세요.",
        "choices": [
            "① 선택지 A", "② 선택지 B", "③ 선택지 C",
            "④ 선택지 D", "⑤ 선택지 E",
        ],
        "answer": "③ 선택지 C",
        "area": "개념 활용",
        "recommended_sec": 35,
    },
    {
        "id": "DEMO-03",
        "text": "다음 보기 중 조건에 맞는 것을 골라주세요.",
        "choices": [
            "① 보기 1", "② 보기 2", "③ 보기 3",
            "④ 보기 4", "⑤ 보기 5",
        ],
        "answer": "④ 보기 4",
        "area": "문제 해결",
        "recommended_sec": 40,
    },
]
