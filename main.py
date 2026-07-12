
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from matplotlib.patches import Rectangle, Circle, Ellipse

st.set_page_config(page_title="인체 질병지도 v2", layout="wide", page_icon="🧍")

st.title("🧍‍♂️ 인체 온도별 질병 발생 지도 (발열 시뮬레이션)")
st.markdown("""
**정상 체온 ≈ 36.5°C**  
신체부위별 온도 차이 + **단백질 변성**과의 관계를 탐구합니다.  
온도를 조절하며 발열 상황을 시뮬레이션해보세요.
""")

# ==================== 데이터 ====================
data = {
    "신체부위": ["뇌", "심장/간", "근육(평균)", "피부(팔/다리)", "손/발", "구강", "직장"],
    "기준 온도 (°C)": [37.0, 37.2, 36.8, 33.5, 32.0, 36.8, 37.0],
    "질병 위험 지수": [85, 78, 65, 45, 35, 60, 82],
    "주요 질병/현상": ["뇌염·경련", "심근염·간염", "근육염", "피부염·동상", "레이노·동상", "구강염", "장염"],
    "단백질 관련": ["신경단백질 변성", "대사효소 불안정", "미오신 변성", "콜라겐 영향", "극한 저온 응집", "효소 영향", "장기 안정"]
}

df_base = pd.DataFrame(data)

# ==================== 사이드바 ====================
st.sidebar.header("🔧 시뮬레이션 파라미터")

base_temp = st.sidebar.slider(
    "기준 체온 (°C)", 
    min_value=30.0, max_value=42.0, 
    value=36.5, step=0.5
)

fever_delta = st.sidebar.slider(
    "발열 상승 (°C)", 
    min_value=0.0, max_value=5.0, 
    value=0.0, step=0.5,
    help="전체 신체 온도를 올려 발열 상황 시뮬레이션"
)

selected_parts = st.sidebar.multiselect(
    "비교할 신체부위", 
    df_base["신체부위"].tolist(), 
    default=df_base["신체부위"].tolist()
)

# ==================== 데이터 조정 ====================
df = df_base.copy()
df["현재 온도 (°C)"] = df["기준 온도 (°C)"] + fever_delta
df = df[df["신체부위"].isin(selected_parts)]

# ==================== 인체 그림 ====================
def draw_body(temp_dict):
    fig, ax = plt.subplots(figsize=(6, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 20)
    ax.axis('off')
    
    # 몸통
    ax.add_patch(Rectangle((3, 6), 4, 8, facecolor=plt.cm.RdYlBu_r((temp_dict.get('심장/간', 36.5)-30)/12), alpha=0.7))
    # 머리
    ax.add_patch(Circle((5, 17), 2.5, facecolor=plt.cm.RdYlBu_r((temp_dict.get('뇌', 36.5)-30)/12), alpha=0.8))
    # 팔
    ax.add_patch(Rectangle((1, 8), 1.5, 6, facecolor=plt.cm.RdYlBu_r((temp_dict.get('피부(팔/다리)', 33.5)-30)/12), alpha=0.6))
    ax.add_patch(Rectangle((7.5, 8), 1.5, 6, facecolor=plt.cm.RdYlBu_r((temp_dict.get('피부(팔/다리)', 33.5)-30)/12), alpha=0.6))
    # 다리
    ax.add_patch(Rectangle((3.5, 1), 1.5, 5, facecolor=plt.cm.RdYlBu_r((temp_dict.get('손/발', 32.0)-30)/12), alpha=0.6))
    ax.add_patch(Rectangle((5, 1), 1.5, 5, facecolor=plt.cm.RdYlBu_r((temp_dict.get('손/발', 32.0)-30)/12), alpha=0.6))
    
    # 라벨
    ax.text(5, 17.5, f"뇌\n{temp_dict.get('뇌', 37.0):.1f}°C", ha='center', fontsize=10, fontweight='bold')
    ax.text(5, 11, f"심장/간\n{temp_dict.get('심장/간', 37.2):.1f}°C", ha='center', fontsize=10)
    ax.text(1.8, 10, f"팔\n{temp_dict.get('피부(팔/다리)', 33.5):.1f}°C", ha='center', fontsize=9)
    ax.text(8.2, 10, f"팔\n{temp_dict.get('피부(팔/다리)', 33.5):.1f}°C", ha='center', fontsize=9)
    ax.text(4.3, 3, f"다리/손발\n{temp_dict.get('손/발', 32.0):.1f}°C", ha='center', fontsize=9)
    
    return fig

# ==================== 메인 ====================
tab1, tab2 = st.tabs(["🧍 인체 지도", "📊 상세 분석"])

with tab1:
    st.subheader(f"현재 시뮬레이션 체온: {base_temp:.1f}°C (+{fever_delta:.1f}°C 발열)")
    
    # 인체 그림
    temp_dict = dict(zip(df["신체부위"], df["현재 온도 (°C)"]))
    body_fig = draw_body(temp_dict)
    st.pyplot(body_fig)
    
    st.dataframe(
        df[["신체부위", "현재 온도 (°C)", "질병 위험 지수", "주요 질병/현상", "단백질 관련"]],
        use_container_width=True,
        hide_index=True
    )

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(
            df, x="신체부위", y="현재 온도 (°C)",
            color="질병 위험 지수",
            title="신체부위별 온도와 질병 위험도",
            color_continuous_scale="RdYlBu_r"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig2 = px.scatter(
            df, x="현재 온도 (°C)", y="질병 위험 지수",
            color="신체부위", size="질병 위험 지수",
            title="온도 vs 질병 위험도 (단백질 변성 영향)"
        )
        st.plotly_chart(fig2, use_container_width=True)

# ==================== 설명 ====================
st.markdown("---")
st.header("🔬 과학적 설명")

st.markdown(f"""
**현재 발열 상황 ({base_temp + fever_delta:.1f}°C)**

- **단백질 변성**: 대부분의 인간 단백질은 **40°C 이상**에서 3차 구조가 풀리기 시작합니다. 
  - 42°C 이상 지속 → 세포 손상, 효소 비활성화, 염증 악화
- **부위별 특징**:
  - **Core 부위 (뇌, 심장)**: 온도가 높아 **단백질 변성 위험**이 가장 큽니다. 발열 시 뇌손상 주의.
  - **Extremity (손/발)**: 평소 온도가 낮아 **저온 스트레스** (단백질 응집) 위험이 있습니다.
- **발열의 이중성**: 적절한 발열은 면역 반응이지만, 과도하면 단백질 파괴 → 장기 손상으로 이어질 수 있습니다.
""")

st.caption("Streamlit 인체 질병지도 v2 | 교육용 시뮬레이션 | 실제 의학적 조언 아님")
