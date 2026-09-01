"""Shared result view-model construction for live and saved attempts."""

import json

from diagnostic_engine import build_result_view_model, calculate_result
from question_registry import get_question_set


def _json_object(value):
    if isinstance(value, dict):
        return value
    try:
        parsed = json.loads(value or "{}")
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def build_saved_result_view_model(record):
    level = record.get("level")
    subject = record.get("subject")
    question_set = get_question_set(level, subject)
    answer_payload = _json_object(record.get("answers_json"))
    times_payload = _json_object(record.get("times_json"))
    answers = {}
    times = {}
    for key, value in answer_payload.items():
        if not str(key).isdigit():
            continue
        number = int(key)
        if isinstance(value, dict):
            answers[number] = value.get("selected_answer")
            if value.get("elapsed_seconds") is not None:
                times[number] = value.get("elapsed_seconds")
        else:
            answers[number] = value
    for key, value in times_payload.items():
        if str(key).isdigit() and int(key) not in times:
            times[int(key)] = value

    metadata = answer_payload.get("_metadata", {})
    if not isinstance(metadata, dict):
        metadata = {}
    if question_set and answers:
        result = calculate_result(
            question_set["questions"], answers, times,
            is_m2_math=level == "중2" and subject == "수학",
            is_preschool=level in {"5세", "6세", "7세"},
            preschool_level=level,
            is_elementary=level in {"초1", "초2", "초3", "초4", "초5", "초6"},
        )
        return build_result_view_model(
            result, level, subject, record.get("student_name", ""),
            record.get("phone", ""), metadata.get("test_version") or record.get("test_version", ""),
            record.get("created_at", ""), legacy=False,
        )

    areas = _json_object(record.get("areas_json"))
    fallback = {
        "accuracy": record.get("accuracy", 0),
        "core_correct": record.get("correct_count", 0),
        "core_total": record.get("total_questions", 0),
        "pass_count": record.get("pass_count", 0),
        "all_pass_count": record.get("pass_count", 0),
        "total_seconds": record.get("total_seconds", 0),
        "recommended_total": record.get("recommended_seconds", 0),
        "areas": areas,
        "advance_correct": metadata.get("advance_correct", 0),
        "advance_total": metadata.get("advance_total", 0),
        "advance_interpretation": metadata.get("advance_interpretation", ""),
    }
    return build_result_view_model(
        fallback, level, subject, record.get("student_name", ""),
        record.get("phone", ""), metadata.get("test_version") or record.get("test_version", "legacy"),
        record.get("created_at", ""), legacy=True,
    )
