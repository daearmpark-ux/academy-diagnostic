"""Privacy-preserving CSV exports for pilot diagnostic records."""

import csv
import hashlib
import io
import json
from datetime import datetime

from question_registry import get_question_set


SUMMARY_FIELDS = [
    "record_id", "student_key", "created_at", "level", "subject", "test_version",
    "core_accuracy", "core_correct", "core_total", "core_pass",
    "total_questions_administered", "total_seconds", "recommended_seconds",
    "time_difference_seconds", "advance_correct", "advance_total", "advance_pass",
    "advance_interpretation", "areas_json", "weakest_area", "strongest_area",
]

ITEM_FIELDS = [
    "record_id", "student_key", "created_at", "level", "subject", "test_version",
    "question_id", "question_number", "official_domain", "unit", "skill",
    "is_advance_probe", "score_in_core", "selected_option_number", "selected_answer",
    "correct_option_number", "correct_answer", "is_correct", "is_pass",
    "elapsed_seconds", "recommended_seconds", "time_ratio", "core_accuracy",
    "core_correct", "core_total", "question_text", "options_json",
]


def _json_value(value):
    if isinstance(value, (dict, list)):
        return value
    if not isinstance(value, str) or not value:
        return {}
    try:
        return json.loads(value)
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}


def _text(value):
    return "" if value is None else str(value)


def student_key(record):
    name = " ".join(_text(record.get("student_name")).split()).strip().lower()
    phone = "".join(_text(record.get("phone")).split())
    return hashlib.sha256(f"{name}|{phone}".encode("utf-8")).hexdigest()[:16]


def _answer_entries(record):
    payload = _json_value(record.get("answers_json"))
    metadata = payload.get("_metadata", {}) if isinstance(payload, dict) else {}
    entries = []
    source = payload.items() if isinstance(payload, dict) else enumerate(payload, 1) if isinstance(payload, list) else []
    for key, value in source:
        if str(key).startswith("_"):
            continue
        number = int(key) if str(key).isdigit() else None
        if number is None:
            continue
        entries.append((number, value if isinstance(value, dict) else {"selected_answer": value}))
    return sorted(entries), metadata


def _question_info(record, number):
    try:
        question_set = get_question_set(record.get("level"), record.get("subject"))
        return question_set["questions"][number - 1]
    except (TypeError, ValueError, KeyError, IndexError):
        return {}


def _record_context(record):
    entries, metadata = _answer_entries(record)
    level, subject = record.get("level", ""), record.get("subject", "")
    questions = [_question_info(record, number) for number, _ in entries]
    test_version = metadata.get("test_version") or record.get("test_version") or "legacy"
    core_total = metadata.get("core_total") or record.get("total_questions") or sum(
        not q.get("is_advance_probe", False) for q in questions
    )
    core_correct = metadata.get("core_correct")
    if core_correct is None:
        core_correct = sum(
            value.get("selected_answer") == q.get("correct_option_text", q.get("answer")
            ) and not q.get("is_advance_probe", False)
            for (_, value), q in zip(entries, questions)
        )
    advance_correct = metadata.get("advance_correct")
    if advance_correct is None:
        advance_correct = sum(
            value.get("selected_answer") == q.get("correct_option_text", q.get("answer"))
            for (_, value), q in zip(entries, questions) if q.get("is_advance_probe", False)
        )
    return entries, metadata, questions, test_version, int(core_correct or 0), int(core_total or 0), int(advance_correct or 0)


def _item_row(record, number, value, question, context):
    _, _, _, test_version, core_correct, core_total, _ = context
    selected = value.get("selected_answer")
    correct = question.get("correct_option_text", question.get("answer", ""))
    elapsed = value.get("elapsed_seconds", "")
    recommended = question.get("recommended_seconds", question.get("recommended_sec", ""))
    is_pass = value.get("is_pass", selected == "__PASS__")
    if is_pass:
        selected_option = ""
        is_correct = False
    else:
        selected_option = value.get("selected_option_number", "")
        if not selected_option and selected and question.get("choices"):
            try:
                selected_option = question["choices"].index(selected) + 1
            except ValueError:
                selected_option = ""
        is_correct = value.get("is_correct", selected == correct)
    ratio = ""
    if recommended not in ("", None) and float(recommended) > 0 and elapsed not in ("", None):
        ratio = float(elapsed) / float(recommended)
    return {
        "record_id": record.get("id", ""), "student_key": student_key(record),
        "created_at": record.get("created_at", ""), "level": record.get("level", ""),
        "subject": record.get("subject", ""), "test_version": test_version,
        "question_id": question.get("id", value.get("question_id", "")),
        "question_number": number, "official_domain": question.get("official_domain", question.get("domain", question.get("area", ""))),
        "unit": question.get("unit", ""), "skill": question.get("skill", ""),
        "is_advance_probe": question.get("is_advance_probe", value.get("is_advance_probe", False)),
        "score_in_core": question.get("score_in_core", not question.get("is_advance_probe", False)),
        "selected_option_number": selected_option, "selected_answer": "" if is_pass else selected,
        "correct_option_number": question.get("correct_option_number", ""), "correct_answer": correct,
        "is_correct": bool(is_correct) if not is_pass else False, "is_pass": bool(is_pass),
        "elapsed_seconds": elapsed, "recommended_seconds": recommended, "time_ratio": ratio,
        "core_accuracy": round(core_correct / core_total * 100) if core_total else 0,
        "core_correct": core_correct, "core_total": core_total,
        "question_text": question.get("text", question.get("question", "")),
        "options_json": json.dumps(question.get("choices", []), ensure_ascii=False),
    }


def normalize_record_for_export(record):
    entries, metadata, questions, test_version, core_correct, core_total, advance_correct = _record_context(record)
    item_rows = [_item_row(record, number, value, question, (entries, metadata, questions, test_version, core_correct, core_total, advance_correct)) for (number, value), question in zip(entries, questions)]
    core_pass = sum(row["is_pass"] and row["score_in_core"] for row in item_rows)
    advance_pass = sum(row["is_pass"] and row["is_advance_probe"] for row in item_rows)
    areas = _json_value(record.get("areas_json"))
    if not isinstance(areas, dict):
        areas = {}
    ranked = sorted(areas.items(), key=lambda item: item[1].get("accuracy", 0) if isinstance(item[1], dict) else 0)
    weakest = ranked[0][0] if ranked else ""
    strongest = ranked[-1][0] if ranked else ""
    total_seconds = record.get("total_seconds", "")
    recommended_seconds = record.get("recommended_seconds", "")
    difference = ""
    if total_seconds not in ("", None) and recommended_seconds not in ("", None):
        difference = float(total_seconds) - float(recommended_seconds)
    summary = {
        "record_id": record.get("id", ""), "student_key": student_key(record),
        "created_at": record.get("created_at", ""), "level": record.get("level", ""),
        "subject": record.get("subject", ""), "test_version": test_version,
        "core_accuracy": round(core_correct / core_total * 100) if core_total else record.get("accuracy", ""),
        "core_correct": core_correct, "core_total": core_total, "core_pass": core_pass,
        "total_questions_administered": len(item_rows), "total_seconds": total_seconds,
        "recommended_seconds": recommended_seconds, "time_difference_seconds": difference,
        "advance_correct": advance_correct, "advance_total": sum(row["is_advance_probe"] for row in item_rows),
        "advance_pass": advance_pass, "advance_interpretation": metadata.get("advance_interpretation", ""),
        "areas_json": json.dumps(areas, ensure_ascii=False), "weakest_area": weakest, "strongest_area": strongest,
    }
    return summary, item_rows


def _csv_bytes(rows, fields):
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode("utf-8-sig")


def build_export_csvs(records):
    summaries, items = [], []
    for record in records or []:
        try:
            summary, item_rows = normalize_record_for_export(record)
            summaries.append(summary)
            items.extend(item_rows)
        except Exception:
            summaries.append({"record_id": record.get("id", ""), "student_key": student_key(record), "test_version": "legacy"})
    return _csv_bytes(summaries, SUMMARY_FIELDS), _csv_bytes(items, ITEM_FIELDS)


def export_date():
    return datetime.now().strftime("%Y%m%d")
