import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. 페이지 설정
st.set_page_config(page_title="ROBOTIS Enterprise Analysis 2026", layout="wide")

# 2. 모든 원본 데이터셋 정의 (JSX 데이터 1:1 매칭)
revenue_data = pd.DataFrame([
    {"year": "2021", "rev": 224, "op": -9, "opM": -4.2},
    {"year": "2022", "rev": 259, "op": -22, "opM": -8.4},
    {"year": "2023", "rev": 291, "op": -53, "opM": -18.2},
    {"year": "2024", "rev": 300, "op": -30, "opM": -10.0},
    {"year": "2025E", "rev": 420, "op": 52, "opM": 12.4},
    {"year": "2026F", "rev": 680, "op": 110, "opM": 16.2},
])

valuation_data = [
    {"label": "현재 주가 (2026.03)", "value": "242,000원", "color": "#E8C547"},
    {"label": "시가총액", "value": "3.67조원", "color": "#E8C547"},
    {"label": "2025 매출 (추정)", "value": "약 420억원", "color": "#aaa"},
    {"label": "PSR (주가/매출)", "value": "약 87x", "color": "#FF8C69", "warn": True},
    {"label": "PBR", "value": "약 12x", "color": "#FF8C69", "warn": True},
    {"label": "애널리스트 목표가 평균", "value": "149,000원", "color": "#4EC9B0"},
]

china_rivals = [
    {"name": "Unitree (🇨🇳)", "threat": "CRITICAL", "desc": "G1 휴머노이드 $16,000 / R1 $5,900. 저가 공세 심화", "strength": "수직계열화 완성", "color": "#FF4444"},
    {"name": "AgiBot (상하이)", "threat": "HIGH", "desc": "LG전자·미래에셋 전략 투자. 2025년 5,200대 출하", "strength": "양산 규모 최대", "color": "#FF8C69"},
    {"name": "Fourier (상하이)", "threat": "HIGH", "desc": "의료·재활 특화. 힘 제어 기반 파지 기술 강점", "strength": "의료 실증 데이터", "color": "#FF8C69"},
    {"name": "MAXON (🇨🇭)", "threat": "MED", "desc": "초정밀 산업용. 단가 다이나믹셀比 3~10배", "strength": "최고 신뢰성/정밀도", "color": "#4EC9B0"},
]

pipeline = [
    {"product": "AI 워커 (고정형)", "stage": "출하 중", "rev": "27년 632억F", "target": "27년 1,000대", "icon": "🦾"},
    {"product": "로봇 손 HX5", "stage": "CES 공개", "rev": "26년 본격 반영", "target": "글로벌 빅테크 납품", "icon": "🤲"},
    {"product": "AI 워커 (모바일)", "stage": "협의 중", "rev": "26년 B2B 본격화", "target": "25 4Q 출시", "icon": "🚀"},
    {"product": "DYNAMIXEL Y", "stage": "개발 중", "rev": "ASP 상승 기여", "target": "26년 양산 확대", "icon": "🔩"},
]

# 3. Custom CSS (JSX의 디자인 스타일 완벽 재현)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&family=IBM+Plex+Mono:wght@400;600&display=swap');
    [data-testid="stAppViewContainer"] { background-color: #0A0A0C; color: #E0DDD5; font-family: 'Noto Sans KR', sans-serif; }
    .card { background: #111114; border: 1px solid #1E1E24; border-radius: 12px; padding: 20px; margin-bottom: 10px; }
    .status-badge { font-size: 10px; padding: 2px 8px; border-radius: 4px; font-weight: 600; }
    .stTabs [data-baseweb="tab-list"] { background-color: #0D0D10; border-bottom: 1px solid #1E1E24; }
    .stTabs [data-baseweb="tab"] { color: #555; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { color: #E8C547 !important; border-bottom: 2px solid #E8C547 !important; }
    </style>
""", unsafe_allow_html=True)

# 4. 헤더
st.markdown(f"""
    <div style='display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #1E1E24; margin-bottom: 20px;'>
        <div>
            <span style='color: #555; font-size: 11px; letter-spacing: 2px;'>KOSDAQ | 로봇 부품 | 기업분석</span>
            <h1 style='margin: 0; font-size: 28px;'>로보티즈 <span style='color: #999; font-size: 16px;'>(108490)</span></h1>
        </div>
        <div style='text-align: right;'>
            <div style='font-family: "IBM Plex Mono"; font-size: 28px; color: #E8C547; font-weight: 600;'>242,000<span style='font-size: 14px; color: #666;'>원</span></div>
            <div style='font-size: 12px; color: #4EC9B0;'>2026.03 UPDATE</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 5. 메인 탭 구성
tabs = st.tabs(["체크포인트", "파이프라인", "경쟁 분석", "실적 & 밸류에이션"])

# --- TAB 1: 체크포인트 ---
with tabs[0]:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("#### 📋 핵심 체크포인트")
        checkpoints = [
            ("📌 액추에이터 해외 매출 확대", "2025 4Q 영업이익률 36% 급등. 고부가 로봇 손 반영"),
            ("📌 AI 워커 수주 가시화", "오픈AI 공급 협의 중. 2027년 1,000대 목표"),
            ("📌 LG전자 협업 구체화", "휴머노이드 공동연구 및 실질 납품 여부 주목")
        ]
        for title, note in checkpoints:
            st.markdown(f"<div class='card'><b>{title}</b><br><small style='color:#666'>{note}</small></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### ⚠️ 리스크 요인")
        st.error("매출의 98% 다이나믹셀 단일 의존 리스크")
        st.warning("시총 3.67조 vs 매출 420억 (PSR 87x 극단적 프리미엄)")
        st.info("중국산(Unitree 등) 저가 휴머노이드 침투 속도")

# --- TAB 2: 파이프라인 ---
with tabs[1]:
    st.markdown("#### 🚀 제품 로드맵 & 파이프라인")
    cols = st.columns(4)
    for i, p in enumerate(pipeline):
        with cols[i]:
            st.markdown(f"""
                <div class='card' style='text-align: center;'>
                    <div style='font-size: 30px;'>{p['icon']}</div>
                    <div style='color: #E8C547; font-weight: 700; margin-top: 10px;'>{p['product']}</div>
                    <div style='font-size: 11px; color: #4EC9B0;'>{p['stage']}</div>
                    <hr style='border: 0.5px solid #222'>
                    <div style='font-size: 11px; color: #888;'>목표: {p['target']}</div>
                    <div style='font-size: 11px; color: #aaa;'>예상매출: {p['rev']}</div>
                </div>
            """, unsafe_allow_html=True)

# --- TAB 3: 경쟁 분석 ---
with tabs[2]:
    st.markdown("<div style='background: #FF444422; border: 1px solid #FF444444; padding: 15px; border-radius: 10px; color: #FF8C69;'>🚨 <b>중국발 가격 파괴:</b> 유니트리 R1 $5,900 — 글로벌 시장 잠식 위험도 'CRITICAL'</div>", unsafe_allow_html=True)
    st.write("")
    
    col_c1, col_c2 = st.columns([1, 1])
    with col_c1:
        st.markdown("#### 🇨🇳 글로벌 경쟁사 현황")
        for r in china_rivals:
            st.markdown(f"""
                <div class='card' style='border-left: 4px solid {r['color']}'>
                    <div style='display: flex; justify-content: space-between;'>
                        <span style='font-weight: 700;'>{r['name']}</span>
                        <span class='status-badge' style='background: {r['color']}22; color: {r['color']}'>{r['threat']}</span>
                    </div>
                    <div style='font-size: 12px; margin-top: 8px;'>{r['desc']}</div>
                    <div style='font-size: 11px; color: #4EC9B0; margin-top: 5px;'>핵심강점: {r['strength']}</div>
                </div>
            """, unsafe_allow_html=True)

    with col_c2:
        st.markdown("#### 🕸️ 기술력/시장성 레이더")
        radar_df = pd.DataFrame([
            {"subject": "정밀도", "로보티즈": 95, "중국산": 70},
            {"subject": "가격", "로보티즈": 60, "중국산": 98},
            {"subject": "생태계", "로보티즈": 90, "중국산": 50},
            {"subject": "양산력", "로보티즈": 45, "중국산": 95},
        ])
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=radar_df['로보티즈'], theta=radar_df['subject'], fill='toself', name='로보티즈', line_color='#E8C547'))
        fig.add_trace(go.Scatterpolar(r=radar_df['중국산'], theta=radar_df['subject'], fill='toself', name='중국 경쟁사', line_color='#FF4444'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#888", height=350)
        st.plotly_chart(fig, use_container_width=True)

# --- TAB 4: 실적 & 밸류에이션 ---
with tabs[3]:
    col_v1, col_v2 = st.columns([2, 1])
    with col_v1:
        st.markdown("#### 📊 실적 추이 (억원)")
        fig_rev = px.bar(revenue_data, x='year', y='rev', text='rev', color_discrete_sequence=['#E8C547'])
        fig_rev.add_scatter(x=revenue_data['year'], y=revenue_data['op'], name="영업이익", line=dict(color='#4EC9B0', width=3))
        fig_rev.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#888")
        st.plotly_chart(fig_rev, use_container_width=True)
    
    with col_v2:
        st.markdown("#### 💎 밸류에이션 요약")
        for v in valuation_data:
            warn_style = "border: 1px solid #FF8C69;" if v.get("warn") else ""
            st.markdown(f"""
                <div class='card' style='{warn_style}'>
                    <div style='font-size: 11px; color: #666;'>{v['label']}</div>
                    <div style='font-size: 18px; font-weight: 700; color: {v['color']}'>{v['value']}</div>
                </div>
            """, unsafe_allow_html=True)
