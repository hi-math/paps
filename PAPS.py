import streamlit as st
#from streamlit_option_menu import option_menu
#pip install streamlit-option-menu 필수
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
# pip install streamlit_extras 필수

df = pd.read_csv("dataframe(unit).csv", encoding='UTF-8')

#pd.read_excel("학생건강체력평가 데이터 프레임(단위).xlsx")

def calculate_bmi(weight, height):
    if height == 0:
        return 0
    # BMI 계산
    bmi = weight / (height * height) * 10000
    return round(bmi,2)

def classify_grades(exercise, records_list, school_level, gender):
    result = {}  # 종목별 등급 결과를 저장할 딕셔너리

    for i, exercise_name in enumerate(exercise):
        record = records_list[i]
        criteria_df = df[(df['종목'] == exercise_name) & (df['성별'] == gender) & (df['학교급'] == school_level)]
        # 종목별 등급 분류 기준을 설정
        grade_thresholds = [criteria_df['4등급'].values[0], criteria_df['3등급'].values[0], criteria_df['2등급'].values[0], criteria_df['1등급'].values[0]]
        
        # 등급 분류를 위한 함수
        if exercise_name == "50m 달리기 (초)":
            def classify_grade(score):
                for i in range(len(grade_thresholds)):
                    threshold = grade_thresholds[i]
                    if score > threshold:  # 기준값 이상인 경우
                        return len(grade_thresholds) - i + 1
                return 1 # 모든 기준을 통과하면 1등급
        else:
            def classify_grade(score):
                for i in range(len(grade_thresholds)):
                    threshold = grade_thresholds[i]
                    if score < threshold:
                        return len(grade_thresholds) - i + 1  # 5부터 2까지의 등급 반환
                return 1  # 모든 기준을 통과하면 1등급

        
        # 각 종목의 기록을 등급으로 변환
        result_grade = classify_grade(record)

        # 결과 딕셔너리에 종목과 해당 등급 추가
        result[exercise_name] = result_grade

    return result


filtered_df1 = df[df["신체능력"] == "심폐지구력"]
filtered_df2 = df[df["신체능력"] == "유연성"]
filtered_df3 = df[df["신체능력"] == "근력지구력"]
filtered_df4 = df[df["신체능력"] == "순발력"]


if 'user_name' not in st.session_state:
    st.session_state['user_name'] = ['']

if 'user_tall' not in st.session_state:
    st.session_state['user_tall'] = 0

if 'user_tall' not in st.session_state:
    st.session_state['school_level'] = ['']    

if 'gender' not in st.session_state:
    st.session_state['gender'] = ['']

if 'exercise' not in st.session_state:
  st.session_state['exercise'] = [[], [], [], [], []]

if 'records_list' not in st.session_state:
  st.session_state['records_list'] = [[], [], [], [], []]

if 'result_grade' not in st.session_state:
  st.session_state['result_grade'] = {}

if 'page' not in st.session_state:
    st.session_state['page'] = 0

title_html = """
<h1 style='text-align: center; color: navy; border-bottom: 2px solid gray;'>PAPS 측정 정보 입력</h1>
"""
st.markdown(title_html, unsafe_allow_html=True)

with st.form("기본정보"):
    st.subheader("기본 정보 :clipboard: ")
    if st.session_state.page == 0 :
        print(st.session_state.page)
        st.session_state.user_name = st.text_input("이름","") #백엔드는 이름을 넣으면 프로필에 보여지는 코드를 작성하세요
        st.session_state.user_tall = st.number_input("키(cm)", value=0.0, step=0.1) #두번째 인자는 비어있는 상태에서 시작하라는 의미
        st.session_state.user_weight = st.number_input("몸무게(kg)", value=0.0, step=0.1) #두번째 인자는 비어있는 상태에서 시작하라는 의미
        st.session_state.school_level = st.selectbox("학교급",df["학교급"].unique()) #이중에 초,중,고만 남기고, 
        st.session_state.gender = st.selectbox("성별",df["성별"].unique())
        st.subheader("체력 요인 :walking: ")
        st.markdown("**<심폐지구력>**")
        st.session_state.exercise[0] = st.selectbox("심폐지구력 종목",filtered_df1["종목"].unique())
        st.session_state.records_list[0] = st.number_input("심폐지구력 기록", value=0.0, step=0.1)

        st.markdown("**<유연성>**")
        st.session_state.exercise[1] = st.selectbox("유연성 종목",filtered_df2["종목"].unique())
        st.session_state.records_list[1] = st.number_input("유연성 기록", value=0.0, step=0.1)

        st.markdown("**<근력지구력>**")
        st.session_state.exercise[2] = st.selectbox("근력지구력 종목",filtered_df3["종목"].unique())
        st.session_state.records_list[2] = st.number_input("근력지구력 기록", value=0.0, step=0.1)

        st.markdown("**<순발력>**")
        st.session_state.exercise[3] = st.selectbox("순발력 종목",filtered_df4["종목"].unique())
        st.session_state.records_list[3] = st.number_input("순발력 기록", value=0.0, step=0.1)

        st.session_state.exercise[4] = "체질량지수 (BMI, kg/m2)"
        st.session_state.records_list[4] = calculate_bmi(st.session_state.user_weight, st.session_state.user_tall)

    #다른 페이지 넘어갔다가 다시 들어와도, 입력했던 정보가 사라지지 않게 하는 코드 작성(아래쪽)
    else:
        print(st.session_state.page)
        user_name = st.session_state.get("user_name", "")
        st.session_state.user_name = st.text_input("이름",user_name) #백엔드는 이름을 넣으면 프로필에 보여지는 코드를 작성하세요

        user_tall = st.session_state.get("user_tall", "")
        st.session_state.user_tall = st.number_input("키(cm)", value=user_tall, step=0.1) #두번째 인자는 비어있는 상태에서 시작하라는 의미
        
        user_weight = st.session_state.get("user_weight", "")
        
        st.session_state.user_weight = st.number_input("몸무게(kg)", value=user_weight, step=0.1) #두번째 인자는 비어있는 상태에서 시작하라는 의미
        school_level = st.session_state.get("school_level", "")

        if school_level == '초6':
            index_school = 1
        elif school_level == '중1':
            index_school = 2
        elif school_level == '중2':
            index_school = 3
        elif school_level == '중3':
            index_school = 4
        elif school_level == '고1':
            index_school = 5
        elif school_level == '고2':
            index_school = 6
        elif school_level == '고3':
            index_school = 7
        else :
            index_school = 0

        st.session_state.school_level = st.selectbox("학교급",df["학교급"].unique(), index = index_school) #이중에 초,중,고만 남기고, 

        gender = st.session_state.get("gender", "")

        if gender == '여':
            index_gender = 1
        else :
            index_gender = 0

        st.session_state.gender = st.selectbox("성별",df["성별"].unique(), index = index_gender)

        st.subheader("체력 요인 :walking: ")
        st.markdown("**<심폐지구력>**")

        # 기존 입력값 유지를 위해 copy
        exercise_copy = st.session_state.get("exercise", "")
        records_list_copy = st.session_state.get("records_list", "")

        if exercise_copy[0] == '오래달리기걷기 (초)':
            index_exercise0 = 1
        elif exercise_copy[0] == '스텝검사 (PEI)':
            index_exercise0 = 2
        else :
            index_exercise0 = 0

        st.session_state.exercise[0] = st.selectbox("심폐지구력 종목",filtered_df1["종목"].unique(), index = index_exercise0)

        st.session_state.records_list[0] = st.number_input("심폐지구력 기록", value=records_list_copy[0], step=0.1)

        st.markdown("**<유연성>**")

        if exercise_copy[1] == '종합유연성 (점수)':
            index_exercise1 = 1
        else :
            index_exercise1 = 0

        st.session_state.exercise[1] = st.selectbox("유연성 종목",filtered_df2["종목"].unique(), index = index_exercise1)
        
        records_list1 = st.session_state.get("records_list[1]", "")
        st.session_state.records_list[1] = st.number_input("유연성 기록", value=records_list_copy[1], step=0.1)

        st.markdown("**<근력지구력>**")


        if exercise_copy[2] == '윗몸말아올리기 (회)':
            index_exercise2 = 1
        elif exercise_copy[2] == '악력(kg, 양손 중 더 높은 무게)':
            index_exercise2 = 2
        else :
            index_exercise2 = 0

        st.session_state.exercise[2] = st.selectbox("근력지구력 종목",filtered_df3["종목"].unique(), index = index_exercise2)
        
        
        records_list2 = st.session_state.get("records_list[2]", "")
        st.session_state.records_list[2] = st.number_input("근력지구력 기록", value=records_list_copy[2], step=0.1)

        st.markdown("**<순발력>**")

        if exercise_copy[3] == '제자리멀리뛰기 (cm)':
            index_exercise3 = 1
        else :
            index_exercise3 = 0

        st.session_state.exercise[3] = st.selectbox("순발력 종목",filtered_df4["종목"].unique(), index = index_exercise3)
        
        records_list3 = st.session_state.get("records_list[3]", "")
        st.session_state.records_list[3] = st.number_input("순발력 기록", value=records_list_copy[3], step=0.1)

        st.session_state.exercise[4] = "체질량지수 (BMI, kg/m2)"
        st.session_state.records_list[4] = calculate_bmi(st.session_state.user_weight, st.session_state.user_tall)


    button = st.form_submit_button("프로필 생성")
    #st.link_button(다음 버튼으로, url, *, help=None, type="secondary", disabled=False, use_container_width=False)

    #user_tall_float=round(float(user_tall), 2)
    #user_weight_folat=round(float(user_weight), 2)

    if button:
        #print(st.session_state.exercise)
        #print(st.session_state.records_list)
        st.session_state.result_grade=classify_grades(st.session_state.exercise, st.session_state.records_list, st.session_state.school_level, st.session_state.gender)

        # 체질량 지수 등급 변화 강제 지정
        # 5등급 -> 2등급(마름)
        # 4등급 -> 1등급(정상)
        # 3등급 -> 2등급(경도 비만)
        # 2등급 -> 4등급(중도 비만)
        # 1등급 -> 5등급(과도 비만)
        
        st.session_state.page = 1

        #print(st.session_state.result_grade[st.session_state.exercise[4]])
        if st.session_state.result_grade[st.session_state.exercise[4]] == 1 :
            st.session_state.result_grade[st.session_state.exercise[4]] = 5
        elif st.session_state.result_grade[st.session_state.exercise[4]] == 2 :
            st.session_state.result_grade[st.session_state.exercise[4]] = 4
        elif st.session_state.result_grade[st.session_state.exercise[4]] == 3 :
            st.session_state.result_grade[st.session_state.exercise[4]] = 2
        elif st.session_state.result_grade[st.session_state.exercise[4]] == 4 :
           st.session_state.result_grade[st.session_state.exercise[4]] = 1
        elif st.session_state.result_grade[st.session_state.exercise[4]] == 5 :
            st.session_state.result_grade[st.session_state.exercise[4]] = 2
        print(st.session_state.result_grade[st.session_state.exercise[4]])

        switch_page("나의 PAPS 프로필")
        print(st.session_state.result_grade)

        # 프로필 생성 버튼이 클릭되었을 때 수행할 작업


