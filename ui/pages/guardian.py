"""Guardian checklist UI renderers."""

from typing import Any

import streamlit as st

from ui.components import render_page_title, render_section_title, render_single_line_button


def render_guardian_info_page(student_name: str, phone: str) -> dict[str, Any]:
    render_page_title("대상자 정보")
    name = st.text_input(
        "아이 이름",
        value=student_name,
        key="routing_name",
    )
    phone = st.text_input(
        "보호자 연락처 (선택)",
        value=phone,
        key="routing_phone",
    )
    level = st.selectbox("연령", ["5세", "6세", "7세"], key="routing_age")
    st.info("보호자가 평소 생활과 놀이에서 관찰한 모습을 바탕으로 체크하는 상담 참고자료입니다. 아동이 직접 문제를 풀거나 학업능력을 평가하는 검사가 아닙니다.")
    confirmed = st.checkbox("이 체크리스트는 보호자가 평소 관찰한 내용을 입력하는 상담 참고자료임을 확인했습니다.", key="routing_confirm")
    start_clicked = render_single_line_button(
        "관찰 체크 시작하기",
        type="primary",
        use_container_width=True,
        disabled=not confirmed,
    )
    return {
        "name": name,
        "phone": phone,
        "level": level,
        "confirmed": confirmed,
        "start_clicked": start_clicked,
    }


def render_guardian_checklist_page(
    item: dict[str, Any],
    number: int,
    total_items: int,
    response_options: dict[str, str],
    selected_value: str | None,
) -> dict[str, Any] | None:
    render_page_title("우리아이 입학준비 관찰 체크")
    st.caption(f"체크 항목 {number} / {total_items}")
    render_section_title(item["domain"])
    st.write(item["statement"])
    for value, label in response_options.items():
        if render_single_line_button(
            label,
            type="primary" if selected_value == value else "secondary",
            use_container_width=True,
            key=f"guardian_{item['item_id']}_{value}",
        ):
            return {"type": "answer", "value": value}
    previous, next_button = st.columns(2)
    with previous:
        if number > 1 and render_single_line_button(
            "이전",
            use_container_width=True,
        ):
            return {"type": "previous"}
    with next_button:
        if render_single_line_button(
            "체크 완료" if number == total_items else "다음",
            type="primary",
            use_container_width=True,
        ):
            return {"type": "next"}
    return None


def render_guardian_result_page(
    view_model: dict[str, Any],
    caption: str,
    back_button_key: str,
) -> bool:
    render_page_title("보호자 관찰 요약")
    st.caption(caption)
    labels = {
        "often": "자주 관찰되는 모습",
        "sometimes": "상황에 따라 관찰되는 모습",
        "not_yet_often": "상담에서 함께 살펴볼 모습",
        "not_observed": "추가로 관찰해볼 모습",
    }
    for response, label in labels.items():
        render_section_title(label)
        entries = view_model["by_response"][response]
        st.write(
            "\n".join(f"- {item.get('statement', '')}" for item in entries)
            if entries
            else "해당 응답이 없습니다."
        )
    st.info("이 결과는 보호자의 관찰 응답을 정리한 상담 참고자료이며, 아동의 학업능력·발달수준·입학 가능 여부 또는 수준별 배정을 판정하는 평가가 아닙니다.")
    return render_single_line_button(
        "처음으로" if back_button_key == "guardian_result_home" else "기록 목록으로",
        use_container_width=True,
        key=back_button_key,
    )
