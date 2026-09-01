"""Pure diagnostic calculations shared by Streamlit and future clients."""


def duration_text(seconds):
    total_seconds = max(0, int(round(seconds)))
    minutes, remaining_seconds = divmod(total_seconds, 60)
    if minutes and remaining_seconds:
        return f"{minutes}분 {remaining_seconds}초"
    if minutes:
        return f"{minutes}분"
    return f"{remaining_seconds}초"


def time_difference_text(actual, recommended):
    difference = int(round(actual - recommended))
    if difference == 0:
        return "권장시간과 동일"
    if difference < 0:
        return f"{duration_text(abs(difference))} 빠름"
    return f"{duration_text(difference)} 초과"


def recommendation_priority(data):
    priority = 100 - data["accuracy"] + data["pass"] * 30
    if data["accuracy"] < 50:
        time_ratio = data["actual"] / data["recommended"] if data["recommended"] else 0
        if time_ratio <= 0.5:
            priority += 20
    return priority


def area_diagnostic(data):
    preschool = data.get("preschool", False)
    elementary = data.get("elementary", False)
    accuracy = data["accuracy"]
    time_ratio = data["actual"] / data["recommended"] if data["recommended"] else 1
    messages = []
    if data["pass"]:
        if preschool:
            messages.append(f"미풀이 문항이 {data['pass']}개 있어 해당 개념을 편안한 상황에서 한 번 더 확인하는 것이 좋습니다.")
        else:
            messages.append(f"미풀이 문항이 {data['pass']}개 있어 개념 이해 여부를 직접 확인할 필요가 있습니다.")
    if preschool or elementary:
        if accuracy >= 80 and not data["pass"]:
            messages.append("이번 검사에서는 안정적인 반응이 나타났습니다.")
        elif accuracy < 50:
            if time_ratio <= 0.5:
                messages.append("매우 짧은 응답시간과 오답이 함께 나타나 개념 이해 여부를 한 번 더 확인하는 것을 권장합니다.")
            elif preschool:
                messages.append("일부 문항에서 어려움이 나타나 핵심 개념을 차근차근 다시 확인하는 것을 권장합니다.")
            else:
                messages.append("일부 문항에서 어려움이 나타나 해당 개념을 다시 확인하는 것을 권장합니다.")
        else:
            if preschool:
                messages.append("일부 문항에서 어려움이 나타나 해당 개념을 놀이처럼 다시 접해보는 것을 권장합니다.")
            else:
                messages.append("일부 문항에서 어려움이 나타나 해당 개념을 다시 확인하는 것을 권장합니다.")
        return " ".join(messages)
    if accuracy >= 80:
        messages.append("이번 검사에서는 정답률이 높아 기본 개념 적용에 강점 신호가 보입니다.")
        if not data["pass"] and time_ratio <= 0.75:
            messages.append("권장시간보다 빠르고 안정적으로 해결한 신호입니다.")
        elif time_ratio >= 1.5:
            messages.append("정확도는 안정적이나 풀이 효율은 추가 확인이 필요해 보입니다.")
    elif accuracy < 50:
        if time_ratio <= 0.5:
            messages.append("매우 짧은 시간에 오답이 집중되어 개념 이해 여부를 재확인하는 것이 좋습니다.")
        elif time_ratio >= 1.5:
            messages.append("충분히 시도했지만 오답이 나타나 해당 개념의 풀이 과정을 점검할 필요가 있습니다.")
        else:
            messages.append("이번 검사에서는 오답이 나타나 핵심 개념과 적용 과정을 추가 확인하는 것이 좋습니다.")
    else:
        messages.append("일부 문항에서 오답이 나타나 핵심 개념과 적용 과정을 보완해 보세요.")
    return " ".join(messages)


def build_recommendations(result):
    areas = list(result["areas"].items())
    strong = [(area, data) for area, data in areas if data["accuracy"] >= 80 and data["pass"] == 0]
    priority = [(area, data) for area, data in areas if data["accuracy"] < 50]
    priority_names = {area for area, _ in priority}
    needs_review = [
        (area, data) for area, data in areas
        if area not in priority_names and (
            data["pass"] > 0 or data["accuracy"] < 80
            or (data["recommended"] and data["actual"] / data["recommended"] >= 1.5)
        )
    ]
    priority.sort(key=lambda item: recommendation_priority(item[1]), reverse=True)
    needs_review.sort(key=lambda item: recommendation_priority(item[1]), reverse=True)
    return {"strong": strong, "priority": priority, "needs_review": needs_review}


def dedupe_preserve_order(items):
    seen = set()
    unique = []
    for item in items:
        normalized = item.strip() if isinstance(item, str) else item
        if normalized in seen:
            continue
        seen.add(normalized)
        unique.append(normalized)
    return unique


def build_result_view_model(result, level, subject, student_name="", phone="",
                            test_version="", created_at="", legacy=False):
    preschool = level in {"5세", "6세", "7세"}
    elementary = level in {"초1", "초2", "초3", "초4", "초5", "초6"}
    is_m2_math = level == "중2" and subject == "수학"
    if is_m2_math:
        diagnostic_title = "현재 학년 진단"
        diagnostic_signal = (
            "핵심 개념 안정" if result["core_correct"] >= 11 else
            "대체로 안정 · 일부 보완 필요" if result["core_correct"] >= 9 else
            "영역별 학습 결손 확인 필요" if result["core_correct"] >= 6 else
            "선수 개념부터 재점검 권장"
        )
    elif preschool:
        diagnostic_title = "입학준비 기초 진단"
        diagnostic_signal = (
            "현재 단계 핵심 기초가 안정적인 신호" if result["core_correct"] >= 11 else
            "대체로 안정 · 일부 영역 추가 확인 권장" if result["core_correct"] >= 9 else
            "영역별 기초 개념 추가 확인 권장" if result["core_correct"] >= 6 else
            "기초 경험부터 차근차근 재확인 권장"
        )
    else:
        diagnostic_title = "기초영어 진단" if elementary and subject == "영어" else "현재 단계 진단" if elementary else "현재 학년 진단"
        diagnostic_signal = (
            "현재 학년 핵심 개념 안정" if elementary and result["core_correct"] >= 11 else
            "대체로 안정 · 일부 보완 필요" if result["core_correct"] >= 9 else
            "영역별 핵심 개념 추가 확인 필요" if elementary and result["core_correct"] >= 6 else
            "선수 개념부터 재점검 권장" if elementary else
            "현재 학년 핵심 개념 안정화 우선"
        )

    recommendation_groups = []
    try:
        recommendations = build_recommendations(result)
    except (KeyError, TypeError):
        recommendations = {"strong": [], "priority": [], "needs_review": []}
    for label, key in (("강점 신호", "strong"), ("우선 보완", "priority"), ("추가 확인", "needs_review")):
        items = recommendations[key]
        if not items:
            continue
        messages = []
        for _, data in items[:2]:
            try:
                messages.append(area_diagnostic(data))
            except (KeyError, TypeError, ZeroDivisionError):
                continue
        recommendation_groups.append({
            "label": label,
            "areas": [area for area, _ in items],
            "messages": dedupe_preserve_order(messages),
        })

    return {
        "student_name": student_name,
        "phone": phone,
        "level": level,
        "subject": subject,
        "test_version": test_version,
        "created_at": created_at,
        "legacy": legacy,
        "accuracy": result["accuracy"],
        "core_correct": result["core_correct"],
        "core_total": result["core_total"],
        "core_pass": result["pass_count"],
        "total_pass": result["all_pass_count"],
        "total_seconds": result["total_seconds"],
        "recommended_seconds": result["recommended_total"],
        "time_difference": time_difference_text(result["total_seconds"], result["recommended_total"]),
        "areas": result["areas"],
        "diagnostic_title": diagnostic_title,
        "diagnostic_signal": diagnostic_signal,
        "recommendation_groups": recommendation_groups,
        "advance_correct": result["advance_correct"],
        "advance_total": result["advance_total"],
        "advance_interpretation": result["advance_interpretation"],
    }


def calculate_result(questions, answers, times, is_m2_math=False, is_preschool=False,
                     preschool_level=None, is_elementary=False):
    total_questions = len(questions)
    core_questions = [question for question in questions if question.get("score_in_core", True)]
    advance_questions = [question for question in questions if question.get("is_advance_probe", False)]
    core_total = len(core_questions)
    correct = passed = all_passed = advance_correct = 0
    total_time = core_actual_seconds = advance_actual_seconds = 0
    recommended_total = core_recommended_seconds = advance_recommended_seconds = 0
    areas = {}

    for number, question in enumerate(questions, start=1):
        answer = answers.get(number)
        elapsed = times.get(number, 0)
        if answer == "__PASS__":
            all_passed += 1
        recommended = question.get("recommended_sec", question.get("recommended_seconds", 0))
        total_time += elapsed
        recommended_total += recommended
        if question.get("is_advance_probe", False):
            advance_actual_seconds += elapsed
            advance_recommended_seconds += recommended
            if answer == question.get("answer"):
                advance_correct += 1
            continue
        core_actual_seconds += elapsed
        core_recommended_seconds += recommended
        area = question.get("area", "기초 개념")
        data = areas.setdefault(area, {"answered": 0, "correct": 0, "pass": 0, "total": 0, "actual": 0, "recommended": 0, "preschool": is_preschool, "elementary": is_elementary})
        data["total"] += 1
        data["actual"] += elapsed
        data["recommended"] += recommended
        if answer == "__PASS__":
            passed += 1
            data["pass"] += 1
        elif answer:
            data["answered"] += 1
            if answer == question.get("answer"):
                correct += 1
                data["correct"] += 1

    attempted = core_total - passed
    accuracy = round(correct / core_total * 100) if (is_m2_math or is_preschool or is_elementary) and core_total else round(correct / attempted * 100) if attempted else 0
    area_result = {}
    for area, data in areas.items():
        denominator = data["total"] if (is_m2_math or is_preschool or is_elementary) else data["answered"]
        area_result[area] = {**data, "accuracy": round(data["correct"] / denominator * 100) if denominator else 0}
    if advance_correct == len(advance_questions) and advance_questions:
        advance_interpretation = "초등 학습 기초 진입 신호 있음" if preschool_level == "7세" else "다음 단계 개념 진입 신호 있음"
    elif advance_correct:
        advance_interpretation = "다음 단계 개념 일부 인지 · 추가 확인 필요" if is_preschool else "상위 학년 개념 일부 인지 · 추가 확인 필요"
    else:
        advance_interpretation = "현재 단계 기초 경험 우선" if is_preschool else "현재 단계 핵심 개념 안정화 우선" if is_elementary else "현재 학년 핵심 개념 안정화 우선"
    return {
        "accuracy": accuracy, "correct": correct, "core_correct": correct,
        "core_total": core_total, "pass_count": passed, "attempted": attempted,
        "total_questions": total_questions, "total_time": total_time, "total_seconds": total_time,
        "all_pass_count": all_passed,
        "core_actual_seconds": core_actual_seconds, "advance_actual_seconds": advance_actual_seconds,
        "core_recommended_seconds": core_recommended_seconds, "advance_recommended_seconds": advance_recommended_seconds,
        "recommended_total": recommended_total, "advance_correct": advance_correct,
        "advance_total": len(advance_questions), "advance_interpretation": advance_interpretation,
        "areas": area_result,
        "is_preschool": is_preschool,
        "is_elementary": is_elementary,
    }
