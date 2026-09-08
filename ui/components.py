"""Reusable Streamlit UI rendering primitives."""

from typing import Any

import streamlit as st

from ui.styles import inject_navigation_styles


def render_page_title(title: str) -> None:
    st.title(title)


def render_section_title(title: str) -> None:
    st.subheader(title)


def render_single_line_button(label: str, **kwargs: Any) -> bool:
    return st.button(label, **kwargs)


def render_selection_card(title: str, container_key: str, **button_kwargs: Any) -> bool:
    with st.container(key=container_key):
        return render_single_line_button(title, **button_kwargs)


def render_context_navigation(organization_name: str, mode_name: str) -> str | None:
    inject_navigation_styles(organization_name, mode_name)
    with st.container(key="organization-navigation"):
        organization_column, assessment_column, records_column = st.columns(3, gap="medium")
        with organization_column.container(key="nav-organization"):
            if render_single_line_button(
                "소속변경",
                key="nav_organization",
                use_container_width=True,
            ):
                return "organization"
        with assessment_column.container(key="nav-assessment"):
            if render_single_line_button(
                "점검변경",
                key="nav_assessment",
                use_container_width=True,
            ):
                return "assessment"
        with records_column.container(key="nav-records"):
            if render_single_line_button(
                "기록보기",
                key="nav_records",
                use_container_width=True,
            ):
                return "records"
    return None
