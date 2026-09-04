"""Academic assessment UI renderers."""

from typing import Any

import streamlit as st

from ui.components import render_page_title, render_single_line_button


def render_academic_info_page(subjects_for_level, student_name: str, phone: str) -> dict[str, Any]:
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
    level = st.selectbox(
        "학년",
        ["초1", "초2", "초3", "초4", "초5", "초6", "중1", "중2", "중3"],
        key="routing_level",
    )
    subject = st.selectbox("과목", subjects_for_level(level), key="routing_subject")
    start_clicked = render_single_line_button(
        "학습점검 시작하기",
        type="primary",
        use_container_width=True,
    )
    return {
        "name": name,
        "phone": phone,
        "level": level,
        "subject": subject,
        "start_clicked": start_clicked,
    }


def render_academic_question_page(
    service_title: str,
    student_name: str,
    level: str,
    subject: str,
    question: dict[str, Any],
    question_number: int,
    total_questions: int,
    selected_answer: str | None,
    preschool: bool,
) -> dict[str, Any] | None:
    progress = int(question_number / total_questions * 100)
    st.html(
        f"""
        <div class="exam-head">

            <div class="exam-kicker">
                {service_title}
            </div>

            <div class="exam-title">
                {student_name} 학생
            </div>

            <div class="exam-meta">
                {level}
                ·
                {subject}
            </div>

        </div>


        <div class="progress-wrap">

            <div class="progress-top">
                <span>
                    {question_number} / {total_questions}
                </span>

                <span>
                    {progress}%
                </span>
            </div>


            <div class="progress-track">

                <div
                    class="progress-fill"
                    style="width:{progress}%">
                </div>

            </div>

        </div>


        <div class="question-card">

            <div class="question-no">
                QUESTION {question_number}
            </div>

            <div class="question-area">
                {question["area"]}
            </div>

            <div class="question-text">
                {question["text"]}
            </div>

            <div class="time-hint">
                권장 풀이시간 약
                {question["recommended_sec"]}초
            </div>

        </div>
        """
    )

    if preschool:
        st.info("문장 읽기는 보호자가 도와도 됩니다. 보기 글자는 대신 읽지 않는 것을 권장합니다.")

    choices = question["choices"]
    outer_left, answer_area, outer_right = st.columns([1.2, 7.6, 1.2])
    with answer_area:
        row1 = st.columns(2)
        row2 = st.columns(2)
        row3 = st.columns(2)
        buttons = [
            (row1[0], 0),
            (row1[1], 1),
            (row2[0], 2),
            (row2[1], 3),
            (row3[0], 4),
        ]
        for column, index in buttons:
            if column.button(
                choices[index],
                use_container_width=True,
                type="primary" if selected_answer == choices[index] else "secondary",
                key=f"answer_{question_number}_{index}",
            ):
                return {"type": "answer", "value": choices[index]}

    nav_left, nav_pass, nav_next = st.columns([1, 1.3, 2])
    with nav_left:
        if question_number > 1 and render_single_line_button(
            "이전",
            use_container_width=True,
            key=f"prev_{question_number}",
        ):
            return {"type": "previous"}
    with nav_pass:
        if render_single_line_button(
            "PASS",
            use_container_width=True,
            key=f"pass_{question_number}",
        ):
            return {"type": "pass"}
    with nav_next:
        label = "점검 완료" if question_number == total_questions else "다음"
        if render_single_line_button(
            label,
            type="primary",
            use_container_width=True,
            key=f"next_{question_number}",
        ):
            return {"type": "next"}

    st.html(
        '<div class="pass-note">'
        "모르는 문제는 찍지 말고 "
        "PASS를 눌러주세요."
        "</div>"
    )
    return None


def render_academic_validation_message(message: str) -> None:
    st.html(
        '<div class="validation-error">'
        f"{message}"
        "</div>"
    )
