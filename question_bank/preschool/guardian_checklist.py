"""Scoreless guardian observation checklist shared by preschool ages 5-7."""

TEST_VERSION = "PRESCHOOL_GUARDIAN_CHECK_2026_v1.0"
ASSESSMENT_MODE = "guardian_checklist"
OBSERVER = "guardian"
RESPONSE_OPTIONS = {
    "often": "자주 보입니다",
    "sometimes": "가끔 보입니다",
    "not_yet_often": "아직 자주 보이지 않습니다",
    "not_observed": "관찰하기 어렵습니다",
}


def _item(item_id, domain, statement, display_summary):
    return {
        "id": item_id,
        "item_id": item_id,
        "domain": domain,
        "statement": statement,
        "display_summary": display_summary,
    }


ITEMS = [
    _item("GC-01", "생활·자기조절", "익숙한 일상 순서(외출 준비, 식사, 정리 등)를 안내받으면 스스로 해보려는 모습을 보입니다.", "일상 순서를 안내받으면 스스로 해보려 합니다."),
    _item("GC-02", "생활·자기조절", "차례를 기다리거나 하고 싶은 것을 잠시 기다려야 할 때, 안내를 받아 기다리려는 모습을 보입니다.", "안내를 받으면 차례나 순서를 기다리려 합니다."),
    _item("GC-03", "생활·자기조절", "새로운 장소나 익숙하지 않은 활동에서도 보호자나 성인의 안내를 받으면 참여를 시작하는 편입니다.", "새로운 장소나 활동에서도 안내를 받으면 참여를 시작합니다."),
    _item("GC-04", "의사소통·이해", "자신이 원하는 것, 불편한 것, 기분이나 생각을 말이나 몸짓으로 표현합니다.", "원하는 것과 기분을 자신의 방식으로 표현합니다."),
    _item("GC-05", "의사소통·이해", "일상에서 간단한 설명이나 부탁을 들으면 무엇을 해야 하는지 이해하고 행동하려는 모습을 보입니다.", "간단한 설명이나 부탁을 이해하고 행동하려 합니다."),
    _item("GC-06", "의사소통·이해", "하루 동안 있었던 일이나 기억에 남는 일을 자신의 방식으로 이야기하려고 합니다.", "경험한 일을 자신의 방식으로 이야기하려 합니다."),
    _item("GC-07", "관계·적응", "또래와 함께 놀 때 차례를 지키거나 함께 정한 약속을 따르려는 모습을 보입니다.", "또래 놀이에서 차례와 약속을 따르려 합니다."),
    _item("GC-08", "관계·적응", "친구와의 갈등이나 어려움이 생겼을 때 말로 표현하거나 성인에게 도움을 요청하려는 모습을 보입니다.", "갈등이나 어려움이 생기면 표현하거나 도움을 요청합니다."),
    _item("GC-09", "관계·적응", "다른 사람의 표정이나 기분 변화를 알아차리고 반응하는 모습을 보입니다.", "다른 사람의 표정이나 기분 변화에 반응합니다."),
    _item("GC-10", "놀이·표현", "자신이 관심 있는 놀이·그림책·만들기 등의 활동을 스스로 선택하고 한동안 이어가는 편입니다.", "관심 있는 활동을 스스로 선택하고 이어갑니다."),
    _item("GC-11", "놀이·표현", "그림, 만들기, 역할놀이, 몸짓 등 여러 방법으로 자신의 생각이나 경험을 표현하는 것을 즐깁니다.", "여러 방법으로 생각이나 경험을 표현합니다."),
    _item("GC-12", "놀이·표현", "처음 접하는 놀이나 활동도 부담이 크지 않다면 한 번 시도해보려는 모습을 보입니다.", "새로운 놀이와 활동을 한 번 시도해보려 합니다."),
    _item("GC-13", "호기심·탐구", "주변의 사물이나 현상에 궁금증을 보이며 '왜?', '어떻게?'와 같은 질문을 하는 편입니다.", "주변의 사물과 현상에 궁금증을 보입니다."),
    _item("GC-14", "호기심·탐구", "놀이와 생활 속에서 많고 적음, 길고 짧음, 순서, 반복되는 모양이나 규칙 등에 관심을 보입니다.", "생활 속 수량·비교·순서·규칙에 관심을 보입니다."),
    _item("GC-15", "호기심·탐구", "간판, 자기 이름, 그림책, 숫자 표시 등 생활 속 글자와 숫자에 관심을 보이거나 그 의미를 묻는 편입니다.", "생활 속 글자와 숫자 표시의 의미에 관심을 보입니다."),
]

QUESTION_SET = {
    "test_version": TEST_VERSION,
    "assessment_mode": ASSESSMENT_MODE,
    "observer": OBSERVER,
    "items": ITEMS,
    "response_options": RESPONSE_OPTIONS,
}


def validate_checklist():
    if len(ITEMS) != 15 or [item["item_id"] for item in ITEMS] != [f"GC-{index:02d}" for index in range(1, 16)]:
        raise ValueError("guardian checklist는 GC-01부터 GC-15까지 15개여야 합니다.")
    if len({item["domain"] for item in ITEMS}) != 5 or any(sum(item["domain"] == domain for item in ITEMS) != 3 for domain in {item["domain"] for item in ITEMS}):
        raise ValueError("guardian checklist는 5개 domain에 각 3개 항목이어야 합니다.")
    if set(RESPONSE_OPTIONS) != {"often", "sometimes", "not_yet_often", "not_observed"}:
        raise ValueError("guardian response option이 올바르지 않습니다.")
    return True


validate_checklist()