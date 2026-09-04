"""Assessment selection page renderer."""

from typing import Literal

import streamlit as st

from ui.components import render_page_title, render_selection_card


AssessmentSelection = Literal["guardian_checklist", "academic_test"]


def render_assessment_page() -> AssessmentSelection | None:
    with st.container(key="assessment-selection"):
        render_page_title("점검 선택")
        left, right = st.columns(2)
        with left:
            if render_selection_card(
                "입학준비 체크리스트",
                "assessment-guardian",
                use_container_width=True,
                key="mode_guardian",
            ):
                return "guardian_checklist"
        with right:
            if render_selection_card(
                "초,중등 학습점검",
                "assessment-academic",
                use_container_width=True,
                key="mode_academic",
            ):
                return "academic_test"
    return None
