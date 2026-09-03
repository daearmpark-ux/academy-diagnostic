"""Registry for selecting an age/grade and subject question set."""

from question_bank.middle.grade2_math import QUESTION_SET as M2_MATH_SET
from question_bank.placeholder import PLACEHOLDER_QUESTIONS
from question_bank.preschool.age5 import QUESTION_SET as P5_SET
from question_bank.preschool.age6 import QUESTION_SET as P6_SET
from question_bank.preschool.age7 import QUESTION_SET as P7_SET
from question_bank.preschool.guardian_checklist import QUESTION_SET as GUARDIAN_CHECKLIST
from question_bank.elementary.grade1_korean import QUESTION_SET as E1_KOR_SET
from question_bank.elementary.grade1_english import QUESTION_SET as E1_ENG_SET
from question_bank.elementary.grade1_math import QUESTION_SET as E1_MATH_SET
from question_bank.elementary.grade2_korean import QUESTION_SET as E2_KOR_SET
from question_bank.elementary.grade2_english import QUESTION_SET as E2_ENG_SET
from question_bank.elementary.grade2_math import QUESTION_SET as E2_MATH_SET
from question_bank.elementary.grade3_english import QUESTION_SET as E3_ENG_SET
from question_bank.elementary.grade3_math import QUESTION_SET as E3_MATH_SET
from question_bank.elementary.grade4_english import QUESTION_SET as E4_ENG_SET
from question_bank.elementary.grade4_math import QUESTION_SET as E4_MATH_SET
from question_bank.elementary.grade5_english import QUESTION_SET as E5_ENG_SET
from question_bank.elementary.grade5_math import QUESTION_SET as E5_MATH_SET
from question_bank.elementary.grade6_english import QUESTION_SET as E6_ENG_SET
from question_bank.elementary.grade6_math import QUESTION_SET as E6_MATH_SET
from question_bank.middle.grade1_english import QUESTION_SET as M1_ENG_SET
from question_bank.middle.grade1_math import QUESTION_SET as M1_MATH_SET
from question_bank.middle.grade2_english import QUESTION_SET as M2_ENG_SET
from question_bank.middle.grade3_english import QUESTION_SET as M3_ENG_SET
from question_bank.middle.grade3_math import QUESTION_SET as M3_MATH_SET


def normalize_question(question):
    """Return the small compatibility schema consumed by the app."""
    normalized = dict(question)
    normalized["text"] = normalized.get("text", normalized.get("question", normalized.get("stem", "")))
    normalized["choices"] = normalized.get("choices", normalized.get("options", []))
    normalized["answer"] = normalized.get(
        "answer",
        normalized.get("correct_answer", normalized.get("correct_option_text")),
    )
    normalized["recommended_sec"] = normalized.get(
        "recommended_sec", normalized.get("recommended_seconds", 0)
    )
    normalized["is_advance_probe"] = normalized.get("is_advance_probe", False)
    normalized["score_in_core"] = normalized.get(
        "score_in_core", not normalized["is_advance_probe"]
    )
    return normalized


QUESTION_SETS = {
    ("중2", "수학"): M2_MATH_SET,
    ("5세", "입학준비"): P5_SET,
    ("6세", "입학준비"): P6_SET,
    ("7세", "입학준비"): P7_SET,
    ("5세", None): P5_SET,
    ("6세", None): P6_SET,
    ("7세", None): P7_SET,
    ("초1", "국어"): E1_KOR_SET,
    ("초1", "영어"): E1_ENG_SET,
    ("초1", "수학"): E1_MATH_SET,
    ("초2", "국어"): E2_KOR_SET,
    ("초2", "영어"): E2_ENG_SET,
    ("초2", "수학"): E2_MATH_SET,
    ("초3", "영어"): E3_ENG_SET,
    ("초3", "수학"): E3_MATH_SET,
    ("초4", "영어"): E4_ENG_SET,
    ("초4", "수학"): E4_MATH_SET,
    ("초5", "영어"): E5_ENG_SET,
    ("초5", "수학"): E5_MATH_SET,
    ("초6", "영어"): E6_ENG_SET,
    ("초6", "수학"): E6_MATH_SET,
    ("중1", "영어"): M1_ENG_SET,
    ("중1", "수학"): M1_MATH_SET,
    ("중2", "영어"): M2_ENG_SET,
    ("중3", "영어"): M3_ENG_SET,
    ("중3", "수학"): M3_MATH_SET,
}


def validate_question_set(question_set):
    """Validate the common contract shared by every registered set."""
    questions = question_set.get("questions", [])
    if not questions:
        raise ValueError("문항 세트에 문항이 없습니다.")
    ids = [question.get("id") for question in questions]
    if any(not question_id for question_id in ids) or len(set(ids)) != len(ids):
        raise ValueError("문항 ID가 없거나 중복되었습니다.")
    for question in questions:
        if not question.get("text"):
            raise ValueError(f"문제 본문이 없습니다: {question['id']}")
        choices = question.get("choices", [])
        answer = question.get("answer")
        if not choices or answer not in choices:
            raise ValueError(f"선택지 또는 정답이 올바르지 않습니다: {question['id']}")
        if question.get("recommended_sec", 0) <= 0:
            raise ValueError(f"권장시간은 양수여야 합니다: {question['id']}")
    return True


def get_question_set(level, subject=None):
    """Return a registered set, or None when the set is not available yet."""
    question_set = QUESTION_SETS.get((level, subject))
    if question_set is None:
        return None
    normalized_set = {
        **question_set,
        "questions": [normalize_question(question) for question in question_set["questions"]],
    }
    validate_question_set(normalized_set)
    return normalized_set


def get_questions(level, subject=None):
    question_set = get_question_set(level, subject)
    if question_set is not None:
        return question_set["questions"]
    return PLACEHOLDER_QUESTIONS


def get_guardian_checklist():
    """Return the shared scoreless preschool checklist."""
    return {
        **GUARDIAN_CHECKLIST,
        "items": [dict(item) for item in GUARDIAN_CHECKLIST["items"]],
        "response_options": dict(GUARDIAN_CHECKLIST["response_options"]),
    }
