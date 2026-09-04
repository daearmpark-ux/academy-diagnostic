import json
import time
import uuid
from datetime import datetime

import requests
import streamlit as st

from diagnostic_engine import (
    area_diagnostic,
    build_recommendations,
    calculate_result,
    build_result_view_model,
    time_difference_text,
)
from question_registry import get_question_set, get_questions
from pilot_export import build_export_csvs, export_date
from result_model import build_saved_result_view_model
from guardian_model import build_guardian_answers, build_guardian_areas, build_guardian_view_model
from organization_registry import ORGANIZATIONS, filter_records, get_organization
from question_registry import get_guardian_checklist
from ui.components import (
    render_context_navigation,
    render_page_title,
    render_section_title,
)
from ui.pages.academic import (
    render_academic_info_page,
    render_academic_question_page,
    render_academic_validation_message,
)
from ui.pages.assessment import render_assessment_page
from ui.pages.guardian import (
    render_guardian_checklist_page,
    render_guardian_info_page,
    render_guardian_result_page,
)
from ui.pages.organization import render_organization_page
from ui.styles import inject_styles


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="우리아이 학습점검",
    page_icon="📘",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# =========================================================
# BASIC DATA
# =========================================================

LEVELS = [
    "5세", "6세", "7세",
    "초1", "초2", "초3", "초4", "초5", "초6",
    "중1", "중2", "중3"
]


# =========================================================
# HELPERS
# =========================================================

def is_preschool(level):
    return level in {"5세", "6세", "7세"}


def is_elementary(level):
    return level in {"초1", "초2", "초3", "초4", "초5", "초6"}


def subjects_for(level):

    if level in {"초1", "초2"}:
        return ["국어", "영어", "수학"]

    if level in {
        "초3", "초4", "초5", "초6",
        "중1", "중2", "중3"
    }:
        return ["영어", "수학"]

    return []


def service_name(level):

    if is_preschool(level):
        return "입학준비도 검사"

    return "우리아이 학습점검"


def mmss(seconds):

    minutes, seconds = divmod(
        max(0, int(seconds)),
        60
    )

    return f"{minutes}:{seconds:02d}"


def question_for(number):
    questions = get_questions(
        st.session_state.get("level"),
        st.session_state.get("subject"),
    )
    return questions[number - 1] if len(questions) > number - 1 else questions[(number - 1) % len(questions)]


def current_question_set():
    level = st.session_state.get("level")
    subject = st.session_state.get("subject")
    question_set = get_question_set(level, subject)
    if question_set is not None:
        return question_set
    fallback_questions = get_questions(level, subject)
    questions = [
        fallback_questions[index % len(fallback_questions)]
        for index in range(15)
    ]
    return {"questions": questions, "core_count": len(questions), "advance_count": 0, "test_version": "PLACEHOLDER"}


# =========================================================
# SUPABASE
# =========================================================

def supabase_ready():

    try:

        return bool(
            st.secrets["SUPABASE_URL"]
            and
            st.secrets["SUPABASE_SECRET_KEY"]
        )

    except Exception:

        return False


def supabase_headers():

    key = st.secrets["SUPABASE_SECRET_KEY"]

    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def admin_records_pin():

    try:

        configured_pin = st.secrets["ADMIN_RECORDS_PIN"]

    except Exception:

        return None

    return str(configured_pin) if str(configured_pin) else None


def validate_records_pin(entered_pin, configured_pin):

    if not configured_pin:

        return False, "관리자 PIN이 설정되지 않았습니다."

    if not entered_pin:

        return False, "PIN 번호를 입력해주세요."

    if str(entered_pin) != str(configured_pin):

        return False, "PIN 번호가 올바르지 않습니다."

    return True, ""


def db_insert(record):

    if not supabase_ready():

        return False, "Supabase 연결정보가 없습니다."

    try:

        url = (
            st.secrets["SUPABASE_URL"].rstrip("/")
            +
            "/rest/v1/diagnostic_records"
        )

        response = requests.post(
            url,
            headers=supabase_headers(),
            json=record,
            timeout=10,
        )

        response.raise_for_status()

        return True, None

    except Exception as exc:

        return False, str(exc)


def db_list():

    if not supabase_ready():

        return []

    organization_code = st.session_state.get("selected_organization_code")
    if not organization_code:
        return []
    try:

        url = (
            st.secrets["SUPABASE_URL"].rstrip("/")
            +
            "/rest/v1/diagnostic_records"
                + f"?select=*&organization_code=eq.{organization_code}&order=created_at.desc"
        )

        response = requests.get(
            url,
            headers=supabase_headers(),
            timeout=10,
        )

        response.raise_for_status()

        organization_code = st.session_state.get("selected_organization_code")
        return filter_records(response.json(), organization_code)

    except Exception:

        return []


def db_list_all_for_export(page_size=500):

    if not supabase_ready():

        return []

    records = []
    organization_code = st.session_state.get("selected_organization_code")
    if not organization_code:
        return records
    offset = 0

    try:

        while True:

            url = (
                st.secrets["SUPABASE_URL"].rstrip("/")
                + "/rest/v1/diagnostic_records"
                + f"?select=*&organization_code=eq.{organization_code}&order=created_at.desc&limit={page_size}&offset={offset}"
            )

            response = requests.get(
                url,
                headers=supabase_headers(),
                timeout=10,
            )
            response.raise_for_status()
            page = response.json()

            if not isinstance(page, list):
                return records

            organization_code = st.session_state.get("selected_organization_code")
            records.extend(filter_records(page, organization_code))
            if len(page) < page_size:
                return records

            offset += page_size

            if offset > 1000000:
                return records

    except Exception:

        return records


def db_delete(record_id):

    if not supabase_ready():

        return False

    try:

        url = (
            st.secrets["SUPABASE_URL"].rstrip("/")
            +
            f"/rest/v1/diagnostic_records?id=eq.{record_id}"
        )

        response = requests.delete(
            url,
            headers=supabase_headers(),
            timeout=10,
        )

        response.raise_for_status()

        return True

    except Exception:

        return False


# =========================================================
# SESSION STATE
# =========================================================

DEFAULTS = {
    "page": "home",
    "level": None,
    "subject": None,
    "student_name": "",
    "phone": "",
    "question_no": 1,
    "answers": {},
    "times": {},
    "question_started_at": None,
    "result_saved": False,
    "current_record_id": None,
    "validation_message": "",
    "delete_confirm_id": None,
    "view_record": None,
    "records_pin_unlocked": False,
    "records_pin_error": "",
    "records_pin_input": "",
    "selected_organization_code": None,
    "selected_organization_name": None,
    "selected_assessment_mode": None,
    "guardian_confirmed": False,
}

for key, value in DEFAULTS.items():

    if key not in st.session_state:

        st.session_state[key] = value


def reset_exam():

    reset_in_progress()
    st.session_state.page = "home"

    st.rerun()


def reset_in_progress():
    for key in ("level", "subject", "student_name", "phone", "question_no", "answers", "times", "question_started_at", "result_saved", "current_record_id", "validation_message", "guardian_confirmed"):
        st.session_state[key] = DEFAULTS[key]


def context_navigation():
    if not st.session_state.get("selected_organization_code"):
        return
    mode_name = (
        "유아" if st.session_state.get("selected_assessment_mode") == "guardian_checklist"
        else "초·중등" if st.session_state.get("selected_assessment_mode") == "academic_test"
        else "-"
    )
    organization_name = st.session_state.selected_organization_name or "-"
    action = render_context_navigation(organization_name, mode_name)
    if action == "organization":
        st.session_state.selected_organization_code = None
        st.session_state.selected_organization_name = None
        st.session_state.selected_assessment_mode = None
        reset_in_progress()
        st.session_state.page = "home"
        st.rerun()
    if action == "assessment":
        st.session_state.selected_assessment_mode = None
        reset_in_progress()
        st.session_state.page = "home"
        st.rerun()
    if action == "records":
        st.session_state.page = "records"
        st.rerun()


def start_timer():

    st.session_state.question_started_at = (
        time.time()
    )


def capture_elapsed(qno):

    if (
        st.session_state.question_started_at
        is not None
    ):

        elapsed = max(
            1,
            int(
                time.time()
                -
                st.session_state.question_started_at
            )
        )

        st.session_state.times[qno] = elapsed


# =========================================================
# RESULT CALCULATION
# =========================================================

def build_result():

    question_set = current_question_set()
    questions = question_set["questions"]
    is_m2_math = (
        st.session_state.get("level") == "중2"
        and st.session_state.get("subject") == "수학"
    )
    preschool = is_preschool(st.session_state.get("level"))
    elementary = is_elementary(st.session_state.get("level"))
    return calculate_result(
        questions,
        st.session_state.answers,
        st.session_state.times,
        is_m2_math=is_m2_math,
        is_preschool=preschool,
        preschool_level=st.session_state.get("level"),
        is_elementary=elementary,
    )

# =========================================================
# SAVE RESULT
# =========================================================

def save_result_once():

    if st.session_state.result_saved:

        return

    organization = get_organization(st.session_state.get("selected_organization_code"))
    assessment_mode = st.session_state.get("selected_assessment_mode")
    if not organization or assessment_mode != "academic_test":
        st.error("소속과 점검 유형을 다시 선택해주세요.")
        return


    result = build_result()


    record_id = str(
        uuid.uuid4()
    )


    created_at = (
        datetime.now()
        .isoformat(
            timespec="seconds"
        )
    )

    is_m2_math = (
        st.session_state.level == "중2"
        and
        st.session_state.subject == "수학"
    )
    elementary = is_elementary(st.session_state.level)

    if is_m2_math or is_preschool(st.session_state.level) or elementary:
        answers_for_storage = {}
        question_set = current_question_set()

        for qno in range(1, len(question_set["questions"]) + 1):
            question = question_for(qno)
            selected = st.session_state.answers.get(qno)
            answers_for_storage[str(qno)] = {
                "question_id": question["id"],
                "selected_answer": selected,
                "correct_answer": question["correct_option_text"],
                "is_correct": selected == question["correct_option_text"],
                "is_pass": selected == "__PASS__",
                "elapsed_seconds": st.session_state.times.get(qno, 0),
                "is_advance_probe": question["is_advance_probe"],
            }

        answers_for_storage["_metadata"] = {
            "test_version": question_set.get("test_version", ""),
            "curriculum": question_set.get("curriculum", ""),
            "curriculum_year": question_set.get("curriculum_year"),
            "core_correct": result["core_correct"],
            "core_total": result["core_total"],
            "advance_correct": result["advance_correct"],
            "advance_total": result["advance_total"],
            "advance_interpretation": result["advance_interpretation"],
        }

    else:
        answers_for_storage = st.session_state.answers


    record = {

        "id":
            record_id,

        "created_at":
            created_at,

        "organization_code": organization["code"],

        "organization_name": organization["name"],

        "assessment_mode": "academic_test",

        "student_name":
            st.session_state.student_name,

        "level":
            st.session_state.level,

        "subject":
            st.session_state.subject,

        "phone":
            st.session_state.phone,

        "accuracy":
            result["accuracy"],

        "correct_count":
            result["correct"],

        "pass_count":
            result["pass_count"],

        "total_questions":
            result["core_total"] if (is_preschool(st.session_state.level) or elementary) else result["total_questions"],

        "total_seconds":
            result["total_time"],

        "recommended_seconds":
            result["recommended_total"],

        "areas_json":
            json.dumps(
                result["areas"],
                ensure_ascii=False,
            ),

        "answers_json":
            json.dumps(
                answers_for_storage,
                ensure_ascii=False,
            ),

        "times_json":
            json.dumps(
                st.session_state.times,
                ensure_ascii=False,
            ),
    }


    success, error = db_insert(
        record
    )


    if success:

        st.session_state.result_saved = True

        st.session_state.current_record_id = (
            record_id
        )


# =========================================================
# DESIGN
# =========================================================

inject_styles()


# =========================================================
# HOME PAGE
# =========================================================

def legacy_home_page():

    menu_left, menu_right = st.columns(
        [8, 1]
    )


    with menu_right:

        if st.button(
            "기록",
            use_container_width=True,
            key="open_records",
        ):

            st.session_state.page = (
                "records"
            )

            st.rerun()


    st.html("""
    <div class="hero">

        <div class="badge">
            5세부터 중학교 3학년까지
        </div>

        <div class="hero-title">
            우리 아이의 학습상태를
            <span class="accent">
                가볍게 확인해보세요
            </span>
        </div>

        <div class="hero-sub">
            짧은 학습점검으로 현재 잘 준비된 부분과
            조금 더 연습하면 좋은 부분을 확인합니다.
        </div>

    </div>


    <div class="features">

        <div class="feature">
            <div class="icon">✓</div>
            <div class="title">간편한 점검</div>
            <div class="sub">약 5~10분</div>
        </div>

        <div class="feature">
            <div class="icon">▥</div>
            <div class="title">영역별 확인</div>
            <div class="sub">정확도 · 풀이시간</div>
        </div>

        <div class="feature">
            <div class="icon">↗</div>
            <div class="title">학습 추천</div>
            <div class="sub">결과 즉시 확인</div>
        </div>

    </div>


    <div class="notice">
        5~7세는
        <b>입학준비도 검사</b>로
        한글·수 개념을 함께 확인하고,
        초·중등은
        <b>우리아이 학습점검</b>으로
        진행합니다.
    </div>
    """)


    st.html(
        '<div class="section-label">'
        '학생 이름'
        '</div>'
    )


    name = st.text_input(
        "학생 이름",
        value=st.session_state.student_name,
        placeholder="학생 이름을 입력해주세요",
        label_visibility="collapsed",
        key="home_name",
    )


    st.html(
        '<div class="section-label">'
        '연령 / 학년'
        '</div>'
    )


    for start in range(
        0,
        len(LEVELS),
        6
    ):

        cols = st.columns(6)


        for idx, level in enumerate(
            LEVELS[start:start + 6]
        ):

            selected = (
                st.session_state.level
                ==
                level
            )


            if cols[idx].button(
                level,
                use_container_width=True,
                type=(
                    "primary"
                    if selected
                    else "secondary"
                ),
                key=f"level_{level}",
            ):

                st.session_state.level = (
                    level
                )


                if is_preschool(level):

                    st.session_state.subject = (
                        "입학준비"
                    )


                elif (
                    st.session_state.subject
                    not in
                    subjects_for(level)
                ):

                    st.session_state.subject = (
                        None
                    )

                st.session_state.validation_message = (
                    ""
                )

                st.rerun()


    level = st.session_state.level


    if level:

        if is_preschool(level):

            st.html(
                f'<div class="notice" '
                f'style="margin-top:8px;'
                f'margin-bottom:4px;">'
                f'{level} · '
                f'<b>입학준비도 검사</b> · '
                f'한글 + 수 개념 통합'
                f'</div>'
            )


        else:

            st.html(
                '<div class="section-label">'
                '점검 과목'
                '</div>'
            )


            subjects = (
                subjects_for(level)
            )


            cols = st.columns(
                len(subjects)
            )


            for idx, subject in enumerate(
                subjects
            ):

                selected = (
                    st.session_state.subject
                    ==
                    subject
                )


                if cols[idx].button(
                    subject,
                    use_container_width=True,
                    type=(
                        "primary"
                        if selected
                        else "secondary"
                    ),
                    key=(
                        f"subject_"
                        f"{level}_"
                        f"{subject}"
                    ),
                ):

                    st.session_state.subject = (
                        subject
                    )

                    st.session_state.validation_message = (
                        ""
                    )

                    st.rerun()


    st.html(
        '<div class="section-label">'
        '점검 결과 받아보기 '
        '<span class="optional">'
        '선택사항'
        '</span>'
        '</div>'
        '<div class="helper">'
        '점검 결과를 휴대폰으로 받아보시려면 '
        '연락처를 남겨주세요.'
        '</div>'
    )


    phone = st.text_input(
        "휴대폰 번호",
        value=st.session_state.phone,
        placeholder="010-0000-0000",
        label_visibility="collapsed",
        key="home_phone",
    )


    st.html(
        '<div class="start-note">'
        '연락처는 선택사항이며 '
        '입력하지 않아도 검사를 진행할 수 있습니다.'
        '</div>'
    )


    if st.session_state.validation_message:

        st.html(
            f'<div class="validation-error">'
            f'{st.session_state.validation_message}'
            f'</div>'
        )


    if st.button(
        "학습점검 시작하기",
        type="primary",
        use_container_width=True,
        key="start_exam",
    ):

        message = ""


        if not name.strip():

            message = (
                "학생 이름을 입력해주세요."
            )


        elif not level:

            message = (
                "연령 또는 학년을 선택해주세요."
            )


        elif (
            not is_preschool(level)
            and
            not st.session_state.subject
        ):

            message = (
                "점검 과목을 선택해주세요."
            )


        if message:

            st.session_state.validation_message = (
                message
            )

            st.rerun()


        st.session_state.student_name = (
            name.strip()
        )


        # 전화번호는 형식 검사하지 않음
        st.session_state.phone = (
            phone.strip()
        )


        st.session_state.question_no = 1

        st.session_state.answers = {}

        st.session_state.times = {}

        st.session_state.question_started_at = (
            time.time()
        )

        st.session_state.result_saved = False

        st.session_state.current_record_id = (
            None
        )

        st.session_state.validation_message = (
            ""
        )

        st.session_state.page = (
            "test"
        )

        st.rerun()


# =========================================================
# ORGANIZATION / MODE HOME
# =========================================================

def home_page():
    if st.session_state.get("selected_organization_code"):
        context_navigation()
    if not st.session_state.get("selected_organization_code"):
        selection = render_organization_page(ORGANIZATIONS)
        if selection:
            selected_code, selected_name = selection
            st.session_state.selected_organization_code = selected_code
            st.session_state.selected_organization_name = selected_name
            st.rerun()
        return
    if not st.session_state.get("selected_assessment_mode"):
        selected_mode = render_assessment_page()
        if selected_mode:
            st.session_state.selected_assessment_mode = selected_mode
            st.rerun()
        return
    if st.session_state.selected_assessment_mode == "guardian_checklist":
        guardian_info = render_guardian_info_page(
            st.session_state.student_name,
            st.session_state.phone,
        )
        if guardian_info["start_clicked"]:
            if not guardian_info["name"].strip():
                st.error("아이 이름을 입력해주세요.")
                return
            st.session_state.update(student_name=guardian_info["name"].strip(), phone=guardian_info["phone"], level=guardian_info["level"], subject=None, question_no=1, answers={}, times={}, result_saved=False, page="guardian_test")
            st.rerun()
        return
    academic_info = render_academic_info_page(
        subjects_for,
        st.session_state.student_name,
        st.session_state.phone,
    )
    if academic_info["start_clicked"]:
        if not academic_info["name"].strip():
            st.error("아이 이름을 입력해주세요.")
            return
        st.session_state.update(student_name=academic_info["name"].strip(), phone=academic_info["phone"], level=academic_info["level"], subject=academic_info["subject"], question_no=1, answers={}, times={}, result_saved=False, page="test")
        st.rerun()


def guardian_test_page():
    checklist = get_guardian_checklist()
    items = checklist["items"]
    number = st.session_state.question_no
    item = items[number - 1]
    context_navigation()
    selected = st.session_state.answers.get(item["item_id"])
    action = render_guardian_checklist_page(
        item,
        number,
        len(items),
        checklist["response_options"],
        selected,
    )
    if action and action["type"] == "answer":
        st.session_state.answers[item["item_id"]] = action["value"]
        st.rerun()
    if action and action["type"] == "previous":
        st.session_state.question_no -= 1
        st.rerun()
    if action and action["type"] == "next":
        if not selected:
            st.error("관찰 응답을 선택해주세요.")
            return
        if number == len(items):
            st.session_state.page = "guardian_result"
        else:
            st.session_state.question_no += 1
        st.rerun()


def guardian_result_page():
    payload = build_guardian_answers(st.session_state.answers)
    record_id = str(uuid.uuid4())
    if not st.session_state.result_saved:
        organization = get_organization(st.session_state.selected_organization_code)
        if not organization:
            st.error("소속을 다시 선택해주세요.")
            return
        record = {"id": record_id, "created_at": datetime.now().isoformat(timespec="seconds"), "student_name": st.session_state.student_name, "phone": st.session_state.phone, "level": st.session_state.level, "subject": None, "organization_code": organization["code"], "organization_name": organization["name"], "assessment_mode": "guardian_checklist", "test_version": "PRESCHOOL_GUARDIAN_CHECK_2026_v1.0", "answers_json": json.dumps(payload, ensure_ascii=False), "areas_json": json.dumps(build_guardian_areas(payload), ensure_ascii=False), "accuracy": None, "correct_count": None, "pass_count": None, "total_questions": None, "total_seconds": None, "recommended_seconds": None}
        success, error = db_insert(record)
        if success:
            st.session_state.result_saved = True
            st.session_state.current_record_id = record_id
        elif error:
            st.warning("현재 Supabase가 연결되지 않아 이 결과는 영구 저장되지 않습니다.")
    view_model = build_guardian_view_model({"student_name": st.session_state.student_name, "phone": st.session_state.phone, "level": st.session_state.level}, payload)
    context_navigation()
    if render_guardian_result_page(
        view_model,
        f"{view_model['level']} · {view_model['student_name']} · {view_model['created_at'] or '현재'}",
        "guardian_result_home",
    ):
        reset_in_progress()
        st.session_state.page = "home"
        st.rerun()


# =========================================================
# TEST PAGE
# =========================================================

def test_page():

    context_navigation()

    total_questions = len(current_question_set()["questions"])

    qno = st.session_state.question_no

    question = question_for(qno)
    selected = st.session_state.answers.get(qno)
    action = render_academic_question_page(
        service_name(st.session_state.level),
        st.session_state.student_name,
        st.session_state.level,
        st.session_state.subject,
        question,
        qno,
        total_questions,
        selected,
        is_preschool(st.session_state.level),
    )

    if action and action["type"] == "answer":
        st.session_state.answers[qno] = action["value"]
        st.session_state.validation_message = ""
        st.rerun()

    if action and action["type"] == "previous":
        capture_elapsed(qno)
        st.session_state.question_no -= 1
        start_timer()
        st.session_state.validation_message = ""
        st.rerun()

    if action and action["type"] == "pass":
        capture_elapsed(qno)
        st.session_state.answers[qno] = "__PASS__"
        st.session_state.validation_message = ""
        if qno == total_questions:
            st.session_state.page = "result"
        else:
            st.session_state.question_no += 1
            start_timer()
        st.rerun()

    if action and action["type"] == "next":
        answer = st.session_state.answers.get(qno)
        if not answer or answer == "__PASS__":
            st.session_state.validation_message = (
                "답안을 선택하거나, 모르는 문제는 PASS를 눌러주세요."
            )
            st.rerun()
        capture_elapsed(qno)
        st.session_state.validation_message = ""
        if qno == total_questions:
            st.session_state.page = "result"
        else:
            st.session_state.question_no += 1
            start_timer()
        st.rerun()


    if st.session_state.validation_message:

        render_academic_validation_message(st.session_state.validation_message)


# =========================================================
# RESULT PAGE
# =========================================================

def legacy_result_page():

    result = build_result()


    save_result_once()

    preschool = is_preschool(st.session_state.level)
    elementary = is_elementary(st.session_state.level)
    accuracy_label = (
        "현재 학년 진단 정확도"
        if st.session_state.level == "중2"
        and st.session_state.subject == "수학"
        else "CORE 13문항 정확도" if preschool else "전체 정확도"
    )
    if elementary and st.session_state.subject == "영어":
        accuracy_label = "기초영어 진단"
    elif elementary:
        accuracy_label = "현재 단계 진단 정확도"


    difference = (
        result["total_time"]
        -
        result["recommended_total"]
    )


    difference_text = time_difference_text(
        result["total_seconds"],
        result["recommended_total"],
    )


    st.html(
        f"""
        <div class="result-hero">

            <div class="result-mark">
                ✓
            </div>

            <div class="result-title">
                점검이 완료되었습니다
            </div>

            <div class="result-sub">
                {st.session_state.student_name}
                학생의 {"입학준비 기초 진단" if preschool else "학습점검"} 결과입니다.
            </div>

        </div>


        <div class="metrics">

            <div class="metric">

                <div class="label">
                    {accuracy_label}
                </div>

                <div class="value">
                    {result["accuracy"]}%
                </div>

            </div>


            <div class="metric">

                <div class="label">
                    총 풀이시간
                </div>

                <div class="value">
                    {mmss(result["total_time"])}
                </div>

            </div>


            <div class="metric">

                <div class="label">
                    권장시간 대비
                </div>

                <div class="value">
                    {difference_text}
                </div>

            </div>


            <div class="metric">

                <div class="label">
                    전체 미풀이
                </div>

                <div class="value">
                    {result["all_pass_count"] if (preschool or elementary) else result["pass_count"]}개
                </div>

            </div>

        </div>
        """
    )

    if st.session_state.level == "중2" and st.session_state.subject == "수학":
        st.html(
            f"""
            <div class="result-card">
                <div class="card-title">현재 학년 진단</div>
                <div class="recommend">
                    <div class="r-label">CORE 13문항</div>
                    <div class="r-text">{result["correct"]} / {result["core_total"]} · {result["accuracy"]}%</div>
                </div>
                <div class="recommend">
                    <div class="r-label">진단 신호</div>
                    <div class="r-text">{
                        "핵심 개념 안정"
                        if result["correct"] >= 11
                        else "대체로 안정 · 일부 보완 필요"
                        if result["correct"] >= 9
                        else "영역별 학습 결손 확인 필요"
                        if result["correct"] >= 6
                        else "선수 개념부터 재점검 권장"
                    }</div>
                </div>
            </div>

            <div class="result-card">
                <div class="card-title">상위 과정 진입 탐색</div>
                <div class="recommend">
                    <div class="r-label">ADVANCE_PROBE</div>
                    <div class="r-text">{result["advance_correct"]} / {result["advance_total"]}</div>
                    <div class="t-sub">{result["advance_interpretation"]}</div>
                </div>
            </div>
            """
        )

    elif preschool:
        core_signal = (
            "현재 단계 핵심 기초가 안정적인 신호"
            if result["core_correct"] >= 11
            else "대체로 안정 · 일부 영역 추가 확인 권장"
            if result["core_correct"] >= 9
            else "영역별 기초 개념 추가 확인 권장"
            if result["core_correct"] >= 6
            else "기초 경험부터 차근차근 재확인 권장"
        )
        st.html(
            f"""
            <div class="result-card">
                <div class="card-title">입학준비 기초 진단</div>
                <div class="recommend">
                    <div class="r-label">CORE 13문항</div>
                    <div class="r-text">{result["core_correct"]} / 13 · {result["accuracy"]}%</div>
                </div>
                <div class="recommend">
                    <div class="r-label">현재 단계 진단</div>
                    <div class="r-text">{core_signal}</div>
                </div>
            </div>
            <div class="result-card">
                <div class="card-title">다음 단계 진입 탐색</div>
                <div class="recommend">
                    <div class="r-label">ADVANCE_PROBE</div>
                    <div class="r-text">{result["advance_correct"]} / {result["advance_total"]}</div>
                    <div class="t-sub">{result["advance_interpretation"]}</div>
                </div>
            </div>
            """
        )

    elif elementary:
        core_signal = (
            "현재 학년 핵심 개념 안정"
            if result["core_correct"] >= 11
            else "대체로 안정 · 일부 보완 필요"
            if result["core_correct"] >= 9
            else "영역별 핵심 개념 추가 확인 필요"
            if result["core_correct"] >= 6
            else "선수 개념부터 재점검 권장"
        )
        st.html(
            f"""
            <div class="result-card">
                <div class="card-title">{('기초영어 진단' if st.session_state.subject == '영어' else '현재 단계 진단')}</div>
                <div class="recommend">
                    <div class="r-label">CORE 13문항</div>
                    <div class="r-text">{result["core_correct"]} / 13 · {result["accuracy"]}%</div>
                </div>
                <div class="recommend">
                    <div class="r-label">진단 신호</div>
                    <div class="r-text">{core_signal}</div>
                </div>
            </div>
            <div class="result-card">
                <div class="card-title">다음 단계 진입 탐색</div>
                <div class="recommend">
                    <div class="r-label">ADVANCE_PROBE</div>
                    <div class="r-text">{result["advance_correct"]} / {result["advance_total"]}</div>
                    <div class="t-sub">{result["advance_interpretation"]}</div>
                </div>
            </div>
            """
        )
    bars = ""


    time_boxes = ""


    for area, data in result["areas"].items():

        bars += f"""
        <div class="bar-row">

            <div class="bar-head">

                <span>
                    {area}
                </span>

                <b>
                    {data["accuracy"]}%
                    ·
                    미풀이 {data["pass"]}개
                </b>

            </div>


            <div class="bar-track">

                <div
                    class="bar-fill"
                    style="width:{data["accuracy"]}%">
                </div>

            </div>

        </div>
        """


        over = (
            data["actual"]
            -
            data["recommended"]
        )


        over_text = time_difference_text(
            data["actual"],
            data["recommended"],
        )


        time_boxes += f"""
        <div class="time-box">

            <div class="t-title">
                {area}
            </div>

            <div class="t-sub">

                실제
                {mmss(data["actual"])}

                · 권장
                {mmss(data["recommended"])}

                ·
                {over_text}

                · 미풀이
                {data["pass"]}개

            </div>

        </div>
        """


    st.html(
        f"""
        <div class="result-card">

            <div class="card-title">
                영역별 학습상태
            </div>

            {bars}

        </div>
        """
    )


    st.html(
        f"""
        <div class="result-card">

            <div class="card-title">
                영역별 풀이시간
            </div>

            <div class="time-grid">
                {time_boxes}
            </div>

        </div>
        """
    )


    recommendations = build_recommendations(result)
    recommendation_sections = []
    for label, key in (
        ("강점 신호", "strong"),
        ("우선 보완", "priority"),
        ("추가 확인", "needs_review"),
    ):
        items = recommendations[key]
        if not items:
            continue
        names = " · ".join(area for area, _ in items)
        explanation = " ".join(area_diagnostic(data) for _, data in items[:2])
        recommendation_sections.append(
            f'''<div class="recommend">
                <div class="r-label">{label}</div>
                <div class="r-text">{names}</div>
                <div class="t-sub">{explanation}</div>
            </div>'''
        )

    st.html(
        f"""
        <div class="result-card">

            <div class="card-title">
                학습 추천
            </div>


            {''.join(recommendation_sections)}

        </div>
        """
    )


    if not supabase_ready():

        st.warning(
            "현재 Supabase가 연결되지 않아 "
            "이 결과는 영구 저장되지 않습니다."
        )


    column1, column2 = st.columns(2)


    if column1.button(
        "처음으로",
        use_container_width=True,
        key="result_home",
    ):

        reset_exam()


    if column2.button(
        "기록 보기",
        use_container_width=True,
        key="result_records",
    ):

        st.session_state.page = (
            "records"
        )

        st.rerun()


def legacy_record_result_view_model(record):
    level = record.get("level")
    subject = record.get("subject")
    question_set = get_question_set(level, subject)
    answers = {}
    times = {}
    answer_payload = {}
    try:
        answer_payload = json.loads(record.get("answers_json") or "{}")
    except (TypeError, ValueError, json.JSONDecodeError):
        answer_payload = {}
    try:
        times_payload = json.loads(record.get("times_json") or "{}")
        times = {int(key): value for key, value in times_payload.items() if str(key).isdigit()}
    except (TypeError, ValueError, json.JSONDecodeError, AttributeError):
        times = {}

    if isinstance(answer_payload, dict):
        for key, value in answer_payload.items():
            if not str(key).isdigit():
                continue
            number = int(key)
            if isinstance(value, dict):
                answers[number] = value.get("selected_answer")
                if value.get("elapsed_seconds") is not None:
                    times[number] = value.get("elapsed_seconds")
            else:
                answers[number] = value

    metadata = answer_payload.get("_metadata", {}) if isinstance(answer_payload, dict) else {}
    if question_set and answers:
        result = calculate_result(
            question_set["questions"], answers, times,
            is_m2_math=level == "중2" and subject == "수학",
            is_preschool=is_preschool(level), preschool_level=level,
            is_elementary=is_elementary(level),
        )
        return build_result_view_model(
            result, level, subject, record.get("student_name", ""),
            record.get("phone", ""), metadata.get("test_version") or record.get("test_version", ""),
            record.get("created_at", ""), legacy=False,
        )

    try:
        areas = json.loads(record.get("areas_json") or "{}")
    except (TypeError, ValueError, json.JSONDecodeError):
        areas = {}
    fallback = {
        "accuracy": record.get("accuracy", 0),
        "core_correct": record.get("correct_count", 0),
        "core_total": record.get("total_questions", 0),
        "pass_count": record.get("pass_count", 0),
        "all_pass_count": record.get("pass_count", 0),
        "total_seconds": record.get("total_seconds", 0),
        "recommended_total": record.get("recommended_seconds", 0),
        "areas": areas if isinstance(areas, dict) else {},
        "advance_correct": metadata.get("advance_correct", 0),
        "advance_total": metadata.get("advance_total", 0),
        "advance_interpretation": metadata.get("advance_interpretation", ""),
    }
    return build_result_view_model(
        fallback, level, subject, record.get("student_name", ""),
        record.get("phone", ""), metadata.get("test_version") or record.get("test_version", "legacy"),
        record.get("created_at", ""), legacy=True,
    )


def record_result_view_model(record):
    return build_saved_result_view_model(record)


def render_result_report(view_model, mode="live"):
    preschool = is_preschool(view_model["level"])
    accuracy_label = "CORE 13문항 정확도" if preschool else "전체 정확도"
    if view_model["level"] == "중2" and view_model["subject"] == "수학":
        accuracy_label = "현재 학년 진단 정확도"
    elif is_elementary(view_model["level"]):
        accuracy_label = "기초영어 진단" if view_model["subject"] == "영어" else "현재 단계 진단 정확도"
    student_title = f'{view_model["student_name"]} 학생 점검 결과'
    subtitle = f'{view_model["level"]} · {view_model["subject"]} · {view_model["created_at"]}' if mode == "saved" else f'{view_model["student_name"]} 학생의 {"입학준비 기초 진단" if preschool else "학습점검"} 결과입니다.'
    st.html(f'''<div class="result-hero"><div class="result-mark">✓</div><div class="result-title">{student_title if mode == "saved" else "점검이 완료되었습니다"}</div><div class="result-sub">{subtitle}</div></div>
    <div class="metrics"><div class="metric"><div class="label">{accuracy_label}</div><div class="value">{view_model["accuracy"]}%</div></div>
    <div class="metric"><div class="label">CORE 정답수 / 전체수</div><div class="value">{view_model["core_correct"]} / {view_model["core_total"]}</div></div>
    <div class="metric"><div class="label">총 풀이시간</div><div class="value">{mmss(view_model["total_seconds"])}</div></div>
    <div class="metric"><div class="label">권장시간 대비</div><div class="value">{view_model["time_difference"]}</div></div>
    <div class="metric"><div class="label">전체 미풀이</div><div class="value">{view_model["total_pass"]}개</div></div></div>''')

    if view_model["level"] == "중2" and view_model["subject"] == "수학" or preschool or is_elementary(view_model["level"]):
        advance_title = "입학준비 기초 진단" if preschool else view_model["diagnostic_title"]
        next_title = "다음 단계 진입 탐색" if preschool or is_elementary(view_model["level"]) else "상위 과정 진입 탐색"
        st.html(f'''<div class="result-card"><div class="card-title">{advance_title}</div><div class="recommend"><div class="r-label">CORE {view_model["core_total"]}문항</div><div class="r-text">{view_model["core_correct"]} / {view_model["core_total"]} · {view_model["accuracy"]}%</div><div class="r-label">진단 신호</div><div class="r-text">{view_model["diagnostic_signal"]}</div></div></div>
        <div class="result-card"><div class="card-title">{next_title}</div><div class="recommend"><div class="r-label">ADVANCE_PROBE</div><div class="r-text">{view_model["advance_correct"]} / {view_model["advance_total"]}</div><div class="t-sub">{view_model["advance_interpretation"]}</div></div></div>''')
    else:
        st.html(f'''<div class="result-card"><div class="card-title">{view_model["diagnostic_title"]}</div><div class="recommend"><div class="r-label">진단 신호</div><div class="r-text">{view_model["diagnostic_signal"]}</div></div></div>''')

    bars = "".join(f'<div class="bar-row"><div class="bar-head"><span>{area}</span><b>{data.get("accuracy", 0)}% · 미풀이 {data.get("pass", 0)}개</b></div><div class="bar-track"><div class="bar-fill" style="width:{data.get("accuracy", 0)}%"></div></div></div>' for area, data in view_model["areas"].items())
    time_boxes = "".join(f'<div class="time-box"><div class="t-title">{area}</div><div class="t-sub">실제 {mmss(data.get("actual", 0))} · 권장 {mmss(data.get("recommended", 0))} · {time_difference_text(data.get("actual", 0), data.get("recommended", 0))} · 미풀이 {data.get("pass", 0)}개</div></div>' for area, data in view_model["areas"].items())
    st.html(f'<div class="result-card"><div class="card-title">영역별 학습상태</div>{bars}</div><div class="result-card"><div class="card-title">영역별 풀이시간</div><div class="time-grid">{time_boxes}</div></div>')
    recommendation_sections = "".join(f'<div class="recommend"><div class="r-label">{group["label"]}</div><div class="r-text">{" · ".join(group["areas"])}</div><div class="t-sub">{" ".join(group["messages"])}</div></div>' for group in view_model["recommendation_groups"])
    st.html(f'<div class="result-card"><div class="card-title">학습 추천</div>{recommendation_sections}</div>')
    if view_model["phone"]:
        st.info("연락처: " + view_model["phone"])
    if view_model["legacy"]:
        st.info("이 기록은 이전 버전에서 생성되어 일부 상세 진단 정보가 제공되지 않습니다.")
    if mode == "saved" and st.button("기록 목록으로", use_container_width=True, key="back_records_common"):
        st.session_state.page = "records"
        st.rerun()


def result_page():
    context_navigation()
    result = build_result_view_model(build_result(), st.session_state.level, st.session_state.subject, st.session_state.student_name, st.session_state.phone, current_question_set().get("test_version", ""))
    save_result_once()
    render_result_report(result)
    if not supabase_ready():
        st.warning("현재 Supabase가 연결되지 않아 이 결과는 영구 저장되지 않습니다.")
    if st.button("처음으로", use_container_width=True, key="result_home_common"):
        reset_exam()


# =========================================================
# RECORDS PAGE
# =========================================================

def records_page():

    st.html(
        '<div class="records-title">'
        f'{st.session_state.get("selected_organization_name", "현재 소속")} 기록'
        '</div>'
        '<div class="records-sub">'
        '누적된 검사 기록과 연락처를 확인합니다.'
        '</div>'
    )

    if not st.session_state.records_pin_unlocked:

        st.info("기록 보기는 관리자 PIN 입력 후 열람할 수 있습니다.")

        if admin_records_pin() is None:

            st.warning(
                "관리자 PIN이 설정되지 않았습니다. "
                "secrets.toml에 ADMIN_RECORDS_PIN을 추가하세요."
            )

            return

        st.text_input(
            "관리자 PIN",
            type="password",
            key="records_pin_input",
        )

        if st.button(
            "기록 보기 열기",
            type="primary",
            use_container_width=True,
            key="records_pin_submit",
        ):

            unlocked, pin_error = validate_records_pin(
                st.session_state.records_pin_input,
                admin_records_pin(),
            )

            if unlocked:

                st.session_state.records_pin_unlocked = True
                st.session_state.records_pin_error = ""
                st.rerun()

            else:

                st.session_state.records_pin_error = pin_error

        if st.session_state.records_pin_error:

            st.error(st.session_state.records_pin_error)

        return

    lock_col, _ = st.columns([1, 3])

    if lock_col.button(
        "다시 잠그기",
        use_container_width=True,
        key="records_pin_lock",
    ):

        st.session_state.records_pin_unlocked = False
        st.session_state.records_pin_error = ""
        st.session_state.pop("records_pin_input", None)
        st.session_state.view_record = None
        st.session_state.delete_confirm_id = None
        st.rerun()


    if not supabase_ready():

        st.warning(
            "영구 기록을 사용하려면 "
            "Supabase 연결이 필요합니다."
        )

        records = []


    else:

        records = db_list()


    if supabase_ready():

        st.html(
            '<div class="result-card">'
            '<div class="card-title">파일럿 데이터 내보내기</div>'
            '<div class="helper">학생 개인정보를 제외한 분석용 데이터를 CSV로 내보냅니다.</div>'
            '</div>'
        )

        export_records = db_list_all_for_export()

        if not export_records:

            st.info("내보낼 기록이 없습니다.")

        else:

            attempts_csv, items_csv = build_export_csvs(export_records)
            today = export_date()
            download_col, item_col = st.columns(2)

            download_col.download_button(
                "파일럿 요약 CSV 내려받기",
                data=attempts_csv,
                file_name=f"academy_pilot_attempts_{today}.csv",
                mime="text/csv",
                key="pilot_attempts_csv_download",
                use_container_width=True,
            )
            item_col.download_button(
                "문항별 분석 CSV 내려받기",
                data=items_csv,
                file_name=f"academy_pilot_items_{today}.csv",
                mime="text/csv",
                key="pilot_items_csv_download",
                use_container_width=True,
            )


    if not records:

        st.info(
            "저장된 점검 기록이 없습니다."
        )


    for record in records:

        record_id = record.get("id")


        phone = (
            record.get("phone")
            or
            "연락처 미입력"
        )


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
                    {mmss(record.get("total_seconds",0))}

                </div>

            </div>
            """
        )


        action1, action2 = st.columns(
            [3, 1]
        )


        if action1.button(
            "결과 보기",
            use_container_width=True,
            key=f"view_{record_id}",
        ):

            st.session_state.view_record = (
                record
            )

            st.session_state.page = (
                "record_detail"
            )

            st.rerun()


        if action2.button(
            "×",
            use_container_width=True,
            key=f"delete_{record_id}",
        ):

            st.session_state.delete_confirm_id = (
                record_id
            )

            st.rerun()


        if (
            st.session_state.delete_confirm_id
            ==
            record_id
        ):

            st.html(
                '<div class="delete-note">'
                '이 기록을 삭제할까요?'
                '</div>'
            )


            cancel_col, delete_col = (
                st.columns(2)
            )


            if cancel_col.button(
                "취소",
                use_container_width=True,
                key=f"cancel_delete_{record_id}",
            ):

                st.session_state.delete_confirm_id = (
                    None
                )

                st.rerun()


            if delete_col.button(
                "삭제",
                type="primary",
                use_container_width=True,
                key=f"confirm_delete_{record_id}",
            ):

                if db_delete(record_id):

                    st.session_state.delete_confirm_id = (
                        None
                    )

                    st.rerun()

                else:

                    st.error(
                        "삭제하지 못했습니다."
                    )


    if st.button(
        "메인으로 돌아가기",
        use_container_width=True,
        key="records_home",
    ):

        st.session_state.page = (
            "home"
        )

        st.rerun()


# =========================================================
# RECORD DETAIL
# =========================================================

def legacy_record_detail_page():

    if not st.session_state.records_pin_unlocked:

        st.session_state.page = "records"
        st.rerun()

    record = (
        st.session_state.view_record
    )


    if not record:

        st.session_state.page = (
            "records"
        )

        st.rerun()


    try:

        areas = json.loads(
            record.get("areas_json")
            or
            "{}"
        )

    except Exception:

        areas = {}

    try:

        answer_payload = json.loads(
            record.get("answers_json")
            or
            "{}"
        )

        answer_metadata = answer_payload.get(
            "_metadata",
            {}
        )

    except Exception:

        answer_metadata = {}


    difference = (
        int(
            record.get(
                "total_seconds",
                0
            )
        )
        -
        int(
            record.get(
                "recommended_seconds",
                0
            )
        )
    )


    difference_text = time_difference_text(
        record.get("total_seconds", 0),
        record.get("recommended_seconds", 0),
    )

    accuracy_label = (
        "현재 학년 진단 정확도"
        if record.get("level") == "중2"
        and record.get("subject") == "수학"
        else "CORE 13문항 정확도"
        if record.get("level") in {"5세", "6세", "7세"}
        else "기초영어 진단"
        if record.get("level") in {"초1", "초2", "초3", "초4", "초5", "초6"}
        and record.get("subject") == "영어"
        else "현재 단계 진단 정확도"
        if record.get("level") in {"초1", "초2", "초3", "초4", "초5", "초6"}
        else "전체 정확도"
    )


    st.html(
        f"""
        <div class="result-hero">

            <div class="result-mark">
                ✓
            </div>

            <div class="result-title">

                {record.get("student_name","")}
                학생 점검 결과

            </div>

            <div class="result-sub">

                {record.get("level","")}
                ·
                {record.get("subject","")}
                ·
                {record.get("created_at","")}

            </div>

        </div>


        <div class="metrics">

            <div class="metric">

                <div class="label">
                    {accuracy_label}
                </div>

                <div class="value">
                    {record.get("accuracy",0)}%
                </div>

            </div>


            <div class="metric">

                <div class="label">
                    총 풀이시간
                </div>

                <div class="value">
                    {mmss(record.get("total_seconds",0))}
                </div>

            </div>


            <div class="metric">

                <div class="label">
                    권장시간 대비
                </div>

                <div class="value">
                    {difference_text}
                </div>

            </div>


            <div class="metric">

                <div class="label">
                    전체 미풀이
                </div>

                <div class="value">
                    {record.get("pass_count",0)}개
                </div>

            </div>

        </div>
        """
    )


    bars = ""


    for area, data in areas.items():

        bars += f"""
        <div class="bar-row">

            <div class="bar-head">

                <span>
                    {area}
                </span>

                <b>
                    {data.get("accuracy",0)}%
                    ·
                    미풀이
                    {data.get("pass",0)}개
                </b>

            </div>


            <div class="bar-track">

                <div
                    class="bar-fill"
                    style="
                        width:
                        {data.get("accuracy",0)}%
                    ">
                </div>

            </div>

        </div>
        """


    st.html(
        f"""
        <div class="result-card">

            <div class="card-title">
                영역별 학습상태
            </div>

            {bars}

        </div>
        """
    )


    if record.get("phone"):

        st.info(
            "연락처: "
            +
            record.get("phone")
        )

    if answer_metadata.get("advance_total") == 2:

        advance_title = (
            "다음 단계 진입 탐색"
            if record.get("level") in {"5세", "6세", "7세"}
            else "상위 과정 진입 탐색"
        )

        st.html(
            f"""
            <div class="result-card">
                <div class="card-title">{advance_title}</div>
                <div class="recommend">
                    <div class="r-label">ADVANCE_PROBE</div>
                    <div class="r-text">{answer_metadata.get("advance_correct", 0)} / 2</div>
                    <div class="t-sub">{answer_metadata.get("advance_interpretation", "")}</div>
                </div>
            </div>
            """
        )


    if st.button(
        "기록 목록으로",
        use_container_width=True,
        key="back_records",
    ):

        st.session_state.page = (
            "records"
        )

        st.rerun()


def record_detail_page():
    if not st.session_state.records_pin_unlocked:
        st.session_state.page = "records"
        st.rerun()
    record = st.session_state.view_record
    if not record:
        st.session_state.page = "records"
        st.rerun()
    if record.get("assessment_mode") == "guardian_checklist":
        view_model = build_guardian_view_model(record)
        context_navigation()
        if render_guardian_result_page(
            view_model,
            f"소속: {record.get('organization_name', '')} · {view_model['level']} · {view_model['created_at']}",
            "back_guardian_records",
        ):
            st.session_state.page = "records"
            st.rerun()
        return
    render_result_report(record_result_view_model(record), mode="saved")


# =========================================================
# ROUTER
# =========================================================

if st.session_state.page == "home":

    home_page()


elif st.session_state.page == "test":

    test_page()


elif st.session_state.page == "guardian_test":

    guardian_test_page()


elif st.session_state.page == "result":

    result_page()


elif st.session_state.page == "guardian_result":

    guardian_result_page()


elif st.session_state.page == "records":

    records_page()


elif st.session_state.page == "record_detail":

    record_detail_page()


else:

    st.session_state.page = "home"

    st.rerun()
