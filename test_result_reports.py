import json
import unittest

from diagnostic_engine import build_result_view_model, calculate_result, dedupe_preserve_order
from question_registry import get_question_set
from result_model import build_saved_result_view_model


REPRESENTATIVE_SETS = [
    ("5세", "입학준비"),
    ("초2", "국어"),
    ("초6", "수학"),
    ("중2", "수학"),
    ("중3", "영어"),
]


def make_record(level, subject):
    question_set = get_question_set(level, subject)
    questions = question_set["questions"]
    answers = {number: question["answer"] for number, question in enumerate(questions, 1)}
    times = {number: number + 4 for number in range(1, len(questions) + 1)}
    result = calculate_result(
        questions, answers, times,
        is_m2_math=level == "중2" and subject == "수학",
        is_preschool=level in {"5세", "6세", "7세"},
        preschool_level=level,
        is_elementary=level in {"초1", "초2", "초3", "초4", "초5", "초6"},
    )
    live = build_result_view_model(result, level, subject, "테스트 학생", "010-1234-5678", question_set["test_version"])
    stored_answers = {
        str(number): {
            "question_id": question["id"],
            "selected_answer": answers[number],
            "correct_answer": question["answer"],
            "is_correct": True,
            "is_pass": False,
            "elapsed_seconds": times[number],
            "is_advance_probe": question.get("is_advance_probe", False),
        }
        for number, question in enumerate(questions, 1)
    }
    stored_answers["_metadata"] = {
        "test_version": question_set["test_version"],
        "advance_correct": result["advance_correct"],
        "advance_total": result["advance_total"],
        "advance_interpretation": result["advance_interpretation"],
    }
    record = {
        "student_name": "테스트 학생",
        "phone": "010-1234-5678",
        "level": level,
        "subject": subject,
        "accuracy": result["accuracy"],
        "correct_count": result["correct"],
        "pass_count": result["pass_count"],
        "total_questions": result["core_total"],
        "total_seconds": result["total_seconds"],
        "recommended_seconds": result["recommended_total"],
        "areas_json": json.dumps(result["areas"], ensure_ascii=False),
        "answers_json": json.dumps(stored_answers, ensure_ascii=False),
        "times_json": json.dumps(times),
    }
    return live, build_saved_result_view_model(record)


class ResultReportTests(unittest.TestCase):
    def test_live_and_saved_models_match_for_representative_sets(self):
        fields = (
            "core_correct", "core_total", "accuracy", "core_pass", "total_pass",
            "total_seconds", "recommended_seconds", "advance_correct", "advance_total",
            "diagnostic_title", "diagnostic_signal", "recommendation_groups",
        )
        for level, subject in REPRESENTATIVE_SETS:
            with self.subTest(level=level, subject=subject):
                live, saved = make_record(level, subject)
                self.assertEqual({field: live[field] for field in fields}, {field: saved[field] for field in fields})
                self.assertEqual(live["areas"], saved["areas"])

    def test_dedupe_removes_only_exact_normalized_duplicates(self):
        self.assertEqual(
            dedupe_preserve_order([" 같은 문장 ", "같은 문장", "다른 문장", "다른  문장"]),
            ["같은 문장", "다른 문장", "다른  문장"],
        )


if __name__ == "__main__":
    unittest.main()
