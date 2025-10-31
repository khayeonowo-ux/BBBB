# pages/유리함수_그래프.py
import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="유리함수 그래프 변형", layout="centered")

st.title("📐 유리함수의 그래프 변형 —  y = a / (x - p) + q")

st.markdown("""
이 앱은 함수 \( y = \dfrac{a}{x - p} + q \) 에서 **p, q, a** 값 변화에 따른
- 그래프 이동(평행이동),
- 수평/수직 점근선( \(y=q\), \(x=p\) )
를 시각화합니다.
""")

# 컨트롤
col1, col2, col3 = st.columns(3)
with col1:
    a = st.slider("a (계수)", -5.0, 5.0, 1.0, 0.1)
with col2:
    p = st.slider("p (x축 평행이동 — 수직점근선 x=p)", -5.0, 5.0, 0.0, 0.1)
with col3:
    q = st.slider("q (y축 평행이동 — 수평점근선 y=q)", -10.0, 10.0, 0.0, 0.1)

# x 범위 설정
x_min, x_max = st.slider("x 범위", -20.0, 20.0, (-10.0, 10.0), step=0.5)
n_points = st.slider("샘플 점 개수 (각 분할마다)", 200, 5000, 800, step=100)

st.markdown("**설명:** 수직점근선 \(x=p\) 근처는 함수가 정의되지 않으므로, 그 주변을 잘라서 좌/우 분할 그래프를 표시합니다.")

# x 데이터: p 근처를 제외한 좌/우 두 구간
eps = 1e-3  # 아주 작은 간격
# 안전하게 p가 범위 밖이면 단일 구간으로 처리
if p <= x_min or p >= x_max:
    x = np.linspace(x_min, x_max, n_points)
    x_left = x
    x_right = np.array([])  # 빈 배열
else:
    x_left = np.linspace(x_min, p - eps, n_points//2)
    x_right = np.linspace(p + eps, x_max, n_points//2)

def rational_y(x_arr, a, p, q):
    return a / (x_arr - p) + q

y_left = rational_y(x_left, a, p, q) if x_left.size > 0 else np.array([])
y_right = rational_y(x_right, a, p, q) if x_right.size > 0 else np.array([])

# 표시용 DataFrame (Streamlit line_chart fallback)
df = pd.DataFrame({
    "x_left": x_left if x_left.size>0 else np.nan,
    "y_left": y_left if y_left.size>0 else np.nan,
    "x_right": x_right if x_right.size>0 else np.nan,
    "y_right": y_right if y_right.size>0 else np.nan
})

# 시도 순서: plotly -> matplotlib -> st.line_chart
used_backend = None
try:
    import plotly.graph_objects as go
    used_backend = "plotly"
    fig = go.Figure()

    if x_left.size > 0:
        fig.add_trace(go.Scatter(x=x_left, y=y_left, mode="lines", name="그래프 (왼쪽 부분)"))
    if x_right.size > 0:
        fig.add_trace(go.Scatter(x=x_right, y=y_right, mode="lines", name="그래프 (오른쪽 부분)"))

    # 점근선
    # 수평점근선 y = q
    fig.add_trace(go.Scatter(x=[x_min, x_max], y=[q, q], mode="lines",
                             name=f"수평점근선 y={q}", line=dict(dash="dash", color="black")))
    # 수직점근선 x = p (표현으로는 아주 큰 값으로 그리기)
    fig.add_trace(go.Scatter(x=[p, p], y=[np.nanmin(np.concatenate([y_left, y_right]))*1.2,
                                         np.nanmax(np.concatenate([y_left, y_right]))*1.2],
                             mode="lines", name=f"수직점근선 x={p}", line=dict(dash="dot", color="red")))

    fig.update_layout(title=f"y = {a}/(x - {p}) + {q}",
                      xaxis_title="x", yaxis_title="y",
                      width=800, height=520)
    st.plotly_chart(fig, use_container_width=True)

except Exception:
    try:
        import matplotlib.pyplot as plt
        used_backend = "matplotlib"
        fig, ax = plt.subplots(figsize=(8,5))

        if x_left.size > 0:
            ax.plot(x_left, y_left, label="그래프 (왼쪽 부분)")
        if x_right.size > 0:
            ax.plot(x_right, y_right, label="그래프 (오른쪽 부분)")

        # 점근선 그리기
        ax.hlines(q, x_min, x_max, colors="black", linestyles="dashed", label=f"수평점근선 y={q}")
        # 수직점근선 (표시)
        ax.vlines(p, np.nanmin(np.concatenate([y_left if y_left.size>0 else [0], y_right if y_right.size>0 else [0]]))*1.2,
                  np.nanmax(np.concatenate([y_left if y_left.size>0 else [0], y_right if y_right.size>0 else [0]]))*1.2,
                  colors="red", linestyles="dotted", label=f"수직점근선 x={p}")

        ax.set_xlim(x_min, x_max)
        # y범위 자동조정에서 극단값 제거 (이상치 때문에 축이 깨지지 않게)
        combined = np.concatenate([y_left, y_right]) if (y_left.size>0 or y_right.size>0) else np.array([0])
        y_med = np.median(combined[np.isfinite(combined)])
        ax.set_ylim(y_med - 10, y_med + 10)  # 기본 보기 범위
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(f"y = {a}/(x - {p}) + {q}")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

    except Exception:
        # 최후의 수단: Streamlit 기본 line_chart (점근선은 숫자로 표시)
        used_backend = "streamlit.line_chart"
        st.warning("시각화에 plotly/matplotlib이 사용 불가하여 간단한 차트로 대체합니다.")
        # Prepare a friendly DataFrame for line_chart: two series (left, right)
        df_plot = pd.DataFrame()
        if x_left.size > 0:
            df_plot = pd.DataFrame({"x": x_left, "y_left": y_left})
            df_plot = df_plot.set_index("x")
        if x_right.size > 0:
            df2 = pd.DataFrame({"x": x_right, "y_right": y_right}).set_index("x")
            df_plot = pd.concat([df_plot, df2], axis=1)
        st.line_chart(df_plot)

# 수치적 정보 출력
st.markdown("---")
st.subheader("수치 정보")
st.write(f"- 수직점근선: x = **{p}** (함수 정의 불가)")
st.write(f"- 수평점근선: y = **{q}**")
# 몇몇 x 값의 근방에서 극한값 확인 표
sample_x = np.array([p - 0.1, p - 0.01, p + 0.01, p + 0.1])
finite_mask = (sample_x > x_min) & (sample_x < x_max)
sample_x = sample_x[finite_mask]
if sample_x.size>0:
    sample_y = rational_y(sample_x, a, p, q)
    info_df = pd.DataFrame({"x": sample_x, "y": sample_y})
    st.table(info_df)
else:
    st.write("점근선 근처의 샘플 x 값들이 현재 x 범위 밖에 있습니다.")

st.caption(f"사용된 시각화 엔진: {used_backend}")
