import streamlit as st

st.set_page_config(
    page_title="우리아이 학습점검",
    page_icon="📘",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =========================================================
# STYLE
# =========================================================

st.html("""
<style>
:root {
    --blue:#246FE5;
    --navy:#17324D;
    --muted:#66788A;
    --border:#D7E2EC;
    --soft:#EEF6FF;
}

.stApp {
    background: linear-gradient(180deg, #F8FBFF 0%, #FFFFFF 42%);
    color: var(--navy);
}

.block-container {
    max-width: 760px;
    padding-top: 1.2rem;
    padding-left: 1rem;
    padding-right: 1rem;
    padding-bottom: 3rem;
}

#MainMenu, footer, header {
    visibility: hidden;
}

/* ---------- 상단 ---------- */

.brand {
    display:flex;
    align-items:center;
    gap:10px;
    margin-bottom:28px;
}

.brand-mark {
    width:38px;
    height:38px;
    border-radius:11px;
    background:var(--blue);
    color:white;
    display:flex;
    align-items:center;
    justify-content:center;
    font-weight:900;
}

.brand-name {
    font-size:14px;
    font-weight:900;
    color:#315577;
}

/* ---------- 메인 타이틀 ---------- */

.hero {
    text-align:center;
    margin-bottom:24px;
}

.badge {
    display:inline-block;
    background:#EAF3FF;
    color:var(--blue);
    padding:7px 14px;
    border-radius:999px;
    font-size:13px;
    font-weight:900;
    margin-bottom:15px;
}

.hero-title {
    font-size:38px;
    line-height:1.25;
    font-weight:900;
    letter-spacing:-1.2px;
    color:var(--navy);
    margin-bottom:14px;
}

.hero-title .accent {
    color:var(--blue);
}

.hero-sub {
    font-size:15px;
    line-height:1.7;
    color:var(--muted);
}

/* ---------- 특징 ---------- */

.features {
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:10px;
    margin:24px 0 20px;
}

.feature {
    background:#fff;
    border:1px solid var(--border);
    border-radius:16px;
    padding:16px 8px;
    text-align:center;
}

.feature .icon {
    font-size:22px;
    margin-bottom:6px;
}

.feature .title {
    font-size:13px;
    font-weight:900;
    color:var(--navy);
}

.feature .sub {
    font-size:11px;
    color:#8A9AAB;
    margin-top:3px;
}

/* ---------- 안내 ---------- */

.notice {
    background:var(--soft);
    border:1px solid #DBEAFF;
    border-radius:15px;
    padding:15px 17px;
    color:#4D6277;
    font-size:13px;
    line-height:1.65;
    margin-bottom:22px;
}

.section-label {
    color:var(--navy);
    font-size:15px;
    font-weight:900;
    margin:20px 0 10px;
}

/* ---------- 이름 입력 ---------- */

div[data-testid="stTextInput"] input {
    background:#fff !important;
    color:#17324D !important;
    -webkit-text-fill-color:#17324D !important;
    border:1px solid #CFDBE7 !important;
    border-radius:12px !important;
    min-height:50px !important;
    font-size:16px !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color:#9AABBC !important;
    -webkit-text-fill-color:#9AABBC !important;
}

/* ---------- 버튼 공통 ---------- */

div.stButton > button {
    min-height:48px !important;
    border-radius:12px !important;
    font-size:15px !important;
    font-weight:900 !important;
}

/* 미선택 버튼 */
div.stButton > button[kind="secondary"] {
    background:#FFFFFF !important;
    color:#17324D !important;
    border:1px solid #CFDBE7 !important;
}

div.stButton > button[kind="secondary"] * {
    color:#17324D !important;
    -webkit-text-fill-color:#17324D !important;
}

/* 선택된 버튼 */
div.stButton > button[kind="primary"] {
    background:#246FE5 !important;
    color:#FFFFFF !important;
    border:1px solid #246FE5 !important;
}

div.stButton > button[kind="primary"] * {
    color:#FFFFFF !important;
    -webkit-text-fill-color:#FFFFFF !important;
}

@media (max-width:600px) {
    .hero-title {
        font-size:31px;
    }

    .hero-sub {
        font-size:14px;
    }

    .features {
        gap:7px;
    }

    .feature {
        padding:13px 5px;
    }

    .feature .title {
        font-size:12px;
    }

    .feature .sub {
        font-size:10px;
    }
}
</style>
""")

# =========================================================
# STATE
# =========================================================

if "level" not in st.session_state:
    st.session_state.level = None

if "subject" not in st.session_state:
    st.session_state.subject = None


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


# =========================================================
# HERO
# =========================================================

st.html("""
<div class="brand">
    <div class="brand-mark">✓</div>
    <div class="brand-name">LEARNING CHECK</div>
</div>

<div class="hero">

    <div class="badge">
        5세부터 중학교 3학년까지
    </div>

    <div class="hero-title">
        우리 아이의 학습상태를<br>
        <span class="accent">가볍게 확인해보세요</span>
    </div>

    <div class="hero-sub">
        짧은 학습점검으로 현재 잘 준비된 부분과<br>
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
    5~7세는 <b>입학준비도 검사</b>로 한글과 수 개념을 함께 확인하고,
    초·중등 학생은 <b>우리아이 학습점검</b>으로 진행합니다.
</div>
""")

# =========================================================
# 학생 이름
# =========================================================

st.html('<div class="section-label">학생 이름</div>')

name = st.text_input(
    "학생 이름",
    placeholder="학생 이름을 입력해주세요",
    label_visibility="collapsed"
)

# =========================================================
# 학년
# =========================================================

st.html('<div class="section-label">연령 / 학년</div>')

for start in range(0, len(LEVELS), 4):

    cols = st.columns(4)

    for i, level in enumerate(LEVELS[start:start + 4]):

        selected = st.session_state.level == level

        if cols[i].button(
            level,
            use_container_width=True,
            type="primary" if selected else "secondary",
            key=f"level_{level}",
        ):

            st.session_state.level = level

            if is_preschool(level):

                st.session_state.subject = "한글 · 수 개념"

            else:

                if st.session_state.subject not in subjects_for(level):
                    st.session_state.subject = None

            st.rerun()

# =========================================================
# 과목
# =========================================================

level = st.session_state.level

if level:

    if is_preschool(level):

        st.info(
            f"{level}는 **입학준비도 검사**로 진행되며, "
            "한글과 수 개념을 함께 확인합니다."
        )

    else:

        st.html('<div class="section-label">점검 과목</div>')

        subjects = subjects_for(level)

        cols = st.columns(len(subjects))

        for i, subject in enumerate(subjects):

            selected = st.session_state.subject == subject

            if cols[i].button(
                subject,
                use_container_width=True,
                type="primary" if selected else "secondary",
                key=f"subject_{level}_{subject}",
            ):

                st.session_state.subject = subject
                st.rerun()

# =========================================================
# 시작 버튼
# =========================================================

st.write("")

if st.button(
    "학습점검 시작하기",
    type="primary",
    use_container_width=True,
):

    if not name.strip():

        st.warning("학생 이름을 입력해주세요.")

    elif not level:

        st.warning("연령 또는 학년을 선택해주세요.")

    elif not is_preschool(level) and not st.session_state.subject:

        st.warning("점검 과목을 선택해주세요.")

    else:

        st.success(
            "현재는 첫 화면 디자인 확인 단계입니다."
        )
