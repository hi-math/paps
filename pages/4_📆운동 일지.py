import streamlit as st
#from streamlit_option_menu import option_menu
#pip install streamlit-option-menu 필수
import pandas as pd

# 운동 일지 내용을 표시
title_html = """
<h1 style='text-align: center; color: navy; border-bottom: 2px solid gray;'>우리의 운동 일지</h1>
"""
st.markdown(title_html, unsafe_allow_html=True)

def main():
    st.subheader("오늘의 운동 기록 :medal: ")
    exercise_factor = st.selectbox('오늘 기를 체력 요인', ['심폐지구력', '유연성', '근력/근지구력', '순발력'])
    exercise_type = st.selectbox('운동 종류', ['셔틀런', '앉아 윗몸 앞으로 굽히기', '악력', '제자리 멀리뛰기', '유산소'])
    exercise_time = st.number_input('운동 시간 (분)', min_value=0)
    exercise_achievement = st.slider('달성도', min_value=1, max_value=10)

    if st.button('저장'):
        save_exercise_log(exercise_type, exercise_time, exercise_achievement)
        #그림을 팝업
        image_source = "https://drive.google.com/uc?id=1-f9AuVu0a-NQFqNWy1187LVxNd3TeclC"
        st.image(image_source, use_column_width=False, width=500)
        st.success('운동일지가 저장되었습니다.')

def save_exercise_log(exercise_type, exercise_time, exercise_achievement):
    # 운동일지를 저장하는 코드를 작성하세요. 데이터베이스에 저장하거나 파일로 저장할 수 있습니다.
    pass

if __name__ == '__main__':
    main()