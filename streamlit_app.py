import streamlit as st

st.set_page_config(
    page_title="학습결손 진단",
    page_icon="📘",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f7f9fc;
    }

    .block-container {
        max-width: 720px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .main-card {
        background: white;
        padding: 32px;
        border-radius: 18px;
        border: 1px solid #e5e9f0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.04);
        margin-top: 20px;
    }

    .brand {
        font-size: 15px;
        color: #667085;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .title {
        font-size: 34px;
        font-weight: 800;
        color: #1d2939;
        line-height: 1.25;
        margin-bottom: 10px;
    }

    .subtitle {
        font-size: 16px;
        color: #667085;
        margin-bottom: 28px;
    }

    .info-box {
        background: #f2f6fb;
        border-radius: 12px;
        padding: 15px 18px;
        color: #475467;
        font-size: 14px;
        margin-bottom: 24px;
    }

    label {
        font-weight: 700 !important;
        color: #344054 !important;
    }

    .stTextInput input {
        background: white !important;
        color: #1d2939 !important;
        border-radius: 10px !important;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        background: white !important;
        color: #1d2939 !important;
        border-radius: 10px !important;
    }

    div.stButton > button {
        width: 100%;
        height: 52px;
        border-radius: 10px;
        font-size: 17px;
        font-weight: 700;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="brand">ACADEMY LEARNING DIAGNOSTIC</div>', unsafe_allow_html=True)
st.markdown('<div class="title">학습결손 진단</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">초등 3학년부터 중등 3학년까지<br>영어·수학 학습 상태를 확인합니다.</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="info-box">
        약 15~20분 동안 문항에 응답하면
        학습 취약 영역과 보완이 필요한 선수개념을 분석합니다.
    </div>
    """,
    unsafe_allow_html=True
)

with st.container(border=True):
    name = st.text_input(
        "학생 이름",
        placeholder="학생 이름을 입력하세요"
    )

    grade = st.selectbox(
        "학년",
        ["초3", "초4", "초5", "초6", "중1", "중2", "중3"]
    )

    subject = st.radio(
        "진단 과목",
        ["영어", "수학"],
        horizontal=True
    )

    st.write("")

    if st.button("진단 시작", type="primary"):
        if not name.strip():
            st.warning("학생 이름을 입력해주세요.")
        else:
            st.success(
                f"{name} 학생의 {grade} {subject} 진단을 시작합니다."
            )

st.caption("진단 결과는 학생의 현재 학습상태를 파악하기 위한 참고자료로 활용됩니다.")
