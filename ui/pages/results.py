"""Result screen renderer shared by live and saved results."""

from typing import Any, Callable

import streamlit as st


def render_result_report(
    view_model: dict[str, Any],
    mode: str = "live",
    is_preschool: bool = False,
    is_elementary: bool = False,
    duration_formatter: Callable[[Any], str] | None = None,
    time_difference_formatter: Callable[[Any, Any], str] | None = None,
) -> str | None:
    if duration_formatter is None or time_difference_formatter is None:
        raise ValueError("Result formatting functions are required.")

    accuracy_label = "CORE 13문항 정확도" if is_preschool else "전체 정확도"
    if view_model["level"] == "중2" and view_model["subject"] == "수학":
        accuracy_label = "현재 학년 진단 정확도"
    elif is_elementary:
        accuracy_label = "기초영어 진단" if view_model["subject"] == "영어" else "현재 단계 진단 정확도"
    student_title = f'{view_model["student_name"]} 학생 점검 결과'
    subtitle = (
        f'{view_model["level"]} · {view_model["subject"]} · {view_model["created_at"]}'
        if mode == "saved"
        else f'{view_model["student_name"]} 학생의 {"입학준비 기초 진단" if is_preschool else "학습점검"} 결과입니다.'
    )
    st.html(f'''<div class="result-hero"><div class="result-mark">✓</div><div class="result-title">{student_title if mode == "saved" else "점검이 완료되었습니다"}</div><div class="result-sub">{subtitle}</div></div>
    <div class="metrics"><div class="metric"><div class="label">{accuracy_label}</div><div class="value">{view_model["accuracy"]}%</div></div>
    <div class="metric"><div class="label">CORE 정답수 / 전체수</div><div class="value">{view_model["core_correct"]} / {view_model["core_total"]}</div></div>
    <div class="metric"><div class="label">총 풀이시간</div><div class="value">{duration_formatter(view_model["total_seconds"])}</div></div>
    <div class="metric"><div class="label">권장시간 대비</div><div class="value">{view_model["time_difference"]}</div></div>
    <div class="metric"><div class="label">전체 미풀이</div><div class="value">{view_model["total_pass"]}개</div></div></div>''')

    if view_model["level"] == "중2" and view_model["subject"] == "수학" or is_preschool or is_elementary:
        advance_title = "입학준비 기초 진단" if is_preschool else view_model["diagnostic_title"]
        next_title = "다음 단계 진입 탐색" if is_preschool or is_elementary else "상위 과정 진입 탐색"
        st.html(f'''<div class="result-card"><div class="card-title">{advance_title}</div><div class="recommend"><div class="r-label">CORE {view_model["core_total"]}문항</div><div class="r-text">{view_model["core_correct"]} / {view_model["core_total"]} · {view_model["accuracy"]}%</div><div class="r-label">진단 신호</div><div class="r-text">{view_model["diagnostic_signal"]}</div></div></div>
        <div class="result-card"><div class="card-title">{next_title}</div><div class="recommend"><div class="r-label">ADVANCE_PROBE</div><div class="r-text">{view_model["advance_correct"]} / {view_model["advance_total"]}</div><div class="t-sub">{view_model["advance_interpretation"]}</div></div></div>''')
    else:
        st.html(f'''<div class="result-card"><div class="card-title">{view_model["diagnostic_title"]}</div><div class="recommend"><div class="r-label">진단 신호</div><div class="r-text">{view_model["diagnostic_signal"]}</div></div></div>''')

    bars = "".join(f'<div class="bar-row"><div class="bar-head"><span>{area}</span><b>{data.get("accuracy", 0)}% · 미풀이 {data.get("pass", 0)}개</b></div><div class="bar-track"><div class="bar-fill" style="width:{data.get("accuracy", 0)}%"></div></div></div>' for area, data in view_model["areas"].items())
    time_boxes = "".join(f'<div class="time-box"><div class="t-title">{area}</div><div class="t-sub">실제 {duration_formatter(data.get("actual", 0))} · 권장 {duration_formatter(data.get("recommended", 0))} · {time_difference_formatter(data.get("actual", 0), data.get("recommended", 0))} · 미풀이 {data.get("pass", 0)}개</div></div>' for area, data in view_model["areas"].items())
    st.html(f'<div class="result-card"><div class="card-title">영역별 학습상태</div>{bars}</div><div class="result-card"><div class="card-title">영역별 풀이시간</div><div class="time-grid">{time_boxes}</div></div>')
    recommendation_sections = "".join(f'<div class="recommend"><div class="r-label">{group["label"]}</div><div class="r-text">{" · ".join(group["areas"])}</div><div class="t-sub">{" ".join(group["messages"])}</div></div>' for group in view_model["recommendation_groups"])
    st.html(f'<div class="result-card"><div class="card-title">학습 추천</div>{recommendation_sections}</div>')
    if view_model["phone"]:
        st.info("연락처: " + view_model["phone"])
    if view_model["legacy"]:
        st.info("이 기록은 이전 버전에서 생성되어 일부 상세 진단 정보가 제공되지 않습니다.")
    if mode == "saved" and st.button("기록 목록으로", use_container_width=True, key="back_records_common"):
        return "records"
    return None
