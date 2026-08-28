"""Shared builders and validation for preschool readiness sets."""


def make_question(qid, domain, skill, question, options, correct_number,
                  correct_text, solution, diagnostic_if_wrong, seconds,
                  is_advance_probe=False):
    return {
        "id": qid,
        "text": question,
        "choices": options,
        "answer": correct_text,
        "correct_option_number": correct_number,
        "correct_option_text": correct_text,
        "recommended_sec": seconds,
        "recommended_seconds": seconds,
        "domain": domain,
        "area": domain,
        "skill": skill,
        "solution": solution,
        "diagnostic_if_wrong": diagnostic_if_wrong,
        "is_advance_probe": is_advance_probe,
        "score_in_core": not is_advance_probe,
    }


def validate_preschool_questions(questions, answer_key, recommended_seconds,
                                 core_seconds, advance_seconds):
    required = {
        "id", "text", "choices", "answer", "correct_option_number",
        "correct_option_text", "recommended_seconds", "domain", "area",
        "skill", "solution", "diagnostic_if_wrong", "is_advance_probe",
        "score_in_core",
    }
    if len(questions) != 15:
        raise ValueError("유아 문항은 정확히 15개여야 합니다.")
    if len({question["id"] for question in questions}) != 15:
        raise ValueError("유아 문항 ID가 중복되었습니다.")
    if sum(question["score_in_core"] for question in questions) != 13:
        raise ValueError("CORE 문항은 정확히 13개여야 합니다.")
    if sum(question["is_advance_probe"] for question in questions) != 2:
        raise ValueError("ADVANCE_PROBE 문항은 정확히 2개여야 합니다.")
    if [question["is_advance_probe"] for question in questions] != [False] * 13 + [True, True]:
        raise ValueError("ADVANCE_PROBE는 Q14와 Q15만이어야 합니다.")
    for question in questions:
        if not required.issubset(question):
            raise ValueError(f"필수 metadata가 없는 문항: {question['id']}")
        if len(question["choices"]) != 5 or len(set(question["choices"])) != 5:
            raise ValueError(f"선택지는 중복 없이 5개여야 합니다: {question['id']}")
        number = question["correct_option_number"]
        if number not in range(1, 6):
            raise ValueError(f"정답 번호가 범위를 벗어났습니다: {question['id']}")
        if question["choices"][number - 1] != question["correct_option_text"]:
            raise ValueError(f"정답 번호와 정답 문자열이 다릅니다: {question['id']}")
        if question["recommended_seconds"] <= 0:
            raise ValueError(f"권장시간은 양수여야 합니다: {question['id']}")
        if question["score_in_core"] == question["is_advance_probe"]:
            raise ValueError(f"CORE/ADVANCE 구분이 충돌합니다: {question['id']}")
    if [question["correct_option_number"] for question in questions] != answer_key:
        raise ValueError("유아 정답키가 canonical 정답키와 다릅니다.")
    if [question["recommended_seconds"] for question in questions] != recommended_seconds:
        raise ValueError("유아 권장시간 배열이 canonical 값과 다릅니다.")
    if sum(recommended_seconds) != core_seconds + advance_seconds:
        raise ValueError("유아 전체 권장시간이 CORE+ADVANCE와 다릅니다.")
    if sum(recommended_seconds[:13]) != core_seconds:
        raise ValueError("유아 CORE 권장시간이 canonical 값과 다릅니다.")
    if sum(recommended_seconds[13:]) != advance_seconds:
        raise ValueError("유아 ADVANCE 권장시간이 canonical 값과 다릅니다.")
    return True
