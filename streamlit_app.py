import re
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


for key, default in {
    "level": None,
    "subject": None,
    "student_name": "",
    "phone": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


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
    padding-bottom:1.4rem;

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
   HERO
===================================================== */

.hero {
    text-align:center;
    margin:0 0 20px;
}

.badge {
    display:inline-block;

    background:#EAF3FF;
    color:var(--blue);

    padding:7px 14px;

    border-radius:999px;

    font-size:13px;
    font-weight:900;

    margin-bottom:13px;
}

.hero-title {
    margin:0;

    color:var(--navy);

    font-size:35px;
    line-height:1.22;

    font-weight:900;

    letter-spacing:-1.1px;
}

.hero-title .accent {
    color:var(--blue);
}

.hero-sub {
    margin-top:10px;

    color:var(--muted);

    font-size:14px;

    line-height:1.6;
}


/* =====================================================
   FEATURE CARDS
===================================================== */

.features {
    display:grid;

    grid-template-columns:
        repeat(3,1fr);

    gap:12px;

    margin:17px 0 15px;
}

.feature {
    background:#FFFFFF;

    border:
        1px solid
        var(--border);

    border-radius:16px;

    padding:15px 10px 13px;

    text-align:center;
}

.feature .icon {
    font-size:20px;

    color:var(--blue);

    font-weight:900;

    margin-bottom:5px;
}

.feature .title {
    font-size:13px;

    color:var(--navy);

    font-weight:900;
}

.feature .sub {
    font-size:10px;

    color:#8A9AAB;

    margin-top:3px;
}


/* =====================================================
   NOTICE
===================================================== */

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
   LABELS
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

    font-size:
        16px !important;

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

    border-radius:11px !important;

    font-size:14px !important;

    font-weight:900 !important;

    padding:.2rem .45rem !important;
}


/* 미선택 */

div.stButton
> button[kind="secondary"] {

    background:#FFFFFF !important;

    color:#17324D !important;

    border:
        1px solid
        #CFDBE7 !important;
}

div.stButton
> button[kind="secondary"] * {

    color:#17324D !important;

    -webkit-text-fill-color:
        #17324D !important;
}

div.stButton
> button[kind="secondary"]:hover {

    background:#F4F8FC !important;

    border-color:#ABC3DD !important;

    color:#17324D !important;
}


/* 선택 */

div.stButton
> button[kind="primary"] {

    background:
        var(--blue) !important;

    color:#FFFFFF !important;

    border:
        1px solid
        var(--blue) !important;
}

div.stButton
> button[kind="primary"] * {

    color:#FFFFFF !important;

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

div[data-testid="stAlert"] {

    padding:.55rem .8rem !important;

    margin:.2rem 0 0 !important;

    border-radius:11px !important;
}

div[data-testid="stAlert"] p {

    font-size:12px !important;

    line-height:1.4 !important;

    margin:0 !important;
}


.start-note {
    margin:10px 0 4px;

    color:#8A9AAB;

    font-size:10px;

    text-align:center;
}


/* =====================================================
   TABLET PORTRAIT
===================================================== */

@media (
    min-width:700px
)
and (
    max-width:900px
) {

    .block-container {
        max-width:800px;

        padding-top:.65rem;
    }

    .hero-title {
        font-size:33px;
    }
}


/* =====================================================
   MOBILE
===================================================== */

@media (
    max-width:699px
) {

    .block-container {

        padding-top:.45rem;

        padding-left:.85rem;
        padding-right:.85rem;
    }

    .hero-title {
        font-size:27px;
    }

    .hero-sub {
        font-size:12px;
    }

    .features {
        gap:7px;
    }

    .feature {
        padding:11px 5px 10px;
    }

    .feature .title {
        font-size:12px;
    }

    .feature .sub {
        font-size:9px;
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

    value=
        st.session_state.student_name,

    placeholder=
        "학생 이름을 입력해주세요",

    label_visibility=
        "collapsed",
)


# =========================================================
# 연령 / 학년
# =========================================================

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
                not in
                subjects_for(level)
            ):

                st.session_state.subject = None

            st.rerun()


# =========================================================
# 점검 과목
# =========================================================

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

        subjects = subjects_for(
            level
        )

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
# 연락처 - 선택사항
# =========================================================

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
)


st.html(
    '<div class="start-note">'
    '연락처를 입력하지 않아도 '
    '학습점검을 진행할 수 있습니다.'
    '</div>'
)


# =========================================================
# 시작 버튼
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

        st.success(
            "현재는 메인페이지 디자인 확인 단계입니다."
        )
