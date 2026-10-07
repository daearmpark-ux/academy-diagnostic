"""Organization selection page renderer."""

from typing import Any

import streamlit as st

from ui.components import render_page_title, render_single_line_button


def render_organization_page(organizations: Any) -> tuple[str, str] | None:
    organizations_by_code = {
        organization["code"]: organization
        for organization in organizations
    }
    bureau = organizations_by_code["JUNGNANG_WOLGYE_BUREAU"]
    center_codes = (
        "WOLGYE_CENTER", "GONGNEUNG_CENTER",
        "MYEONMOK_CENTER", "SINNAE_CENTER",
        "GWAGIDAE_CENTER", "JUNGNANG_CENTER",
    )
    madle = organizations_by_code["MADLE_CENTER"]
    hagye = organizations_by_code["HAGYE_CENTER"]
    with st.container(key="organization-selection"):
        render_page_title("소속을 선택해주세요")
        with st.container(key="organization-bureau"):
            bureau_column, madle_column = st.columns(2)
            with bureau_column:
                if render_single_line_button(
                    bureau["name"],
                    key=f"org_{bureau['code']}",
                    use_container_width=True,
                ):
                    return bureau["code"], bureau["name"]
            with madle_column:
                if render_single_line_button(
                    madle["name"],
                    key=f"org_{madle['code']}",
                    use_container_width=True,
                ):
                    return madle["code"], madle["name"]
        with st.container(key="organization-grid"):
            for row_start in range(0, len(center_codes), 2):
                columns = st.columns(2)
                for column, code in zip(columns, center_codes[row_start:row_start + 2]):
                    organization = organizations_by_code[code]
                    if column.button(
                        organization["name"],
                        key=f"org_{organization['code']}",
                        use_container_width=True,
                    ):
                        return organization["code"], organization["name"]
        with st.container(key="organization-hagye"):
            if render_single_line_button(
                hagye["name"],
                key=f"org_{hagye['code']}",
                use_container_width=True,
            ):
                return hagye["code"], hagye["name"]
    return None
