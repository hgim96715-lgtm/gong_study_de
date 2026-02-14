import streamlit as st

st.title("Streamlit widgets Demo")

name=st.text_input("Enter your name:")

age=st.slider("Select your age",0,100,25)

language=st.selectbox("가장 좋아하는 언어는?",
                      ["Python","JavaScript","Java"])

if st.button("Submit"):
    st.write(f"안녕하세요🤗 {name}님 당신의 나이는 {age}이고 제일 좋아하는 언어는 {language}이군요 {name}님에 대해 정보를 알게 되어서 즐거워요")
    