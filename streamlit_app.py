import json
import time
import uuid
from datetime import datetime

import requests
import streamlit as st


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


# UI 검토용 임시 문항
# 실제 문항은 2차에서 전부 교체합니다.

PLACEHOLDER_QUESTIONS = [
    {
        "id": "DEMO-01",
        "text": "다음 중 알맞은 답을 골라주세요.",
        "choices": [
            "① 첫 번째 보기",
            "② 두 번째 보기",
            "③ 세 번째 보기",
            "④ 네 번째 보기",
            "⑤ 다섯 번째 보기",
        ],
        "answer": "② 두 번째 보기",
        "area": "기초 개념",
        "recommended_sec": 30,
    },
    {
        "id": "DEMO-02",
        "text": "문제를 읽고 가장 알맞은 답을 선택해주세요.",
        "choices": [
            "① 선택지 A",
            "② 선택지 B",
            "③ 선택지 C",
            "④ 선택지 D",
            "⑤ 선택지 E",
        ],
        "answer": "③ 선택지 C",
        "area": "개념 활용",
        "recommended_sec": 35,
    },
    {
        "id": "DEMO-03",
        "text": "다음 보기 중 조건에 맞는 것을 골라주세요.",
        "choices": [
            "① 보기 1",
            "② 보기 2",
            "③ 보기 3",
            "④ 보기 4",
            "⑤ 보기 5",
        ],
        "answer": "④ 보기 4",
        "area": "문제 해결",
        "recommended_sec": 40,
    },
]


# =========================================================
# HELPERS
# =========================================================

def is_preschool(level):
    return level in {"5세", "6세", "7세"}


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

    return PLACEHOLDER_QUESTIONS[
        (number - 1) % len(PLACEHOLDER_QUESTIONS)
    ]


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

    try:

        url = (
            st.secrets["SUPABASE_URL"].rstrip("/")
            +
            "/rest/v1/diagnostic_records"
            +
            "?select=*&order=created_at.desc"
        )

        response = requests.get(
            url,
            headers=supabase_headers(),
            timeout=10,
        )

        response.raise_for_status()

        return response.json()

    except Exception:

        return []


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
}

for key, value in DEFAULTS.items():

    if key not in st.session_state:

        st.session_state[key] = value


def reset_exam():

    for key, value in DEFAULTS.items():

        st.session_state[key] = value

    st.session_state.page = "home"

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

    total_questions = 15

    correct = 0
    passed = 0

    total_time = 0
    recommended_total = 0

    areas = {}


    for qno in range(
        1,
        total_questions + 1
    ):

        question = question_for(qno)

        area = question["area"]

        areas.setdefault(
            area,
            {
                "answered": 0,
                "correct": 0,
                "pass": 0,
                "actual": 0,
                "recommended": 0,
            },
        )


        answer = (
            st.session_state.answers.get(qno)
        )

        elapsed = (
            st.session_state.times.get(qno, 0)
        )


        areas[area]["actual"] += elapsed

        areas[area]["recommended"] += (
            question["recommended_sec"]
        )


        total_time += elapsed

        recommended_total += (
            question["recommended_sec"]
        )


        if answer == "__PASS__":

            passed += 1

            areas[area]["pass"] += 1


        elif answer:

            areas[area]["answered"] += 1


            if answer == question["answer"]:

                correct += 1

                areas[area]["correct"] += 1


    attempted = (
        total_questions
        -
        passed
    )


    if attempted > 0:

        accuracy = round(
            correct
            /
            attempted
            *
            100
        )

    else:

        accuracy = 0


    area_result = {}


    for area, data in areas.items():

        if data["answered"] > 0:

            area_accuracy = round(
                data["correct"]
                /
                data["answered"]
                *
                100
            )

        else:

            area_accuracy = 0


        area_result[area] = {
            **data,
            "accuracy": area_accuracy,
        }


    return {

        "accuracy":
            accuracy,

        "correct":
            correct,

        "pass_count":
            passed,

        "attempted":
            attempted,

        "total_questions":
            total_questions,

        "total_time":
            total_time,

        "recommended_total":
            recommended_total,

        "areas":
            area_result,
    }


# =========================================================
# SAVE RESULT
# =========================================================

def save_result_once():

    if st.session_state.result_saved:

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


    record = {

        "id":
            record_id,

        "created_at":
            created_at,

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
            result["total_questions"],

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
                st.session_state.answers,
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

st.html("""
<style>

:root {

    --blue:#246FE5;
    --blue-dark:#175FC9;

    --navy:#17324D;

    --muted:#6B7D90;

    --border:#D5E1EC;

    --soft:#EEF6FF;

    --danger:#D92D20;
}


html,
body,
[class*="css"] {

    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        "Noto Sans KR",
        Arial,
        sans-serif;
}


.stApp {

    background:
        linear-gradient(
            180deg,
            #F8FBFF 0%,
            #FFFFFF 46%
        );

    color:
        var(--navy);
}


.block-container {

    max-width:
        840px;

    padding:
        .85rem
        1.55rem
        2.8rem;
}


#MainMenu,
footer,
header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] {

    display:
        none !important;
}


/* COMMON */

.section-label {

    color:
        var(--navy);

    font-size:
        14px;

    font-weight:
        900;

    margin:
        15px
        0
        7px;
}


.optional {

    color:
        #8A9AAB;

    font-size:
        11px;

    font-weight:
        700;

    margin-left:
        4px;
}


.helper {

    color:
        #7B8DA0;

    font-size:
        11px;

    line-height:
        1.45;

    margin:
        -1px
        0
        6px;
}


.notice {

    background:
        var(--soft);

    border:
        1px solid
        #DBEAFF;

    border-radius:
        13px;

    padding:
        11px
        14px;

    color:
        #50667A;

    font-size:
        12px;

    line-height:
        1.5;

    text-align:
        center;

    margin:
        0
        0
        16px;
}


.notice b {

    color:
        #1F66C7;
}


.validation-error {

    color:
        var(--danger);

    font-size:
        12px;

    font-weight:
        900;

    line-height:
        1.5;

    margin:
        8px
        0
        3px;
}


/* INPUT */

div[data-testid="stTextInput"] input {

    min-height:
        47px !important;

    height:
        47px !important;

    background:
        #FFFFFF !important;

    color:
        #17324D !important;

    -webkit-text-fill-color:
        #17324D !important;

    border:
        1px solid
        #CFDBE7 !important;

    border-radius:
        11px !important;

    font-size:
        16px !important;
}


div[data-testid="stTextInput"]
input::placeholder {

    color:
        #9AABBC !important;

    -webkit-text-fill-color:
        #9AABBC !important;
}


/* BUTTON */

div.stButton > button {

    min-height:
        45px !important;

    border-radius:
        11px !important;

    font-size:
        14px !important;

    font-weight:
        900 !important;

    padding:
        .45rem
        .6rem !important;

    white-space:
        normal !important;

    height:
        auto !important;
}


div.stButton
> button[kind="secondary"] {

    background:
        #FFFFFF !important;

    color:
        #17324D !important;

    border:
        1px solid
        #CFDBE7 !important;
}


div.stButton
> button[kind="secondary"] * {

    color:
        #17324D !important;

    -webkit-text-fill-color:
        #17324D !important;
}


div.stButton
> button[kind="primary"] {

    background:
        #246FE5 !important;

    color:
        #FFFFFF !important;

    border:
        1px solid
        #246FE5 !important;
}


div.stButton
> button[kind="primary"] * {

    color:
        #FFFFFF !important;

    -webkit-text-fill-color:
        #FFFFFF !important;
}


[data-testid="stVerticalBlock"] {

    gap:
        .46rem !important;
}


[data-testid="stHorizontalBlock"] {

    gap:
        .58rem !important;
}


/* HOME */

.hero {

    text-align:
        center;

    margin:
        0
        0
        20px;
}


.badge {

    display:
        inline-block;

    background:
        #EAF3FF;

    color:
        var(--blue);

    padding:
        7px
        14px;

    border-radius:
        999px;

    font-size:
        13px;

    font-weight:
        900;

    margin-bottom:
        13px;
}


.hero-title {

    margin:
        0;

    color:
        var(--navy);

    font-size:
        35px;

    line-height:
        1.22;

    font-weight:
        900;

    letter-spacing:
        -1.1px;
}


.hero-title .accent {

    color:
        var(--blue);
}


.hero-sub {

    margin-top:
        10px;

    color:
        var(--muted);

    font-size:
        14px;

    line-height:
        1.6;
}


.features {

    display:
        grid;

    grid-template-columns:
        repeat(3,1fr);

    gap:
        12px;

    margin:
        17px
        0
        15px;
}


.feature {

    background:
        #FFFFFF;

    border:
        1px solid
        var(--border);

    border-radius:
        16px;

    padding:
        15px
        10px
        13px;

    text-align:
        center;
}


.feature .icon {

    font-size:
        20px;

    color:
        var(--blue);

    font-weight:
        900;

    margin-bottom:
        5px;
}


.feature .title {

    font-size:
        13px;

    color:
        var(--navy);

    font-weight:
        900;
}


.feature .sub {

    font-size:
        10px;

    color:
        #8A9AAB;

    margin-top:
        3px;
}


.start-note {

    margin:
        10px
        0
        4px;

    color:
        #8A9AAB;

    font-size:
        10px;

    text-align:
        center;
}


/* TEST */

.exam-head {

    margin:
        0
        0
        18px;
}


.exam-kicker {

    color:
        var(--blue);

    font-size:
        12px;

    font-weight:
        900;

    margin-bottom:
        4px;
}


.exam-title {

    color:
        var(--navy);

    font-size:
        28px;

    line-height:
        1.25;

    font-weight:
        900;

    margin:
        0
        0
        4px;
}


.exam-meta {

    color:
        var(--muted);

    font-size:
        12px;
}


.progress-wrap {

    margin:
        12px
        0
        22px;
}


.progress-top {

    display:
        flex;

    justify-content:
        space-between;

    color:
        #66788A;

    font-size:
        11px;

    margin-bottom:
        6px;
}


.progress-track {

    height:
        8px;

    background:
        #E5EDF6;

    border-radius:
        999px;

    overflow:
        hidden;
}


.progress-fill {

    height:
        100%;

    background:
        var(--blue);

    border-radius:
        999px;
}


.question-card {

    background:
        #FFFFFF;

    border:
        1px solid
        var(--border);

    border-radius:
        18px;

    padding:
        30px
        26px;

    margin:
        0
        0
        20px;

    box-shadow:
        0
        6px
        20px
        rgba(43,76,110,.04);
}


.question-no {

    color:
        var(--blue);

    font-size:
        11px;

    font-weight:
        900;

    margin-bottom:
        10px;
}


.question-area {

    color:
        #7A8DA1;

    font-size:
        11px;

    margin-bottom:
        7px;
}


.question-text {

    color:
        var(--navy);

    font-size:
        21px;

    line-height:
        1.7;

    font-weight:
        900;

    word-break:
        keep-all;
}


.time-hint {

    color:
        #8B9BAD;

    font-size:
        10px;

    text-align:
        right;

    margin-top:
        16px;
}


.pass-note {

    color:
        #7B8DA0;

    font-size:
        11px;

    text-align:
        center;

    margin-top:
        5px;
}


/* RESULT */

.result-hero {

    text-align:
        center;

    margin:
        4px
        0
        20px;
}


.result-mark {

    width:
        54px;

    height:
        54px;

    border-radius:
        50%;

    background:
        #EAF3FF;

    color:
        var(--blue);

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    margin:
        0
        auto
        10px;

    font-size:
        25px;

    font-weight:
        900;
}


.result-title {

    color:
        var(--navy);

    font-size:
        27px;

    font-weight:
        900;
}


.result-sub {

    color:
        var(--muted);

    font-size:
        12px;

    margin-top:
        5px;
}


.metrics {

    display:
        grid;

    grid-template-columns:
        repeat(4,1fr);

    gap:
        10px;

    margin:
        0
        0
        14px;
}


.metric {

    background:
        #FFFFFF;

    border:
        1px solid
        var(--border);

    border-radius:
        15px;

    padding:
        14px
        8px;

    text-align:
        center;
}


.metric .label {

    color:
        #7B8DA0;

    font-size:
        10px;

    margin-bottom:
        4px;
}


.metric .value {

    color:
        var(--navy);

    font-size:
        20px;

    font-weight:
        900;
}


.result-card {

    background:
        #FFFFFF;

    border:
        1px solid
        var(--border);

    border-radius:
        17px;

    padding:
        18px;

    margin-bottom:
        12px;
}


.card-title {

    color:
        var(--navy);

    font-size:
        15px;

    font-weight:
        900;

    margin-bottom:
        14px;
}


.bar-row {

    margin-bottom:
        14px;
}


.bar-head {

    display:
        flex;

    justify-content:
        space-between;

    color:
        #4D6277;

    font-size:
        12px;

    margin-bottom:
        5px;
}


.bar-track {

    height:
        8px;

    background:
        #E8EEF5;

    border-radius:
        999px;

    overflow:
        hidden;
}


.bar-fill {

    height:
        100%;

    background:
        var(--blue);

    border-radius:
        999px;
}


.time-grid {

    display:
        grid;

    grid-template-columns:
        repeat(2,1fr);

    gap:
        8px;
}


.time-box {

    background:
        #F8FBFE;

    border:
        1px solid
        #E4ECF4;

    border-radius:
        12px;

    padding:
        11px
        12px;
}


.time-box .t-title {

    color:
        var(--navy);

    font-size:
        12px;

    font-weight:
        900;
}


.time-box .t-sub {

    color:
        #72859A;

    font-size:
        10px;
}


.recommend {

    background:
        #F8FBFE;

    border:
        1px solid
        #E4ECF4;

    border-radius:
        12px;

    padding:
        11px
        12px;

    margin-bottom:
        7px;
}


.recommend .r-label {

    color:
        var(--blue);

    font-size:
        10px;

    font-weight:
        900;
}


.recommend .r-text {

    color:
        var(--navy);

    font-size:
        13px;

    font-weight:
        900;
}


/* RECORDS */

.records-title {

    color:
        var(--navy);

    font-size:
        24px;

    font-weight:
        900;
}


.records-sub {

    color:
        var(--muted);

    font-size:
        11px;

    margin-bottom:
        14px;
}


.record-card {

    background:
        #FFFFFF;

    border:
        1px solid
        var(--border);

    border-radius:
        14px;

    padding:
        13px
        14px;

    margin-bottom:
        8px;
}


.record-top {

    display:
        flex;

    justify-content:
        space-between;

    gap:
        10px;
}


.record-name {

    color:
        var(--navy);

    font-size:
        14px;

    font-weight:
        900;
}


.record-meta {

    color:
        #72859A;

    font-size:
        10px;
}


.record-phone {

    color:
        var(--blue);

    font-size:
        11px;

    font-weight:
        900;

    text-align:
        right;
}


.record-score {

    color:
        var(--navy);

    font-size:
        12px;

    margin-top:
        8px;
}


.delete-note {

    color:
        var(--danger);

    font-size:
        11px;

    font-weight:
        800;

    margin:
        6px
        0;
}


/* MOBILE */

@media(max-width:699px) {

    .block-container {

        padding-left:
            .85rem;

        padding-right:
            .85rem;
    }


    .hero-title {

        font-size:
            27px;
    }


    .question-text {

        font-size:
            18px;
    }


    .metrics {

        grid-template-columns:
            repeat(2,1fr);
    }


    .time-grid {

        grid-template-columns:
            1fr;
    }
}

</style>
""")


# =========================================================
# HOME PAGE
# =========================================================

def home_page():

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
                        "한글 · 수 개념"
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
# TEST PAGE
# =========================================================

def test_page():

    total_questions = 15

    qno = st.session_state.question_no

    question = question_for(qno)

    progress = int(
        qno
        /
        total_questions
        *
        100
    )


    st.html(
        f"""
        <div class="exam-head">

            <div class="exam-kicker">
                {service_name(st.session_state.level)}
            </div>

            <div class="exam-title">
                {st.session_state.student_name} 학생
            </div>

            <div class="exam-meta">
                {st.session_state.level}
                ·
                {st.session_state.subject}
            </div>

        </div>


        <div class="progress-wrap">

            <div class="progress-top">
                <span>
                    {qno} / {total_questions}
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
                QUESTION {qno}
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


    choices = question["choices"]

    selected = (
        st.session_state.answers.get(qno)
    )


    # 답안 버튼 영역
    # 1 / 2
    # 3 / 4
    # 5 / 빈칸

    outer_left, answer_area, outer_right = (
        st.columns(
            [1.2, 7.6, 1.2]
        )
    )


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
                type=(
                    "primary"
                    if selected
                    ==
                    choices[index]
                    else
                    "secondary"
                ),
                key=(
                    f"answer_"
                    f"{qno}_"
                    f"{index}"
                ),
            ):

                st.session_state.answers[qno] = (
                    choices[index]
                )

                st.session_state.validation_message = (
                    ""
                )

                st.rerun()


    # -----------------------------------------------------
    # Navigation
    # -----------------------------------------------------

    nav_left, nav_pass, nav_next = (
        st.columns(
            [1, 1.3, 2]
        )
    )


    with nav_left:

        if qno > 1:

            if st.button(
                "이전",
                use_container_width=True,
                key=f"prev_{qno}",
            ):

                capture_elapsed(qno)

                st.session_state.question_no -= 1

                start_timer()

                st.session_state.validation_message = (
                    ""
                )

                st.rerun()


    with nav_pass:

        if st.button(
            "PASS",
            use_container_width=True,
            key=f"pass_{qno}",
        ):

            capture_elapsed(qno)

            st.session_state.answers[qno] = (
                "__PASS__"
            )

            st.session_state.validation_message = (
                ""
            )


            if qno == total_questions:

                st.session_state.page = (
                    "result"
                )

            else:

                st.session_state.question_no += 1

                start_timer()


            st.rerun()


    with nav_next:

        label = (
            "점검 완료"
            if qno == total_questions
            else "다음"
        )


        if st.button(
            label,
            type="primary",
            use_container_width=True,
            key=f"next_{qno}",
        ):

            answer = (
                st.session_state.answers.get(qno)
            )


            if (
                not answer
                or
                answer == "__PASS__"
            ):

                st.session_state.validation_message = (
                    "답안을 선택하거나, "
                    "모르는 문제는 PASS를 눌러주세요."
                )

                st.rerun()


            capture_elapsed(qno)

            st.session_state.validation_message = (
                ""
            )


            if qno == total_questions:

                st.session_state.page = (
                    "result"
                )

            else:

                st.session_state.question_no += 1

                start_timer()


            st.rerun()


    st.html(
        '<div class="pass-note">'
        '모르는 문제는 찍지 말고 '
        'PASS를 눌러주세요.'
        '</div>'
    )


    if st.session_state.validation_message:

        st.html(
            f'<div class="validation-error">'
            f'{st.session_state.validation_message}'
            f'</div>'
        )


# =========================================================
# RESULT PAGE
# =========================================================

def result_page():

    result = build_result()


    save_result_once()


    difference = (
        result["total_time"]
        -
        result["recommended_total"]
    )


    difference_text = (
        ("+" if difference >= 0 else "-")
        +
        mmss(
            abs(difference)
        )
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
                학생의 현재 학습상태입니다.
            </div>

        </div>


        <div class="metrics">

            <div class="metric">

                <div class="label">
                    전체 정확도
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
                    미풀이 문항
                </div>

                <div class="value">
                    {result["pass_count"]}개
                </div>

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


        over_text = (
            ("+" if over >= 0 else "-")
            +
            mmss(
                abs(over)
            )
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


    st.html(
        """
        <div class="result-card">

            <div class="card-title">
                학습 추천
            </div>


            <div class="recommend">

                <div class="r-label">
                    잘 준비되어 있어요
                </div>

                <div class="r-text">
                    기초 개념
                </div>

            </div>


            <div class="recommend">

                <div class="r-label">
                    조금 더 연습하면 좋아요
                </div>

                <div class="r-text">
                    개념 활용
                </div>

            </div>


            <div class="recommend">

                <div class="r-label">
                    추가 확인을 추천해요
                </div>

                <div class="r-text">
                    PASS가 나온 영역과 문제 해결 영역
                </div>

            </div>

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


# =========================================================
# RECORDS PAGE
# =========================================================

def records_page():

    st.html(
        '<div class="records-title">'
        '점검 기록'
        '</div>'
        '<div class="records-sub">'
        '누적된 검사 기록과 연락처를 확인합니다.'
        '</div>'
    )


    if not supabase_ready():

        st.warning(
            "영구 기록을 사용하려면 "
            "Supabase 연결이 필요합니다."
        )

        records = []


    else:

        records = db_list()


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

def record_detail_page():

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


    difference_text = (
        ("+" if difference >= 0 else "-")
        +
        mmss(
            abs(difference)
        )
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
                    전체 정확도
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
                    미풀이 문항
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


    if st.button(
        "기록 목록으로",
        use_container_width=True,
        key="back_records",
    ):

        st.session_state.page = (
            "records"
        )

        st.rerun()


# =========================================================
# ROUTER
# =========================================================

if st.session_state.page == "home":

    home_page()


elif st.session_state.page == "test":

    test_page()


elif st.session_state.page == "result":

    result_page()


elif st.session_state.page == "records":

    records_page()


elif st.session_state.page == "record_detail":

    record_detail_page()


else:

    st.session_state.page = "home"

    st.rerun()
