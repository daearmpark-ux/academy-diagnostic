"""Presentation and storage helpers for scoreless guardian observations."""

import json

from question_bank.preschool.guardian_checklist import (
    ITEMS, OBSERVER, RESPONSE_OPTIONS, TEST_VERSION,
)


def build_guardian_answers(responses):
    return {
        "assessment_mode": "guardian_checklist",
        "observer": OBSERVER,
        "items": [
            {
                "item_id": item["item_id"],
                "domain": item["domain"],
                "statement": item["statement"],
                "response": responses.get(item["item_id"], ""),
            }
            for item in ITEMS
        ],
    }


def build_guardian_areas(payload):
    counts = {item["domain"]: {option: 0 for option in RESPONSE_OPTIONS} for item in ITEMS}
    for item in payload.get("items", []):
        if item.get("domain") in counts and item.get("response") in RESPONSE_OPTIONS:
            counts[item["domain"]][item["response"]] += 1
    return counts


def parse_guardian_answers(value):
    if isinstance(value, dict):
        return value
    try:
        parsed = json.loads(value or "{}")
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def build_guardian_view_model(record, payload=None):
    payload = payload or parse_guardian_answers(record.get("answers_json"))
    items = payload.get("items", [])
    by_response = {option: [] for option in RESPONSE_OPTIONS}
    for item in items:
        if item.get("response") in by_response:
            by_response[item["response"]].append(item)
    return {
        "student_name": record.get("student_name", ""),
        "phone": record.get("phone", ""),
        "level": record.get("level", ""),
        "created_at": record.get("created_at", ""),
        "test_version": record.get("test_version") or TEST_VERSION,
        "items": items,
        "by_response": by_response,
        "areas": build_guardian_areas(payload),
    }