import streamlit as st
import time

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
# SESSION STATE
# =========================================================

defaults = {
    "page": "home",
    "student_name": "",
    "level": None,
    "subject": None,
    "question_no": 1,
    "answers": {},
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# DESIGN SYSTEM
# =========================================================

st.markdown(
    """
    <style>

    /* ---------- 전체 ---------- */

    html, body, [class*="css"] {
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
                #F8FBFF 0px,
                #FFFFFF 360px
            );
        color: #172B4D;
    }

    .block-container {
        max-width: 760px;
        padding-top: 1.2rem;
        padding-bottom: 4rem;
        padding-left: 1.15rem;
        padding-right: 1.15rem;
    }

    /* Streamlit 기본 UI 최소화 */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    div[data-testid="stToolbar"] {
        visibility: hidden;
        height: 0;
    }


    /* ---------- 브랜드 ---------- */

    .brand-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 36px;
        color: #2474E5;
        font-size: 17px;
        font-weight: 800;
    }

    .brand-icon {
        width: 34px;
        height: 34px;
        border-radius: 10px;
        background: #2474E5;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 19px;
    }


    /* ---------- HERO ---------- */

    .hero {
        text-align: center;
        padding: 12px 4px 25px 4px;
    }

    .hero-badge {
        display: inline-block;
        padding: 7px 14px;
        background: #EAF3FF;
        color: #2474E5;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 800;
        margin-bottom: 17px;
    }

    .hero-title {
        font-size: 38px;
        line-height: 1.22;
        font-weight: 900;
        letter-spacing: -1.5px;
        color: #172B4D;
        margin-bottom: 15px;
    }

    .hero-title span {
        color: #2474E5;
    }

    .hero-subtitle {
        font-size: 16px;
        line-height: 1.75;
        color: #667085;
        margin: 0 auto;
        max-width: 570px;
    }


    /* ---------- 특징 ---------- */

    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin: 22px 0 25px 0;
    }

    .feature-card {
        background: #FFFFFF;
        border: 1px solid #E5ECF5;
        border-radius: 16px;
        padding: 18px 8px;
        text-align: center;
        box-shadow: 0 4px 14px rgba(24, 74, 120, 0.04);
    }

    .feature-icon {
        font-size: 24px;
        margin-bottom: 7px;
    }

    .feature-title {
        font-size: 13px;
        font-weight: 800;
        color: #344054;
    }

    .feature-text {
        font-size: 11px;
        color: #98A2B3;
        margin-top: 3px;
    }


    /* ---------- 안내 ---------- */

    .notice-box {
        background: #EEF6FF;
        border-radius: 15px;
        padding: 16px 18px;
        margin-bottom: 20px;
        color: #475467;
        font-size: 13px;
        line-height: 1.7;
    }

    .notice-title {
        color: #2474E5;
        font-weight: 800;
        margin-bottom: 3px;
    }


    /* ---------- 입력 카드 ---------- */

    .section-label {
        margin-top: 10px;
        margin-bottom: 7px;
        font-size: 14px;
        font-weight: 800;
        color: #344054;
    }

    div[data-testid="stTextInput"] input {
        min-height: 50px;
        border-radius: 12px !important;
        border: 1px solid #D8E0EA !important;
        background: #FFFFFF !important;
        color: #172B4D !important;
        font-size: 16px !important;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #2474E5 !important;
        box-shadow: 0 0 0 3px rgba(36,116,229,0.10) !important;
    }

    div[data-testid="stSelectbox"] > div > div {
        min-height: 50px;
        border-radius: 12px !important;
        background: white !important;
        color: #172B4D !important;
    }


    /* ---------- 버튼 ---------- */

    div.stButton > button {
        min-height: 50px;
        border-radius: 12px;
        font-weight: 800;
        font-size: 15px;
        transition: 0.15s ease;
    }

    div.stButton > button[kind="primary"] {
        background: #2474E5;
        border-color: #2474E5;
        color: white;
    }

    div.stButton > button[kind="primary"]:hover {
        background: #1765D2;
        border-color: #1765D2;
    }


    /* ---------- 검사화면 ---------- */

    .test-top {
        margin-bottom: 18px;
    }

    .test-category {
        color: #2474E5;
        font-size: 13px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .test-title {
        color: #172B4D;
        font-size: 24px;
        font-weight: 900;
        margin-bottom: 5px;
    }

    .progress-text {
        color: #667085;
        font-size: 13px;
    }

    .progress-bg {
        width: 100%;
        height: 8px;
        background: #E8EEF6;
        border-radius: 100px;
        margin: 12px 0 28px 0;
        overflow: hidden;
    }

    .progress-bar {
        height: 100%;
        background: #2474E5;
        border-radius: 100px;
    }

    .question-card {
        background: white;
        border: 1px solid #E4EAF2;
        border-radius: 20px;
        padding: 28px 22px;
        margin-bottom: 18px;
        box-shadow: 0 5px 20px rgba(26, 71, 116, 0.05);
    }

    .question-number {
        color: #2474E5;
        font-size: 13px;
        font-weight: 900;
        margin-bottom: 13px;
    }

    .question-text {
        color: #172B4D;
        font-size: 20px;
        line-height: 1.6;
        font-weight: 800;
    }


    /* ---------- 결과 ---------- */

    .result-hero {
        text-align: center;
        margin: 12px 0 26px 0;
    }

    .result-check {
        width: 62px;
        height: 62px;
        margin: auto;
        border-radius: 50%;
        background: #EAF4FF;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #2474E5;
        font-size: 30px;
        margin-bottom: 13px;
    }

    .result-title {
        color: #172B4D;
        font-size: 28px;
        font-weight: 900;
    }

    .result-subtitle {
        color: #667085;
        margin-top: 5px;
        font-size: 14px;
    }

    .metric-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin-bottom: 22px;
    }

    .metric-card {
        background: white;
        border: 1px solid #E5EAF1;
        border-radius: 16px;
        padding: 18px 8px;
        text-align: center;
    }

    .metric-label {
        color: #667085;
        font-size: 12px;
        margin-bottom: 5px;
    }

    .metric-value {
        color: #172B4D;
        font-size: 21px;
        font-weight: 900;
    }

    .result-section {
        background: white;
        border: 1px solid #E5EAF1;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 15px;
    }

    .result-section-title {
        font-size: 16px;
        color: #172B4D;
        font-weight: 900;
        margin-bottom: 16px;
    }

    .result-row {
        margin-bottom: 16px;
    }

    .result-row-head {
        display: flex;
        justify-content: space-between;
        font-size: 13px;
        margin-bottom: 6px;
        color: #475467;
    }

    .result-track {
        height: 8px;
        border-radius: 100px;
        background: #E9EEF5;
        overflow: hidden;
    }

    .result-fill {
        height: 100%;
        border-radius: 100px;
        background: #2474E5;
    }

    .recommend-box {
        border-radius: 14px;
        background: #F7FAFD;
        padding: 15px 16px;
        margin-bottom: 9px;
    }

    .recommend-label {
        color: #2474E5;
        font-size: 12px;
        font-weight: 900;
        margin-bottom: 3px;
    }

    .recommend-text {
        color: #344054;
        font-size: 14px;
        font-weight: 700;
    }


    /* ---------- 개인정보 ---------- */

    .phone-box {
        margin-top: 20px;
        padding: 20px;
        background: #F7FAFD;
        border-radius: 18px;
    }

    .phone-title {
        color: #172B4D;
        font-size: 17px;
        font-weight: 900;
        margin-bottom: 4px;
    }

    .phone-description {
        color: #667085;
        font-size: 12px;
        line-height: 1.6;
        margin-bottom: 10px;
    }


    /* ---------- 모바일 ---------- */

    @media (max-width: 600px) {

        .block-container {
            padding-top: 0.8rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .brand-row {
            margin-bottom: 22px;
        }

        .hero {
            padding-top: 5px;
        }

        .hero-title {
            font-size: 31px;
        }

        .hero-subtitle {
            font-size: 14px;
        }

        .feature-grid {
            gap: 7px;
        }

        .feature-card {
            padding: 14px 4px;
        }

        .feature-title {
            font-size: 12px;
        }

        .feature-text {
            font-size: 10px;
        }

        .metric-value {
            font-size: 18px;
        }

        .question-text {
            font-size: 18px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HELPER
# =========================================================

LEVELS = [
    "5세", "6세", "7세",
    "초1", "초2", "초3", "초4", "초5", "초6",
    "중1", "중2", "중3"
]


def is_preschool(level):
    return level in ["5세", "6세", "7세"]


def available_subjects(level):

    if level in ["초1", "초2"]:
        return ["국어", "영어", "수학"]

    if level in [
        "초3", "초4", "초5", "초6",
        "중1", "중2", "중3"
    ]:
        return ["영어", "수학"]

    return []


def go(page):
    st.session_state.page = page
    st.rerun()


# =========================================================
# HOME PAGE
# =========================================================

def home_page():

    st.markdown(
        """
        <div class="brand-row">
            <div class="brand-icon">✓</div>
            <div>LEARNING CHECK</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero">
            <div class="hero-badge">5세부터 중학교 3학년까지</div>

            <div class="hero-title">
                우리 아이의 학습상태를<br>
                <span>가볍게 확인해보세요</span>
            </div>

            <div class="hero-subtitle">
                짧은 학습점검을 통해 현재 잘 준비된 부분과<br>
                조금 더 연습하면 좋은 부분을 확인합니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="feature-grid">

            <div class="feature-card">
                <div class="feature-icon">✓</div>
                <div class="feature-title">간편한 점검</div>
                <div class="feature-text">약 5~10분</div>
            </div>

            <div class="feature-card">
                <div class="feature-icon">▥</div>
                <div class="feature-title">영역별 확인</div>
                <div class="feature-text">정확도 · 풀이시간</div>
            </div>

            <div class="feature-card">
                <div class="feature-icon">↗</div>
                <div class="feature-title">맞춤 학습추천</div>
                <div class="feature-text">결과 즉시 확인</div>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="notice-box">
            <div class="notice-title">검사 안내</div>
            유아는 <b>입학준비도 검사</b>,
            초·중등 학생은 <b>우리아이 학습점검</b>으로 진행됩니다.
            실제 진단문항은 UI 확정 후 적용합니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-label">학생 이름</div>',
        unsafe_allow_html=True,
    )

    name = st.text_input(
        "학생 이름",
        value=st.session_state.student_name,
        placeholder="학생 이름을 입력해주세요",
        label_visibility="collapsed",
    )

    st.markdown(
        '<div class="section-label">연령 / 학년</div>',
        unsafe_allow_html=True,
    )

    level = st.selectbox(
        "연령 또는 학년",
        ["선택해주세요"] + LEVELS,
        label_visibility="collapsed",
    )

    if level != "선택해주세요":

        st.session_state.level = level

        if is_preschool(level):

            st.session_state.subject = "한글 · 수 개념"

            st.info(
                f"{level}는 **입학준비도 검사**로 진행됩니다. "
                "한글과 수 개념을 함께 확인합니다."
            )

        else:

            subjects = available_subjects(level)

            st.markdown(
                '<div class="section-label">점검 과목</div>',
                unsafe_allow_html=True,
            )

            cols = st.columns(len(subjects))

            for index, subject in enumerate(subjects):

                with cols[index]:

                    button_type = (
                        "primary"
                        if st.session_state.subject == subject
                        else "secondary"
                    )

                    if st.button(
                        subject,
                        use_container_width=True,
                        type=button_type,
                        key=f"subject_{subject}",
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

            st.warning("학생 이름을 입력해주세요.")

        elif level == "선택해주세요":

            st.warning("연령 또는 학년을 선택해주세요.")

        elif not is_preschool(level) and not st.session_state.subject:

            st.warning("점검 과목을 선택해주세요.")

        else:

            st.session_state.student_name = name.strip()
            st.session_state.question_no = 1
            st.session_state.answers = {}

            go("test")


# =========================================================
# TEST PAGE
# =========================================================

def test_page():

    level = st.session_state.level
    subject = st.session_state.subject

    preschool = is_preschool(level)

    service_name = (
        "입학준비도 검사"
        if preschool
        else "우리아이 학습점검"
    )

    total_questions = 15

    q = st.session_state.question_no

    progress = int((q / total_questions) * 100)

    st.markdown(
        f"""
        <div class="test-top">
            <div class="test-category">
                {service_name}
            </div>

            <div class="test-title">
                {st.session_state.student_name} 학생
            </div>

            <div class="progress-text">
                {level} · {subject} &nbsp;&nbsp; | &nbsp;&nbsp;
                {q} / {total_questions}
            </div>

            <div class="progress-bg">
                <div
                    class="progress-bar"
                    style="width:{progress}%">
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # UI 검토용 임시 문항
    # 실제 문항은 2차에서 교체
    # -----------------------------------------------------

    demo_questions = [

        {
            "question": "다음 중 알맞은 답을 골라주세요.",
            "choices": [
                "① 첫 번째 보기",
                "② 두 번째 보기",
                "③ 세 번째 보기",
                "④ 네 번째 보기",
            ],
        },

        {
            "question": "문제를 읽고 가장 알맞은 답을 선택해주세요.",
            "choices": [
                "① 선택지 A",
                "② 선택지 B",
                "③ 선택지 C",
                "④ 선택지 D",
            ],
        },

    ]

    demo = demo_questions[(q - 1) % len(demo_questions)]

    st.markdown(
        f"""
        <div class="question-card">

            <div class="question-number">
                QUESTION {q}
            </div>

            <div class="question-text">
                {demo["question"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    answer = st.radio(
        "답안",
        demo["choices"],
        index=None,
        label_visibility="collapsed",
        key=f"answer_{q}",
    )

    st.write("")

    col1, col2 = st.columns([1, 2])

    with col1:

        if q > 1:

            if st.button(
                "이전",
                use_container_width=True,
            ):
                st.session_state.question_no -= 1
                st.rerun()

    with col2:

        if q < total_questions:

            if st.button(
                "다음",
                type="primary",
                use_container_width=True,
            ):

                if answer is None:

                    st.warning("답을 선택해주세요.")

                else:

                    st.session_state.answers[q] = answer
                    st.session_state.question_no += 1
                    st.rerun()

        else:

            if st.button(
                "점검 완료",
                type="primary",
                use_container_width=True,
            ):

                if answer is None:

                    st.warning("답을 선택해주세요.")

                else:

                    st.session_state.answers[q] = answer
                    go("result")


# =========================================================
# RESULT PAGE
# =========================================================

def result_page():

    st.markdown(
        f"""
        <div class="result-hero">

            <div class="result-check">
                ✓
            </div>

            <div class="result-title">
                점검이 완료되었습니다
            </div>

            <div class="result-subtitle">
                {st.session_state.student_name} 학생의
                현재 학습상태를 확인해보세요.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # UI 검토용 임시 데이터
    # 2차에서 실제 채점값으로 교체

    st.markdown(
        """
        <div class="metric-grid">

            <div class="metric-card">
                <div class="metric-label">전체 정확도</div>
                <div class="metric-value">80%</div>
            </div>

            <div class="metric-card">
                <div class="metric-label">총 풀이시간</div>
                <div class="metric-value">7:42</div>
            </div>

            <div class="metric-card">
                <div class="metric-label">권장시간 대비</div>
                <div class="metric-value">+0:52</div>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="result-section">

            <div class="result-section-title">
                영역별 학습상태
            </div>

            <div class="result-row">
                <div class="result-row-head">
                    <span>기초 개념</span>
                    <b>90%</b>
                </div>
                <div class="result-track">
                    <div class="result-fill" style="width:90%"></div>
                </div>
            </div>

            <div class="result-row">
                <div class="result-row-head">
                    <span>개념 활용</span>
                    <b>75%</b>
                </div>
                <div class="result-track">
                    <div class="result-fill" style="width:75%"></div>
                </div>
            </div>

            <div class="result-row">
                <div class="result-row-head">
                    <span>문제 해결</span>
                    <b>65%</b>
                </div>
                <div class="result-track">
                    <div class="result-fill" style="width:65%"></div>
                </div>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="result-section">

            <div class="result-section-title">
                학습 추천
            </div>

            <div class="recommend-box">
                <div class="recommend-label">
                    잘 준비되어 있어요
                </div>
                <div class="recommend-text">
                    기초 개념
                </div>
            </div>

            <div class="recommend-box">
                <div class="recommend-label">
                    조금 더 연습하면 좋아요
                </div>
                <div class="recommend-text">
                    개념 활용
                </div>
            </div>

            <div class="recommend-box">
                <div class="recommend-label">
                    추가 확인을 추천해요
                </div>
                <div class="recommend-text">
                    문제 해결
                </div>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="phone-box">

            <div class="phone-title">
                점검결과를 휴대폰으로 받아보세요
            </div>

            <div class="phone-description">
                결과 전송을 희망하시면
                연락받으실 휴대폰 번호를 남겨주세요.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    phone = st.text_input(
        "휴대폰 번호",
        placeholder="010-0000-0000",
    )

    agree = st.checkbox(
        "점검결과 전달을 위한 개인정보 수집·이용에 동의합니다."
    )

    if st.button(
        "결과 전송 신청",
        use_container_width=True,
    ):

        if not phone.strip():

            st.warning("휴대폰 번호를 입력해주세요.")

        elif not agree:

            st.warning("개인정보 수집·이용 동의가 필요합니다.")

        else:

            st.success(
                "결과 전송 신청이 접수되었습니다. "
                "현재 화면은 UI 검토용으로 실제 저장은 아직 하지 않습니다."
            )

    st.write("")

    if st.button(
        "처음으로 돌아가기",
        use_container_width=True,
    ):

        st.session_state.page = "home"
        st.session_state.subject = None
        st.session_state.question_no = 1
        st.session_state.answers = {}

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
