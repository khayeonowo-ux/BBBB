import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="이차함수 그래프 평행이동 학습", layout="centered")

st.title("📈 이차함수 y = a(x - p)² + q 그래프 학습")

st.write("""
이 앱은 **이차함수 그래프의 평행이동**을 시각적으로 이해하도록 도와줍니다.  
- **p** 값은 그래프를 **x축 방향으로 이동**시킵니다.  
- **q** 값은 그래프를 **y축 방향으로 이동**시킵니다.
""")

# 기본 함수 계수 a 선택
a = st.slider("a 값 (그래프의 모양)", min_value=-3.0, max_value=3.0, value=1.0, step=0.1)

# 평행이동 변수 p, q 슬라이더
p = st.slider("p 값 (x축 평행이동)", min_value=-5.0, max_value=5.0, value=0.0, step=0.5)
q = st.slider("q 값 (y축 평행이동)", min_value=-5.0, max_value=5.0, value=0.0, step=0.5)

# 데이터 생성
x = np.linspace(-10, 10, 400)
y_base = a * x**2
y_shifted = a * (x - p)**2 + q

# 그래프 출력
fig, ax = plt.subplots()
ax.plot(x, y_base, label=f"기준: y = {a}x²", color="gray", linestyle="--")
ax.plot(x, y_shifted, label=f"이동된 그래프: y = {a}(x - {p})² + {q}", color="blue")
ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend()
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("이차함수의 평행이동")

st.pyplot(fig)

# 설명
st.markdown(f"""
### 그래프 해석
- **p = {p}** → 그래프가 **x축 방향으로 {'오른쪽' if p > 0 else '왼쪽' if p < 0 else '이동 없음'}으로 {abs(p)}만큼 이동**
- **q = {q}** → 그래프가 **y축 방향으로 {'위쪽' if q > 0 else '아래쪽' if q < 0 else '이동 없음'}으로 {abs(q)}만큼 이동**
""")

st.info("💡 팁: a의 부호가 바뀌면 그래프의 **모양(위로 볼록 / 아래로 볼록)**도 달라집니다.")
