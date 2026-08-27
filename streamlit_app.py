import streamlit as st

st.set_page_config(
    page_title="우리아이 학습점검",
    page_icon="📘",
    layout="centered",
    initial_sidebar_state="collapsed",
)

LEVELS = [
    "5세", "6세", "7세",
    "초1", "초2", "초3", "초4", "초5", "초6",
    "중1", "중2", "중3"
]


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


if "level" not in st.session_state:
    st.session_state.level = None

if "subject" not in st.session_state:
    st.session_state.subject = None


# =========================================================
# STYLE
# =========================================================

st.html("""
<style>

:root {
    --blue: #246FE5;
    --navy: #17324D;
    --muted: #6A7C8F;
    --border: #D7E2EC;
    --soft: #EEF6FF;
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
            #FFFFFF 38%
        );

    color: var(--navy);
}

.block-container {
    max-width: 760px;

    padding-top: 0.35rem;
    padding-bottom: 0.65rem;

    padding-left: 1rem;
    padding-right: 1rem;
}

#MainMenu,
footer,
header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    display: none !important;
}


/* =====================================================
   HERO
===================================================== */

.hero {
    text-align: center;
    margin: 0 0 10px 0;
}

.badge {
    display: inline-block;

    background: #EAF3FF;
    color: var(--blue);

    padding: 5px 12px;

    border-radius: 999px;

    font-size: 12px;
    font-weight: 900;

    margin-bottom: 8px;
}

.hero-title {
    font-size: 30px;

    line-height: 1.18;

    font-weight: 900;

    letter-spacing: -1px;

    color: var(--navy);

    margin: 0;
}

.hero-title .accent {
    color: var(--blue);
}

.hero-sub {
    margin-top: 8px;

    color: var(--muted);

    font-size: 13px;

    line-height: 1.5;
}


/* =====================================================
   FEATURE CARDS
===================================================== */

.features {
    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 8px;

    margin: 10px 0 9px;
}

.feature {
    background: #FFFFFF;

    border:
        1px solid
        var(--border);

    border-radius: 13px;

    padding: 9px 5px 8px;

    text-align: center;
}

.feature .icon {
    color: var(--blue);

    font-size: 17px;

    line-height: 1;

    margin-bottom: 3px;

    font-weight: 900;
}

.feature .title {
    color: var(--navy);

    font-size: 12px;

    line-height: 1.2;

    font-weight: 900;
}

.feature .sub {
    color: #8A9AAB;

    font-size: 10px;

    line-height: 1.2;

    margin-top: 2px;
}


/* =====================================================
   NOTICE
===================================================== */

.notice {
    background: var(--soft);

    border:
        1px solid
        #DBEAFF;

    border-radius: 12px;

    padding: 9px 12px;

    color: #50667A;

    font-size: 11px;

    line-height: 1.45;

    margin: 0 0 10px;

    text-align: center;
}

.notice b {
    color: #1F66C7;
}


/* =====================================================
   LABEL
===================================================== */

.section-label {
    color: var(--navy);

    font-size: 13px;

    font-weight: 900;

    margin: 9px 0 5px;
}


/* =====================================================
   INPUT
===================================================== */

div[data-testid="stTextInput"] {
    margin-bottom: 0 !important;
}

div[data-testid="stTextInput"] input {

    min-height: 42px !important;
    height: 42px !important;

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
        10px !important;

    font-size:
        15px !important;

    padding-top:
        0 !important;

    padding-bottom:
        0 !important;
}

div[data-testid="stTextInput"]
input::placeholder {

    color:
        #9AABBC !important;

    -webkit-text-fill-color:
        #9AABBC !important;
}


/* =====================================================
   BUTTONS
===================================================== */

div.stButton {
    margin: 0 !important;
}

div.stButton > button {

    min-height:
        40px !important;

    height:
        40px !important;

    border-radius:
        10px !important;

    font-size:
        13px !important;

    font-weight:
        900 !important;

    padding:
        0.15rem 0.35rem !important;
}


/* 미선택 */

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


/* 선택 */

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


/* =====================================================
   STREAMLIT GAP COMPRESSION
===================================================== */

[data-testid="stVerticalBlock"] {
    gap:
        0.28rem !important;
}

[data-testid="stHorizontalBlock"] {
    gap:
        0.35rem !important;
}

div[data-testid="stAlert"] {

    padding:
        0.45rem 0.7rem !important;

    margin:
        0.15rem 0 0 !important;

    border-radius:
        10px !important;
}

div[data-testid="stAlert"] p {

    font-size:
        11px !important;

    line-height:
        1.35 !important;

    margin:
        0 !important;
}


/* =====================================================
   TABLET PORTRAIT
===================================================== */

@media (
    min-width: 700px
)
and (
    max-width: 900px
) {

    .block-container {
        max-width: 720px;
        padding-top: 0.2rem;
    }

    .hero-title {
        font-size: 28px;
    }

    .hero-sub {
        font-size: 12px;
    }
}


/* =====================================================
   MOBILE
===================================================== */

@media (
    max-width: 699px
) {

    .block-container {
        padding-top: 0.2rem;
        padding-left: 0.7rem;
        padding-right: 0.7rem;
    }

    .hero-title {
        font-size: 25px;
    }

    .hero-sub {
        font-size: 12px;
    }

    .features {
        gap: 5px;
    }

    .feature {
        padding: 8px 3px 7px;
    }

    .feature .title {
        font-size: 11px;
    }

    .feature .sub {
        font-size: 9px;
    }
}

</style>
""")


# =========================================================
# HERO
# =========================================================

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


# =========================================================
# 학생 이름
# =========================================================

st.html(
    '<div class="section-label">'
    '학생 이름'
    '</div>'
)

name = st.text_input(
    "학생 이름",
    placeholder="학생 이름을 입력해주세요",
    label_visibility="collapsed",
)


# =========================================================
# 학년
# =========================================================

st.html(
    '<div class="section-label">'
    '연령 / 학년'
    '</div>'
)


# 태블릿 세로 화면 기준
# 6개씩 2줄

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


# =========================================================
# 과목
# =========================================================

level = st.session_state.level


if level:

    if is_preschool(level):

        st.html(
            f"""
            <div
                class="notice"
                style="
                    margin-top:7px;
                    margin-bottom:2px;
                "
            >
                {level}
                ·
                <b>입학준비도 검사</b>
                ·
                한글 + 수 개념 통합
            </div>
            """
        )

    else:

        st.html(
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


# =========================================================
# 시작
# =========================================================

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

        st.success(
            "현재는 첫 화면 디자인 확인 단계입니다."
        )
