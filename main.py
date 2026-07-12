import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="인체 질병지도", layout="wide", page_icon="🧍")

st.title("🧍‍♂️ 인체 온도별 질병 발생 비율 분포 (인체 질병지도)")
st.markdown("""
**정상 체온 ≈ 36.5°C**  
신체부위마다 온도가 다르고, **단백질(효소)**은 온도에 매우 민감합니다.  
이 앱으로 **온도-단백질 변성-질병 위험** 관계를 탐구해보세요.

**주의**: 교육용 시뮬레이션입니다. 실제 의학적 조언이 아닙니다.
""")

# ==================== 데이터 ====================
data = {
    "신체부위": ["뇌 (Core)", "심장/간 (Core)", "근육 (평균)", "피부 (팔/다리)", "손/발 (Extremity)", "구강", "직장 (Core)"],
    "평균 온도 (°C)": [37.0, 37.2, 36.8, 33.5, 32.0, 36.8, 37.0],
    "질병 위험 지수 (0-100)": [85, 78, 65, 45, 35, 60, 82],
    "주요 연관 질병/현상": [
        "뇌염, 발열성 경련, 단백질 변성 (뇌졸중 위험↑)",
        "간염, 심근염, 효소 비활성화",
        "근육통, 염증, 근육 단백질 변성",
        "피부염, 동상, 감염 (피부 장벽 약화)",
        "동상, 레이노 증후군, 순환기 문제",
        "구강염, 치주염",
        "장염, 복부 장기 염증"
    ],
    "단백질 변성 관련": [
        "효소·신경단백질 변성 시작 (40°C↑)",
        "대사 효소 불안정",
        "근육 단백질 (미오신) 변성",
        "피부 콜라겐·케라틴 영향",
        "극한 저온 → 단백질 응집",
        "구강 내 효소 영향",
        "장기 단백질 안정성 높음"
    ]
}

df = pd.DataFrame(data)

# ==================== 사이드바 ====================
st.sidebar.header("🔧 탐구 도구")

selected_parts = st.sidebar.multiselect(
    "신체부위 선택 (여러 개 가능)",
    df["신체부위"].tolist(),
    default=df["신체부위"].tolist()[:4]
)

temp_adjust = st.sidebar.slider(
    "전체 온도 변화 (°C, 발열/저체온 시뮬레이션)",
    -3.0, 5.0, 0.0, 0.1
)

# ==================== 데이터 조정 ====================
df_display = df.copy()
df_display["조정된 온도 (°C)"] = df_display["평균 온도 (°C)"] + temp_adjust
df_display = df_display[df_display["신체부위"].isin(selected_parts)]

# ==================== 메인 대시보드 ====================
tab1, tab2, tab3 = st.tabs(["📊 질병지도", "📈 차트 분석", "🔬 단백질 & 온도 설명"])

with tab1:
    st.subheader("인체 질병지도 (온도 + 위험도)")
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # 간단한 바 차트
        fig = px.bar(
            df_display, 
            x="신체부위", 
            y="조정된 온도 (°C)",
            color="질병 위험 지수 (0-100)",
            title="신체부위별 온도와 질병 위험도",
            color_continuous_scale="RdYlBu_r",
            text="주요 연관 질병/현상"
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.dataframe(
            df_display[["신체부위", "조정된 온도 (°C)", "질병 위험 지수 (0-100)", "주요 연관 질병/현상"]],
            use_container_width=True,
            hide_index=True
        )

with tab2:
    st.subheader("온도 vs 질병 위험도 상관관계")
    
    fig2 = px.scatter(
        df_display, 
        x="조정된 온도 (°C)", 
        y="질병 위험 지수 (0-100)",
        color="신체부위",
        size="질병 위험 지수 (0-100)",
        hover_data=["주요 연관 질병/현상"],
        title="온도가 높을수록 질병 위험도가 증가하는 경향 (단백질 변성 영향)"
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    st.info("""
    **관찰 포인트**: 
    - Core 부위(뇌, 심장)는 온도가 높고 질병 위험도도 높음
    - Extremity(손/발)는 온도가 낮아 감염/동상 위험이 상대적으로 높음
    """)

with tab3:
    st.subheader("🔬 단백질과 온도의 인과관계")
    st.markdown("""
    **단백질 변성 (Protein Denaturation)**  
    - 대부분의 인간 단백질(효소)은 **37~42°C**에서 최적 활성을 보입니다.
    - **40°C 이상** 지속되면 3차 구조가 풀리며 기능 상실 (변성).
    - **43°C 이상** 장기간 → 세포 사멸 (열사병, 장기 손상).
    
    **신체부위별 의미**
    - 뇌·심장: 고온에 매우 민감 → 발열 시 뇌손상 위험이 큼
    - 피부: 낮은 온도 → 면역·장벽 기능 저하
    - 발열 시 전체 체온 상승 → 단백질 변성 → 염증 악순환
    
    **탐구 질문**
    - 38.5°C 발열이 지속되면 어떤 부위가 가장 먼저 위험해질까?
    - 저체온증(35°C 이하)에서는 어떤 단백질 문제가 생길까?
    """)
    
    st.warning("**의학적 사실**: 실제 질병은 온도 외에 면역, 감염원, 유전 등 복합적 요인입니다. 이 앱은 교육용 시각화입니다.")

st.caption("Streamlit 인체 질병지도 | 단백질-온도 탐구용 | 데이터는 교육용 근사치입니다.")
