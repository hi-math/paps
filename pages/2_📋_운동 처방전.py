import streamlit as st
#from streamlit_option_menu import option_menu
#pip install streamlit-option-menu 필수
import pandas as pd 
# 운동 처방전 내용을 표시
import openai
#pip install openai
from streamlit_extras.switch_page_button import switch_page
# pip install streamlit_extras 필수

# OpenAI API 키 설정
api_key = "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"
openai.api_key = api_key

# Streamlit 앱 시작
title_html = """
    <h1 style='text-align: center; color: navy; border-bottom: 2px solid gray;'>고심이가 알려주는 운동 처방전</h1>
    """
st.markdown(title_html, unsafe_allow_html=True)

# 사용자 선택 옵션 추가
st.subheader("부족한 영역 중에서 개선하고 싶은 영역을 선택해봐! :point_up_2: ")

# 데이터 준비

df = pd.DataFrame({
    'Character': [st.session_state.user_name],
    '심폐지구력': [st.session_state.result_grade[st.session_state.exercise[0]]],
    '유연성': [st.session_state.result_grade[st.session_state.exercise[1]]],
    '근력지구력': [st.session_state.result_grade[st.session_state.exercise[2]]],
    '순발력': [st.session_state.result_grade[st.session_state.exercise[3]]],
    '체질량지수': [st.session_state.result_grade[st.session_state.exercise[4]]]
})

excellent_fitness = []
poor_fitness = []

for column in df.columns[1:]:
    value = df[column].values[0]  # 각 요소에 대한 값

    if value in [1, 2]:
        excellent_fitness.append(column)
    if value not in [1, 2, 3]:
        poor_fitness.append(column)

excellent_message = ', '.join(excellent_fitness)
poor_message = ', '.join(poor_fitness)

message = f"{st.session_state.user_name} 님의 우수한 체력 요소는 {excellent_message}이고, 부족한 체력 요소는 {poor_message}입니다."
st.warning(message)

areas = ["심폐지구력", "체지방", "유연성", "근력/근지구력", "체지방"]
selected_area = st.radio("선택한 영역으로 처방전을 적어줄게~", areas)

# 각 영역에 대한 운동처방 생성
if st.button("고심이의 운동 처방전"):
    if selected_area:
        prompt = f"{selected_area}을 개선시키는 운동방법 4가지를 처방전으로 작성해주세요."
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # GPT-3.5 Turbo 모델 선택
        messages=[{"role": "system", "content": "You are a helpful assistant that generates exercise prescriptions."}, {"role": "user", "content": prompt}],
        temperature=0.7,  # 난수 생성 확률 설정
        max_tokens=1000 # 생성할 토큰 수 제한 (적절한 값으로 조정)
        )
        prescription = response.choices[0].message["content"].strip()
        st.subheader(f"{selected_area}을 개선시키는 고심이의 운동처방전:")
        st.write(prescription)
    else:
        st.warning("부족한 영역 중에서 개선하고 싶은 영역을 선택해주세요.")
        pass
