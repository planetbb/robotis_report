"""
로보티즈 IR 대시보드 2026 — Streamlit 버전
원본 JSX: robotis_ir_2026.jsx
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ── 페이지 설정 ──────────────────────────────────────────
st.set_page_config(
    page_title="로보티즈 IR 2026",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── 글로벌 CSS ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; background: #0A0A0C; color: #E0DDD5; }
.stApp { background: #0A0A0C; }
section[data-testid="stSidebar"] { background: #0D0D10; }
div[data-testid="stMetricValue"] { color: #E8C547; font-family: 'IBM Plex Mono', monospace; }

/* 카드 */
.ir-card {
    background: #111114;
    border: 1px solid #1E1E24;
    border-radius: 12px;
    padding: 20px 22px;
    margin-bottom: 12px;
}
.ir-card-green { border-top: 3px solid #4EC9B0; }
.ir-card-yellow { border-top: 3px solid #E8C547; }
.ir-card-red { border-top: 3px solid #FF8C69; }
.ir-card-blue { border-top: 3px solid #7B9FFF; }

/* 배지 */
.badge {
    display: inline-block;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 11px;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
}

/* 탭 스타일 오버라이드 */
button[data-baseweb="tab"] {
    background: none !important;
    color: #555 !important;
    font-family: 'Noto Sans KR', sans-serif !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #E8C547 !important;
    border-bottom: 2px solid #E8C547 !important;
}
div[data-testid="stHorizontalBlock"] { gap: 12px; }

/* 모노 */
.mono { font-family: 'IBM Plex Mono', monospace; }

/* 진행바 래퍼 */
.progress-bar-bg {
    background: #1A1A1E;
    border-radius: 4px;
    height: 7px;
    overflow: hidden;
    margin: 4px 0 8px 0;
}
.progress-bar-fill { height: 100%; border-radius: 4px; }

/* 헤더 배너 */
.header-banner {
    background: #0D0D10;
    border-bottom: 1px solid #1E1E24;
    padding: 18px 24px 0 24px;
    margin: -1rem -1rem 1.5rem -1rem;
}
.header-price {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 26px;
    font-weight: 700;
    color: #E8C547;
}
.info-banner {
    background: #0F1620;
    border: 1px solid #1E2E3E;
    border-radius: 10px;
    padding: 10px 16px;
    font-size: 13px;
    color: #7B9FFF;
    line-height: 1.7;
    margin-bottom: 16px;
}
.kv-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
}
.kv-item {
    background: #0D0D10;
    border-radius: 6px;
    padding: 8px 10px;
}
.kv-label { font-size: 10px; color: #555; margin-bottom: 3px; }
.kv-value { font-size: 12px; color: #C0BDB4; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════
#  데이터
# ════════════════════════════════════════════════════

revenue_data = pd.DataFrame([
    {"year": "2021", "rev": 224, "op": -9,  "opM": -4.2},
    {"year": "2022", "rev": 259, "op": -22, "opM": -8.4},
    {"year": "2023", "rev": 291, "op": -53, "opM": -18.2},
    {"year": "2024", "rev": 300, "op": -30, "opM": -10.0},
    {"year": "2025E","rev": 420, "op":  52, "opM":  12.4},
    {"year": "2026F","rev": 680, "op": 110, "opM":  16.2},
])

quarter_data = pd.DataFrame([
    {"q": "24Q1", "rev":  70, "op": -12},
    {"q": "24Q2", "rev":  75, "op":  -9},
    {"q": "24Q3", "rev":  68, "op":  -9},
    {"q": "24Q4", "rev":  87, "op":   0},
    {"q": "25Q1", "rev": 102, "op":   8},
    {"q": "25Q2", "rev": 105, "op":  11},
    {"q": "25Q3", "rev":  97, "op":  12},
    {"q": "25Q4", "rev": 116, "op":  21},
])

radar_data = {
    "subject": ["유동성","안정성","성장성","수익성","활동성"],
    "value":   [75, 68, 90, 55, 62],
}

valuation = [
    {"label": "현재 주가 (2026.03)",    "value": "242,000원",        "color": "#E8C547"},
    {"label": "시가총액",               "value": "3.67조원",          "color": "#E8C547"},
    {"label": "2025 연간 매출 (추정)",   "value": "약 420억원",        "color": "#aaa"},
    {"label": "PSR (주가/매출)",         "value": "약 87x",            "color": "#FF8C69", "warn": True},
    {"label": "PBR",                    "value": "약 12x",            "color": "#FF8C69", "warn": True},
    {"label": "애널리스트 목표가 평균",  "value": "149,000원",         "color": "#4EC9B0"},
    {"label": "다이와증권 목표가",       "value": "360,000원",         "color": "#7B9FFF"},
    {"label": "컨센서스 하락 여력",      "value": "-38% (고평가 구간)", "color": "#FF8C69", "warn": True},
]

peers = [
    {"name": "로보티즈",      "cap": "3.67조", "psr25": "87x",  "pbr25": "12x",  "color": "#E8C547"},
    {"name": "레인보우로보틱스","cap": "2.9조", "psr25": "N/A",  "pbr25": "18x",  "color": "#4EC9B0"},
    {"name": "두산로보틱스",   "cap": "3.2조",  "psr25": "N/A",  "pbr25": "9x",   "color": "#7B9FFF"},
    {"name": "에스피지",       "cap": "0.7조",  "psr25": "2.2x", "pbr25": "3.4x", "color": "#FF8C69"},
]

checkpoints = [
    {"icon": "📌", "label": "액추에이터 해외 매출 확대 속도",    "note": "2025 4Q 영업이익률 36%로 급등. 고부가 로봇 손 제품 반영"},
    {"icon": "📌", "label": "AI 워커 양산 및 수주 가시화",       "note": "2025년 70대 → 2027년 1,000대 목표. 오픈AI 공급 협의 진행 중"},
    {"icon": "📌", "label": "LG전자 협업 구체화 여부",           "note": "2024년 6월 휴머노이드 공동연구 협약 체결. 실질 납품 여부 주목"},
    {"icon": "📌", "label": "로봇 손(5F·20DoF) 양산 시점",      "note": "2026년부터 글로벌 빅테크 선주문 반영 기대"},
    {"icon": "📌", "label": "물적분할 후 지배구조 안정화",       "note": "2025년 자율주행 사업부 분할 완료. 주주가치 영향 모니터링"},
]

risks = [
    "매출의 98% 다이나믹셀 단일 의존 → 집중 리스크 여전히 상존",
    "모터 외부 조달 의존 → 공급망 병목 리스크",
    "시총 3.67조 vs 매출 420억 → PSR 87x 극단적 프리미엄",
    "자율주행로봇 규제·현장 배치 지연 가능성",
    "테슬라 옵티머스 생산량 발표(2Q26) 기준치 미달 시 로봇주 전반 조정 우려",
]

radar_compare = pd.DataFrame([
    {"subject": "기술 원천성",   "로보티즈": 92, "유니트리": 70, "아지봇": 65, "MAXON": 95},
    {"subject": "가격 경쟁력",   "로보티즈": 70, "유니트리": 98, "아지봇": 90, "MAXON": 20},
    {"subject": "양산 규모",     "로보티즈": 45, "유니트리": 95, "아지봇": 98, "MAXON": 60},
    {"subject": "글로벌 생태계", "로보티즈": 85, "유니트리": 55, "아지봇": 40, "MAXON": 80},
    {"subject": "수익성",        "로보티즈": 72, "유니트리": 50, "아지봇": 30, "MAXON": 85},
    {"subject": "규제 리스크",   "로보티즈": 90, "유니트리": 40, "아지봇": 35, "MAXON": 95},
])

comp_data = [
    {"name": "로보티즈",     "cap": 3.67, "rev25": 420, "op25":  52, "backer": "LG전자(2대주주)", "color": "#E8C547"},
    {"name": "레인보우로보틱스","cap": 9.0,"rev25": 220, "op25": -30, "backer": "삼성전자 인수",  "color": "#4EC9B0"},
    {"name": "두산로보틱스", "cap": 5.2,  "rev25": 200, "op25":-277, "backer": "두산그룹",       "color": "#7B9FFF"},
    {"name": "에스피지",     "cap": 0.7,  "rev25": 800, "op25": 110, "backer": "독립",           "color": "#FF8C69"},
]

pipeline_items = [
    {"stage":"출하 중",  "stageColor":"#4EC9B0","product":"AI 워커 (고정형)","icon":"🦾",
     "detail":"오픈AI·국내외 40곳+ 주문 접수. 고정형 4천만원대, 이동형 7천만원대. PoC 완료, 공식 판매 개시.",
     "target":"2025년 70대 → 2027년 1,000대","rev":"25년 35억E → 27년 632억F","risk":"생산 캐파 제약"},
    {"stage":"CES 공개","stageColor":"#7B9FFF","product":"로봇 손 HX5 (20자유도)","icon":"🤲",
     "detail":"CES 2026 K-휴머노이드관 시연. 핑거 전용 액추에이터 자체 개발. 오픈AI에 R&D용 소량 납품 완료.",
     "target":"2026년 양산 · 글로벌 빅테크 납품","rev":"26년부터 매출 본격 반영","risk":"경쟁사(테솔로, 샤르파) 동시 출시"},
    {"stage":"협의 중",  "stageColor":"#E8C547","product":"AI 워커 (모바일형)","icon":"🚀",
     "detail":"바퀴형 베이스 추가. 25자유도 자체 액추에이터. 대기업 물류센터·공장 R&D 검증 진행 중.",
     "target":"2025 4Q 정식 출시","rev":"26년 B2B 납품 본격화","risk":"현장 검증 지연 가능성"},
    {"stage":"개발 중",  "stageColor":"#FF8C69","product":"DYNAMIXEL Y 시리즈","icon":"🔩",
     "detail":"고성능 프레임리스 모터 + 전자식 브레이크. 협동로봇 관절 최적화. 기존 X·P 대비 정밀도 향상.",
     "target":"2026년 양산 확대","rev":"액추에이터 부문 ASP 상승 기여","risk":"기존 제품 캐니벌라이제이션"},
    {"stage":"RaaS 운영","stageColor":"#C084FC","product":"GAEMI 자율주행 로봇","icon":"🚗",
     "detail":"운행안전인증 국내 1호. CJ물류 협약. 호텔·관공서 구독 서비스 중. 실외 배송 본격화 준비.",
     "target":"26년 RaaS 가입처 확대","rev":"구독 MRR 성장 중","risk":"규제·현장 배치 속도"},
]

roadmap = [
    {"period":"25 1H","events":["AI 워커 고정형 출시","흑자 전환 달성","오픈AI 협의 구체화"]},
    {"period":"25 2H","events":["로봇 손 CoRL 공개","모바일형 AI 워커 출시","연간 흑자 확정"]},
    {"period":"26 1H","events":["CES 2026 HX5 시연","로봇 손 양산 개시","AI 워커 100대 달성 목표"]},
    {"period":"26 2H","events":["글로벌 빅테크 납품 본격화","DYD 감속기 협동로봇 채택","GAEMI RaaS 확대"]},
    {"period":"27+",  "events":["AI 워커 1,000대","액추에이터 매출 970억F","휴머노이드 매출 632억F"]},
]

adoption_scenarios = pd.DataFrame([
    {"year":"2024",  "연구기관": 80, "초기상업": 15, "대량양산":  5},
    {"year":"2025E", "연구기관": 72, "초기상업": 22, "대량양산":  6},
    {"year":"2026F", "연구기관": 60, "초기상업": 30, "대량양산": 10},
    {"year":"2027F", "연구기관": 48, "초기상업": 35, "대량양산": 17},
    {"year":"2028F", "연구기관": 38, "초기상업": 36, "대량양산": 26},
    {"year":"2030F", "연구기관": 25, "초기상업": 33, "대량양산": 42},
])

tam_data = pd.DataFrame([
    {"year":"2025",  "market": 0.18, "tam": 0.016},
    {"year":"2026F", "market": 0.72, "tam": 0.055},
    {"year":"2027F", "market": 1.8,  "tam": 0.12},
    {"year":"2028F", "market": 3.5,  "tam": 0.20},
    {"year":"2030F", "market": 6.0,  "tam": 0.28},
    {"year":"2035F", "market": 51,   "tam": 1.50},
])

china_rivals = [
    {"name":"유니트리 (Unitree)","country":"🇨🇳","city":"항저우",
     "threat":"CRITICAL","tc":"#FF4444",
     "product":"G1·H1 액추에이터 내재화","price":"G1 휴머노이드 $16,000 / R1 $5,900",
     "shipment":"2025년 4,200대 출하 (글로벌 2위)",
     "strength":"초저가 + 자체 액추에이터 수직계열화 완성. 글로벌 연구기관·대학 대량 납품",
     "weakness":"정밀도·내구성은 다이나믹셀 대비 열위. 선진국 수출 규제 리스크",
     "overlap":"연구·교육 시장에서 다이나믹셀 직접 대체 위협"},
    {"name":"아지봇 (AgiBot)","country":"🇨🇳","city":"상하이",
     "threat":"HIGH","tc":"#FF8C69",
     "product":"링시X2 전용 액추에이터","price":"휴머노이드 완제품 위주, 부품 비공개",
     "shipment":"2025년 5,200대 출하 (글로벌 1위). LG전자·미래에셋 전략 투자",
     "strength":"최대 양산 규모. 알리바바 다모아카데미 AI 기술 접목. 중국 정부 지원",
     "weakness":"부품 외판보다 완제품 판매 중심. 해외 진출 제한적",
     "overlap":"직접 경쟁 낮으나 완제품 가격 압력으로 글로벌 시장 간접 압박"},
    {"name":"푸리에 (Fourier)","country":"🇨🇳","city":"상하이",
     "threat":"HIGH","tc":"#FF8C69",
     "product":"GR-2·GR-3 전용 액추에이터 + 재활로봇","price":"기업가치 80억위안 (유니콘). 부품 OEM 판매",
     "shipment":"의료 재활 누적 100만명+ 서비스. 휴머노이드 연구기관 납품",
     "strength":"의료·재활 실증 데이터 강점. 힘 제어 기반 파지 기술. 글로벌 연구기관 파트너",
     "weakness":"휴머노이드 상용화 초기 단계. 양산 속도 느림",
     "overlap":"연구·의료 시장에서 다이나믹셀 연구용 수요 잠식 가능"},
    {"name":"MAXON Motor","country":"🇨🇭","city":"스위스",
     "threat":"MED","tc":"#4EC9B0",
     "product":"고정밀 DC 모터·액추에이터","price":"프리미엄 산업용. 단가 다이나믹셀 대비 3~10배",
     "shipment":"화성 탐사로버 포함 우주·의료 분야 납품",
     "strength":"최고 신뢰성·정밀도. 방산·의료 인증 다수 보유",
     "weakness":"가격 매우 높음. 연구용 표준화 생태계 없음",
     "overlap":"프리미엄 산업 시장. 직접 충돌 낮음"},
]

price_events = [
    {"date":"2024.06","event":"LG전자 휴머노이드 협약",           "dir":"↑"},
    {"date":"2024.10","event":"보스턴다이내믹스 700개 공급",       "dir":"↑"},
    {"date":"2024.12","event":"자율주행 사업부 물적분할",           "dir":"↓"},
    {"date":"2025.01","event":"피지컬 AI 테마 급등 시작",          "dir":"↑↑"},
    {"date":"2025.05","event":"1Q25 흑자전환 발표",                "dir":"↑"},
    {"date":"2025.11","event":"3Q25 누적 흑자전환 확인",           "dir":"↑"},
    {"date":"2026.01","event":"최고가 349,500원 기록",             "dir":"▲"},
    {"date":"2026.03","event":"현재 242,000원 (고점比 -31%)",      "dir":"↓"},
]

# ════════════════════════════════════════════════════
#  헬퍼 함수
# ════════════════════════════════════════════════════

DARK_TEMPLATE = dict(
    template="plotly_dark",
    paper_bgcolor="#111114",
    plot_bgcolor="#111114",
    font=dict(family="Noto Sans KR, sans-serif", color="#888"),
    margin=dict(l=10, r=10, t=30, b=10),
)

def bar_color(val, is_forecast=False):
    if is_forecast:
        return "rgba(232,197,71,0.4)"
    return "#E8C547"

def op_color(val, is_forecast=False):
    if is_forecast:
        return "rgba(78,201,176,0.4)" if val >= 0 else "rgba(255,140,105,0.4)"
    return "rgba(78,201,176,0.67)" if val >= 0 else "rgba(255,140,105,0.67)"


def metric_card(label, value, sub, color):
    st.markdown(f"""
    <div style="background:#111114;border:1px solid #1E1E24;border-radius:12px;
                padding:16px 18px;border-top:2px solid {color};">
      <div style="font-size:10px;color:#555;font-family:'IBM Plex Mono',monospace;
                  letter-spacing:1px;margin-bottom:8px;">{label.upper()}</div>
      <div style="font-size:20px;font-weight:700;color:{color};">{value}</div>
      <div style="font-size:11px;color:#555;margin-top:4px;">{sub}</div>
    </div>
    """, unsafe_allow_html=True)


def section_title(emoji, text, color="#888"):
    st.markdown(f"""
    <div style="font-size:12px;color:{color};font-weight:600;margin-bottom:12px;">
      {emoji} {text}
    </div>""", unsafe_allow_html=True)


def card_wrap(content_html, extra_style=""):
    st.markdown(f"""
    <div class="ir-card" style="{extra_style}">
      {content_html}
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════
#  헤더
# ════════════════════════════════════════════════════

st.markdown("""
<div style="background:#0D0D10;border-bottom:1px solid #1E1E24;padding:18px 8px 0;">
  <div style="display:flex;align-items:center;justify-content:space-between;padding-bottom:14px;">
    <div style="display:flex;align-items:center;gap:14px;">
      <div style="background:linear-gradient(135deg,#E8C547,#FF8C69);width:38px;height:38px;
                  border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px;">🤖</div>
      <div>
        <div style="font-size:11px;font-family:'IBM Plex Mono',monospace;color:#555;letter-spacing:2px;margin-bottom:2px;">
          KOSDAQ | 자본재 | 기업분석
        </div>
        <div style="font-size:22px;font-weight:700;letter-spacing:-0.5px;">
          로보티즈 <span style="color:#999;font-size:14px;font-weight:400;">(108490)</span>
        </div>
      </div>
    </div>
    <div style="display:flex;gap:24px;align-items:center;">
      <div style="text-align:right;">
        <div style="font-family:'IBM Plex Mono',monospace;font-size:24px;font-weight:600;color:#E8C547;">
          242,000<span style="font-size:12px;color:#666;">원</span>
        </div>
        <div style="font-size:11px;color:#555;">시총 3.67조 · KOSDAQ</div>
      </div>
      <div style="background:#1A2A1A;border:1px solid #2A4A2A;border-radius:8px;
                  padding:6px 14px;font-size:11px;color:#4EC9B0;font-family:'IBM Plex Mono',monospace;letter-spacing:1px;">
        2026.03 UPDATE
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-banner" style="margin-top:16px;">
  <span style="font-weight:600;">■ </span>
  로보티즈는 피지컬 AI 시대 핵심 부품(다이나믹셀 액추에이터·감속기) 및 AI 워커 전문기업. 2025년 코스닥 상장(2018년) 이후 첫 연간 흑자 전환 달성.&nbsp;&nbsp;
  <span style="font-weight:600;">■ </span>
  주가 1년 +1,052% 급등으로 PSR 87배 수준의 극단적 프리미엄 형성. 실적 가시화 속도가 핵심 변수.&nbsp;&nbsp;
  <span style="font-weight:600;">■ </span>
  2025년 매출 약 420억원, 영업이익 약 52억원 추정(4Q25 영업이익률 36% 기록).
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════
#  탭 네비게이션
# ════════════════════════════════════════════════════

tabs = st.tabs(["✅ 체크포인트", "🏢 기업 개요", "📡 마켓 포지셔닝",
                "🔧 파이프라인", "⚔️ 경쟁 분석", "📈 실적 추이", "💰 밸류에이션"])

# ════════════════════════════════════════════════════
#  0. 체크포인트
# ════════════════════════════════════════════════════
with tabs[0]:
    # KPI 카드
    kpi_cols = st.columns(4)
    kpi_data = [
        ("2025 매출(E)", "420억원",   "+40% YoY",       "#E8C547"),
        ("2025 영업이익(E)", "+52억원","첫 연간 흑자",   "#4EC9B0"),
        ("4Q25 OPM", "36%",          "역대 최고 수준",   "#7B9FFF"),
        ("2026 매출 목표","680억원(F)","다이와증권 추정", "#FF8C69"),
    ]
    for col, (label, value, sub, color) in zip(kpi_cols, kpi_data):
        with col:
            metric_card(label, value, sub, color)

    st.markdown("<div style='height:8px'/>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="ir-card">
          <div style="font-size:12px;color:#E8C547;font-weight:600;margin-bottom:14px;">📋 향후 주목 체크포인트</div>
        """, unsafe_allow_html=True)
        if "cp_checked" not in st.session_state:
            st.session_state.cp_checked = {i: False for i in range(len(checkpoints))}
        for i, cp in enumerate(checkpoints):
            checked = st.session_state.cp_checked[i]
            key = f"cp_{i}"
            col_cb, col_text = st.columns([1, 11])
            with col_cb:
                val = st.checkbox("", value=checked, key=key)
                st.session_state.cp_checked[i] = val
            with col_text:
                style = "text-decoration:line-through;color:#555;" if val else "color:#C0BDB4;"
                st.markdown(f"""
                <div style="{style}font-size:13px;margin-bottom:2px;">{cp['icon']} {cp['label']}</div>
                <div style="font-size:11px;color:#555;line-height:1.5;">{cp['note']}</div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="ir-card ir-card-red">
          <div style="font-size:12px;color:#FF8C69;font-weight:600;margin-bottom:14px;">⚠️ 리스크 요인</div>
        """, unsafe_allow_html=True)
        for r in risks:
            st.markdown(f"""
            <div style="display:flex;gap:10px;margin-bottom:12px;padding-bottom:12px;border-bottom:1px solid #1A1A1E;">
              <div style="width:6px;height:6px;border-radius:50%;background:#FF8C69;margin-top:6px;flex-shrink:0;"></div>
              <div style="font-size:13px;color:#A0A09A;line-height:1.6;">{r}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # 주가 이벤트
    st.markdown("""
    <div class="ir-card">
      <div style="font-size:12px;color:#888;font-weight:500;margin-bottom:14px;">📈 주요 주가 이벤트 (2024~2026)</div>
      <div style="display:flex;gap:8px;overflow-x:auto;padding-bottom:4px;">
    """, unsafe_allow_html=True)

    ev_html = ""
    for ev in price_events:
        dir_color = "#4EC9B0" if "↑" in ev["dir"] or "▲" in ev["dir"] else "#FF8C69"
        ev_html += f"""
        <div style="flex-shrink:0;width:130px;padding:10px 12px;background:#0D0D10;border-radius:8px;border:1px solid #1E1E24;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#555;margin-bottom:6px;">{ev['date']}</div>
          <div style="font-size:11px;color:#B0ACA4;line-height:1.5;margin-bottom:6px;">{ev['event']}</div>
          <div style="font-size:14px;color:{dir_color};">{ev['dir']}</div>
        </div>"""

    st.markdown(ev_html + "</div></div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════
#  1. 기업 개요
# ════════════════════════════════════════════════════
with tabs[1]:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="ir-card">
          <div style="font-size:12px;color:#888;font-weight:500;margin-bottom:14px;">🏢 기업 개요</div>
          <div style="font-size:13px;color:#B0ACA4;line-height:1.9;">
            1999년 설립. 로봇전용 스마트 액추에이터
            <span style="color:#E8C547;font-weight:600;">다이나믹셀(DYNAMIXEL)</span> 제조를 주력으로 성장.
            2018년 코스닥 기술특례 상장. 글로벌 로봇 연구·대회 플랫폼
            <span style="color:#4EC9B0;">약 80%</span>에 채택.
            2024~2025년 피지컬 AI 워커, 로봇 손 등 신사업으로 확장.
            2025년 코스닥 상장(2018년) 이후 첫 연간 흑자 전환 달성.
          </div>
          <div class="kv-grid" style="margin-top:16px;">
        """, unsafe_allow_html=True)

        kv_items = [
            ("설립","1999.04"),("대표","김병수"),
            ("상장","2018년 코스닥"),("임직원","약 114명"),
            ("수출 비중","약 70%+"),("미국법인","ROBOTIS Inc."),
        ]
        kv_html = "".join(f"""
        <div class="kv-item">
          <div class="kv-label">{k}</div>
          <div class="kv-value">{v}</div>
        </div>""" for k, v in kv_items)
        st.markdown(kv_html + "</div></div>", unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="ir-card">
          <div style="font-size:12px;color:#888;font-weight:500;margin-bottom:14px;">🔗 주주 구성 &amp; 주요 파트너</div>
        """, unsafe_allow_html=True)

        shareholders = [
            {"name":"김병수 외 특수관계인","pct":"23.85%","pct_val":23.85,"role":"최대주주","color":"#E8C547"},
            {"name":"LG전자","pct":"6.60%","pct_val":6.60,"role":"2대주주 · 휴머노이드 협약","color":"#4EC9B0"},
            {"name":"기타 소액주주","pct":"69.55%","pct_val":69.55,"role":"유동주식","color":"#555"},
        ]
        for s in shareholders:
            st.markdown(f"""
            <div style="margin-bottom:12px;padding-bottom:12px;border-bottom:1px solid #1A1A1E;">
              <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                <span style="color:{s['color']};font-weight:600;font-size:13px;">{s['name']}</span>
                <span style="font-family:'IBM Plex Mono',monospace;color:{s['color']};font-size:13px;">{s['pct']}</span>
              </div>
              <div style="background:#1A1A1E;border-radius:3px;height:5px;overflow:hidden;margin-bottom:4px;">
                <div style="width:{s['pct_val']}%;height:100%;background:{s['color']};border-radius:3px;"></div>
              </div>
              <div style="font-size:11px;color:#555;">{s['role']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
          <div style="margin-top:12px;font-size:11px;color:#4EC9B0;background:#0F1F18;border-radius:8px;padding:10px 12px;line-height:1.7;">
            💡 2024.06 LG전자와 '휴머노이드 로봇 공동연구 및 사업화' 협약 체결.
            MIT 피지컬AI 공동연구, 보스턴다이내믹스·오픈AI 공급 협의 중.
          </div>
        </div>
        """, unsafe_allow_html=True)

    # 제품 포트폴리오
    st.markdown("""
    <div class="ir-card" style="margin-top:4px;">
      <div style="font-size:12px;color:#888;font-weight:500;margin-bottom:16px;">🤖 제품 포트폴리오 (2026 기준)</div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:12px;">
    """, unsafe_allow_html=True)

    products = [
        {"icon":"🔩","name":"DYNAMIXEL","sub":"X·P·Y 시리즈","status":"매출 98%","badge":"캐시카우","bc":"#E8C547","desc":"100여종 라인업. 보스턴다이내믹스 납품. 글로벌 표준."},
        {"icon":"🦾","name":"AI 워커","sub":"피지컬 AI 세미 휴머노이드","status":"25년 출하 70대","badge":"신성장","bc":"#4EC9B0","desc":"오픈AI 공급 협의. 27년 1,000대 목표."},
        {"icon":"🤲","name":"로봇 손","sub":"5F·20DoF 고정밀","status":"2026 양산","badge":"파이프라인","bc":"#7B9FFF","desc":"팔당 15kg 하중. 글로벌 빅테크 선주문."},
        {"icon":"🚗","name":"GAEMI","sub":"실외 자율주행로봇","status":"RaaS 운영 중","badge":"RaaS","bc":"#FF8C69","desc":"운행안전인증 국내 1호. 배송·순찰 서비스."},
    ]
    prod_html = "".join(f"""
    <div style="background:#0D0D10;border-radius:10px;padding:14px;border:1px solid {p['bc']}22;">
      <div style="font-size:20px;margin-bottom:8px;">{p['icon']}</div>
      <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">
        <span style="font-weight:700;font-size:13px;color:{p['bc']};">{p['name']}</span>
        <span style="background:{p['bc']}22;color:{p['bc']};font-size:9px;padding:2px 6px;border-radius:4px;">{p['badge']}</span>
      </div>
      <div style="font-size:11px;color:#666;margin-bottom:8px;">{p['sub']}</div>
      <div style="font-size:10px;font-family:'IBM Plex Mono',monospace;color:{p['bc']};margin-bottom:8px;">{p['status']}</div>
      <div style="font-size:11px;color:#666;line-height:1.5;">{p['desc']}</div>
    </div>""" for p in products)
    st.markdown(prod_html + "</div></div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════
#  2. 마켓 포지셔닝
# ════════════════════════════════════════════════════
with tabs[2]:
    section_title("📊","글로벌 휴머노이드 시장 TAM vs 로보티즈 기회")

    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        fig.add_bar(x=tam_data["year"], y=tam_data["market"],
                    name="글로벌 시장(조원)", marker_color="rgba(123,159,255,0.27)")
        fig.add_bar(x=tam_data["year"], y=tam_data["tam"],
                    name="로보티즈 TAM(조원)", marker_color="#E8C547")
        fig.update_layout(**DARK_TEMPLATE, title="시장 vs 로보티즈 TAM (조원)", barmode="overlay",
                          legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = go.Figure()
        fig2.add_bar(x=adoption_scenarios["year"], y=adoption_scenarios["연구기관"],
                     name="연구기관", marker_color="#4EC9B0")
        fig2.add_bar(x=adoption_scenarios["year"], y=adoption_scenarios["초기상업"],
                     name="초기상업화", marker_color="#E8C547")
        fig2.add_bar(x=adoption_scenarios["year"], y=adoption_scenarios["대량양산"],
                     name="대량양산", marker_color="#FF8C69")
        fig2.update_layout(**DARK_TEMPLATE, title="모듈형 채택률 시나리오 (%)", barmode="stack",
                           legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig2, use_container_width=True)

    # 페이스메이커 Phase
    section_title("🔄","피지컬 AI 시장 로보티즈 수혜 4단계")

    pacemaker = [
        {"label":"Phase 1","title":"연구 표준 (현재)","color":"#4EC9B0","icon":"🔬",
         "desc":"글로벌 연구기관 80%+ 다이나믹셀 채택. 피지컬 AI 학습 데이터가 다이나믹셀 환경에서 생성됨.",
         "robotis":"다이나믹셀 = 피지컬AI 학습의 표준 하드웨어.",
         "kpi":"글로벌 연구기관 채택 수 / ROS2 패키지 DYNAMIXEL 의존도"},
        {"label":"Phase 2","title":"초기 상업화 전환 (2025~2027)","color":"#E8C547","icon":"🏭",
         "desc":"연구 프로토타입 → 소량 B2B 납품. 검증된 다이나믹셀 기반 설계가 그대로 양산 BOM에 탑재.",
         "robotis":"오픈AI AI 워커, K-휴머노이드 연합이 이 단계. 수직계열화 전환 전 모듈형 수요 피크.",
         "kpi":"AI 워커 수주 누적 / 로봇 손 빅테크 납품 건수"},
        {"label":"Phase 3","title":"대량양산 분기점 (2027~2030)","color":"#FF8C69","icon":"⚠️",
         "desc":"연간 수만 대 이상 생산 시 OEM들이 원가 절감 위해 내재화 검토. 모듈형 비중 감소 압력.",
         "robotis":"핵심 위험 구간. 고마진 Y 시리즈·로봇 손으로 포지션 유지해야.",
         "kpi":"DYNAMIXEL Y 시리즈 OEM 채택 비율 / 로봇 손 대형 고객사 Lock-in 수"},
        {"label":"Phase 4","title":"생태계 플랫폼화 (2030+)","color":"#7B9FFF","icon":"🌐",
         "desc":"다이나믹셀이 로봇 관절의 USB-C처럼 통용 표준이 된 경우 vs. 틈새 프리미엄으로 축소된 경우.",
         "robotis":"낙관: 피지컬 AI OS + 하드웨어 표준 통합으로 인텔 CPU급 위상. 비관: 중국 저가에 시장 잠식.",
         "kpi":"독립 로봇 스타트업의 DYNAMIXEL 기본 채택 여부 / 표준화 기구 참여"},
    ]

    pm_cols = st.columns(4)
    for col, pm in zip(pm_cols, pacemaker):
        with col:
            st.markdown(f"""
            <div style="background:#111114;border:1px solid #1E1E24;border-radius:12px;padding:16px;
                        border-top:3px solid {pm['color']};">
              <div style="font-size:10px;color:{pm['color']};font-family:'IBM Plex Mono',monospace;
                          margin-bottom:6px;">{pm['label']}</div>
              <div style="font-size:12px;font-weight:700;color:#E0DDD5;margin-bottom:10px;">
                {pm['icon']} {pm['title']}
              </div>
              <div style="font-size:11px;color:#666;line-height:1.6;margin-bottom:8px;">{pm['desc']}</div>
              <div style="background:{pm['color']}11;border:1px solid {pm['color']}33;border-radius:6px;
                          padding:8px 10px;font-size:11px;color:#888;line-height:1.6;margin-bottom:6px;">
                🎯 {pm['robotis']}
              </div>
              <div style="font-size:10px;color:#555;border-top:1px solid #1A1A1E;padding-top:6px;">
                📊 KPI: {pm['kpi']}
              </div>
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════
#  3. 파이프라인
# ════════════════════════════════════════════════════
with tabs[3]:
    # 1000억 유상증자
    st.markdown("""
    <div style="border:1px solid #4EC9B066;border-radius:12px;padding:20px 24px;margin-bottom:18px;
                background:linear-gradient(135deg,#0A0D10,#0A120F);">
      <div style="font-size:14px;font-weight:700;color:#4EC9B0;margin-bottom:8px;">
        📋 1,000억 유상증자 자금사용 계획 — 공시 원문 기반 (2025.08.28)
      </div>
      <div style="font-size:12px;color:#666;line-height:1.7;">
        <span style="color:#E8C547;font-weight:600;">핵심 전략:</span>
        피지컬 AI 시대의 두 가지 병목 — <strong style="color:#E0DDD5;">가격경쟁력 있는 QDD 액추에이터</strong>와
        <strong style="color:#E0DDD5;">실세계 피지컬 데이터</strong> — 을 동시에 해결.
        우즈베키스탄을 글로벌 생산·데이터 거점으로 구축.
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    facility_items = [
        ("우즈베키스탄 신공장 건설·인수","~480억",80,"타슈켄트 인근 2만평 부지. 우즈벡 정부 국가전략사업 지정."),
        ("정밀 가공시설 확충","350억",58,"Capa 10배 이상 확대. 26년/28년 분할 투자."),
        ("모터 생산시설","75억",13,"모터 내재화율 제고. 중국 부품 의존 탈피."),
        ("로봇 완제품 생산라인","150억",25,"AI 워커·휴머노이드 양산 대응."),
        ("데이터팩토리 구축","25억",4,"2025년 8월 우즈벡 1단계 운영 이미 개시."),
    ]
    with c1:
        st.markdown("""<div style="background:#0A0A0C;border-radius:8px;padding:16px;border:1px solid #4EC9B033;">
        <div style="display:flex;justify-content:space-between;margin-bottom:12px;">
          <span style="font-size:12px;font-weight:700;color:#4EC9B0;">🏭 시설자금</span>
          <span style="font-size:14px;font-weight:700;color:#4EC9B0;font-family:'IBM Plex Mono',monospace;">600억원</span>
        </div>""", unsafe_allow_html=True)
        for item, amt, pct, note in facility_items:
            st.markdown(f"""
            <div style="margin-bottom:10px;padding-bottom:10px;border-bottom:1px solid #1A1A1E;">
              <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                <span style="font-size:12px;color:#C0BDB4;">{item}</span>
                <span style="font-size:12px;color:#4EC9B0;font-family:'IBM Plex Mono',monospace;">{amt}</span>
              </div>
              <div style="background:#1A1A1E;border-radius:3px;height:5px;margin-bottom:4px;overflow:hidden;">
                <div style="width:{pct}%;height:100%;background:#4EC9B0;border-radius:3px;"></div>
              </div>
              <div style="font-size:10px;color:#555;line-height:1.5;">{note}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    opex_items = [
        ("QDD 액추에이터 R&D","120억",30,"#E8C547","QDD: 기어비 낮춰 역구동성 극대화 → 강화학습 수용 최적 구조."),
        ("자체 신규 모터 개발","120억",30,"#E8C547","모터 자체 생산 → 핵심 원가 내재화. 중국산 모터 의존 탈피."),
        ("데이터팩토리 운영비","60억",15,"#C084FC","실세계 피지컬 데이터 수집·가공. AI 파운데이션 모델 학습용."),
        ("정밀 가공·모터 운영비","100억",25,"#7B9FFF","신규 생산 시설 가동 준비 인건비·재료비 선확보."),
    ]
    with c2:
        st.markdown("""<div style="background:#0A0A0C;border-radius:8px;padding:16px;border:1px solid #E8C54733;">
        <div style="display:flex;justify-content:space-between;margin-bottom:12px;">
          <span style="font-size:12px;font-weight:700;color:#E8C547;">⚙️ 운영자금</span>
          <span style="font-size:14px;font-weight:700;color:#E8C547;font-family:'IBM Plex Mono',monospace;">400억원</span>
        </div>""", unsafe_allow_html=True)
        for item, amt, pct, color, note in opex_items:
            st.markdown(f"""
            <div style="margin-bottom:10px;padding-bottom:10px;border-bottom:1px solid #1A1A1E;">
              <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                <span style="font-size:12px;color:#C0BDB4;">{item}</span>
                <span style="font-size:12px;color:{color};font-family:'IBM Plex Mono',monospace;">{amt}</span>
              </div>
              <div style="background:#1A1A1E;border-radius:3px;height:5px;margin-bottom:4px;overflow:hidden;">
                <div style="width:{pct}%;height:100%;background:{color};border-radius:3px;"></div>
              </div>
              <div style="font-size:10px;color:#555;line-height:1.5;">{note}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # 로드맵 타임라인
    st.markdown("""
    <div class="ir-card" style="margin-top:8px;">
      <div style="font-size:12px;color:#888;font-weight:500;margin-bottom:16px;">🗓️ 제품 로드맵 타임라인</div>
      <div style="display:flex;gap:12px;overflow-x:auto;padding-bottom:8px;">
    """, unsafe_allow_html=True)

    rm_html = ""
    for i, r in enumerate(roadmap):
        is_now = (i == 2)
        bg = "#E8C547" if is_now else "#1A1A1E"
        border = "#E8C547" if is_now else "#333"
        tc = "#0A0A0C" if is_now else "#E8C547"
        etc = "#0A0A0C" if is_now else "#888"
        border_color = "rgba(10,10,12,0.27)" if is_now else "#333"
        events_html = "".join(
            f'<div style="font-size:11px;color:{etc};line-height:1.6;margin-bottom:4px;padding-left:8px;border-left:2px solid {border_color};">{ev}</div>'
            for ev in r["events"]
        )
        label = f"{r['period']} ◀ 현재" if is_now else r["period"]
        rm_html += f"""
        <div style="flex:0 0 175px;background:{bg};border:2px solid {border};border-radius:8px;padding:12px 14px;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:12px;font-weight:700;color:{tc};margin-bottom:10px;">{label}</div>
          {events_html}
        </div>"""

    st.markdown(rm_html + "</div></div>", unsafe_allow_html=True)

    # 파이프라인 카드
    section_title("🔧","제품 파이프라인")
    if "pl_checked" not in st.session_state:
        st.session_state.pl_checked = {i: False for i in range(len(pipeline_items))}

    for i, p in enumerate(pipeline_items):
        key = f"pl_{i}"
        checked = st.session_state.pl_checked[i]
        col_cb, col_card = st.columns([1, 20])
        with col_cb:
            val = st.checkbox("", value=checked, key=key)
            st.session_state.pl_checked[i] = val
        with col_card:
            st.markdown(f"""
            <div style="background:#111114;border:1px solid #1E1E24;border-radius:12px;
                        padding:16px 20px;border-left:3px solid {p['stageColor']};">
              <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                <span style="font-size:18px;">{p['icon']}</span>
                <span style="font-size:13px;font-weight:700;color:#E0DDD5;">{p['product']}</span>
                <span style="background:{p['stageColor']}22;color:{p['stageColor']};font-size:10px;
                             padding:2px 8px;border-radius:4px;font-family:'IBM Plex Mono',monospace;">
                  {p['stage']}
                </span>
              </div>
              <div style="font-size:12px;color:#888;line-height:1.6;margin-bottom:6px;">{p['detail']}</div>
              <div style="display:flex;gap:16px;font-size:11px;color:#555;">
                <span>🎯 {p['target']}</span>
                <span style="color:{p['stageColor']};">💰 {p['rev']}</span>
                <span style="color:#FF8C69;">⚠️ {p['risk']}</span>
              </div>
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════
#  4. 경쟁 분석
# ════════════════════════════════════════════════════
with tabs[4]:
    # 경고 배너
    st.markdown("""
    <div style="background:linear-gradient(90deg,#FF444422,#FF8C6911);border:1px solid #FF444444;
                border-radius:10px;padding:14px 20px;margin-bottom:16px;display:flex;align-items:center;gap:14px;">
      <span style="font-size:24px;">🚨</span>
      <div>
        <div style="font-size:13px;font-weight:700;color:#FF6B6B;margin-bottom:4px;">
          중국발 가격 파괴 위협 — 투자 핵심 리스크
        </div>
        <div style="font-size:12px;color:#888;line-height:1.7;">
          2025년 글로벌 휴머노이드 출하 1.6만대 중
          <span style="color:#FF8C69;font-weight:600;">중국산 80%+</span> 점유.
          유니트리 R1 <span style="color:#FF8C69;font-weight:600;">$5,900</span> — 미국 경쟁사의 ⅛ 수준.
          다이나믹셀 연구·교육 시장 잠식 속도가 가장 큰 단기 위협.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 중국 경쟁사 카드
    section_title("🇨🇳","중국 액추에이터·휴머노이드 경쟁사 (핵심 위협)")
    for r in china_rivals:
        st.markdown(f"""
        <div class="ir-card" style="border-left:3px solid {r['tc']};display:grid;
             grid-template-columns:200px 1fr 1fr;gap:20px;align-items:start;margin-bottom:10px;">
          <div>
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
              <span style="font-size:16px;">{r['country']}</span>
              <span style="font-size:14px;font-weight:700;color:#E0DDD5;">{r['name']}</span>
            </div>
            <div style="font-size:10px;color:#555;margin-bottom:8px;">{r['city']}</div>
            <div style="display:inline-block;background:{r['tc']}22;color:{r['tc']};font-size:10px;
                        padding:3px 10px;border-radius:4px;font-family:'IBM Plex Mono',monospace;font-weight:700;">
              위협도: {r['threat']}
            </div>
            <div style="margin-top:8px;font-size:11px;color:#666;">{r['product']}</div>
            <div style="margin-top:6px;font-size:11px;color:#E8C547;font-family:'IBM Plex Mono',monospace;">{r['price']}</div>
          </div>
          <div>
            <div style="font-size:10px;color:#4EC9B0;margin-bottom:4px;font-weight:600;">📦 출하 현황</div>
            <div style="font-size:11px;color:#888;line-height:1.6;margin-bottom:10px;">{r['shipment']}</div>
            <div style="font-size:10px;color:#4EC9B0;margin-bottom:4px;font-weight:600;">✅ 강점</div>
            <div style="font-size:11px;color:#888;line-height:1.6;">{r['strength']}</div>
          </div>
          <div>
            <div style="font-size:10px;color:#FF8C69;margin-bottom:4px;font-weight:600;">⚠️ 약점·한계</div>
            <div style="font-size:11px;color:#888;line-height:1.6;margin-bottom:10px;">{r['weakness']}</div>
            <div style="font-size:10px;color:{r['tc']};margin-bottom:4px;font-weight:600;">🎯 로보티즈 충돌 영역</div>
            <div style="font-size:11px;color:#888;line-height:1.6;">{r['overlap']}</div>
          </div>
        </div>""", unsafe_allow_html=True)

    # 레이더 + 차별화
    c1, c2 = st.columns(2)
    with c1:
        section_title("🕸️","글로벌 경쟁력 비교 레이더")
        cats = radar_compare["subject"].tolist()
        fig = go.Figure()
        for col, color, name in [
            ("로보티즈","#E8C547","로보티즈"),
            ("유니트리","#FF4444","유니트리"),
            ("아지봇","#FF8C69","아지봇"),
            ("MAXON","#4EC9B0","MAXON"),
        ]:
            vals = radar_compare[col].tolist() + [radar_compare[col].iloc[0]]
            c_cats = cats + [cats[0]]
            fig.add_trace(go.Scatterpolar(r=vals, theta=c_cats, name=name,
                line=dict(color=color, width=2), fill="toself",
                fillcolor=color.replace("#","rgba(") + ",0.1)" if False else color,
                opacity=0.85))
        fig.update_layout(**DARK_TEMPLATE,
                          polar=dict(bgcolor="#111114",
                                     radialaxis=dict(visible=True, range=[0,100], color="#333"),
                                     angularaxis=dict(color="#555")),
                          showlegend=True,
                          legend=dict(orientation="h", y=-0.15, font=dict(color="#666", size=11)))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        section_title("⚔️","로보티즈 차별화 포인트")
        diff_items = [
            {"title":"vs 유니트리·아지봇 (중국)","color":"#FF4444",
             "win":"오픈소스 생태계 80% 점유, 글로벌 연구 표준, 미·EU 수출 규제 수혜",
             "lose":"가격 경쟁력 (유니트리 대비 연구용 ASP 2~3배), 양산 규모"},
            {"title":"vs MAXON·Faulhaber (유럽)","color":"#4EC9B0",
             "win":"모듈형 설계·오픈소스·가격·피지컬AI 통합",
             "lose":"초정밀 산업·방산·의료 인증 신뢰도"},
            {"title":"vs 레인보우·두산 (국내)","color":"#7B9FFF",
             "win":"유일한 흑자·부품 원천기술·LG·오픈AI 글로벌 파트너십",
             "lose":"완성품 라인업 폭, 삼성·두산그룹 인프라·브랜드"},
        ]
        for d in diff_items:
            st.markdown(f"""
            <div style="margin-bottom:14px;padding-bottom:14px;border-bottom:1px solid #1A1A1E;">
              <div style="font-size:12px;color:{d['color']};font-weight:600;margin-bottom:6px;">{d['title']}</div>
              <div style="font-size:11px;color:#666;line-height:1.7;">
                <span style="color:#4EC9B0;">✅ 우위:</span> {d['win']}<br>
                <span style="color:#FF8C69;">⚠️ 열위:</span> {d['lose']}
              </div>
            </div>""", unsafe_allow_html=True)

    # K-로봇 재무 비교
    section_title("📊","K-로봇 빅4 재무 비교 (2025E)")
    comp_cols = st.columns(4)
    for col, c in zip(comp_cols, comp_data):
        op_col = "#4EC9B0" if c["op25"] > 0 else "#FF8C69"
        op_str = f"+{c['op25']}억" if c["op25"] > 0 else f"{c['op25']}억"
        with col:
            st.markdown(f"""
            <div style="background:#0D0D10;border-radius:10px;padding:14px 16px;border:1px solid {c['color']}33;">
              <div style="font-size:13px;font-weight:700;color:{c['color']};margin-bottom:10px;">{c['name']}</div>
              <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                <span style="font-size:10px;color:#555;">시총</span>
                <span style="font-size:11px;color:#C0BDB4;font-family:'IBM Plex Mono',monospace;">{c['cap']}조</span>
              </div>
              <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                <span style="font-size:10px;color:#555;">매출(E)</span>
                <span style="font-size:11px;color:#C0BDB4;font-family:'IBM Plex Mono',monospace;">{c['rev25']}억</span>
              </div>
              <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                <span style="font-size:10px;color:#555;">영업이익(E)</span>
                <span style="font-size:11px;color:{op_col};font-family:'IBM Plex Mono',monospace;">{op_str}</span>
              </div>
              <div style="font-size:10px;background:{c['color']}15;color:{c['color']};border-radius:4px;padding:3px 8px;text-align:center;">{c['backer']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#0F1F18;border-radius:8px;padding:10px 16px;font-size:12px;
                color:#4EC9B0;line-height:1.7;margin-top:8px;">
      💡 로보티즈는 K-로봇 4사 중 <strong>유일한 흑자 기업</strong>. 단, 진짜 위협은 국내 경쟁사가 아닌
      중국 완성품 업체의 <strong>수직계열화 + 초저가</strong> 전략. 미·EU 수출 규제가 로보티즈의 최대 지정학적 해자.
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════
#  5. 실적 추이
# ════════════════════════════════════════════════════
with tabs[5]:
    c1, c2 = st.columns(2)

    with c1:
        section_title("📊","연간 실적 추이 (억원)")
        st.caption("* 2025E 추정 · 2026F 다이와증권 전망")

        fig = go.Figure()
        rev_colors = ["#E8C547" if i < 4 else "rgba(232,197,71,0.4)" for i in range(len(revenue_data))]
        op_colors  = [op_color(row["op"], i >= 4) for i, row in revenue_data.iterrows()]

        fig.add_bar(x=revenue_data["year"], y=revenue_data["rev"], name="매출액",
                    marker_color=rev_colors)
        fig.add_bar(x=revenue_data["year"], y=revenue_data["op"], name="영업이익",
                    marker_color=op_colors)
        fig.add_hline(y=0, line_color="#333")
        fig.update_layout(**DARK_TEMPLATE, barmode="group",
                          legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig, use_container_width=True)

        # 실적 요약표
        section_title("📋","실적 요약표 (연결기준)")
        summary = {
            "구분": ["매출액(억)","YoY(%)","영업이익(억)","OPM(%)","지배순이익(억)"],
            "2023": ["291","+11.8","-53","-18.2","-27"],
            "2024": ["300","+3.1","-30","-10.0","-5"],
            "2025E":["420","+40","+52","+12.4","+18"],
        }
        df_summary = pd.DataFrame(summary)

        def color_val(val):
            if str(val).startswith("-"):
                return "color: #FF8C69"
            elif str(val).startswith("+"):
                return "color: #4EC9B0"
            return "color: #B0ACA4"

        st.dataframe(
            df_summary.set_index("구분"),
            use_container_width=True,
        )
        st.markdown("""
        <div style="background:#0F1F18;border-radius:8px;padding:10px 12px;font-size:11px;color:#4EC9B0;line-height:1.7;margin-top:8px;">
          ✅ 2025년 코스닥 상장(2018년) 이후 첫 연간 흑자 전환. 4Q25 액추에이터 OPM 36% 달성.
        </div>""", unsafe_allow_html=True)

    with c2:
        section_title("📈","분기별 실적 추이 (2024~2025)")
        st.caption("매출액(막대, 억원) / 영업이익(선, 억원)")

        q_colors = ["rgba(232,197,71,0.27)" if i < 4 else "rgba(232,197,71,0.53)" for i in range(len(quarter_data))]
        fig2 = go.Figure()
        fig2.add_bar(x=quarter_data["q"], y=quarter_data["rev"], name="매출액",
                     marker_color=q_colors)
        fig2.add_scatter(x=quarter_data["q"], y=quarter_data["op"], name="영업이익",
                         line=dict(color="#4EC9B0", width=2),
                         marker=dict(size=7, color="#4EC9B0"))
        fig2.add_hline(y=0, line_color="#333")
        fig2.update_layout(**DARK_TEMPLATE, legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig2, use_container_width=True)

        # 재무 레이더
        section_title("🕸️","재무 건전성 레이더")
        cats_r = radar_data["subject"] + [radar_data["subject"][0]]
        vals_r = radar_data["value"]  + [radar_data["value"][0]]
        fig3 = go.Figure(go.Scatterpolar(r=vals_r, theta=cats_r,
            fill="toself", fillcolor="rgba(232,197,71,0.15)",
            line=dict(color="#E8C547", width=2), name="로보티즈"))
        fig3.update_layout(**DARK_TEMPLATE,
                           polar=dict(bgcolor="#111114",
                                      radialaxis=dict(visible=True, range=[0,100], color="#333"),
                                      angularaxis=dict(color="#555")))
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown("""
        <div style="font-size:11px;color:#555;line-height:1.8;">
          ● 2025년 1분기부터 4분기 연속 흑자. 3Q25 매출 97억원(+35% YoY), 영업이익 22억원.<br>
          ● 4Q25 매출 116억원, 영업이익 21억원 — 액추에이터 OPM 36% 역대 최고.
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════
#  6. 밸류에이션
# ════════════════════════════════════════════════════
with tabs[6]:
    c1, c2 = st.columns(2)

    with c1:
        section_title("💰","밸류에이션 지표")
        for i, v in enumerate(valuation):
            border = "1px solid #1A1A1E" if i < len(valuation)-1 else "none"
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:9px 0;border-bottom:{border};">
              <span style="font-size:12px;color:#666;">{v['label']}</span>
              <span style="font-size:13px;font-weight:600;color:{v['color']};
                           font-family:'IBM Plex Mono',monospace;">{v['value']}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown("""
        <div style="margin-top:14px;background:#1A1010;border:1px solid #3A2020;border-radius:8px;
                    padding:10px 12px;font-size:11px;color:#FF8C69;line-height:1.7;">
          ⚠️ 2025년 주가 +1,052% 급등 이후 PSR 87배 수준의 극단적 프리미엄.
          컨센서스 대비 -38% 하락 여력 존재. 실적 추가 가시화 확인 필수.
        </div>""", unsafe_allow_html=True)

    with c2:
        section_title("📊","동종업종 밸류에이션 비교")
        peers_df = pd.DataFrame(peers)[["name","cap","psr25","pbr25"]]
        peers_df.columns = ["기업명","시총","PSR(25E)","PBR(25E)"]
        st.dataframe(peers_df.set_index("기업명"), use_container_width=True)

        # 목표주가 범위 시각화
        section_title("📏","애널리스트 목표주가 범위")
        fig_val = go.Figure()
        fig_val.add_trace(go.Scatter(
            x=[77000, 149000, 360000],
            y=[1, 1, 1],
            mode="markers+text",
            marker=dict(color=["#4EC9B0","#E8C547","#7B9FFF"], size=14),
            text=["77,000<br>최저","149,000<br>컨센서스","360,000<br>다이와"],
            textposition="top center",
            textfont=dict(size=10, color=["#4EC9B0","#E8C547","#7B9FFF"]),
        ))
        fig_val.add_trace(go.Scatter(
            x=[242000], y=[1],
            mode="markers+text",
            marker=dict(color="#FF8C69", size=16, symbol="diamond"),
            text=["242,000<br>현재"],
            textposition="bottom center",
            textfont=dict(size=10, color="#FF8C69"),
        ))
        fig_val.update_layout(
            **DARK_TEMPLATE,
            xaxis=dict(title="주가 (원)", color="#555"),
            yaxis=dict(visible=False),
            showlegend=False,
            height=200,
        )
        st.plotly_chart(fig_val, use_container_width=True)

    # 종합 의견
    st.markdown("""
    <div class="ir-card" style="border-top:3px solid #7B9FFF;margin-top:8px;">
      <div style="font-size:13px;font-weight:600;color:#7B9FFF;margin-bottom:14px;">
        🔍 애널리스트 종합 의견 (2026.03 기준)
      </div>
      <div style="font-size:13px;color:#B0ACA4;line-height:2;">
        로보티즈는 26년 원천기술 기반의
        <span style="color:#E8C547;font-weight:600;">피지컬 AI 핵심 부품사</span>로,
        2025년 코스닥 상장(2018년) 이후 첫 연간 흑자 전환에 성공했습니다.
        보스턴다이내믹스 공급, MIT 공동연구, LG전자 협약 등 글로벌 파트너십을 통해 기술력이 입증됐습니다.<br>
        단, <span style="color:#FF8C69;font-weight:600;">주가 1년 +1,052% 급등으로 PSR 87배의 극단적 프리미엄</span>이 형성된 상태이며,
        컨센서스 목표가 대비 38% 하락 여력이 존재합니다. 2026년 로봇 손 양산 개시·AI 워커 수주 가시화·흑자 지속 여부가
        핵심 촉매입니다.
        <span style="color:#E8C547;">신규 진입은 2Q26 테슬라 옵티머스 생산량 발표 이후 실적 추가 확인 후 분할 접근을 권고합니다.</span>
      </div>
      <div style="margin-top:16px;background:#0D0D0F;border-radius:8px;padding:12px 16px;
                  font-size:11px;color:#444;line-height:1.7;">
        ⚠️ 본 자료는 투자 참고 목적이며, 투자 결정의 최종 책임은 투자자 본인에게 있습니다.
        2023년 한국IR협의회 리포트 포맷을 기반으로 2026년 공개 정보를 재구성하였습니다.
      </div>
    </div>""", unsafe_allow_html=True)
