import streamlit as st
#from streamlit_option_menu import option_menu
#pip install streamlit-option-menu 필수
import pandas as pd

# 운동 계획표 내용을 표시
title_html = """
<h1 style='text-align: center; color: navy; border-bottom: 2px solid gray;'>우리의 운동 계획표 작성하기</h1>
"""

st.markdown(title_html, unsafe_allow_html=True)

st.header("체력 요인 :muscle: ")

options = ["심폐 지구력", "유연성", "근력/지구력", "순발력", "체지방"]

selected_option = st.radio("운동을 통해 키워 볼 체력 요인을 선택하기", options)

st.write(f"우리의 선택: {selected_option}")

st.header("운동 계획표 :star: ")    

data = {
    '월요일': '',
    '화요일': '',
    '수요일': '',
    '목요일': '',
    '금요일': ''
}

for day in data:
    data[day] = st.text_input(day, data[day])

st.table([data])