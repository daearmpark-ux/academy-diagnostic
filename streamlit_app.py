import streamlit as st

st.title("학습결손 진단 시스템")
st.write("초3 ~ 중3 영어·수학 진단")

name = st.text_input("학생 이름")

grade = st.selectbox(
    "학년",
    ["초3", "초4", "초5", "초6", "중1", "중2", "중3"]
)

subject = st.radio(
    "과목",
    ["영어", "수학"]
)

if st.button("진단 시작"):
    st.success(f"{name} 학생의 {grade} {subject} 진단을 시작합니다.")
