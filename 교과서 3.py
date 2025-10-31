import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("📉 유리함수의 그래프 변형 시각화")
st.markdown("""
**함수식:**  
\\( y = \\frac{a}{x - p} + q \\)

왼쪽에서 **a, p, q 값을 조절**하면  
오른쪽에서 그래프가 즉시 변합니다.
""")

# 화면을 두 부분으로 나눔 (왼쪽: 슬라이더, 오른쪽: 그래프)
col1, col2 = st.columns([1, 2])  # 비율 조정 (1:2 비율로 오른쪽이 더 넓음)

with col1:
    st.subheader("🎛️ 조절 패널")
    a = st.slider("a (그래프의 모양)", -5.0, 5.0, 1.0, 0.1)
    p = st.slider("p (좌우 이동)", -5.0, 5.0, 0.0, 0.1)
    q = st.slider("q (상하 이동)", -5.0, 5.0, 0.0, 0.1)

with col2:
    st.subheader("📊 그래프 시각화")

    x = np.linspace(-10, 10, 400)
    y = a / (x - p) + q

    fig = go.Figure()

    # 유리함수 그래프
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='y = a/(x - p) + q'))

    # 점근선 표시 (수직, 수평)
    fig.add_vline(x=p, line=dict(color="red", dash="dash"), name="수직 점근선")
    fig.add_hline(y=q, line=dict(color="blue", dash="dash"), name="수평 점근선")

    fig.update_layout(
        title=f"y = {a:.1f}/(x - {p:.1f}) + {q:.1f}",
        xaxis_title="x",
        yaxis_title="y",
        width=700,
        height=500,
        template="plotly_white",
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)
