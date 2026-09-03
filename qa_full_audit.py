"""Full regression audit for all registered diagnostic question sets."""

from diagnostic_engine import calculate_result, time_difference_text
from question_registry import QUESTION_SETS, get_question_set, get_questions
from question_bank.middle.grade2_math import M2_MATH_ANSWER_KEY
from organization_registry import ORGANIZATIONS, filter_records, validate_organizations
from question_bank.preschool.guardian_checklist import ITEMS, RESPONSE_OPTIONS, TEST_VERSION

EXPECTED = {
    ("5세", "입학준비"), ("6세", "입학준비"), ("7세", "입학준비"),
    ("초1", "국어"), ("초1", "영어"), ("초1", "수학"),
    ("초2", "국어"), ("초2", "영어"), ("초2", "수학"),
    ("초3", "영어"), ("초3", "수학"),
    ("초4", "영어"), ("초4", "수학"), ("초5", "영어"),
    ("초5", "수학"), ("초6", "영어"), ("초6", "수학"),
    ("중1", "영어"), ("중1", "수학"), ("중2", "영어"),
    ("중2", "수학"), ("중3", "영어"), ("중3", "수학"),
}


def audit_sets():
    assert EXPECTED.issubset(QUESTION_SETS)
    assert all(get_question_set(level, None) for level in ("5세", "6세", "7세"))
    all_ids = []
    for pair in sorted(EXPECTED):
        question_set = get_question_set(*pair)
        questions = question_set["questions"]
        assert len(questions) == 15
        assert question_set["core_count"] == 13
        assert question_set["advance_count"] == 2
        assert [q["is_advance_probe"] for q in questions] == [False] * 13 + [True] * 2
        assert [q["score_in_core"] for q in questions] == [True] * 13 + [False] * 2
        for question in questions:
            required = {"id", "text", "choices", "answer",
                        "correct_option_number", "correct_option_text",
                        "recommended_seconds", "skill",
                        "solution", "diagnostic_if_wrong", "is_advance_probe",
                        "score_in_core"}
            assert required.issubset(question), question["id"]
            if "options" in question:
                assert question["choices"] == question["options"]
            assert len(question["choices"]) == 5
            assert len(set(question["choices"])) == 5
            number = question["correct_option_number"]
            assert number in range(1, 6)
            assert question["choices"][number - 1] == question["correct_option_text"]
            assert question["answer"] == question["correct_option_text"]
            assert question["recommended_seconds"] > 0
            assert question["solution"] and question["diagnostic_if_wrong"]
            assert question.get("level", pair[0]) == pair[0]
            assert question.get("subject", pair[1]) == pair[1]
            assert question.get("official_domain", question.get("domain", question.get("area")))
        all_ids.extend(q["id"] for q in questions)
    assert len(all_ids) == 345
    assert len(set(all_ids)) == 345


def audit_scoring():
    for pair in sorted(EXPECTED):
        questions = get_question_set(*pair)["questions"]
        answers = {i: q["answer"] for i, q in enumerate(questions, 1)}
        wrong = {i: next(x for x in q["choices"] if x != q["answer"])
                 for i, q in enumerate(questions, 1)}
        cases = [
            (answers, (13, 2, 0)),
            ({**{i: answers[i] for i in range(1, 14)}, 14: wrong[14], 15: wrong[15]}, (13, 0, 0)),
            ({**{i: wrong[i] for i in range(1, 14)}, 14: answers[14], 15: answers[15]}, (0, 2, 0)),
            ({i: "__PASS__" for i in range(1, 16)}, (0, 0, 13)),
            ({**{i: wrong[i] for i in range(1, 14)}, 14: answers[14], 15: wrong[15]}, (0, 1, 0)),
            ({**{i: wrong[i] for i in range(1, 14)}, 14: wrong[14], 15: answers[15]}, (0, 1, 0)),
        ]
        for case_answers, expected in cases:
            result = calculate_result(questions, case_answers, {i: 7 for i in range(1, 16)},
                                      is_m2_math=pair == ("중2", "수학"),
                                      is_preschool=pair[0] in {"5세", "6세", "7세"},
                                      preschool_level=pair[0],
                                      is_elementary=pair[0].startswith("초"))
            assert (result["core_correct"], result["advance_correct"], result["pass_count"]) == expected
            assert result["accuracy"] == round(expected[0] / 13 * 100)
            assert result["core_actual_seconds"] + result["advance_actual_seconds"] == result["total_seconds"]


def audit_metadata_and_regressions():
    for pair in EXPECTED:
        question_set = get_question_set(*pair)
        curriculum = question_set["curriculum"]
        if pair[0] == "중3":
            assert "2015 개정" in curriculum and "2022 개정" not in curriculum
        elif pair in {("초1", "영어"), ("초2", "영어")}:
            assert "학원 기초영어 진단" in curriculum
        elif pair[0] in {"초1", "초2", "중1", "중2"}:
            assert "2022 개정" in curriculum
    assert get_question_set("초3", "국어") is None
    assert get_questions("초6", "국어")[0]["id"] == "DEMO-01"
    m2 = get_question_set("중2", "수학")
    assert [q["correct_option_number"] for q in m2["questions"]] == M2_MATH_ANSWER_KEY
    assert sum(q["recommended_seconds"] for q in m2["questions"][:13]) == 670
    assert sum(q["recommended_seconds"] for q in m2["questions"][13:]) == 80
    assert sum(q["recommended_seconds"] for q in m2["questions"]) == 750
    assert time_difference_text(60, 80) == "20초 빠름"
    assert time_difference_text(115, 80) == "35초 초과"
    assert time_difference_text(80, 80) == "권장시간과 동일"


def audit_guardian_and_organizations():
    assert validate_organizations()
    assert len(ORGANIZATIONS) == 7
    assert len(ITEMS) == 15
    assert [item["item_id"] for item in ITEMS] == [f"GC-{index:02d}" for index in range(1, 16)]
    assert len({item["domain"] for item in ITEMS}) == 5
    assert all(sum(item["domain"] == domain for item in ITEMS) == 3 for domain in {item["domain"] for item in ITEMS})
    assert set(RESPONSE_OPTIONS) == {"often", "sometimes", "not_yet_often", "not_observed"}
    assert TEST_VERSION == "PRESCHOOL_GUARDIAN_CHECK_2026_v1.0"
    assert not any("answer" in item or "recommended_seconds" in item for item in ITEMS)
    records = [
        {"organization_code": "GWAGIDAE_CENTER", "assessment_mode": "academic_test"},
        {"organization_code": "GWAGIDAE_CENTER", "assessment_mode": "guardian_checklist"},
        {"organization_code": "GONGNEUNG_CENTER", "assessment_mode": "academic_test"},
        {"organization_code": None, "assessment_mode": None},
    ]
    assert len(filter_records(records, "GWAGIDAE_CENTER")) == 2
    assert len(filter_records(records, "GONGNEUNG_CENTER")) == 1


def run():
    for _ in range(20):
        audit_sets()
        audit_scoring()
        audit_metadata_and_regressions()
        audit_guardian_and_organizations()
    print("FULL_AUDIT_PASS: 23 sets / 345 questions / guardian / organizations / 20 cycles")


if __name__ == "__main__":
    run()
