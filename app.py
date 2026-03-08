import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. 페이지 기본 설정 및 테마 적용
st.set_page_config(page_title="로보티즈 기업분석 리포트", layout="wide")

# Custom CSS: JSX의 다크 모드 스타일 재현
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0A0A0C;
        color: #E0DDD5;
        font-family: 'Noto Sans KR', sans-serif;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: #0D0D10;
        border-bottom: 1px solid #1E1E24;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent;
        color: #555;
        font-weight: 400;
    }
    .stTabs [aria-selected="true"] {
        color: #E8C547 !important;
        border-bottom: 2px solid #E8C547 !important;
    }
    .report-card {
        background: #111114;
        border: 1px solid #1E1E24;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .kpi-title { font-size: 10px; color: #555; letter-spacing: 1px; margin-bottom: 8px; }
    .kpi-value { font-size: 22px; font-weight: 700; }
    .risk-banner {
        background: linear-gradient(90deg, #FF444422, #FF8C6911);
        border: 1px solid #FF444444;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 데이터셋 (JSX의 데이터 객체들을 파이썬 딕셔너리로 변환)
revenue_data = pd.DataFrame([
    {"year": "2021", "rev": 224, "op": -9, "opM": -4.2},
    {"year": "2022", "rev": 259, "op": -22, "opM": -8.4},
    {"year": "2023", "rev": 291, "op": -53, "opM": -18.2},
    {"year": "2024", "rev": 300, "op": -30, "opM": -10.0},
    {"year": "2025E", "rev": 420, "op": 52, "opM": 12.4},
    {"year": "2026F", "rev": 680, "op": 110, "opM": 16.2},
])

radar_data = pd.DataFrame([
    {"subject": "기술 원천성", "robotis": 92, "unitree": 70, "agibot": 65, "maxon": 95},
    {"subject": "가격 경쟁력", "robotis": 70, "unitree": 98, "agibot": 90, "maxon": 20},
    {"subject": "양산 규모", "robotis": 45, "unitree": 95, "agibot": 98, "maxon": 60},
    {"subject": "글로벌 생태계", "robotis": 85, "unitree": 55, "agibot": 40, "maxon": 80},
    {"subject": "수익성", "robotis": 72, "unitree": 50, "agibot": 30, "maxon": 85},
    {"subject": "규제 리스크", "robotis": 90, "unitree": 40, "agibot": 35, "maxon": 95},
])

# 3. 헤더 영역
col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    st.markdown("""
        <div style='display: flex; align-items: center; gap: 15px;'>
            <div style='background: linear-gradient(135deg,#E8C547,#FF8C69); width: 45px; height: 45px; border-radius: 10px; display: flex; align-items: center; justifyContent: center; font-size: 22px;'>🤖</div>
            <div>
                <div style='font-size: 11px; color: #555; letter-spacing: 2px;'>KOSDAQ | 자본재 | 기업분석</div>
                <div style='font-size: 24px; font-weight: 700;'>로보티즈 <span style='color: #999; font-size: 16px; font-weight: 400;'>(108490)</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_h2:
    st.markdown("<div style='text-align: right;'><div style='font-size: 26px; font-weight: 600; color: #E8C547;'>242,000<span style='font-size: 14px; color: #666;'>원</span></div><div style='font-size: 12px; color: #555;'>시총 3.67조 · 2026.03 UPDATE</div></div>", unsafe_allow_html=True)

# 4. 탭 구성
tabs = st.tabs(["체크포인트", "기업 개요", "경쟁 분석", "실적 추이"])

# --- TAB 0: 체크포인트 ---
with tabs[0]:
    st.markdown("<div class='risk-banner'>■ 로보티즈는 피지컬 AI 시대 핵심 부품 전문기업으로 2025년 첫 연간 흑자 전환 달성.</div>", unsafe_allow_html=True)
    
    kpi_cols = st.columns(4)
    kpi_data = [
        {"label": "2025 매출(E)", "val": "420억", "color": "#E8C547"},
        {"label": "2025 영업이익(E)", "val": "+52억", "color": "#4EC9B0"},
        {"label": "4Q25 OPM", "val": "36%", "color": "#7B9FFF"},
        {"label": "2026 매출 목표", "val": "680억(F)", "color": "#FF8C69"},
    ]
    for i, kpi in enumerate(kpi_data):
        with kpi_cols[i]:
            st.markdown(f"""
                <div class="report-card" style="border-top: 2px solid {kpi['color']}">
                    <div class="kpi-title">{kpi['label']}</div>
                    <div class="kpi-value" style="color: {kpi['color']}">{kpi['val']}</div>
                </div>
            """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📋 향후 주목 체크포인트")
        st.checkbox("액추에이터 해외 매출 확대 속도", value=True)
        st.caption("2025 4Q 영업이익률 36%로 급등. 고부가 로봇 손 제품 반영")
        st.checkbox("AI 워커 양산 및 수주 가시화")
        st.caption("2025년 70대 → 2027년 1,000대 목표")
    
    with c2:
        st.subheader("⚠️ 리스크 요인")
        st.error("매출의 98% 다이나믹셀 단일 의존 리스크")
        st.warning("시총 3.67조 vs 매출 420억 (PSR 87x 고평가)")

# --- TAB 2: 경쟁 분석 (레이더 차트 포함) ---
with tabs[2]:
    st.markdown("<div class='risk-banner'>🚨 중국발 가격 파괴 위협 — 유니트리 R1 $5,900 (미국산의 1/8 수준)</div>", unsafe_allow_html=True)
    
    col_r1, col_r2 = st.columns([1, 1])
    with col_r1:
        st.markdown("#### 🕸️ 글로벌 경쟁력 비교")
        fig_radar = go.Figure()
        for col, color in zip(['robotis', 'unitree', 'maxon'], ['#E8C547', '#FF4444', '#4EC9B0']):
            fig_radar.add_trace(go.Scatterpolar(
                r=radar_data[col],
                theta=radar_data['subject'],
                fill='toself',
                name=col.upper(),
                line_color=color
            ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100]), bgcolor='#111114'),
            showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#666")
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_r2:
        st.markdown("#### ⚔️ 로보티즈 차별화 포인트")
        st.info("**vs 중국:** 오픈소스 생태계 80% 점유, 글로벌 연구 표준")
        st.info("**vs 유럽:** 모듈형 설계로 인한 가격 경쟁력 및 피지컬AI 통합")

# --- TAB 3: 실적 추이 ---
with tabs[3]:
    st.markdown("#### 📈 연도별 실적 추이 (억원)")
    fig_rev = px.bar(revenue_data, x='year', y='rev', text='rev', 
                     title="매출액 추이", color_discrete_sequence=['#E8C547'])
    fig_rev.add_scatter(x=revenue_data['year'], y=revenue_data['opM'], name="영업이익률(%)", 
                        yaxis="y2", line=dict(color='#4EC9B0'))
    fig_rev.update_layout(
        yaxis2=dict(title="이익률(%)", overlaying="y", side="right"),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#888"
    )
    st.plotly_chart(fig_rev, use_container_width=True)