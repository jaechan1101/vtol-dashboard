import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="차세대 VTOL 형식별 성능 비교 대시보드",
    layout="wide",
    page_icon="🚁",
)

st.title("🚁 차세대 VTOL 형식별 종합 성능 비교 및 분석 대시보드")
st.markdown(
    "리프트 앤 크루즈, 쿼드플레인, 틸트로터뿐만 아니라 **틸트윙**과 **테일시터**까지"
    " 포함하여 핵심 비행 스펙(배터리 효율, 체공시간, 페이로드, 속도)을 비교합니다."
)

# 확장된 비교 데이터 정의
data = {
    "VTOL 형식": [
        "리프트 앤 크루즈",
        "쿼드플레인",
        "틸트로터",
        "틸트윙",
        "테일시터",
    ],
    "이동속도(순항)": ["중~고속", "보통", "매우 높음", "높음", "매우 높음"],
    "배터리 효율": ["보통", "낮음~보통", "높음", "높음", "매우 높음"],
    "최대 체공시간": ["보통 (약 1~2시간)", "보통", "우수 (약 2~3시간)", "우수", "우수"],
    "페이로드 무게": ["우수 (안정적 공간)", "보통", "보통~우수", "보통", "낮음~보통"],
    "기계적 복잡도": ["중간", "낮음", "매우 높음", "높음", "중간~높음"],
    # 레이더 차트용 점수 (5점 만점 기준)
    "속도/순항 성능": [4, 3, 5, 4, 5],
    "에너지/배터리 효율": [3, 2, 4, 4, 5],
    "체공 지속력": [3, 3, 4, 4, 4],
    "페이로드 탑재력": [4, 3, 3, 3, 2],
    "제어 및 구조 안정성": [4, 5, 3, 3, 2],
}
df = pd.DataFrame(data)

# 탭 구성
tab1, tab2, tab3 = st.tabs(["📊 상세 스펙 매트릭스", "📈 종합 성능 레이더 차트", "🎯 임무별 최적 형식 추천"])

with tab1:
    st.subheader("주요 5대 VTOL 형식별 핵심 스펙 비교")
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📝 형식별 특징 요약")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 🛫 리프트 앤 크루즈")
        st.write("- 수직 전용 모터와 순항용 푸셔 분리")
        st.write("- 페이로드 탑재 공간 확보가 유리함")
        st.markdown("#### 🛩️ 쿼드플레인")
        st.write("- 제작과 제어가 가장 안정적이고 직관적")
        st.write("- 호버링 시 항력으로 인해 배터리 효율은 다소 낮음")
    with col2:
        st.markdown("#### 🚀 틸트로터")
        st.write("- 모든 로터가 추력에 기여해 효율 극대화")
        st.write("- 고속 비행과 긴 체공시간에 강점")
        st.markdown("#### 🦅 틸트윙")
        st.write("- 날개 자체가 틸팅되어 천이 구간 양력 활용 우수")
        st.write("- 기계적 링크 구조가 복잡함")
    with col3:
        st.markdown("#### 🛸 테일시터")
        st.write("- 꼬리로 서서 이착륙 후 기수를 전환해 고속 비행")
        st.write("- 구조가 단순하고 고속/고효율이나 제어 난이도 극상")

with tab2:
    st.subheader("형식별 다차원 성능 비교 (Radar Chart)")
    categories = [
        "속도/순항 성능",
        "에너지/배터리 효율",
        "체공 지속력",
        "페이로드 탑재력",
        "제어 및 구조 안정성",
    ]

    fig = go.Figure()
    for i, row in df.iterrows():
        fig.add_trace(
            go.Scatterpolar(
                r=[
                    row["속도/순항 성능"],
                    row["에너지/배터리 효율"],
                    row["체공 지속력"],
                    row["페이로드 탑재력"],
                    row["제어 및 구조 안정성"],
                ],
                theta=categories,
                fill="toself",
                name=row["VTOL 형식"],
            )
        )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
        showlegend=True,
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("임무 목적에 따른 최적 VTOL 추천 시뮬레이터")
    mission_type = st.selectbox(
        "수행할 핵심 임무를 선택하세요:",
        [
            "초장거리 감시侦察 및 고속 이동 (Speed & Long Endurance)",
            "무거운 센서/화물 탑재 (Heavy Payload Focus)",
            "안정적인 개발 및 유지보수 편의성 (Easy Maintenance & Stability)",
            "협소한 공간 이착륙 및 고효율 비행 (High Efficiency & VTOL Agility)",
        ],
    )

    if st.button("최적 VTOL 도출하기"):
        if "초장거리" in mission_type:
            st.success("💡 **추천 형식: 틸트로터 또는 테일시터**")
            st.write(
                "배터리 효율과 이동 속도가 뛰어나 장거리 임무에 적합합니다."
            )
        elif "무거운" in mission_type:
            st.success("💡 **추천 형식: 리프트 앤 크루즈 (Lift + Cruise)**")
            st.write(
                "동체 내부 공간 활용도가 높아 페이로드 장착에 가장 유리합니다."
            )
        elif "안정적인" in mission_type:
            st.success("💡 **추천 형식: 쿼드플레인 (Quadplane)**")
            st.write(
                "오픈소스(아두파일럿 등) 생태계가 넓고 제어가 안정적입니다."
            )
        else:
            st.success("💡 **추천 형식: 틸트윙 (Tilt-wing)**")
            st.write(
                "천이 구역에서 양력을 적극 활용하여 고효율 비행이 가능합니다."
            )