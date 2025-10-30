import streamlit as st
import random

st.title("🎰 로또 번호 생성기")

# 게임 수 선택
num_games = st.number_input("몇 게임을 생성할까요?", min_value=1, max_value=10, value=1, step=1)

# 생성 버튼
if st.button("🎲 번호 생성"):
    st.subheader(f"총 {num_games}개의 로또 번호 조합")
    for i in range(num_games):
        # 1~45 사이의 숫자 중 6개 무작위 선택
        numbers = sorted(random.sample(range(1, 46), 6))
        st.write(f"게임 {i+1}: 🎟️ {numbers}")
