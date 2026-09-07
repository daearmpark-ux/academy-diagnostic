"""Academic assessment UI renderers."""

from typing import Any

import streamlit as st

from ui.components import render_page_title, render_single_line_button


def render_academic_info_page(subjects_for_level, student_name: str, phone: str) -> dict[str, Any]:
    levels = ["초1", "초2", "초3", "초4", "초5", "초6", "중1", "중2", "중3"]
    with st.container(key="academic-info"):
        render_page_title("정보를 입력해주세요")
        name = st.text_input("이름", value=student_name, key="routing_name")
        phone = st.text_input(
            "보호자 연락처 (선택)", value=phone, key="routing_phone"
        )

        st.markdown("#### 학년")
        level = st.session_state.get("routing_level", levels[0])
        if level not in levels:
            level = levels[0]
        for start in range(0, len(levels), 3):
            columns = st.columns(3)
            for column, option in zip(columns, levels[start:start + 3]):
                if column.button(
                    option,
                    type="primary" if level == option else "secondary",
                    use_container_width=True,
                    key=f"routing_level_{option}",
                ):
                    level = option
                    st.session_state.routing_level = option

        subjects = list(subjects_for_level(level))
        subject = st.session_state.get("routing_subject", subjects[0])
        if subject not in subjects:
            subject = subjects[0]
            st.session_state.routing_subject = subject
        st.markdown("#### 과목")
        subject_columns = st.columns(len(subjects))
        for column, option in zip(subject_columns, subjects):
            if column.button(
                option,
                type="primary" if subject == option else "secondary",
                use_container_width=True,
                key=f"routing_subject_{option}",
            ):
                subject = option
                st.session_state.routing_subject = option

        start_clicked = render_single_line_button(
            "학습점검 시작하기",
            type="primary",
            use_container_width=True,
            key="academic_start",
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
    with st.container(key="academic-answers"):
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

    with st.container(key="academic-navigation"):
        nav_spacer_left, nav_previous, nav_next, nav_gap, nav_pass, nav_spacer_right = st.columns(
            [0.5, 1.25, 1.25, 0.55, 1.25, 0.5]
        )
    with nav_previous:
        if question_number > 1 and render_single_line_button(
            "이전",
            use_container_width=True,
            key=f"prev_{question_number}",
        ):
            return {"type": "previous"}
    with nav_next:
        label = "점검 완료" if question_number == total_questions else "다음"
        if render_single_line_button(
            label,
            type="primary",
            use_container_width=True,
            key=f"next_{question_number}",
        ):
            return {"type": "next"}
    with nav_pass:
        if render_single_line_button(
            "PASS", use_container_width=True, key=f"pass_{question_number}"
        ):
            return {"type": "pass"}

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
