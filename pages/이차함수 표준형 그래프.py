import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="이차함수 그래프 표준형", layout="centered")

st.title("📘 이차함수 그래프 표준형 y = a(x - p)² + q")

st.markdown("""
이 앱은 **이차함수의 평행이동 원리**를 직관적으로 이해할 수 있도록 제작되었습니다.  
- `p` 값은 그래프를 **x축 방향**으로 이동시킵니다.  
- `q` 값은 그래프를 **y축 방향**으로 이동시킵니다.  
""")

# 슬라이더 입력
a = st.slider("a 값 (그래프의 모양)", -3.0, 3.0, 1.0, 0.1)
p = st.slider("p 값 (x축 평행이동)", -5.0, 5.0, 0.0, 0.5)
q = st.slider("q 값 (y축 평행이동)", -5.0, 5.0, 0.0, 0.5)

# 그래프 데이터
x = np.linspace(-10, 10, 400)
y_base = a * x**2
y_shift = a * (x - p)**2 + q

# Plotly 그래프
fig = go.Figure()

# 기준 그래프 (y = ax²)
fig.add_trace(go.Scatter(
    x=x, y=y_base,
    mode="lines",
    name=f"기준: y = {a}x²",
    line=dict(color="gray", dash="dash")
))

# 이동된 그래프 (y = a(x-p)² + q)
fig.add_trace(go.Scatter(
    x=x, y=y_shift,
    mode="lines",
    name=f"이동된 그래프: y = {a}(x - {p})² + {q}",
    line=dict(color="blue")
))

# 축 표시
fig.add_hline(y=0, line_color="black")
fig.add_vline(x=0, line_color="black")

# 그래프 설정
fig.update_layout(
    xaxis_title="x",
    yaxis_title="y",
    title="이차함수의 평행이동 (표준형)",
    legend=dict(x=0.02, y=0.98),
    width=700, height=500
)

st.plotly_chart(fig)

# 해석
st.markdown(f"""
### 그래프 해석
- **p = {p}** → 그래프가 **x축 방향으로 {'오른쪽' if p > 0 else '왼쪽' if p < 0 else '이동 없음'} {abs(p)}만큼 이동**  
- **q = {q}** → 그래프가 **y축 방향으로 {'위쪽' if q > 0 else '아래쪽' if q < 0 else '이동 없음'} {abs(q)}만큼 이동**
""")

st.info("💡 a값이 음수면 그래프가 아래로 볼록, |a|가 커질수록 그래프가 더 좁아집니다.")
