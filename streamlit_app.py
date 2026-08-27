import re
import time
import textwrap
import streamlit as st

st.set_page_config(
    page_title="우리아이 학습점검",
    page_icon="📘",
    layout="centered",
    initial_sidebar_state="collapsed",
)

DEFAULTS = {
    "page": "home",
    "student_name": "",
    "level": None,
    "subject": None,
    "question_no": 1,
    "answers": {},
    "question_started_at": None,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


LEVELS = [
    "5세", "6세", "7세",
    "초1", "초2", "초3", "초4", "초5", "초6",
    "중1", "중2", "중3"
]


def html(block):
    st.markdown(
        textwrap.dedent(block).strip(),
        unsafe_allow_html=True
    )


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


def service_title(level):

    if is_preschool(level):
        return "입학준비도 검사"

    return "우리아이 학습점검"


def go(page):
    st.session_state.page = page
    st.rerun()


def reset_all():

    for key, value in DEFAULTS.items():
        st.session_state[key] = value

    st.rerun()


# =========================================================
# DESIGN
# =========================================================

html(
"""
<style>

:root {
    --bg: #f7fbff;
    --card: #ffffff;
    --text: #17324d;
    --muted: #66788a;
    --border: #d7e2ec;
    --accent: #246fe5;
    --accent-dark: #175ec7;
    --soft: #eaf3ff;
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
            #f7fbff 0,
            #ffffff 390px
        );
    color: var(--text);
}

.block-container {
    max-width: 760px;
    padding-top: 1rem;
    padding-bottom: 3rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

#MainMenu,
footer,
header[data-testid="stHeader"],
div[data-testid="stToolbar"] {
    visibility: hidden !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}


/* =============================
   BRAND
============================= */

.brand {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 4px 0 28px;
}

.brand-mark {
    width: 38px;
    height: 38px;
    border-radius: 11px;

    background:
        linear-gradient(
            135deg,
            #2f7df1,
            #185ecb
        );

    color: white;

    display: flex;
    align-items: center;
    justify-content: center;

    font-weight: 900;
}

.brand-name {
    font-size: 14px;
    font-weight: 900;
    color: #315577;
    letter-spacing: .2px;
}


/* =============================
   HERO
============================= */

.hero {
    text-align: center;
    margin-bottom: 24px;
}

.badge {
    display: inline-block;

    padding: 7px 14px;

    border-radius: 999px;

    background: var(--soft);
    color: var(--accent);

    font-size: 13px;
    font-weight: 900;

    margin-bottom: 15px;
}

.hero h1 {

    margin: 0;

    color: var(--text);

    font-size: 38px;
    line-height: 1.25;

    font-weight: 900;

    letter-spacing: -1.2px;
}

.hero h1 span {
    color: var(--accent);
}

.hero p {

    margin: 14px auto 0;

    color: var(--muted);

    font-size: 15px;
    line-height: 1.75;

    max-width: 560px;
}


/* =============================
   INFO CARDS
============================= */

.features {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 10px;

    margin: 24px 0 18px;
}

.feature {

    background: white;

    border:
        1px solid var(--border);

    border-radius: 16px;

    padding: 16px 8px;

    text-align: center;

    box-shadow:
        0 4px 16px
        rgba(44, 78, 110, .05);
}

.feature .icon {

    font-size: 21px;

    margin-bottom: 7px;
}

.feature .title {

    color: var(--text);

    font-size: 13px;

    font-weight: 900;
}

.feature .sub {

    color: #8a9aab;

    font-size: 11px;

    margin-top: 3px;
}


/* =============================
   NOTICE
============================= */

.notice {

    background: #eef6ff;

    border:
        1px solid #dbeaff;

    border-radius: 15px;

    padding: 15px 17px;

    color: #4d6277;

    font-size: 13px;

    line-height: 1.65;

    margin-bottom: 20px;
}

.notice b {
    color: #1e67c9;
}


.section-label {

    color: var(--text);

    font-size: 15px;

    font-weight: 900;

    margin:
        22px 0 10px;
}


/* =============================
   INPUT
============================= */

div[data-testid="stTextInput"] input {

    min-height: 52px !important;

    background:
        #ffffff !important;

    color:
        #17324d !important;

    -webkit-text-fill-color:
        #17324d !important;

    border:
        1px solid #cfdbe7 !important;

    border-radius:
        12px !important;

    font-size:
        16px !important;
}

div[data-testid="stTextInput"]
input::placeholder {

    color:
        #9aabbc !important;

    -webkit-text-fill-color:
        #9aabbc !important;
}

div[data-testid="stTextInput"]
input:focus {

    border-color:
        var(--accent) !important;

    box-shadow:
        0 0 0 3px
        rgba(36, 111, 229, .10)
        !important;
}


/* =============================
   BUTTONS
============================= */

div.stButton > button {

    min-height:
        48px !important;

    border-radius:
        12px !important;

    font-size:
        15px !important;

    font-weight:
        900 !important;
}


/* 미선택 버튼 */

div.stButton
> button[kind="secondary"] {

    background:
        #ffffff !important;

    color:
        #17324d !important;

    border:
        1px solid
        #cfdbe7 !important;
}

div.stButton
> button[kind="secondary"] p,

div.stButton
> button[kind="secondary"] span {

    color:
        #17324d !important;

    -webkit-text-fill-color:
        #17324d !important;
}


/* 미선택 hover */

div.stButton
> button[kind="secondary"]:hover,

div.stButton
> button[kind="secondary"]:focus {

    background:
        #f1f6fc !important;

    color:
        #17324d !important;

    border-color:
        #9ebce2 !important;
}


/* 선택 버튼 */

div.stButton
> button[kind="primary"] {

    background:
        var(--accent) !important;

    color:
        #ffffff !important;

    border:
        1px solid
        var(--accent) !important;
}

div.stButton
> button[kind="primary"] p,

div.stButton
> button[kind="primary"] span {

    color:
        #ffffff !important;

    -webkit-text-fill-color:
        #ffffff !important;
}


/* 선택 hover */

div.stButton
> button[kind="primary"]:hover,

div.stButton
> button[kind="primary"]:focus {

    background:
        var(--accent-dark) !important;

    color:
        #ffffff !important;

    border-color:
        var(--accent-dark) !important;
}


/* =============================
   RADIO
============================= */

div[data-testid="stRadio"] label,

div[data-testid="stRadio"] label p {

    color:
        #17324d !important;

    -webkit-text-fill-color:
        #17324d !important;

    font-size:
        15px !important;
}

div[data-testid="stRadio"]
div[role="radiogroup"] {

    gap: 10px;
}

div[data-testid="stRadio"] label {

    background:
        #ffffff !important;

    border:
        1px solid
        #cfdbe7 !important;

    border-radius:
        12px !important;

    padding:
        11px 14px !important;
}


/* =============================
   CHECKBOX
============================= */

div[data-testid="stCheckbox"] label,

div[data-testid="stCheckbox"] label p {

    color:
        #40566b !important;

    -webkit-text-fill-color:
        #40566b !important;

    font-size:
        13px !important;
}


/* =============================
   TEST
============================= */

.test-title {

    color:
        var(--accent);

    font-size:
        13px;

    font-weight:
        900;

    margin-bottom:
        4px;
}

.test-name {

    color:
        var(--text);

    font-size:
        26px;

    font-weight:
        900;

    margin-bottom:
        3px;
}

.test-meta {

    color:
        var(--muted);

    font-size:
        13px;
}

.track {

    height:
        8px;

    background:
        #e7eef6;

    border-radius:
        999px;

    overflow:
        hidden;

    margin:
        12px 0 24px;
}

.fill {

    height:
        100%;

    background:
        var(--accent);

    border-radius:
        999px;
}

.qcard {

    background:
        #ffffff;

    border:
        1px solid
        var(--border);

    border-radius:
        20px;

    padding:
        26px 22px;

    box-shadow:
        0 7px 24px
        rgba(42, 73, 104, .05);

    margin-bottom:
        14px;
}

.qnum {

    color:
        var(--accent);

    font-size:
        12px;

    font-weight:
        900;

    margin-bottom:
        12px;
}

.qtext {

    color:
        var(--text);

    font-size:
        20px;

    line-height:
        1.6;

    font-weight:
        900;
}


/* =============================
   RESULT
============================= */

.result-hero {

    text-align:
        center;

    padding:
        8px 0 22px;
}

.result-mark {

    width:
        58px;

    height:
        58px;

    border-radius:
        50%;

    background:
        var(--soft);

    color:
        var(--accent);

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    margin:
        0 auto 12px;

    font-size:
        28px;

    font-weight:
        900;
}

.result-title {

    color:
        var(--text);

    font-size:
        28px;

    font-weight:
        900;
}

.result-sub {

    color:
        var(--muted);

    font-size:
        14px;

    margin-top:
        5px;
}

.metrics {

    display:
        grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap:
        10px;

    margin-bottom:
        16px;
}

.metric {

    background:
        #ffffff;

    border:
        1px solid
        var(--border);

    border-radius:
        16px;

    padding:
        17px 8px;

    text-align:
        center;
}

.metric .label {

    color:
        var(--muted);

    font-size:
        11px;

    margin-bottom:
        5px;
}

.metric .value {

    color:
        var(--text);

    font-size:
        20px;

    font-weight:
        900;
}

.card {

    background:
        #ffffff;

    border:
        1px solid
        var(--border);

    border-radius:
        18px;

    padding:
        20px;

    margin-bottom:
        15px;
}

.card-title {

    color:
        var(--text);

    font-size:
        16px;

    font-weight:
        900;

    margin-bottom:
        16px;
}

.bar {

    margin-bottom:
        15px;
}

.bar-head {

    display:
        flex;

    justify-content:
        space-between;

    color:
        #42586e;

    font-size:
        13px;

    margin-bottom:
        6px;
}

.bar-track {

    height:
        9px;

    background:
        #e9eff5;

    border-radius:
        999px;

    overflow:
        hidden;
}

.bar-fill {

    height:
        100%;

    background:
        var(--accent);

    border-radius:
        999px;
}

.reco {

    background:
        #f7fafc;

    border:
        1px solid
        #edf1f5;

    border-radius:
        13px;

    padding:
        13px 14px;

    margin-bottom:
        8px;
}

.reco .label {

    color:
        var(--accent);

    font-size:
        11px;

    font-weight:
        900;

    margin-bottom:
        3px;
}

.reco .text {

    color:
        var(--text);

    font-size:
        14px;

    font-weight:
        900;
}


/* =============================
   MOBILE
============================= */

@media(max-width:600px) {

    .hero h1 {
        font-size:
            31px;
    }

    .hero p {
        font-size:
            14px;
    }

    .features {
        gap:
            7px;
    }

    .feature {
        padding:
            14px 5px;
    }

    .feature .title {
        font-size:
            12px;
    }

    .feature .sub {
        font-size:
            10px;
    }

    .qtext {
        font-size:
            18px;
    }

    .metric .value {
        font-size:
            18px;
    }
}

</style>
"""
)


# =========================================================
# HOME
# =========================================================

def home_page():

    html(
    """
    <div class="brand">

        <div class="brand-mark">
            ✓
        </div>

        <div class="brand-name">
            LEARNING CHECK
        </div>

    </div>


    <section class="hero">

        <div class="badge">
            5세부터 중학교 3학년까지
        </div>

        <h1>
            우리 아이의 학습상태를<br>
            <span>
                가볍게 확인해보세요
            </span>
        </h1>

        <p>
            짧은 학습점검으로
            현재 잘 준비된 부분과<br>
            조금 더 연습하면 좋은 부분을
            확인합니다.
        </p>

    </section>


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

        <b>
            검사 안내
        </b>

        <br>

        5~7세는
        <b>입학준비도 검사</b>로
        한글과 수 개념을 함께 확인하고,

        초·중등 학생은
        <b>우리아이 학습점검</b>으로
        진행합니다.

    </div>
    """
    )


    html(
        '<div class="section-label">학생 이름</div>'
    )


    name = st.text_input(
        "학생 이름",
        value=st.session_state.student_name,
        placeholder="학생 이름을 입력해주세요",
        label_visibility="collapsed",
    )


    html(
        '<div class="section-label">연령 / 학년</div>'
    )


    # 4개씩 3줄

    for start in range(
        0,
        len(LEVELS),
        4
    ):

        cols = st.columns(4)

        for idx, level in enumerate(
            LEVELS[start:start + 4]
        ):

            selected = (
                st.session_state.level
                == level
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

                st.session_state.level = level


                if is_preschool(level):

                    st.session_state.subject = (
                        "한글 · 수 개념"
                    )


                elif (
                    st.session_state.subject
                    not in subjects_for(level)
                ):

                    st.session_state.subject = None


                st.rerun()


    level = st.session_state.level


    if level:

        if is_preschool(level):

            st.session_state.subject = (
                "한글 · 수 개념"
            )


            st.info(
                f"{level}는 "
                f"**입학준비도 검사**로 진행되며 "
                f"한글과 수 개념을 함께 확인합니다."
            )


        else:

            html(
                '<div class="section-label">'
                '점검 과목'
                '</div>'
            )


            subjects = subjects_for(level)

            cols = st.columns(
                len(subjects)
            )


            for idx, subject in enumerate(
                subjects
            ):

                selected = (
                    st.session_state.subject
                    == subject
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

                    st.session_state.subject = subject

                    st.rerun()


    st.write("")


    if st.button(
        "학습점검 시작하기",

        type="primary",

        use_container_width=True,
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


        else:

            st.session_state.student_name = (
                name.strip()
            )

            st.session_state.question_no = 1

            st.session_state.answers = {}

            st.session_state.question_started_at = (
                time.time()
            )

            go("test")


# =========================================================
# TEST
# =========================================================

def test_page():

    total = 15

    q = st.session_state.question_no

    progress = round(
        q / total * 100
    )


    html(
    f"""
    <div class="test-title">
        {service_title(st.session_state.level)}
    </div>

    <div class="test-name">
        {st.session_state.student_name} 학생
    </div>

    <div class="test-meta">

        {st.session_state.level}

        ·

        {st.session_state.subject}

        &nbsp;|&nbsp;

        {q} / {total}

    </div>


    <div class="track">

        <div
            class="fill"
            style="width:{progress}%">
        </div>

    </div>


    <div class="qcard">

        <div class="qnum">
            QUESTION {q}
        </div>

        <div class="qtext">
            다음 중 알맞은 답을 골라주세요.
        </div>

    </div>
    """
    )


    choices = [

        "① 첫 번째 보기",

        "② 두 번째 보기",

        "③ 세 번째 보기",

        "④ 네 번째 보기",
    ]


    answer = st.radio(
        "답안",

        choices,

        index=None,

        label_visibility="collapsed",

        key=f"answer_{q}",
    )


    left, right = st.columns(
        [1, 2]
    )


    if (
        q > 1
        and
        left.button(
            "이전",
            use_container_width=True,
        )
    ):

        st.session_state.question_no -= 1

        st.session_state.question_started_at = (
            time.time()
        )

        st.rerun()


    label = (
        "점검 완료"
        if q == total
        else "다음"
    )


    if right.button(
        label,

        type="primary",

        use_container_width=True,
    ):

        if answer is None:

            st.warning(
                "답을 선택해주세요."
            )


        else:

            st.session_state.answers[q] = answer


            if q == total:

                go("result")


            else:

                st.session_state.question_no += 1

                st.session_state.question_started_at = (
                    time.time()
                )

                st.rerun()


# =========================================================
# RESULT
# =========================================================

def result_page():

    html(
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
                80%
            </div>

        </div>


        <div class="metric">

            <div class="label">
                총 풀이시간
            </div>

            <div class="value">
                7:42
            </div>

        </div>


        <div class="metric">

            <div class="label">
                권장시간 대비
            </div>

            <div class="value">
                +0:52
            </div>

        </div>

    </div>


    <div class="card">

        <div class="card-title">
            영역별 학습상태
        </div>


        <div class="bar">

            <div class="bar-head">

                <span>
                    기초 개념
                </span>

                <b>
                    90%
                </b>

            </div>

            <div class="bar-track">

                <div
                    class="bar-fill"
                    style="width:90%">
                </div>

            </div>

        </div>


        <div class="bar">

            <div class="bar-head">

                <span>
                    개념 활용
                </span>

                <b>
                    75%
                </b>

            </div>

            <div class="bar-track">

                <div
                    class="bar-fill"
                    style="width:75%">
                </div>

            </div>

        </div>


        <div class="bar">

            <div class="bar-head">

                <span>
                    문제 해결
                </span>

                <b>
                    65%
                </b>

            </div>

            <div class="bar-track">

                <div
                    class="bar-fill"
                    style="width:65%">
                </div>

            </div>

        </div>

    </div>


    <div class="card">

        <div class="card-title">
            학습 추천
        </div>


        <div class="reco">

            <div class="label">
                잘 준비되어 있어요
            </div>

            <div class="text">
                기초 개념
            </div>

        </div>


        <div class="reco">

            <div class="label">
                조금 더 연습하면 좋아요
            </div>

            <div class="text">
                개념 활용
            </div>

        </div>


        <div class="reco">

            <div class="label">
                추가 확인을 추천해요
            </div>

            <div class="text">
                문제 해결
            </div>

        </div>

    </div>


    <div class="notice">

        <b>
            점검결과를 휴대폰으로 받아보세요
        </b>

        <br>

        결과 전달을 희망하시면
        연락받으실 휴대폰 번호를
        남겨주세요.

    </div>
    """
    )


    phone = st.text_input(
        "휴대폰 번호",

        placeholder="010-0000-0000",
    )


    agree = st.checkbox(
        "점검결과 전달을 위한 "
        "개인정보 수집·이용에 동의합니다."
    )


    if st.button(
        "결과 전송 신청",

        use_container_width=True,
    ):

        if not phone.strip():

            st.warning(
                "휴대폰 번호를 입력해주세요."
            )


        elif not re.fullmatch(
            r"01[016789]-?\d{3,4}-?\d{4}",
            phone.strip(),
        ):

            st.warning(
                "휴대폰 번호 형식을 확인해주세요."
            )


        elif not agree:

            st.warning(
                "개인정보 수집·이용 동의가 필요합니다."
            )


        else:

            st.success(
                "현재는 디자인 검토 단계이므로 "
                "실제 저장은 아직 하지 않습니다."
            )


    st.write("")


    if st.button(
        "처음으로 돌아가기",

        use_container_width=True,
    ):

        reset_all()


# =========================================================
# ROUTER
# =========================================================

if st.session_state.page == "home":

    home_page()


elif st.session_state.page == "test":

    test_page()


elif st.session_state.page == "result":

    result_page()


else:

    reset_all()
