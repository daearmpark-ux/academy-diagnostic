"""Shared schema builder and canonical validation for elementary sets."""


def make_question(qid, level, subject, area, skill, text, options, correct_number,
                  seconds, solution, diagnostic_if_wrong, advance=False):
    correct_text = options[correct_number - 1]
    return {
        "id": qid, "level": level, "subject": subject, "text": text,
        "question": text, "choices": options, "options": options,
        "answer": correct_text, "correct_option_number": correct_number,
        "correct_option_text": correct_text, "recommended_sec": seconds,
        "recommended_seconds": seconds, "official_domain": area, "unit": skill,
        "skill": skill, "solution": solution,
        "diagnostic_if_wrong": diagnostic_if_wrong, "area": area,
        "is_advance_probe": advance, "score_in_core": not advance,
    }


def validate_elementary_questions(questions, answer_key, core_seconds, advance_seconds):
    required = {"id", "level", "subject", "text", "choices", "correct_option_number",
                "correct_option_text", "recommended_seconds", "official_domain",
                "unit", "skill", "solution", "diagnostic_if_wrong",
                "is_advance_probe", "score_in_core"}
    if len(questions) != 15 or len({q["id"] for q in questions}) != 15:
        raise ValueError("초등 문항은 고유 ID를 가진 정확히 15개여야 합니다.")
    if sum(q["score_in_core"] for q in questions) != 13:
        raise ValueError("CORE 문항은 정확히 13개여야 합니다.")
    if sum(q["is_advance_probe"] for q in questions) != 2:
        raise ValueError("ADVANCE 문항은 정확히 2개여야 합니다.")
    if [q["is_advance_probe"] for q in questions] != [False] * 13 + [True] * 2:
        raise ValueError("ADVANCE 문항은 Q14와 Q15만이어야 합니다.")
    for q in questions:
        if not required.issubset(q):
            raise ValueError(f"필수 metadata가 없습니다: {q['id']}")
        if len(q["choices"]) != 5 or len(set(q["choices"])) != 5:
            raise ValueError(f"선택지는 중복 없이 5개여야 합니다: {q['id']}")
        number = q["correct_option_number"]
        if number not in range(1, 6) or q["choices"][number - 1] != q["correct_option_text"]:
            raise ValueError(f"정답 번호와 정답 문구가 다릅니다: {q['id']}")
        if q["recommended_seconds"] <= 0 or q["score_in_core"] == q["is_advance_probe"]:
            raise ValueError(f"문항 metadata가 올바르지 않습니다: {q['id']}")
    if [q["correct_option_number"] for q in questions] != answer_key:
        raise ValueError("canonical answer key가 다릅니다.")
    if sum(q["recommended_seconds"] for q in questions[:13]) != core_seconds:
        raise ValueError("CORE 권장시간이 다릅니다.")
    if sum(q["recommended_seconds"] for q in questions[13:]) != advance_seconds:
        raise ValueError("ADVANCE 권장시간이 다릅니다.")
    return True
