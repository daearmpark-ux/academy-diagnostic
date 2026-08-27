import re
import time
from datetime import datetime

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
# 실제 문항은 2차에서 전부 교체
PLACEHOLDER_QUESTIONS = [
    {
        "text": "다음 중 알맞은 답을 골라주세요.",
        "choices": [
            "① 첫 번째 보기",
            "② 두 번째 보기",
            "③ 세 번째 보기",
            "④ 네 번째 보기",
        ],
        "area": "기초 개념",
        "recommended_sec": 30,
    },
    {
        "text": "문제를 읽고 가장 알맞은 답을 선택해주세요.",
        "choices": [
            "① 선택지 A",
            "② 선택지 B",
            "③ 선택지 C",
            "④ 선택지 D",
        ],
        "area": "개념 활용",
        "recommended_sec": 35,
    },
    {
        "text": "다음 보기 중 조건에 맞는 것을 골라주세요.",
        "choices": [
            "① 보기 1",
            "② 보기 2",
            "③ 보기 3",
            "④ 보기 4",
        ],
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


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "page": "home",
    "level": None,
    "subject": None,
    "student_name": "",
    "phone": "",
    "question_no": 1,
    "answers": {},
    "times": {},
    "question_started_at": None,
    "records": [],
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


def reset_exam_state():

    records = st.session_state.records

    st.session_state.page = "home"
    st.session_state.level = None
    st.session_state.subject = None
    st.session_state.student_name = ""
    st.session_state.phone = ""
    st.session_state.question_no = 1
    st.session_state.answers = {}
    st.session_state.times = {}
    st.session_state.question_started_at = None
    st.session_state.records = records

    st.rerun()


# =========================================================
# DESIGN SYSTEM
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

    --green:#2A9D6F;

    --amber:#E79B2F;

    --red:#D85858;
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

    color:var(--navy);
}


.block-container {

    max-width:840px;

    padding-top:.85rem;

    padding-bottom:2.4rem;

    padding-left:1.55rem;

    padding-right:1.55rem;
}


#MainMenu,
footer,
header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] {

    display:none !important;
}


/* =====================================================
   COMMON
===================================================== */


.section-label {

    color:var(--navy);

    font-size:14px;

    font-weight:900;

    margin:15px 0 7px;
}


.optional {

    color:#8A9AAB;

    font-size:11px;

    font-weight:700;

    margin-left:4px;
}


.helper {

    color:#7B8DA0;

    font-size:11px;

    line-height:1.45;

    margin:-1px 0 6px;
}


.notice {

    background:var(--soft);

    border:
        1px solid
        #DBEAFF;

    border-radius:13px;

    padding:11px 14px;

    color:#50667A;

    font-size:12px;

    line-height:1.5;

    text-align:center;

    margin:0 0 16px;
}


.notice b {

    color:#1F66C7;
}


/* =====================================================
   TEXT INPUT
===================================================== */


div[data-testid="stTextInput"] {

    margin-bottom:0 !important;
}


div[data-testid="stTextInput"] input {

    min-height:47px !important;

    height:47px !important;

    background:#FFFFFF !important;

    color:#17324D !important;

    -webkit-text-fill-color:
        #17324D !important;

    border:
        1px solid
        #CFDBE7 !important;

    border-radius:
        11px !important;

    font-size:16px !important;

    padding-top:0 !important;

    padding-bottom:0 !important;
}


div[data-testid="stTextInput"]
input::placeholder {

    color:#9AABBC !important;

    -webkit-text-fill-color:
        #9AABBC !important;
}


div[data-testid="stTextInput"]
input:focus {

    border-color:
        var(--blue) !important;

    box-shadow:
        0 0 0 3px
        rgba(36,111,229,.09)
        !important;
}


/* =====================================================
   BUTTONS
===================================================== */


div.stButton {

    margin:0 !important;
}


div.stButton > button {

    min-height:45px !important;

    height:45px !important;

    border-radius:
        11px !important;

    font-size:
        14px !important;

    font-weight:
        900 !important;

    padding:
        .2rem .45rem !important;
}


/* 미선택 버튼 */

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
> button[kind="secondary"]:hover {

    background:
        #F4F8FC !important;

    border-color:
        #ABC3DD !important;

    color:
        #17324D !important;
}


/* 선택 버튼 */

div.stButton
> button[kind="primary"] {

    background:
        var(--blue) !important;

    color:
        #FFFFFF !important;

    border:
        1px solid
        var(--blue) !important;
}


div.stButton
> button[kind="primary"] * {

    color:
        #FFFFFF !important;

    -webkit-text-fill-color:
        #FFFFFF !important;
}


div.stButton
> button[kind="primary"]:hover {

    background:
        var(--blue-dark) !important;

    border-color:
        var(--blue-dark) !important;
}


/* =====================================================
   STREAMLIT SPACING
===================================================== */


[data-testid="stVerticalBlock"] {

    gap:.46rem !important;
}


[data-testid="stHorizontalBlock"] {

    gap:.58rem !important;
}


/* =====================================================
   HOME HERO
===================================================== */


.hero {

    text-align:center;

    margin:0 0 20px;
}


.badge {

    display:inline-block;

    background:
        #EAF3FF;

    color:
        var(--blue);

    padding:
        7px 14px;

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

    margin:0;

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


/* =====================================================
   HOME FEATURE CARDS
===================================================== */


.features {

    display:grid;

    grid-template-columns:
        repeat(3,1fr);

    gap:
        12px;

    margin:
        17px 0 15px;
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
        15px 10px 13px;

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
        10px 0 4px;

    color:
        #8A9AAB;

    font-size:
        10px;

    text-align:
        center;
}


/* =====================================================
   TEST PAGE
===================================================== */


.exam-head {

    margin:
        0 0 16px;
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
        0 0 4px;
}


.exam-meta {

    color:
        var(--muted);

    font-size:
        12px;
}


.progress-wrap {

    margin:
        12px 0 18px;
}


.progress-top {

    display:flex;

    justify-content:
        space-between;

    align-items:center;

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
        26px 22px;

    margin:
        0 0 14px;

    box-shadow:
        0 6px 20px
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
        20px;

    line-height:
        1.65;

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
        14px;
}


/* 테스트 선택지 */

div[data-testid="stRadio"] label {

    background:
        #FFFFFF !important;

    border:
        1px solid
        #D7E2EC !important;

    border-radius:
        12px !important;

    padding:
        12px 13px !important;

    margin-bottom:
        7px !important;
}


div[data-testid="stRadio"] label p {

    color:
        #17324D !important;

    -webkit-text-fill-color:
        #17324D !important;

    font-size:
        14px !important;
}


/* =====================================================
   RESULT PAGE
===================================================== */


.result-hero {

    text-align:
        center;

    margin:
        4px 0 20px;
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
        0 auto 10px;

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

    line-height:
        1.3;

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
        repeat(3,1fr);

    gap:
        10px;

    margin:
        0 0 14px;
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
        14px 8px;

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

    display:flex;

    justify-content:
        space-between;

    gap:
        8px;

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


/* =====================================================
   TIME RESULT
===================================================== */


.time-grid {

    display:grid;

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
        11px 12px;
}


.time-box .t-title {

    color:
        var(--navy);

    font-size:
        12px;

    font-weight:
        900;

    margin-bottom:
        3px;
}


.time-box .t-sub {

    color:
        #72859A;

    font-size:
        10px;
}


/* =====================================================
   RECOMMEND RESULT
===================================================== */


.recommend {

    background:
        #F8FBFE;

    border:
        1px solid
        #E4ECF4;

    border-radius:
        12px;

    padding:
        11px 12px;

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

    margin-bottom:
        3px;
}


.recommend .r-text {

    color:
        var(--navy);

    font-size:
        13px;

    font-weight:
        900;
}


/* =====================================================
   RECORD PAGE
===================================================== */


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

    margin-top:
        3px;

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
        13px 14px;

    margin-bottom:
        8px;
}


.record-top {

    display:flex;

    justify-content:
        space-between;

    gap:
        10px;

    align-items:
        flex-start;
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

    margin-top:
        3px;
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


/* =====================================================
   TABLET
===================================================== */


@media (
    min-width:700px
)
and (
    max-width:900px
) {

    .block-container {

        max-width:
            800px;

        padding-top:
            .65rem;
    }


    .hero-title {

        font-size:
            33px;
    }


    .question-text {

        font-size:
            21px;
    }
}


/* =====================================================
   MOBILE
===================================================== */


@media (
    max-width:699px
) {

    .block-container {

        padding-top:
            .45rem;

        padding-left:
            .85rem;

        padding-right:
            .85rem;

        padding-bottom:
            2rem;
    }


    .hero-title {

        font-size:
            27px;
    }


    .hero-sub {

        font-size:
            12px;
    }


    .features {

        gap:
            7px;
    }


    .feature {

        padding:
            11px 5px 10px;
    }


    .feature .title {

        font-size:
            12px;
    }


    .feature .sub {

        font-size:
            9px;
    }


    .exam-title {

        font-size:
            24px;
    }


    .question-card {

        padding:
            20px 17px;
    }


    .question-text {

        font-size:
            18px;
    }


    .metrics {

        gap:
            7px;
    }


    .metric .value {

        font-size:
            17px;
    }


    .time-grid {

        grid-template-columns:
            1fr;
    }
}

</style>
""")


# =========================================================
# SHARED FUNCTIONS
# =========================================================

def current_question():

    index = (
        st.session_state.question_no - 1
    ) % len(PLACEHOLDER_QUESTIONS)

    return PLACEHOLDER_QUESTIONS[index]


def save_current_answer(answer):

    q = st.session_state.question_no

    if (
        st.session_state.question_started_at
        is not None
    ):

        elapsed = int(
            time.time()
            -
            st.session_state.question_started_at
        )

        st.session_state.times[q] = max(
            1,
            elapsed
        )

    st.session_state.answers[q] = answer


def build_demo_result():

    total_seconds = sum(
        st.session_state.times.values()
    )

    if total_seconds <= 0:
        total_seconds = 462


    recommended_total = 410


    areas = {

        "기초 개념": {
            "accuracy": 90,
            "actual": 142,
            "recommended": 120,
        },

        "개념 활용": {
            "accuracy": 75,
            "actual": 168,
            "recommended": 150,
        },

        "문제 해결": {
            "accuracy": 65,
            "actual": 152,
            "recommended": 140,
        },
    }

    return (
        80,
        total_seconds,
        recommended_total,
        areas,
    )


# =========================================================
# HOME PAGE
# =========================================================

def home_page():

    # 오른쪽 기록 메뉴
    menu_col1, menu_col2 = st.columns(
        [8, 1]
    )

    with menu_col2:

        if st.button(
            "기록",
            use_container_width=True,
            key="home_records"
        ):

            st.session_state.page = "records"

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

            <div class="icon">
                ✓
            </div>

            <div class="title">
                간편한 점검
            </div>

            <div class="sub">
                약 5~10분
            </div>

        </div>


        <div class="feature">

            <div class="icon">
                ▥
            </div>

            <div class="title">
                영역별 확인
            </div>

            <div class="sub">
                정확도 · 풀이시간
            </div>

        </div>


        <div class="feature">

            <div class="icon">
                ↗
            </div>

            <div class="title">
                학습 추천
            </div>

            <div class="sub">
                결과 즉시 확인
            </div>

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


    # -----------------------------------------------------
    # 학생 이름
    # -----------------------------------------------------

    st.html(
        '<div class="section-label">'
        '학생 이름'
        '</div>'
    )


    name = st.text_input(

        "학생 이름",

        value=
            st.session_state.student_name,

        placeholder=
            "학생 이름을 입력해주세요",

        label_visibility=
            "collapsed",

        key=
            "home_name",
    )


    # -----------------------------------------------------
    # 연령 / 학년
    # -----------------------------------------------------

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

        for index, level in enumerate(
            LEVELS[start:start + 6]
        ):

            selected = (
                st.session_state.level
                ==
                level
            )

            if cols[index].button(

                level,

                use_container_width=True,

                type=(
                    "primary"
                    if selected
                    else "secondary"
                ),

                key=
                    f"level_{level}",
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

                    st.session_state.subject = None


                st.rerun()


    level = st.session_state.level


    # -----------------------------------------------------
    # 과목
    # -----------------------------------------------------

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


            subjects = subjects_for(
                level
            )


            cols = st.columns(
                len(subjects)
            )


            for index, subject in enumerate(
                subjects
            ):

                selected = (
                    st.session_state.subject
                    ==
                    subject
                )


                if cols[index].button(

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

                    st.rerun()


    # -----------------------------------------------------
    # 연락처
    # -----------------------------------------------------

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

        value=
            st.session_state.phone,

        placeholder=
            "010-0000-0000",

        label_visibility=
            "collapsed",

        key=
            "home_phone",
    )


    st.html(
        '<div class="start-note">'
        '연락처를 입력하지 않아도 '
        '학습점검을 진행할 수 있습니다.'
        '</div>'
    )


    # -----------------------------------------------------
    # 시작
    # -----------------------------------------------------

    if st.button(

        "학습점검 시작하기",

        type="primary",

        use_container_width=True,

        key=
            "start_exam",
    ):

        if not name.strip():

            st.warning(
                "학생 이름을 입력해주세요."
            )


        elif not level:

            st.warning(
                "연령 또는 학년을 선택해주세요."
            )


        elif (
            not is_preschool(level)
            and
            not st.session_state.subject
        ):

            st.warning(
                "점검 과목을 선택해주세요."
            )


        elif (
            phone.strip()
            and
            not re.fullmatch(
                r"01[016789]-?\d{3,4}-?\d{4}",
                phone.strip(),
            )
        ):

            st.warning(
                "휴대폰 번호 형식을 확인해주세요."
            )


        else:

            st.session_state.student_name = (
                name.strip()
            )

            st.session_state.phone = (
                phone.strip()
            )

            st.session_state.question_no = 1

            st.session_state.answers = {}

            st.session_state.times = {}

            st.session_state.question_started_at = (
                time.time()
            )

            st.session_state.page = "test"

            st.rerun()


# =========================================================
# TEST PAGE
# =========================================================

def test_page():

    total_questions = 15

    q = st.session_state.question_no

    question = current_question()

    progress = int(
        q / total_questions * 100
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
                    {q} / {total_questions}
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
                QUESTION {q}
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


    previous_answer = (
        st.session_state.answers.get(q)
    )


    if (
        previous_answer
        in question["choices"]
    ):

        radio_index = (
            question["choices"].index(
                previous_answer
            )
        )

    else:

        radio_index = None


    answer = st.radio(

        "답안",

        question["choices"],

        index=
            radio_index,

        label_visibility=
            "collapsed",

        key=
            f"radio_q_{q}",
    )


    previous_col, next_col = st.columns(
        [1, 2]
    )


    # 이전 버튼

    with previous_col:

        if q > 1:

            if st.button(

                "이전",

                use_container_width=True,

                key=
                    f"prev_{q}",
            ):

                if answer is not None:

                    save_current_answer(
                        answer
                    )


                st.session_state.question_no -= 1

                st.session_state.question_started_at = (
                    time.time()
                )

                st.rerun()


    # 다음 버튼

    with next_col:

        button_label = (

            "점검 완료"

            if q == total_questions

            else "다음"
        )


        if st.button(

            button_label,

            type="primary",

            use_container_width=True,

            key=
                f"next_{q}",
        ):

            if answer is None:

                st.warning(
                    "답을 선택해주세요."
                )


            else:

                save_current_answer(
                    answer
                )


                if q == total_questions:

                    st.session_state.page = (
                        "result"
                    )


                else:

                    st.session_state.question_no += 1

                    st.session_state.question_started_at = (
                        time.time()
                    )


                st.rerun()


# =========================================================
# RESULT PAGE
# =========================================================

def result_page():

    (
        accuracy,
        total_seconds,
        recommended_total,
        areas,

    ) = build_demo_result()


    difference = (
        total_seconds
        -
        recommended_total
    )


    if difference >= 0:

        difference_text = (
            "+"
            +
            mmss(difference)
        )

    else:

        difference_text = (
            "-"
            +
            mmss(abs(difference))
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
                학생의 현재 학습상태 예시입니다.

            </div>

        </div>


        <div class="metrics">

            <div class="metric">

                <div class="label">
                    전체 정확도
                </div>

                <div class="value">
                    {accuracy}%
                </div>

            </div>


            <div class="metric">

                <div class="label">
                    총 풀이시간
                </div>

                <div class="value">
                    {mmss(total_seconds)}
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

        </div>
        """
    )


    # -----------------------------------------------------
    # 영역별 정확도
    # -----------------------------------------------------

    bars = ""


    for area_name, data in areas.items():

        bars += f"""

        <div class="bar-row">

            <div class="bar-head">

                <span>
                    {area_name}
                </span>

                <b>
                    {data["accuracy"]}%
                </b>

            </div>

            <div class="bar-track">

                <div
                    class="bar-fill"
                    style="
                        width:{data["accuracy"]}%
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


    # -----------------------------------------------------
    # 영역별 시간
    # -----------------------------------------------------

    time_boxes = ""


    for area_name, data in areas.items():

        over = (
            data["actual"]
            -
            data["recommended"]
        )


        if over >= 0:

            over_text = (
                "+"
                +
                mmss(over)
            )

        else:

            over_text = (
                "-"
                +
                mmss(abs(over))
            )


        time_boxes += f"""

        <div class="time-box">

            <div class="t-title">
                {area_name}
            </div>

            <div class="t-sub">

                실제
                {mmss(data["actual"])}

                · 권장
                {mmss(data["recommended"])}

                ·
                {over_text}

            </div>

        </div>
        """


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


    # -----------------------------------------------------
    # 추천
    # -----------------------------------------------------

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
                    문제 해결
                </div>

            </div>

        </div>
        """
    )


    if st.session_state.phone:

        st.info(
            "점검 결과 수신 연락처: "
            +
            st.session_state.phone
        )


    # -----------------------------------------------------
    # 결과 저장
    # -----------------------------------------------------

    if st.button(

        "현재 결과 저장",

        type="primary",

        use_container_width=True,

        key=
            "save_result",
    ):

        record = {

            "time":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                ),

            "name":
                st.session_state.student_name,

            "level":
                st.session_state.level,

            "subject":
                st.session_state.subject,

            "phone":
                st.session_state.phone,

            "accuracy":
                accuracy,

            "total_time":
                mmss(total_seconds),
        }


        st.session_state.records.append(
            record
        )


        st.success(
            "현재 세션의 기록 목록에 저장했습니다."
        )


    home_col, records_col = st.columns(2)


    with home_col:

        if st.button(

            "처음으로",

            use_container_width=True,

            key=
                "result_home",
        ):

            reset_exam_state()


    with records_col:

        if st.button(

            "기록 보기",

            use_container_width=True,

            key=
                "result_records",
        ):

            st.session_state.page = "records"

            st.rerun()


# =========================================================
# RECORDS PAGE
# =========================================================

def records_page():

    st.html(
        """
        <div class="records-title">
            점검 기록
        </div>

        <div class="records-sub">
            결과 전달을 희망한 연락처와
            점검 결과를 간단히 확인합니다.
        </div>
        """
    )


    if not st.session_state.records:

        st.info(
            "아직 저장된 점검 기록이 없습니다."
        )


    else:

        for record in reversed(
            st.session_state.records
        ):

            phone = (

                record["phone"]

                if record["phone"]

                else "연락처 미입력"
            )


            st.html(

                f"""
                <div class="record-card">

                    <div class="record-top">

                        <div>

                            <div class="record-name">

                                {record["name"]}
                                ·
                                {record["level"]}
                                ·
                                {record["subject"]}

                            </div>

                            <div class="record-meta">

                                {record["time"]}

                            </div>

                        </div>


                        <div class="record-phone">

                            {phone}

                        </div>

                    </div>


                    <div class="record-score">

                        정확도
                        {record["accuracy"]}%

                        ·

                        총 풀이시간
                        {record["total_time"]}

                    </div>

                </div>
                """
            )


    if st.button(

        "메인으로 돌아가기",

        use_container_width=True,

        key=
            "records_home",
    ):

        st.session_state.page = "home"

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


else:

    st.session_state.page = "home"

    st.rerun()
