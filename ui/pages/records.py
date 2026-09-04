"""Records and PIN UI renderers."""

from typing import Any

import streamlit as st

from ui.components import render_single_line_button


def render_records_header(organization_name: str) -> None:
    st.html(
        '<div class="records-title">'
        f"{organization_name} 기록"
        "</div>"
        '<div class="records-sub">'
        "누적된 검사 기록과 연락처를 확인합니다."
        "</div>"
    )


def render_records_pin_page(pin_configured: bool, pin_error: str) -> str | None:
    st.info("기록 보기는 관리자 PIN 입력 후 열람할 수 있습니다.")
    if not pin_configured:
        st.warning(
            "관리자 PIN이 설정되지 않았습니다. "
            "secrets.toml에 ADMIN_RECORDS_PIN을 추가하세요."
        )
        return None
    st.text_input("관리자 PIN", type="password", key="records_pin_input")
    if render_single_line_button(
        "기록 보기 열기",
        type="primary",
        use_container_width=True,
        key="records_pin_submit",
    ):
        return "unlock"
    if pin_error:
        st.error(pin_error)
    return None


def render_records_list_page(
    records: list[dict[str, Any]],
    organization_name: str,
    supabase_available: bool,
    attempts_csv: bytes | None,
    items_csv: bytes | None,
    export_date: str | None,
    duration_formatter,
    delete_confirm_id: str | None,
) -> dict[str, Any] | None:
    lock_col, _ = st.columns([1, 3])
    if lock_col.button(
        "다시 잠그기",
        use_container_width=True,
        key="records_pin_lock",
    ):
        return {"type": "lock"}

    if supabase_available:
        st.html(
            '<div class="result-card">'
            '<div class="card-title">파일럿 데이터 내보내기</div>'
            '<div class="helper">학생 개인정보를 제외한 분석용 데이터를 CSV로 내보냅니다.</div>'
            "</div>"
        )
        if not attempts_csv or not items_csv:
            st.info("내보낼 기록이 없습니다.")
        else:
            download_col, item_col = st.columns(2)
            download_col.download_button(
                "파일럿 요약 CSV 내려받기",
                data=attempts_csv,
                file_name=f"academy_pilot_attempts_{export_date}.csv",
                mime="text/csv",
                key="pilot_attempts_csv_download",
                use_container_width=True,
            )
            item_col.download_button(
                "문항별 분석 CSV 내려받기",
                data=items_csv,
                file_name=f"academy_pilot_items_{export_date}.csv",
                mime="text/csv",
                key="pilot_items_csv_download",
                use_container_width=True,
            )

    if not records:
        st.info("저장된 점검 기록이 없습니다.")

    for record in records:
        record_id = record.get("id")
        phone = record.get("phone") or "연락처 미입력"
        st.html(
            f"""
            <div class="record-card">

                <div class="record-top">

                    <div>

                        <div class="record-name">

                            {record.get("student_name","")}
                            ·
                            {record.get("level","")}
                            ·
                            {record.get("subject","")}

                        </div>

                        <div class="record-meta">

                            {record.get("created_at","")}

                        </div>

                    </div>


                    <div class="record-phone">

                        {phone}

                    </div>

                </div>


                <div class="record-score">

                    정확도
                    {record.get("accuracy",0)}%

                    ·

                    미풀이
                    {record.get("pass_count",0)}개

                    ·

                    총 풀이시간
                    {duration_formatter(record.get("total_seconds",0))}

                </div>

            </div>
            """
        )

        action1, action2 = st.columns([3, 1])
        if action1.button(
            "결과 보기",
            use_container_width=True,
            key=f"view_{record_id}",
        ):
            return {"type": "view", "record": record}
        if action2.button(
            "×",
            use_container_width=True,
            key=f"delete_{record_id}",
        ):
            return {"type": "delete", "record_id": record_id}

        if delete_confirm_id == record_id:
            st.html(
                '<div class="delete-note">'
                "이 기록을 삭제할까요?"
                "</div>"
            )
            cancel_col, delete_col = st.columns(2)
            if cancel_col.button(
                "취소",
                use_container_width=True,
                key=f"cancel_delete_{record_id}",
            ):
                return {"type": "cancel_delete", "record_id": record_id}
            if delete_col.button(
                "삭제",
                type="primary",
                use_container_width=True,
                key=f"confirm_delete_{record_id}",
            ):
                return {"type": "confirm_delete", "record_id": record_id}

    if render_single_line_button(
        "메인으로 돌아가기",
        use_container_width=True,
        key="records_home",
    ):
        return {"type": "home"}
    return None
