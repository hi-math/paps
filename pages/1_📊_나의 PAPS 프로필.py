import streamlit as st
#from streamlit_option_menu import option_menu
#pip install streamlit-option-menu 필수
import pandas as pd
from math import pi
import random
import matplotlib.pyplot as plt
from streamlit_extras.switch_page_button import switch_page
#from PIL import Image
# pip install streamlit_extras 필수

plt.rcParams['font.family'] = 'Malgun Gothic'

# 나의 PAPS 프로필에 대한 내용을 표시
title_html = """
    <h1 style='text-align: center; color: navy; border-bottom: 2px solid gray;'>PAPS 프로필</h1>
    """

st.markdown(title_html, unsafe_allow_html=True)

    # 데이터 준비
df = pd.DataFrame({
'Character': [st.session_state.user_name],
'Cardiorespiratory Endurance': [st.session_state.result_grade[st.session_state.exercise[0]]],
'Flexibility': [st.session_state.result_grade[st.session_state.exercise[1]]],
'Muscular Strength and Endurance': [st.session_state.result_grade[st.session_state.exercise[2]]],
'Agility': [st.session_state.result_grade[st.session_state.exercise[3]]],
'Body Mass Index (BMI)': [st.session_state.result_grade[st.session_state.exercise[4]]]
})

# 전체 등급 평균 구하기
average_grade=sum(st.session_state.result_grade.values()) / len(st.session_state.result_grade)

#오각형 그리기
labels = df.columns[1:]
num_labels = len(labels)
    
angles = [x/float(num_labels)*(2*pi) for x in range(num_labels)] # 각 등분점
angles += angles[:1] # 시작점으로 다시 돌아와야하므로 시작점 추가
    
my_palette = plt.cm.get_cmap("Set2", 10)
fig = plt.figure(figsize=(15,20))
fig.set_facecolor('white')
for i, row in df.iterrows():
    color = my_palette(random.randint(1, 10))
    data = df.iloc[i].drop('Character').tolist()
    data += data[:1]
    
    ax = plt.subplot(3,2,i+1, polar=True)
    ax.set_theta_offset(pi / 2) # 시작점
    ax.set_theta_direction(-1) # 그려지는 방향 시계방향
    
    plt.xticks(angles[:-1], labels, fontsize=20) # x축 눈금 라벨
    ax.tick_params(axis='x', which='major', pad=15) # x축과 눈금 사이에 여백을 준다.
    ax.set_rlabel_position(0) ## y축 각도 설정(degree 단위)
    plt.yticks([5,4,3,2,1],['5grade','4grade','3grade','2grade','1grade'], fontsize=16) # y축 눈금 설정
    plt.ylim(6,1)
    
    ax.plot(angles, data, color=color, linewidth=2, linestyle='solid') # 레이더 차트 출력
    ax.fill(angles, data, color=color, alpha=0.4) ## 도형 안쪽에 색을 채워준다.
    
    #plt.title(row.Character, size=22, color=color, x=0.0, y=1.0, ha='left') # 타이틀은 캐릭터 클래스로 한다.

plt.tight_layout(pad=5) ## subplot간 패딩 조절

# 이미지 경로 설정 (성별 & 등급에 따른 이미지 바꿈) 
# 성별에 따라 이미지 달라지지 않으므로(여 1등급 이미지 = 남 1등급 이미지) 성별 삭제함(수진)

if average_grade <= 2.0:
    image_source = "https://drive.google.com/uc?id=1-SBQHSZGqN5VGBKbeYx5XjDqwhertJ90" #평균 1~2등급
elif average_grade <= 3.0:
    image_source = "https://drive.google.com/uc?id=1-UiPfTgUftn_BMyta5urfBzfPkagsMe2" #평균 2~3등급
elif average_grade <= 4.0:
    image_source = "https://drive.google.com/uc?id=1-ZF6BtQ81J3aDiTFChSSRwIX3yArvUs2" #평균 3~4등급
else:
    image_source = "https://drive.google.com/uc?id=1-ePHddrT45L0sK_M6VK036HHm92rGsXd" #평균 4~5등급

    

# 2열 2행의 colume 생성
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# 1열 1행: 등급별 이미지 삽입
with col1:
    st.image(image_source, use_column_width=False, width=300)

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


# 1열 2행: 오각형 그림
with col2:
    st.pyplot(fig)

#2열 1행: 나의 PAPS 측정 결과값
with col3:
    st.info('심폐지구력(Cardiorespiratory Endurance)')
    result0 = f'{st.session_state.exercise[0]}: {st.session_state.records_list[0]}'
    st.write(result0)
    st.info('유연성(Flexibility)')
    result1 = f'{st.session_state.exercise[1]}: {st.session_state.records_list[1]}'
    st.write(result1)
    st.info('근력. 근지구력(Muscular Strength and Enduranc)')
    result2 = f'{st.session_state.exercise[2]}: {st.session_state.records_list[2]}'
    st.write(result2)
    st.info('순발력(Agility)')
    result3 = f'{st.session_state.exercise[3]}: {st.session_state.records_list[3]}'
    st.write(result3)
    st.info('체질량지수(Body Mass Index (BMI))')
    result4 = f'{st.session_state.exercise[4]}: {st.session_state.records_list[4]}'
    st.write(result4)
    st.success('평균등급')
    result5 = f'평균등급: {average_grade}'
    st.write(result5)

# 2열 2행: 그래프로 나타내기
with col4:
    # 5개의 서브플롯을 세로로 배치
    fig, axs = plt.subplots(5, 1, figsize=(5, 5))  # figsize는 전체 figure의 크기를 조정합니다.

    subplot_names = ["Cardiorespiratory Endurance", "Flexibility", "Muscular Strength and Endurance", "Agility", "Body Mass Index (BMI)"]

    # 각 서브플롯에 대한 내용을 반복문을 통해 설정
    for i in range(len(st.session_state.records_list)) : 
        axs[i].scatter(st.session_state.result_grade[st.session_state.exercise[i]], 0, color='#50586C')
        axs[i].set_title(subplot_names[i])
        axs[i].set_xticks([0.5,1,2,3,4,5,5.5])
        axs[i].set_xticklabels(['','1grade','2grade','3grade','4grade','5grade',''])
        axs[i].get_yaxis().set_visible(False)
        axs[i].set_facecolor('#DCE2F0')

    # 서브플롯 간의 간격 조정
    plt.tight_layout()

    # 그래프 보여주기
    st.pyplot(fig)

if st.button("처방전 생성"):
    # 처방전 생성 버튼이 클릭되었을 때 수행할 작업
    switch_page("운동 처방전")

    # st.subheader("PAPS 기본정보를 입력해주세요 :clipboard: ")
    # if st.button("PAPS 기본정보 입력하러 가기"):
    #     switch_page("PAPS")