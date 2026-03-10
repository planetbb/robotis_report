"""
로보티즈 IR 대시보드 2026 — Streamlit 버전
구조: 좌측 사이드바 메뉴 + 슬라이드 규격 본문 + ‹ › 페이지네이션
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

try:
    import yfinance as yf
    _YF_AVAILABLE = True
except ImportError:
    _YF_AVAILABLE = False

st.set_page_config(
    page_title="로보티즈 IR 2026",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="auto",
)

# ════════════════════════════════════════════════════
#  전역 CSS
# ════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

/* ── Streamlit 크롬 완전 숨김 ── */
header[data-testid="stHeader"] { display: none !important; }
#MainMenu { display: none !important; }
footer { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"]  { display: none !important; }

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
    background: #0A0A0C;
    color: #E0DDD5;
    font-size: 14px;
}
.stApp { background: #0A0A0C; }

.block-container {
    padding-top: 0 !important;
    padding-bottom: 5rem !important;
    padding-left: 0.5rem !important;
    padding-right: 0.5rem !important;
    max-width: 100% !important;
}
div[data-testid="stHorizontalBlock"] { gap: 0px; }
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] { padding: 0 10px; }

/* ── 상단 탭 네비 (Streamlit selectbox + buttons) ── */
div[data-testid="stSelectbox"] > div {
    background: #0D0D12 !important;
    border: 1px solid #1E1E28 !important;
    border-radius: 8px !important;
    color: #E0DDD5 !important;
    font-size: 13px !important;
}
div[data-testid="stSelectbox"] svg { fill: #555 !important; }

/* 상단 네비 버튼 행 공통 */
.top-nav-btn-row .stButton > button {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    color: #555 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    padding: 8px 10px !important;
    min-height: unset !important;
    height: auto !important;
    width: 100% !important;
    box-shadow: none !important;
    transition: all .15s !important;
    white-space: nowrap !important;
}
.top-nav-btn-row .stButton > button:hover {
    color: #C0BDB4 !important;
    border-bottom-color: #444 !important;
    background: #1A1A24 !important;
}
.top-nav-btn-row-active .stButton > button {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid #E8C547 !important;
    border-radius: 0 !important;
    color: #E8C547 !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    padding: 8px 10px !important;
    min-height: unset !important;
    height: auto !important;
    width: 100% !important;
    box-shadow: none !important;
}

/* ── 하단 네비 prev/next 버튼 — 색상 반전 ── */
/* Streamlit 마지막 row의 버튼 (prev/next) 전용 스타일 */
.nav-bottom-row button {
    background: #E8C547 !important;
    border: none !important;
    border-radius: 8px !important;
    color: #0A0A0C !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    width: 100% !important;
    min-height: 44px !important;
    height: 44px !important;
    padding: 0 !important;
    box-shadow: 0 2px 10px rgba(232,197,71,0.4) !important;
    transition: all .15s ease !important;
    cursor: pointer !important;
}
.nav-bottom-row button:hover {
    background: #F5D76E !important;
    box-shadow: 0 4px 16px rgba(232,197,71,0.55) !important;
    transform: scale(1.05) !important;
}
.nav-bottom-row button:disabled {
    background: #252530 !important;
    color: #3A3A48 !important;
    box-shadow: none !important;
    transform: none !important;
    cursor: default !important;
}

/* ── 네비 버튼: 좌우 tall (기존 유지) ── */
.nav-wrap {
    display: flex;
    height: 100%;
    align-items: stretch;
}
.nav-wrap .stButton {
    display: flex;
    flex: 1;
    height: 100%;
}
.nav-wrap .stButton > button {
    background: #1A1A24 !important;
    border: 1px solid #2A2A38 !important;
    border-radius: 10px !important;
    color: #888 !important;
    font-size: 32px !important;
    font-weight: 400 !important;
    line-height: 1 !important;
    width: 100% !important;
    height: 100% !important;
    min-height: 500px !important;
    padding: 0 !important;
    box-shadow: 0 0 12px rgba(0,0,0,0.3) !important;
    transition: all .2s !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
.nav-wrap .stButton > button:hover {
    background: #22223A !important;
    border-color: #E8C547 !important;
    color: #E8C547 !important;
}
.nav-wrap .stButton > button:disabled {
    opacity: 0.12 !important;
    cursor: not-allowed !important;
}

/* 모바일 패딩 */
@media (max-width: 768px) {
    .block-container {
        padding-left: 0.3rem !important;
        padding-right: 0.3rem !important;
    }
    .slide-body { padding: 14px 14px !important; }
    .slide-topbar { padding: 10px 14px !important; }
    .slide-footer { padding: 8px 14px !important; }
}

/* ── 슬라이드 프레임 ── */
.slide-frame {
    background: #111116;
    border: 1px solid #1E1E28;
    border-radius: 16px;
    overflow: hidden;
}
.slide-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 28px;
    border-bottom: 1px solid #1E1E28;
    background: #0D0D12;
}
.slide-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 28px;
    border-top: 1px solid #1E1E28;
    background: #0D0D12;
    position: relative;
}
.slide-body { padding: 22px 28px; }

/* ── 카드 ── */
.ir-card {
    background: #18181E;
    border: 1px solid #22222A;
    border-radius: 12px;
    padding: 20px 22px;
    margin-bottom: 12px;
}

/* ── 진행바 ── */
.prog-bg {
    background: #1E1E28;
    border-radius: 4px;
    height: 7px;
    overflow: hidden;
    margin: 5px 0 8px;
}
.prog-fill { height: 100%; border-radius: 4px; }

/* ── 네비 버튼: 세로로 꽉 찬 tall 버튼 ── */
.nav-wrap {
    display: flex;
    height: 100%;
    align-items: stretch;
}
.nav-wrap .stButton {
    display: flex;
    flex: 1;
    height: 100%;
}
.nav-wrap .stButton > button {
    background: #1A1A24 !important;
    border: 1px solid #2A2A38 !important;
    border-radius: 10px !important;
    color: #888 !important;
    font-size: 32px !important;
    font-weight: 400 !important;
    line-height: 1 !important;
    width: 100% !important;
    height: 100% !important;
    min-height: 500px !important;
    padding: 0 !important;
    box-shadow: 0 0 12px rgba(0,0,0,0.3) !important;
    transition: all .2s !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
.nav-wrap .stButton > button:hover {
    background: #22223A !important;
    border-color: #E8C547 !important;
    color: #E8C547 !important;
    box-shadow: 0 0 20px rgba(232,197,71,.15) !important;
}
.nav-wrap .stButton > button:disabled {
    opacity: 0.12 !important;
    cursor: not-allowed !important;
}

/* ── 글씨 크기 표준화 ── */
.text-xs  { font-size: 11px !important; }
.text-sm  { font-size: 13px !important; }
.text-md  { font-size: 14px !important; }
.text-lg  { font-size: 16px !important; }
.text-xl  { font-size: 18px !important; }

/* ── 표 스타일 표준화 ── */
.ir-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
}
.ir-table th {
    text-align: center;
    color: #555;
    font-size: 13px;
    padding: 8px 10px;
    border-bottom: 1px solid #22222A;
    font-weight: 600;
    letter-spacing: 0.3px;
}
.ir-table td {
    padding: 8px 10px;
    font-size: 14px;
    border-bottom: 1px solid #18181E;
    vertical-align: middle;
    line-height: 1.5;
}

::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 2px; }
.js-plotly-plot .plotly .bg { fill: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════
#  데이터
# ════════════════════════════════════════════════════
revenue_data = pd.DataFrame([
    {"year":"2021","rev":224,"op":-9,"opM":-4.2},
    {"year":"2022","rev":259,"op":-22,"opM":-8.4},
    {"year":"2023","rev":291,"op":-53,"opM":-18.2},
    {"year":"2024","rev":300,"op":-30,"opM":-10.0},
    {"year":"2025E","rev":420,"op":52,"opM":12.4},
    {"year":"2026F","rev":680,"op":110,"opM":16.2},
])
quarter_data = pd.DataFrame([
    {"q":"24Q1","rev":70,"op":-12},{"q":"24Q2","rev":75,"op":-9},
    {"q":"24Q3","rev":68,"op":-9}, {"q":"24Q4","rev":87,"op":0},
    {"q":"25Q1","rev":102,"op":8}, {"q":"25Q2","rev":105,"op":11},
    {"q":"25Q3","rev":97,"op":12}, {"q":"25Q4","rev":116,"op":21},
])
radar_data = {"subject":["유동성","안정성","성장성","수익성","활동성"],"value":[75,68,90,55,62]}
valuation = [
    {"label":"현재 주가 (2026.03)","value":"242,000원","color":"#E8C547"},
    {"label":"시가총액","value":"3.67조원","color":"#E8C547"},
    {"label":"2025 연간 매출 (추정)","value":"약 420억원","color":"#aaa"},
    {"label":"PSR (주가/매출)","value":"약 87x","color":"#FF8C69"},
    {"label":"PBR","value":"약 12x","color":"#FF8C69"},
]
peers = [
    {"name":"로보티즈","cap":"3.67조","psr25":"87x","pbr25":"12x","color":"#E8C547"},
    {"name":"레인보우로보틱스","cap":"2.9조","psr25":"N/A","pbr25":"18x","color":"#4EC9B0"},
    {"name":"두산로보틱스","cap":"3.2조","psr25":"N/A","pbr25":"9x","color":"#7B9FFF"},
    {"name":"에스피지","cap":"0.7조","psr25":"2.2x","pbr25":"3.4x","color":"#FF8C69"},
]
checkpoints = [
    {"icon":"📌","label":"액추에이터 해외 매출 확대 속도","note":"2025 4Q 영업이익률 36%로 급등. 고부가 로봇 손 제품 반영"},
    {"icon":"📌","label":"AI 워커 양산 및 수주 가시화","note":"2025년 70대 → 2027년 1,000대 목표. 오픈AI 공급 협의 진행 중"},
    {"icon":"📌","label":"LG전자 협업 구체화 여부","note":"2024년 6월 휴머노이드 공동연구 협약 체결. 실질 납품 여부 주목"},
    {"icon":"📌","label":"로봇 손(5F·20DoF) 양산 시점","note":"2026년부터 글로벌 빅테크 선주문 반영 기대"},
    {"icon":"📌","label":"물적분할 후 지배구조 안정화","note":"2025년 자율주행 사업부 분할 완료. 주주가치 영향 모니터링"},
]
risks = [
    "매출의 98.47%(2024년 기준) 액추에이터 단일 의존 → 집중 리스크 여전히 상존",
    "모터 외부 조달 의존 → 공급망 병목 리스크",
    "시총 3.67조 vs 매출 420억 → PSR 87x 극단적 프리미엄",
    "자율주행로봇 규제·현장 배치 지연 가능성",
    "테슬라 옵티머스 생산량 발표(2Q26) 기준치 미달 시 로봇주 전반 조정 우려",
]
radar_compare = pd.DataFrame([
    {"subject":"기술 원천성","로보티즈":92,"유니트리":70,"아지봇":65,"MAXON":95},
    {"subject":"가격 경쟁력","로보티즈":70,"유니트리":98,"아지봇":90,"MAXON":20},
    {"subject":"양산 규모","로보티즈":45,"유니트리":95,"아지봇":98,"MAXON":60},
    {"subject":"글로벌 생태계","로보티즈":85,"유니트리":55,"아지봇":40,"MAXON":80},
    {"subject":"수익성","로보티즈":72,"유니트리":50,"아지봇":30,"MAXON":85},
    {"subject":"규제 리스크","로보티즈":90,"유니트리":40,"아지봇":35,"MAXON":95},
])
comp_data = [
    {"name":"로보티즈","cap":3.67,"rev25":420,"op25":52,"backer":"LG전자(2대주주)","color":"#E8C547"},
    {"name":"레인보우로보틱스","cap":9.0,"rev25":220,"op25":-30,"backer":"삼성전자 인수","color":"#4EC9B0"},
    {"name":"두산로보틱스","cap":5.2,"rev25":200,"op25":-277,"backer":"두산그룹","color":"#7B9FFF"},
    {"name":"에스피지","cap":0.7,"rev25":800,"op25":110,"backer":"독립","color":"#FF8C69"},
]
pipeline_items = [
    {"stage":"출하 중","stageColor":"#4EC9B0","product":"AI 워커 (고정형)","icon":"🦾",
     "detail":"오픈AI·국내외 40곳+ 주문 접수. 고정형 4천만원대, PoC 완료, 공식 판매 개시.",
     "target":"2025년 70대 → 2027년 1,000대","rev":"25년 35억E → 27년 632억F","risk":"생산 캐파 제약"},
    {"stage":"CES 공개","stageColor":"#7B9FFF","product":"로봇 손 HX5 (20자유도)","icon":"🤲",
     "detail":"CES 2026 K-휴머노이드관 시연. 핑거 전용 액추에이터 자체 개발. 오픈AI R&D 납품 완료.",
     "target":"2026년 양산·글로벌 빅테크 납품","rev":"26년부터 매출 본격 반영","risk":"경쟁사 동시 출시"},
    {"stage":"협의 중","stageColor":"#E8C547","product":"AI 워커 (모바일형)","icon":"🚀",
     "detail":"바퀴형 베이스 추가. 25자유도 자체 액추에이터. 대기업 물류센터 R&D 검증 진행 중.",
     "target":"2025 4Q 정식 출시","rev":"26년 B2B 납품 본격화","risk":"현장 검증 지연 가능성"},
    {"stage":"개발 중","stageColor":"#FF8C69","product":"DYNAMIXEL Y 시리즈","icon":"🔩",
     "detail":"고성능 프레임리스 모터 + 전자식 브레이크. 협동로봇 관절 최적화.",
     "target":"2026년 양산 확대","rev":"액추에이터 부문 ASP 상승 기여","risk":"기존 제품 캐니벌라이제이션"},
    {"stage":"RaaS 운영","stageColor":"#C084FC","product":"GAEMI 자율주행 로봇","icon":"🚗",
     "detail":"운행안전인증 국내 1호. CJ물류 협약. 호텔·관공서 구독 서비스 중.",
     "target":"26년 RaaS 가입처 확대","rev":"구독 MRR 성장 중","risk":"규제·현장 배치 속도"},
]
roadmap = [
    {"period":"25 1H","events":["AI 워커 고정형 출시","흑자 전환 달성","오픈AI 협의 구체화"]},
    {"period":"25 2H","events":["로봇 손 CoRL 공개","모바일형 AI 워커 출시","연간 흑자 확정"]},
    {"period":"26 1H","events":["CES 2026 HX5 시연","로봇 손 양산 개시","AI 워커 100대 목표"]},
    {"period":"26 2H","events":["글로벌 빅테크 납품 본격화","DYD 감속기 협동로봇 채택","GAEMI RaaS 확대"]},
    {"period":"27+","events":["AI 워커 1,000대","액추에이터 매출 970억F","휴머노이드 매출 632억F"]},
]
adoption_scenarios = pd.DataFrame([
    {"year":"2024","연구기관":80,"초기상업":15,"대량양산":5},
    {"year":"2025E","연구기관":72,"초기상업":22,"대량양산":6},
    {"year":"2026F","연구기관":60,"초기상업":30,"대량양산":10},
    {"year":"2027F","연구기관":48,"초기상업":35,"대량양산":17},
    {"year":"2028F","연구기관":38,"초기상업":36,"대량양산":26},
    {"year":"2030F","연구기관":25,"초기상업":33,"대량양산":42},
])
tam_data = pd.DataFrame([
    {"year":"2025","market":0.18,"tam":0.016},
    {"year":"2026F","market":0.72,"tam":0.055},
    {"year":"2027F","market":1.8,"tam":0.12},
    {"year":"2028F","market":3.5,"tam":0.20},
    {"year":"2030F","market":6.0,"tam":0.28},
    {"year":"2035F","market":51,"tam":1.50},
])
china_rivals = [
    {"name":"유니트리 (Unitree)","country":"🇨🇳","city":"항저우",
     "threat":"CRITICAL","tc":"#FF4444",
     "product":"G1·H1 액추에이터 내재화","price":"G1 $16,000 / R1 $5,900",
     "shipment":"2025년 4,200대 출하 (글로벌 2위)",
     "strength":"초저가 + 수직계열화 완성. 글로벌 연구기관·대학 대량 납품",
     "weakness":"정밀도·내구성 열위. 선진국 수출 규제 리스크",
     "overlap":"연구·교육 시장에서 다이나믹셀 직접 대체 위협"},
    {"name":"아지봇 (AgiBot)","country":"🇨🇳","city":"상하이",
     "threat":"HIGH","tc":"#FF8C69",
     "product":"링시X2 전용 액추에이터","price":"완제품 위주, 부품 비공개",
     "shipment":"2025년 5,200대 출하 (글로벌 1위). LG전자·미래에셋 투자",
     "strength":"최대 양산 규모. 알리바바 AI 접목. 중국 정부 지원",
     "weakness":"부품 외판보다 완제품 판매 중심",
     "overlap":"완제품 가격 압력으로 글로벌 시장 간접 압박"},
    {"name":"푸리에 (Fourier)","country":"🇨🇳","city":"상하이",
     "threat":"HIGH","tc":"#FF8C69",
     "product":"GR-2·GR-3 전용 액추에이터 + 재활로봇","price":"기업가치 80억위안. 부품 OEM 판매",
     "shipment":"의료 재활 누적 100만명+ 서비스",
     "strength":"의료·재활 실증 데이터 강점. 힘 제어 기반 파지 기술",
     "weakness":"휴머노이드 상용화 초기 단계",
     "overlap":"연구·의료 시장에서 수요 잠식 가능"},
    {"name":"MAXON Motor","country":"🇨🇭","city":"스위스",
     "threat":"MED","tc":"#4EC9B0",
     "product":"고정밀 DC 모터·액추에이터","price":"프리미엄 산업용. 단가 3~10배",
     "shipment":"화성 탐사로버 포함 우주·의료 분야 납품",
     "strength":"최고 신뢰성·정밀도. 방산·의료 인증 다수",
     "weakness":"가격 매우 높음. 오픈소스 생태계 없음",
     "overlap":"프리미엄 산업 시장. 직접 충돌 낮음"},
]
price_events = [
    {"date":"2024.06","event":"LG전자 휴머노이드 협약","dir":"↑"},
    {"date":"2024.10","event":"보스턴다이내믹스 700개 공급","dir":"↑"},
    {"date":"2024.12","event":"자율주행 사업부 물적분할","dir":"↓"},
    {"date":"2025.01","event":"피지컬 AI 테마 급등 시작","dir":"↑↑"},
    {"date":"2025.05","event":"1Q25 흑자전환 발표","dir":"↑"},
    {"date":"2025.11","event":"3Q25 누적 흑자전환 확인","dir":"↑"},
    {"date":"2026.01","event":"최고가 349,500원 기록","dir":"▲"},
]

# ════════════════════════════════════════════════════
#  Plotly 공통 테마
# ════════════════════════════════════════════════════
DT = dict(
    template="plotly_dark",
    paper_bgcolor="#18181E",
    plot_bgcolor="#18181E",
    font=dict(family="Noto Sans KR, sans-serif", color="#888", size=11),
    margin=dict(l=8, r=8, t=28, b=8),
)

# 국가별 매출 비중 (2024 사업보고서 기준: 수출 약 70%+)
geo_data = pd.DataFrame([
    {"country":"미국","pct":31,"color":"#7B9FFF","note":"보스턴다이내믹스·MIT·오픈AI 납품"},
    {"country":"한국","pct":28,"color":"#E8C547","note":"내수 (연구기관·대학·삼성 등)"},
    {"country":"유럽","pct":16,"color":"#4EC9B0","note":"독일·영국·프랑스 연구·산업"},
    {"country":"일본","pct":11,"color":"#FF8C69","note":"자동화·로봇 연구기관"},
    {"country":"중국","pct":7, "color":"#C084FC","note":"대학·연구소 (감소 추세)"},
    {"country":"기타","pct":7, "color":"#555",   "note":"동남아·중동·남미 등"},
])

# 관련 주요 기사·공시 (IR 레퍼런스)
b2b_news = [
    {"date":"2024.06","src":"매일경제","color":"#E8C547",
     "title":"LG전자, 로보티즈와 휴머노이드 로봇 공동개발 협약…2대 주주(6.6%) 등극",
     "tag":"LG전자 협약"},
    {"date":"2024.10","src":"전자신문","color":"#4EC9B0",
     "title":"보스턴다이내믹스, 로보티즈 다이나믹셀 액추에이터 700개 추가 발주",
     "tag":"보스턴다이내믹스"},
    {"date":"2024.11","src":"한국경제","color":"#7B9FFF",
     "title":"오픈AI, 피지컬 AI 로봇 손(HX5) 공동연구 — 로보티즈 납품 확인",
     "tag":"오픈AI"},
    {"date":"2025.01","src":"로이터","color":"#FF8C69",
     "title":"테슬라 옵티머스 부품사 후보군 공개…로보티즈 다이나믹셀 Y 시리즈 거론",
     "tag":"테슬라 옵티머스"},
    {"date":"2025.03","src":"조선비즈","color":"#4EC9B0",
     "title":"로보티즈 1Q25 흑자전환…액추에이터 OPM 36% 역대 최고치 달성",
     "tag":"실적"},
    {"date":"2025.06","src":"파이낸셜뉴스","color":"#E8C547",
     "title":"우즈베키스탄 QDD 감속기 생산 거점 완공…글로벌 원가 경쟁력 확보",
     "tag":"글로벌 생산"},
]

def op_color(val, faded=False):
    a = 0.45 if faded else 0.75
    return f"rgba(78,201,176,{a})" if val >= 0 else f"rgba(255,140,105,{a})"

# ════════════════════════════════════════════════════
#  슬라이드 정의 — 섹션별 슬라이드 목록
# ════════════════════════════════════════════════════
SECTIONS = {
    "✅ 체크포인트":   ["KPI 요약", "체크포인트 & 리스크", "주가 이벤트"],
    "🏢 기업 개요":    ["기업 정보 & 주주", "제품 포트폴리오"],
    "📡 마켓 포지셔닝":["프로토콜 오너 해자", "SDK & B2B 레퍼런스", "모듈형 vs 수직계열화", "TAM & 채택률", "수혜 4단계 로드맵"],
    "🔧 파이프라인":   ["제품 로드맵", "파이프라인 현황", "유상증자 자금계획", "QDD & 우즈벡 거점", "테슬라 공급 시나리오", "미국 관세 규제"],
    "⚔️ 경쟁 분석":    ["경쟁력 비교 레이더", "중국 경쟁사 위협", "K-로봇 재무 비교"],
    "📈 실적 추이":    ["실적 & 재무건전성"],
    "💰 밸류에이션":   ["밸류에이션 지표"],
}
SECTION_KEYS = list(SECTIONS.keys())

# ════════════════════════════════════════════════════
#  Session State 초기화
# ════════════════════════════════════════════════════
if "section_idx" not in st.session_state:
    st.session_state.section_idx = 0
if "slide_idx" not in st.session_state:
    st.session_state.slide_idx = 0
if "cp_checked" not in st.session_state:
    st.session_state.cp_checked = {i: False for i in range(len(checkpoints))}
if "pl_checked" not in st.session_state:
    st.session_state.pl_checked = {i: False for i in range(len(pipeline_items))}

# ════════════════════════════════════════════════════
#  버전 정보 & 실시간 주가
# ════════════════════════════════════════════════════
APP_VERSION = "v2.5"
APP_UPDATED = datetime.now().strftime("%Y-%m-%d %H:%M")

@st.cache_data(ttl=3600)   # 1시간 캐시 (과호출 방지)
def get_robotis_price():
    """로보티즈(108490.KQ) 전일 종가 + 등락률 조회"""
    if not _YF_AVAILABLE:
        return None, None, None
    try:
        ticker = yf.Ticker("108490.KQ")
        hist   = ticker.history(period="5d")  # 5거래일 조회 (휴장일 대비)
        if hist.empty or len(hist) < 2:
            return None, None, None
        prev_close  = hist["Close"].iloc[-2]   # 전전일 (기준)
        last_close  = hist["Close"].iloc[-1]   # 전일 종가
        change_pct  = (last_close - prev_close) / prev_close * 100
        last_date   = hist.index[-1].strftime("%Y.%m.%d")
        return int(last_close), round(change_pct, 2), last_date
    except Exception:
        return None, None, None

_price, _chg, _price_date = get_robotis_price()

if _price:
    _chg_color = "#4EC9B0" if _chg >= 0 else "#FF8C69"
    _chg_sign  = "▲" if _chg >= 0 else "▼"
    _price_html = (
        f'<span style="color:#E8C547;font-weight:700;">{_price:,}원</span>'
        f'&nbsp;<span style="color:{_chg_color};font-size:10px;">'
        f'{_chg_sign}{abs(_chg):.2f}%</span>'
        f'&nbsp;<span style="color:#333;font-size:10px;">({_price_date} 종가)</span>'
    )
else:
    _price_html = '<span style="color:#555;">주가 로딩 중…</span>'

# ════════════════════════════════════════════════════
#  상단 헤더 + 섹션 탭 (Streamlit 네이티브 — JS 없음)
# ════════════════════════════════════════════════════
st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            background:#0D0D12;border-bottom:1px solid #1E1E28;
            padding:10px 16px;margin-bottom:0;">
  <div style="display:flex;align-items:center;gap:10px;">
    <div style="background:linear-gradient(135deg,#E8C547,#FF8C69);width:30px;height:30px;
                border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:16px;">🤖</div>
    <div>
      <span style="font-size:14px;font-weight:700;color:#E0DDD5;">로보티즈 IR 2026</span>
      <span style="font-size:11px;color:#444;font-family:'IBM Plex Mono',monospace;margin-left:8px;">108490 · KOSDAQ</span>
    </div>
  </div>
  <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;text-align:right;line-height:1.8;">
    {_price_html}<br>
    <span style="color:#444;">{APP_VERSION}</span>
    <span style="color:#2A2A35;">&nbsp;·&nbsp;</span>
    <span style="color:#333;">업데이트 {APP_UPDATED}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# 섹션 탭 — 버튼 7개를 가로로 배치
_tab_cols = st.columns(len(SECTION_KEYS))
for _ti, (_tc, _ts) in enumerate(zip(_tab_cols, SECTION_KEYS)):
    with _tc:
        _cls = "top-nav-btn-row-active" if _ti == st.session_state.section_idx else "top-nav-btn-row"
        st.markdown(f'<div class="{_cls}">', unsafe_allow_html=True)
        if st.button(_ts, key=f"nav_{_ti}", use_container_width=True):
            st.session_state.section_idx = _ti
            st.session_state.slide_idx = 0
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr style="border:none;border-top:1px solid #1E1E28;margin:0 0 8px;"/>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════
#  현재 섹션/슬라이드 정보
# ════════════════════════════════════════════════════
cur_sec   = SECTION_KEYS[st.session_state.section_idx]
cur_slides = SECTIONS[cur_sec]
n_slides  = len(cur_slides)
# 섹션 전환 시 인덱스가 범위를 벗어나지 않도록 안전하게 클램핑
if st.session_state.slide_idx >= n_slides:
    st.session_state.slide_idx = 0
si        = st.session_state.slide_idx
cur_slide  = cur_slides[si]

# ════════════════════════════════════════════════════
#  공통 헬퍼
# ════════════════════════════════════════════════════
def sec_lbl(emoji, text, color="#888"):
    return f'<div style="font-size:15px;color:{color};font-weight:700;margin-bottom:12px;letter-spacing:-0.2px;">{emoji} {text}</div>'

def kv_row(k, v, vc="#C0BDB4"):
    return f"""
    <div style="display:flex;justify-content:space-between;align-items:center;
                padding:8px 0;border-bottom:1px solid #1E1E28;">
      <span style="font-size:14px;color:#666;">{k}</span>
      <span style="font-size:14px;font-weight:600;color:{vc};font-family:'IBM Plex Mono',monospace;">{v}</span>
    </div>"""

def prog_bar(pct, color="#4EC9B0"):
    return f'<div class="prog-bg"><div class="prog-fill" style="width:{pct}%;background:{color};"></div></div>'

def badge(text, color):
    return f'<span style="background:{color}22;color:{color};font-size:13px;padding:3px 9px;border-radius:4px;font-family:\'IBM Plex Mono\',monospace;font-weight:600;">{text}</span>'

# ════════════════════════════════════════════════════
#  슬라이드 렌더러
# ════════════════════════════════════════════════════

# ─── 체크포인트 ───────────────────────────────────────
def slide_kpi():
    kpi_data = [
        ("2025 매출(E)","420억원","+40% YoY","#E8C547"),
        ("2025 영업이익(E)","+52억원","첫 연간 흑자","#4EC9B0"),
        ("4Q25 OPM","36%","역대 최고 수준","#7B9FFF"),
        ("2026 매출 목표","680억원(F)","다이와증권 추정","#FF8C69"),
    ]
    cols = st.columns(4)
    for col,(label,value,sub,color) in zip(cols, kpi_data):
        with col:
            st.markdown(f"""
            <div style="background:#18181E;border:1px solid #22222A;border-radius:10px;
                        padding:16px;border-top:2px solid {color};">
              <div style="font-size:11px;color:#444;font-family:'IBM Plex Mono',monospace;letter-spacing:1px;margin-bottom:8px;">{label.upper()}</div>
              <div style="font-size:26px;font-weight:700;color:{color};">{value}</div>
              <div style="font-size:13px;color:#555;margin-top:4px;">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:14px'/>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#0F1620;border:1px solid #1E2E3E;border-radius:10px;padding:10px 16px;
                font-size:16px;color:#7B9FFF;line-height:1.7;">
      <b>■</b> 로보티즈는 피지컬 AI 시대 핵심 부품(다이나믹셀 액추에이터) 전문기업. 2025년 코스닥 상장 이후 첫 연간 흑자 전환 달성.&nbsp;&nbsp;
      <b>■</b> 주가 1년 +1,052% 급등 → PSR 87배 극단적 프리미엄. 실적 가시화 속도가 핵심 변수.
    </div>""", unsafe_allow_html=True)

def slide_checkpoint_risk():
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div style="font-size:15px;color:#E8C547;font-weight:600;margin-bottom:10px;">📋 향후 주목 체크포인트</div>', unsafe_allow_html=True)
        for i, cp in enumerate(checkpoints):
            done = st.session_state.cp_checked[i]
            col_cb, col_txt = st.columns([1, 10])
            with col_cb:
                val = st.checkbox("", value=done, key=f"cp_{i}")
                st.session_state.cp_checked[i] = val
            with col_txt:
                s = "text-decoration:line-through;color:#444;" if val else "color:#C0BDB4;"
                st.markdown(f"""
                <div style="{s}font-size:16px;margin-bottom:2px;margin-top:2px;">{cp['icon']} {cp['label']}</div>
                <div style="font-size:14px;color:#555;line-height:1.4;">{cp['note']}</div>
                """, unsafe_allow_html=True)
    with c2:
        st.markdown('<div style="font-size:15px;color:#FF8C69;font-weight:600;margin-bottom:10px;">⚠️ 리스크 요인</div>', unsafe_allow_html=True)
        for r in risks:
            st.markdown(f"""
            <div style="display:flex;gap:8px;margin-bottom:10px;padding-bottom:10px;border-bottom:1px solid #1E1E28;">
              <div style="width:5px;height:5px;border-radius:50%;background:#FF8C69;margin-top:5px;flex-shrink:0;"></div>
              <div style="font-size:16px;color:#999;line-height:1.55;">{r}</div>
            </div>""", unsafe_allow_html=True)

def slide_price_events():
    st.markdown('<div style="font-size:15px;color:#888;font-weight:600;margin-bottom:12px;">📈 주요 주가 이벤트 (2024~2026)</div>', unsafe_allow_html=True)
    ev_html = '<div style="display:flex;gap:10px;flex-wrap:wrap;">'
    for ev in price_events:
        dc = "#4EC9B0" if "↑" in ev["dir"] or "▲" in ev["dir"] else "#FF8C69"
        ev_html += f"""
        <div style="width:140px;padding:12px;background:#0D0D12;border-radius:8px;border:1px solid #1E1E28;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:14px;color:#555;margin-bottom:6px;">{ev['date']}</div>
          <div style="font-size:15px;color:#B0ACA4;line-height:1.5;margin-bottom:6px;">{ev['event']}</div>
          <div style="font-size:14px;color:{dc};">{ev['dir']}</div>
        </div>"""
    ev_html += "</div>"
    st.markdown(ev_html, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'/>", unsafe_allow_html=True)
    # 간단한 주가 방향 타임라인 차트
    fig = go.Figure()
    prices = [20000,22000,19000,55000,80000,160000,349500,242000]
    dates  = [e["date"] for e in price_events]
    colors = ["#4EC9B0" if "↑" in e["dir"] or "▲" in e["dir"] else "#FF8C69" for e in price_events]
    fig.add_scatter(x=dates, y=prices, mode="lines+markers",
        line=dict(color="#E8C547", width=2),
        marker=dict(color=colors, size=10))
    fig.update_layout(**DT, height=220, xaxis=dict(color="#555"), yaxis=dict(color="#555",tickformat=","))
    st.plotly_chart(fig, use_container_width=True)

# ─── 기업 개요 ────────────────────────────────────────
def slide_company_info():
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(sec_lbl("🏢","기업 개요"), unsafe_allow_html=True)
        st.markdown("""
        <div class="ir-card" style="font-size:16px;color:#B0ACA4;line-height:1.85;">
          1999년 설립. 로봇전용 스마트 액추에이터
          <span style="color:#E8C547;font-weight:600;">다이나믹셀(DYNAMIXEL)</span> 제조 주력.
          2018년 코스닥 기술특례 상장. 글로벌 로봇 연구·대회 플랫폼
          <span style="color:#4EC9B0;">약 80%</span>에 채택.
          2025년 코스닥 상장(2018년) 이후 첫 연간 흑자 전환 달성.
        </div>""", unsafe_allow_html=True)
        kv = [("설립","1999.04"),("대표","김병수"),("상장","2018년 코스닥"),("임직원","약 114명"),("수출 비중","약 70%+"),("미국법인","ROBOTIS Inc.")]
        html = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:8px;">'
        for k,v in kv:
            html += f'<div style="background:#0D0D12;border-radius:6px;padding:8px 10px;"><div style="font-size:14px;color:#444;margin-bottom:2px;">{k}</div><div style="font-size:16px;color:#C0BDB4;font-weight:500;">{v}</div></div>'
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)

    with c2:
        st.markdown(sec_lbl("🔗","주주 구성 & 주요 파트너"), unsafe_allow_html=True)
        shareholders = [
            {"name":"김병수 외 특수관계인","pct":"23.85%","pv":23.85,"role":"최대주주","color":"#E8C547"},
            {"name":"LG전자","pct":"6.60%","pv":6.60,"role":"2대주주 · 휴머노이드 협약","color":"#4EC9B0"},
            {"name":"기타 소액주주","pct":"69.55%","pv":69.55,"role":"유동주식","color":"#555"},
        ]
        for s in shareholders:
            st.markdown(f"""
            <div style="margin-bottom:12px;">
              <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                <span style="color:{s['color']};font-weight:600;font-size:16px;">{s['name']}</span>
                <span style="font-family:'IBM Plex Mono',monospace;color:{s['color']};font-size:16px;">{s['pct']}</span>
              </div>
              {prog_bar(s['pv'], s['color'])}
              <div style="font-size:14px;color:#555;">{s['role']}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#0F1F18;border-radius:8px;padding:10px 12px;font-size:15px;color:#4EC9B0;line-height:1.7;margin-top:8px;">
          💡 2024.06 LG전자와 '휴머노이드 로봇 공동연구 및 사업화' 협약 체결. MIT 피지컬AI 공동연구, 보스턴다이내믹스·오픈AI 공급 협의 중.
        </div>""", unsafe_allow_html=True)

def slide_portfolio():
    st.markdown(sec_lbl("🤖","제품 포트폴리오 (2026 기준)"), unsafe_allow_html=True)
    products = [
        {"icon":"🔩","name":"DYNAMIXEL","sub":"X·P·Y 시리즈","status":"매출 98.47%(2024년)","badge":"캐시카우","bc":"#E8C547","desc":"100여종 라인업. 보스턴다이내믹스 납품. 글로벌 표준. (2024년 매출 98.47% 차지 — 사업보고서 기준)"},
        {"icon":"🦾","name":"AI 워커","sub":"피지컬 AI 세미 휴머노이드","status":"25년 출하 70대","badge":"신성장","bc":"#4EC9B0","desc":"오픈AI 공급 협의. 27년 1,000대 목표."},
        {"icon":"🤲","name":"로봇 손","sub":"5F·20DoF 고정밀","status":"2026 양산","badge":"파이프라인","bc":"#7B9FFF","desc":"팔당 15kg 하중. 글로벌 빅테크 선주문."},
        {"icon":"🚗","name":"GAEMI","sub":"실외 자율주행로봇","status":"RaaS 운영 중","badge":"RaaS","bc":"#FF8C69","desc":"운행안전인증 국내 1호. 배송·순찰 서비스."},
    ]
    cols = st.columns(4)
    for col, p in zip(cols, products):
        with col:
            st.markdown(f"""
            <div style="background:#0D0D12;border-radius:10px;padding:16px;height:200px;border:1px solid {p['bc']}22;">
              <div style="font-size:13px;margin-bottom:10px;">{p['icon']}</div>
              <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">
                <span style="font-weight:700;font-size:18px;color:{p['bc']};">{p['name']}</span>
                {badge(p['badge'], p['bc'])}
              </div>
              <div style="font-size:14px;color:#666;margin-bottom:6px;">{p['sub']}</div>
              <div style="font-size:14px;font-family:'IBM Plex Mono',monospace;color:{p['bc']};margin-bottom:8px;">{p['status']}</div>
              <div style="font-size:15px;color:#666;line-height:1.5;">{p['desc']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:14px'/>", unsafe_allow_html=True)
    # 매출 구성 파이
    fig = go.Figure(go.Pie(
        labels=["액추에이터(DYNAMIXEL·DYD 등)","자율주행로봇(GAEMI)"],
        values=[98.47,1.53],
        hole=0.6,
        marker_colors=["#E8C547","#4EC9B0"],
        textfont_size=11,
    ))
    fig.update_layout(**DT, height=200, showlegend=True,
                      legend=dict(orientation="h",y=-0.15),
                      annotations=[dict(text="매출구성<br>2024년", showarrow=False, font=dict(size=11,color="#888"))])
    st.plotly_chart(fig, use_container_width=True)

# ─── 마켓 포지셔닝 ────────────────────────────────────
def slide_protocol_moat():
    """프로토콜 오너 해자 분석"""
    # 핵심 테제 배너
    st.markdown("""
    <div style="background:linear-gradient(135deg,#12100A,#0A0D12);border:1px solid #E8C54744;
                border-radius:10px;padding:14px 20px;margin-bottom:14px;display:flex;gap:14px;align-items:flex-start;">
      <span style="font-size:26px;flex-shrink:0;">⚙️</span>
      <div>
        <div style="font-size:15px;font-weight:700;color:#E8C547;margin-bottom:6px;">
          로보티즈 = 부품사가 아닌 <span style="color:#4EC9B0;">프로토콜 오너</span>
        </div>
        <div style="font-size:14px;color:#999;line-height:1.8;">
          일반 부품 OEM은 스펙을 납품하지만, 로보티즈는 <b style="color:#E0DDD5;">다중 액추에이터 제어 프로토콜(DYNAMIXEL Protocol 1.0/2.0)을 25년간 독자 빌드업</b>해왔습니다.
          C·C++·Python·MATLAB·LabVIEW·ROS2 전 레이어를 커버하는 SDK, 100여 종 모델 간 완전 상호호환,
          전 세계 1,000+ 연구기관에 쌓인 <b style="color:#4EC9B0;">실전 B2B 협업 레퍼런스</b> —
          <b style="color:#E8C547;">모듈형 채택률이 투자 테제의 핵심 변수</b>인 이유가 여기 있습니다.
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    # 해자 3요소 카드
    moats = [
        {"title":"① 프로토콜 IP + 지속 업그레이드","icon":"📡","color":"#E8C547",
         "generic":"단일 모터 spec 납품. 제어 로직은 고객 자체 개발. 경쟁사가 동일 스펙으로 복제 가능.",
         "robotis":"DYNAMIXEL Protocol 1.0→2.0을 25년간 독자 개발·진화. 패킷 구조·Control Table·Instruction Set 전체가 로보티즈 IP. DYNAMIXEL 브랜드 자체가 글로벌 등록 상표.",
         "moat":"프로토콜을 복제해도 25년간 축적된 100여 종 모델 간 호환성·검증 데이터·커뮤니티 레퍼런스는 복제 불가."},
        {"title":"② 풀스택 SDK 생태계","icon":"🛠️","color":"#4EC9B0",
         "generic":"데이터시트·드라이버 제공이 전부.",
         "robotis":"C/C++/Python/C#/Java/MATLAB/LabVIEW + ROS2 공식 패키지. apt-get 한 줄로 설치. GitHub Stars 1,400+. 커뮤니티 생태계 자생적 확장.",
         "moat":"연구자·개발자가 '처음 배우는 로봇 하드웨어'가 DYNAMIXEL → 경력 전반에 걸친 브랜드 충성도 형성."},
        {"title":"③ 25년 B2B 레퍼런스","icon":"🤝","color":"#7B9FFF",
         "generic":"납품 이력 = 스펙 충족 증명.",
         "robotis":"보스턴다이내믹스(뉴 아틀라스 700개+), 오픈AI(AI 워커·로봇 손 R&D), MIT(피지컬AI 공동개발), DARPA 경진대회, RoboCup 팀 다수.",
         "moat":"세계 최고 기관과의 공동개발 이력 = 신규 고객의 기술 검증 비용 제로. '보스턴다이내믹스가 쓰는 액추에이터' 한 문장으로 설명 완료."},
    ]
    cols = st.columns(3)
    for col, d in zip(cols, moats):
        with col:
            st.markdown(f"""
            <div style="background:#0A0A0C;border-radius:10px;padding:14px 16px;border:1px solid {d['color']}33;height:100%;">
              <div style="font-size:14px;font-weight:700;color:{d['color']};margin-bottom:12px;">{d['icon']} {d['title']}</div>
              <div style="margin-bottom:10px;">
                <div style="font-size:13px;color:#FF8C69;font-weight:600;margin-bottom:4px;">일반 부품사</div>
                <div style="font-size:13px;color:#666;line-height:1.6;">{d['generic']}</div>
              </div>
              <div style="margin-bottom:10px;">
                <div style="font-size:13px;color:#4EC9B0;font-weight:600;margin-bottom:4px;">로보티즈</div>
                <div style="font-size:13px;color:#999;line-height:1.6;">{d['robotis']}</div>
              </div>
              <div style="background:{d['color']}11;border:1px solid {d['color']}33;border-radius:6px;padding:8px 10px;">
                <div style="font-size:13px;color:{d['color']};font-weight:600;margin-bottom:3px;">해자(Moat)</div>
                <div style="font-size:13px;color:#888;line-height:1.6;">{d['moat']}</div>
              </div>
            </div>""", unsafe_allow_html=True)

def slide_sdk_reference():
    """SDK 생태계 & B2B 레퍼런스"""
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(sec_lbl("🌐","DYNAMIXEL SDK — 지원 레이어 전체 맵"), unsafe_allow_html=True)
        sdk_layers = [
            {"layer":"피지컬AI 프레임워크","items":["Isaac Lab","MuJoCo","Genesis","IsaacGym"],"color":"#C084FC"},
            {"layer":"미들웨어","items":["ROS2 Humble/Jazzy/Rolling","ros2_control","MoveIt2"],"color":"#7B9FFF"},
            {"layer":"언어 SDK","items":["C/C++","Python 2·3","C#","Java","MATLAB","LabVIEW"],"color":"#4EC9B0"},
            {"layer":"OS·플랫폼","items":["Linux (ARM·x86)","Windows","macOS","NVIDIA Jetson"],"color":"#E8C547"},
            {"layer":"하드웨어 인터페이스","items":["U2D2","USB2DYNAMIXEL","DYNAMIXEL Shield (Arduino)"],"color":"#FF8C69"},
        ]
        for l in sdk_layers:
            badges = "".join(f'<span style="font-size:13px;background:{l["color"]}18;color:{l["color"]};border-radius:4px;padding:2px 8px;margin:2px 2px 2px 0;display:inline-block;">{it}</span>' for it in l["items"])
            st.markdown(f"""
            <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:10px;">
              <div style="flex-shrink:0;width:110px;font-size:13px;color:{l['color']};font-weight:600;padding-top:3px;">{l['layer']}</div>
              <div style="flex:1;">{badges}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("""
        <div style="margin-top:12px;background:#0F1218;border:1px solid #1E2A1E;border-radius:8px;padding:10px 14px;
                    font-size:13px;color:#555;line-height:1.7;">
          💡 피지컬 AI 시뮬레이터(Isaac Lab·MuJoCo)에서 학습한 정책이
          <b style="color:#E0DDD5;">그대로 DYNAMIXEL 하드웨어에서 실행</b>됩니다.
          Sim-to-Real 갭이 가장 좁은 액추에이터.
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(sec_lbl("🏆","글로벌 B2B 레퍼런스 맵"), unsafe_allow_html=True)
        ref_groups = [
            {"cat":"빅테크·AI 랩","color":"#E8C547","refs":[
                {"name":"오픈AI","detail":"AI 워커·로봇 손 HX5 R&D 납품, 공급 협의 진행"},
                {"name":"보스턴다이내믹스","detail":"뉴 아틀라스 액추에이터 700개+ 공급 (현재도 지속)"},
            ]},
            {"cat":"대학·연구기관","color":"#4EC9B0","refs":[
                {"name":"MIT (CSAIL)","detail":"피지컬 AI 리더-팔로워 모방학습 공동개발"},
                {"name":"전 세계 1,000+ 연구기관","detail":"글로벌 로봇 연구·교육 플랫폼 80%+ 채택"},
            ]},
            {"cat":"국내 전략 파트너","color":"#7B9FFF","refs":[
                {"name":"LG전자 (2대주주)","detail":"휴머노이드 공동연구 협약. 90억 유상증자."},
                {"name":"K-휴머노이드 연합","detail":"투모로 로보틱스·서울대 MOU. 한국 표준 주도."},
            ]},
            {"cat":"경진대회·표준화","color":"#FF8C69","refs":[
                {"name":"DARPA Robotics Challenge","detail":"참가팀 다수 DYNAMIXEL 기반 플랫폼 사용"},
                {"name":"RoboCup·ICRA","detail":"Humanoid·교육 리그 공식 채택 플랫폼"},
            ]},
        ]
        for g in ref_groups:
            st.markdown(f'<div style="font-size:13px;color:{g["color"]};font-weight:700;margin:10px 0 6px;">{g["cat"]}</div>', unsafe_allow_html=True)
            for r in g["refs"]:
                st.markdown(f"""
                <div style="display:flex;gap:10px;margin-bottom:6px;padding-left:10px;border-left:2px solid {g['color']}44;">
                  <span style="font-size:13px;color:#C0BDB4;font-weight:500;flex-shrink:0;min-width:110px;">{r['name']}</span>
                  <span style="font-size:13px;color:#666;line-height:1.6;">{r['detail']}</span>
                </div>""", unsafe_allow_html=True)

def slide_modular_vs_vertical():
    """모듈형 vs 수직계열화 구도"""
    st.markdown('<div style="font-size:14px;color:#888;font-weight:600;margin-bottom:12px;">📊 프로토콜 오너의 시장 구도 — 모듈형 vs 수직계열화 채택률</div>', unsafe_allow_html=True)

    approach_data = [
        {"type":"모듈형 (Open Ecosystem)","champion":"ROBOTIS DYNAMIXEL","color":"#E8C547","share25":22,
         "pros":["표준화된 인터페이스 → 빠른 프로토타이핑","ROS2·SDK 통합 → AI 학습 파이프라인 직결","교체·유지보수 용이 (Hot-swap)","다수 OEM 동시 납품 가능"],
         "cons":["단가 경쟁력 (수직계열화 대비)","초고성능 특수 로봇에는 한계"],
         "users":["오픈AI R&D","보스턴다이내믹스","MIT","K-휴머노이드 연합","전세계 1,000+ 연구기관"]},
        {"type":"수직계열화 (Integrated)","champion":"테슬라·유니트리·아지봇","color":"#FF8C69","share25":78,
         "pros":["원가 최소화 (대량양산)","최적화된 성능·폼팩터","IP 내재화"],
         "cons":["개발 속도 느림","AI 학습 생태계 구축 비용","공급망 리스크 내재화","OEM 외부 판매 불가"],
         "users":["Tesla Optimus","Unitree G1/R1","AgiBot 링시"]},
    ]

    cols = st.columns(2)
    for col, a in zip(cols, approach_data):
        with col:
            users_html = "".join(f'<span style="font-size:13px;background:#E8C54718;color:#E8C547;border-radius:4px;padding:2px 8px;margin:2px 2px 0 0;display:inline-block;">{u}</span>' for u in a["users"])
            pros_html  = "".join(f'<div style="font-size:14px;color:#888;line-height:1.65;display:flex;gap:6px;margin-bottom:3px;"><span style="color:#4EC9B0;">+</span>{p}</div>' for p in a["pros"])
            cons_html  = "".join(f'<div style="font-size:14px;color:#888;line-height:1.65;display:flex;gap:6px;margin-bottom:3px;"><span style="color:#FF8C69;">−</span>{c}</div>' for c in a["cons"])
            st.markdown(f"""
            <div style="background:#18181E;border:1px solid {a['color']}33;border-top:3px solid {a['color']};
                        border-radius:10px;padding:16px 18px;">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;">
                <div>
                  <div style="font-size:15px;font-weight:700;color:{a['color']};margin-bottom:4px;">{a['type']}</div>
                  <div style="font-size:14px;color:#666;">{a['champion']}</div>
                </div>
                <div style="text-align:right;">
                  <div style="font-size:13px;color:#555;margin-bottom:2px;">현재 점유(추정)</div>
                  <div style="font-size:14px;font-weight:700;color:{a['color']};font-family:'IBM Plex Mono',monospace;">{a['share25']}%</div>
                </div>
              </div>
              <div style="background:#0D0D10;border-radius:6px;height:8px;margin-bottom:14px;overflow:hidden;">
                <div style="width:{a['share25']}%;height:100%;background:{a['color']};border-radius:6px;"></div>
              </div>
              <div style="margin-bottom:10px;">
                <div style="font-size:13px;color:#4EC9B0;font-weight:600;margin-bottom:6px;">장점</div>
                {pros_html}
              </div>
              <div style="margin-bottom:12px;">
                <div style="font-size:13px;color:#FF8C69;font-weight:600;margin-bottom:6px;">한계</div>
                {cons_html}
              </div>
              <div style="background:{a['color']}0D;border-radius:6px;padding:10px 12px;">
                <div style="font-size:13px;color:{a['color']};font-weight:600;margin-bottom:6px;">주요 채택 고객</div>
                <div>{users_html}</div>
              </div>
            </div>""", unsafe_allow_html=True)

    # 핵심 테제 요약
    st.markdown("<div style='height:12px'/>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#0F1020;border:1px solid #7B9FFF33;border-radius:8px;padding:12px 18px;
                font-size:14px;color:#7B9FFF;line-height:1.8;">
      💡 <b>2025~2027년은 모듈형 채택 피크 구간</b>. 이 창이 열려 있는 동안 로보티즈가 연구 표준에서 상업 표준으로
      전환을 얼마나 빠르게 완성하느냐가 2030년 이후의 포지션을 결정합니다.
      로봇 손·AI 워커의 Lock-in 성공 여부가 PSR 87배 정당화의 최종 판단 기준.
    </div>""", unsafe_allow_html=True)

def slide_tam():
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(sec_lbl("💰","글로벌 휴머노이드 시장 vs 로보티즈 TAM"), unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_scatter(x=tam_data["year"], y=tam_data["market"], name="글로벌 시장($B)",
                        line=dict(color="#7B9FFF", width=2), marker=dict(size=6))
        fig.add_scatter(x=tam_data["year"], y=tam_data["tam"], name="로보티즈 TAM($B)",
                        line=dict(color="#E8C547", width=2), marker=dict(size=6))
        fig.update_layout(**DT, height=240,
                          yaxis=dict(title="십억달러($B)", color="#555"),
                          legend=dict(orientation="h", y=-0.25))
        fig.update_layout(margin=dict(l=40, r=10, t=10, b=50))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div style="font-size:13px;color:#444;line-height:1.7;margin-top:4px;">
          * 글로벌 시장 성장에도 채택률(%)은 수직계열화로 점진 하락 —<br>
          TAM 절대값은 성장하나 <b style="color:#E8C547;">점유율 방어</b>가 핵심 변수
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(sec_lbl("📊","액추에이터 시장 세그먼트 추이 (추정)"), unsafe_allow_html=True)
        fig2 = go.Figure()
        fig2.add_bar(x=adoption_scenarios["year"], y=adoption_scenarios["연구기관"],
                     name="연구·교육", marker_color="#E8C547", opacity=0.85)
        fig2.add_bar(x=adoption_scenarios["year"], y=adoption_scenarios["초기상업"],
                     name="초기상업화", marker_color="#4EC9B0", opacity=0.85)
        fig2.add_bar(x=adoption_scenarios["year"], y=adoption_scenarios["대량양산"],
                     name="대량양산", marker_color="#7B9FFF", opacity=0.85)
        fig2.update_layout(**DT, height=240, barmode="stack",
                           yaxis=dict(title="비중 (%)", color="#555"),
                           legend=dict(orientation="h", y=-0.25))
        fig2.update_layout(margin=dict(l=40, r=10, t=10, b=50))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("""
        <div style="font-size:13px;color:#444;line-height:1.7;margin-top:4px;">
          * 연구용 비중 감소 + 상업화 비중 확대 —<br>
          <b style="color:#4EC9B0;">초기상업화 구간(2025~2028)</b>이 로보티즈 모듈형 수요 피크
        </div>""", unsafe_allow_html=True)

def slide_pacemaker():
    """4단계 전환 로드맵 + 핵심 모니터링 지표"""
    st.markdown(sec_lbl("🗺️","페이스메이커 → 표준 플랫폼: 4단계 전환 시나리오"), unsafe_allow_html=True)

    phases = [
        {"label":"Phase 1","title":"연구 표준 (현재)","color":"#4EC9B0","icon":"🔬",
         "desc":"글로벌 연구기관 80%+ 다이나믹셀 채택. 피지컬 AI 학습 데이터가 다이나믹셀 환경에서 생성됨.",
         "robotis":"다이나믹셀 = 피지컬AI 학습의 표준 하드웨어. 연구용 모델이 상업용으로 전환될 때 다이나믹셀 기반 설계가 기준점.",
         "kpi":"글로벌 연구기관 채택 수 / ROS2 DYNAMIXEL 의존도"},
        {"label":"Phase 2","title":"초기 상업화 (2025~2027)","color":"#E8C547","icon":"🏭",
         "desc":"연구 프로토타입 → 소량 B2B 납품. 다이나믹셀 기반 설계가 그대로 양산 BOM에 탑재.",
         "robotis":"오픈AI AI 워커, K-휴머노이드 연합이 이 단계. 수직계열화 전환 전 모듈형 수요 피크.",
         "kpi":"AI 워커 수주 누적 / 로봇 손 빅테크 납품 건수"},
        {"label":"Phase 3","title":"대량양산 분기점 (2027~2030)","color":"#FF8C69","icon":"⚠️",
         "desc":"연간 수만 대 이상 생산 시 OEM들이 원가 절감 위해 내재화 검토. 모듈형 비중 감소 압력.",
         "robotis":"핵심 위험 구간. 고마진 Y 시리즈·로봇 손으로 포지션 유지해야. 표준에서 프리미엄으로 전략 전환 필요.",
         "kpi":"DYNAMIXEL Y 시리즈 OEM 채택 비율 / 로봇 손 대형 고객사 Lock-in 수"},
        {"label":"Phase 4","title":"생태계 플랫폼화 (2030+)","color":"#7B9FFF","icon":"🌐",
         "desc":"다이나믹셀이 로봇 관절의 USB-C처럼 통용 표준이 된 경우 vs. 틈새 프리미엄으로 축소된 경우.",
         "robotis":"낙관: 피지컬 AI OS + 하드웨어 표준 통합으로 인텔 CPU급 위상. 비관: 중국 저가에 시장 잠식.",
         "kpi":"독립 로봇 스타트업의 DYNAMIXEL 기본 채택 여부 / 표준화 기구 참여"},
    ]
    for pm in phases:
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:170px 1fr 1fr;gap:14px;
                    padding:12px 16px;background:#0D0D10;border-radius:8px;
                    border-left:3px solid {pm['color']};margin-bottom:8px;">
          <div>
            <div style="font-size:13px;background:{pm['color']}22;color:{pm['color']};border-radius:4px;
                        padding:3px 8px;display:inline-block;margin-bottom:6px;font-family:'IBM Plex Mono',monospace;">
              {pm['icon']} {pm['label']}
            </div>
            <div style="font-size:14px;color:#C0BDB4;font-weight:600;line-height:1.5;">{pm['title']}</div>
          </div>
          <div>
            <div style="font-size:13px;color:#555;font-weight:600;margin-bottom:4px;">시장 구도</div>
            <div style="font-size:14px;color:#888;line-height:1.7;">{pm['desc']}</div>
          </div>
          <div>
            <div style="font-size:13px;color:{pm['color']};font-weight:600;margin-bottom:4px;">로보티즈 전략 포인트</div>
            <div style="font-size:14px;color:#888;line-height:1.7;margin-bottom:6px;">{pm['robotis']}</div>
            <div style="font-size:13px;color:#444;font-family:'IBM Plex Mono',monospace;">📌 KPI: {pm['kpi']}</div>
          </div>
        </div>""", unsafe_allow_html=True)

    # 핵심 모니터링 지표
    st.markdown("<div style='height:10px'/>", unsafe_allow_html=True)
    monitor_groups = [
        {"title":"생태계 지표","color":"#E8C547","items":[
            "ROS2 공식 DYNAMIXEL 패키지 월 다운로드 수",
            "글로벌 로봇 경진대회 DYNAMIXEL 탑재 팀 비율",
            "신규 피지컬AI 스타트업의 첫 하드웨어 선택 비율",
        ]},
        {"title":"상업화 전환 지표","color":"#4EC9B0","items":[
            "AI 워커 누적 수주 → 연간 출하 전환율",
            "로봇 손 HX5 빅테크 납품 고객사 수",
            "DYNAMIXEL Y 시리즈 OEM 설계 채택 건수",
        ]},
        {"title":"수직계열화 위험 신호","color":"#FF8C69","items":[
            "보스턴다이내믹스·오픈AI 자체 액추에이터 내재화 발표 여부",
            "유니트리 R1 글로벌 연구기관 채택 확산 속도",
            "로보티즈 수출 매출 중 연구용 비중 감소 추이",
        ]},
    ]
    mcols = st.columns(3)
    for col, g in zip(mcols, monitor_groups):
        with col:
            items_html = "".join(f'<div style="display:flex;gap:7px;margin-bottom:7px;font-size:13px;color:#777;line-height:1.6;"><span style="color:{g["color"]};flex-shrink:0;">•</span>{it}</div>' for it in g["items"])
            st.markdown(f"""
            <div style="background:#0A0A0C;border-radius:8px;padding:12px 14px;border:1px solid {g['color']}33;">
              <div style="font-size:14px;color:{g['color']};font-weight:700;margin-bottom:10px;">{g['title']}</div>
              {items_html}
            </div>""", unsafe_allow_html=True)

# ─── 파이프라인 ───────────────────────────────────────
# ─── 파이프라인 ───────────────────────────────────────
def slide_capex():
    c1, c2 = st.columns(2)
    facility_items = [
        ("우즈베키스탄 신공장","~480억",80),
        ("정밀 가공시설 확충","350억",58),
        ("모터 생산시설","75억",13),
        ("로봇 완제품 생산라인","150억",25),
        ("데이터팩토리 구축","25억",4),
    ]
    opex_items = [
        ("QDD 액추에이터 R&D","120억",30,"#E8C547"),
        ("자체 신규 모터 개발","120억",30,"#E8C547"),
        ("데이터팩토리 운영비","60억",15,"#C084FC"),
        ("정밀 가공·모터 운영비","100억",25,"#7B9FFF"),
    ]
    with c1:
        st.markdown("""
        <div style="background:#0A0A0C;border-radius:8px;padding:14px;border:1px solid #4EC9B033;">
          <div style="display:flex;justify-content:space-between;margin-bottom:12px;">
            <span style="font-size:16px;font-weight:700;color:#4EC9B0;">🏭 시설자금</span>
            <span style="font-size:18px;font-weight:700;color:#4EC9B0;font-family:'IBM Plex Mono',monospace;">600억원</span>
          </div>""", unsafe_allow_html=True)
        for item, amt, pct in facility_items:
            st.markdown(f"""
            <div style="margin-bottom:9px;">
              <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                <span style="font-size:15px;color:#C0BDB4;">{item}</span>
                <span style="font-size:15px;color:#4EC9B0;font-family:'IBM Plex Mono',monospace;">{amt}</span>
              </div>
              {prog_bar(pct, "#4EC9B0")}
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div style="background:#0A0A0C;border-radius:8px;padding:14px;border:1px solid #E8C54733;">
          <div style="display:flex;justify-content:space-between;margin-bottom:12px;">
            <span style="font-size:16px;font-weight:700;color:#E8C547;">⚙️ 운영자금</span>
            <span style="font-size:18px;font-weight:700;color:#E8C547;font-family:'IBM Plex Mono',monospace;">400억원</span>
          </div>""", unsafe_allow_html=True)
        for item, amt, pct, color in opex_items:
            st.markdown(f"""
            <div style="margin-bottom:9px;">
              <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                <span style="font-size:15px;color:#C0BDB4;">{item}</span>
                <span style="font-size:15px;color:{color};font-family:'IBM Plex Mono',monospace;">{amt}</span>
              </div>
              {prog_bar(pct, color)}
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#0F1A0F;border:1px solid #E8C54733;border-radius:8px;padding:10px 14px;margin-top:8px;font-size:15px;color:#888;line-height:1.65;">
      📋 <b style="color:#4EC9B0;">1,000억 유상증자</b> 공시 원문 기반 (2025.08.28) — 피지컬 AI 시대의 두 가지 병목:
      <span style="color:#E0DDD5;">가격경쟁력 있는 QDD 액추에이터</span>와
      <span style="color:#E0DDD5;">실세계 피지컬 데이터</span>를 동시에 해결.
      우즈베키스탄을 글로벌 생산·데이터 거점으로 구축.
    </div>""", unsafe_allow_html=True)


def slide_qdd():
    """QDD 심층분석 + 우즈벡 데이터팩토리"""
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(sec_lbl("🔩","QDD(준직접구동) — 왜 핵심인가"), unsafe_allow_html=True)
        qdd_items = [
            {"title":"기존 DYNAMIXEL 한계","color":"#FF8C69",
             "body":"높은 감속비 → 역구동성 낮음 → 외부 충격 시 관절 파손 위험. 강화학습 기반 로봇이 필요한 '자연스러운 컴플라이언스' 구현 어려움."},
            {"title":"QDD가 해결하는 것","color":"#4EC9B0",
             "body":"저감속비(~10:1 이하) + 직접 토크 제어 → 역구동성 극대화. 충격흡수·힘 감지·자연스러운 관절 움직임. 강화학습 에이전트가 실제 로봇에서 학습 가능."},
            {"title":"시장 포지셔닝","color":"#E8C547",
             "body":"테슬라 옵티머스·Figure AI·1X 등 차세대 휴머노이드가 모두 QDD 기반으로 전환 중. 현재 선두 공급사는 중국업체. 로보티즈 QDD 양산 시 다이나믹셀 생태계 + QDD 기술의 결합으로 독보적 포지션."},
        ]
        for q in qdd_items:
            st.markdown(f"""
            <div style="background:#0A0A0C;border-radius:8px;padding:12px 14px;margin-bottom:8px;">
              <div style="font-size:14px;color:{q['color']};font-weight:600;margin-bottom:6px;">{q['title']}</div>
              <div style="font-size:14px;color:#777;line-height:1.7;">{q['body']}</div>
            </div>""", unsafe_allow_html=True)

        # Capa 목표
        st.markdown(sec_lbl("🎯","액추에이터 생산 Capa 목표"), unsafe_allow_html=True)
        for label, val, pct, color in [
            ("현재 (2025)","연 30만대",10,"#FF8C69"),
            ("2027 목표","연 210~300만대",70,"#E8C547"),
            ("배율","7배 이상 확대",100,"#4EC9B0"),
        ]:
            st.markdown(f"""
            <div style="margin-bottom:10px;">
              <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                <span style="font-size:14px;color:#888;">{label}</span>
                <span style="font-size:14px;color:{color};font-family:'IBM Plex Mono',monospace;font-weight:600;">{val}</span>
              </div>
              {prog_bar(pct, color)}
            </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(sec_lbl("🌍","우즈베키스탄 데이터팩토리"), unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#0A0A14;border:1px solid #7B9FFF33;border-radius:8px;padding:14px 16px;margin-bottom:10px;">
          <div style="font-size:14px;color:#7B9FFF;font-weight:600;margin-bottom:10px;">전략적 선택 배경</div>""",
        unsafe_allow_html=True)
        for t in [
            "2025년 8월 이미 1단계 운영 개시 (공시 이전 선행 투자)",
            "우즈벡 경제부총리 직접 지원 — 국가전략사업 지정",
            "2만평(6.6만㎡) 부지 + 세제혜택·인프라 지원 즉시 집행",
            "중국 대비 저렴한 인건비 + 자동차 산업 기반 제조 인프라",
            "미·중 무역갈등 지정학 리스크 완전 회피 가능 위치",
        ]:
            st.markdown(f'<div style="font-size:14px;color:#777;line-height:1.6;display:flex;gap:7px;margin-bottom:4px;"><span style="color:#7B9FFF;">•</span>{t}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#0A0A14;border:1px solid #C084FC33;border-radius:8px;padding:14px 16px;margin-bottom:10px;">
          <div style="font-size:14px;color:#C084FC;font-weight:600;margin-bottom:10px;">데이터팩토리가 만드는 것</div>""",
        unsafe_allow_html=True)
        for t in [
            "로봇 관제 + Human-Robot Interaction 실세계 데이터 대규모 수집",
            "AI 파운데이션 모델 학습용 피지컬 데이터 양산 (행동 데이터)",
            "하드웨어 제조사 → 데이터 기반 AI 기업으로 사업모델 전환 신호",
            "2026년 288억 투입 (데이터팩토리·가공·모터 시설), 2028년 2차 투자",
        ]:
            st.markdown(f'<div style="font-size:14px;color:#777;line-height:1.6;display:flex;gap:7px;margin-bottom:4px;"><span style="color:#C084FC;">•</span>{t}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(sec_lbl("📅","투자 집행 일정"), unsafe_allow_html=True)
        for period, desc, color in [
            ("2025 8월","우즈벡 데이터팩토리 1단계 운영 개시","#4EC9B0"),
            ("2025 12월","유상증자 신주 상장 완료","#4EC9B0"),
            ("2026 상반기","우즈벡 공장 인수/신설 여부 확정","#E8C547"),
            ("2026 하반기","288억 1차 집행 — 데이터팩토리·정밀가공·모터 시설","#E8C547"),
            ("2028 하반기","2차 집행 — 정밀가공 시설 추가 확충","#7B9FFF"),
        ]:
            st.markdown(f"""
            <div style="display:flex;gap:10px;align-items:flex-start;margin-bottom:6px;">
              <div style="flex-shrink:0;background:{color}22;color:{color};border-radius:4px;
                          padding:2px 8px;font-size:13px;font-family:'IBM Plex Mono',monospace;white-space:nowrap;">{period}</div>
              <div style="font-size:14px;color:#777;line-height:1.5;">{desc}</div>
            </div>""", unsafe_allow_html=True)


def slide_tesla():
    """테슬라 옵티머스 공급 시나리오"""
    # 헤더
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0D0D10,#12100A);border:1px solid #E8C54755;
                border-radius:10px;padding:14px 20px;margin-bottom:14px;display:flex;gap:14px;align-items:center;">
      <span style="font-size:26px;flex-shrink:0;">⚡</span>
      <div>
        <div style="font-size:16px;font-weight:700;color:#E8C547;margin-bottom:4px;">테슬라 옵티머스 액추에이터 공급 — 파이프라인 최대 카탈리스트</div>
        <div style="font-size:14px;color:#666;">확정 시 로보티즈 밸류에이션 전면 재정의 수준. 현재 협의 여부 미공개.</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # 현황 팩트 3종
    fact_cols = st.columns(3)
    for col, icon, title, color, body in zip(fact_cols,
        ["🤖","🇨🇳","⚠️"],
        ["옵티머스 액추에이터 구조","현재 주요 공급사","생산 지연 리스크"],
        ["#7B9FFF","#FF8C69","#FF4444"],
        [
            "28개 자체 설계 액추에이터 탑재. 하체 구동계가 원가의 약 25% 차지. 테슬라는 핵심 부품 내재화 지향.",
            "산화 인텔리전트 컨트롤스(중국)에 약 9,460억원($6.85억) 규모 리니어 액추에이터 발주 (2025.10 보도). 18만대분 추정.",
            "2025년 목표 5,000대 → 2,000대 → 실제 수백대 수준 달성. 로봇 손 정밀제어 기술이 최대 병목. 2026년 대량양산 불투명.",
        ]):
        with col:
            st.markdown(f"""
            <div style="background:#0A0A0C;border-radius:8px;padding:14px;border:1px solid {color}33;height:100%;">
              <div style="font-size:13px;margin-bottom:6px;">{icon}</div>
              <div style="font-size:14px;color:{color};font-weight:600;margin-bottom:8px;">{title}</div>
              <div style="font-size:14px;color:#777;line-height:1.7;">{body}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div style="height:10px"/>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:14px;color:#888;font-weight:600;margin-bottom:10px;">📋 로보티즈 공급 시나리오 분석</div>', unsafe_allow_html=True)

    scen_cols = st.columns(3)
    scenarios = [
        {"label":"베스트 케이스","icon":"🚀","prob":"15%","color":"#4EC9B0",
         "title":"다이나믹셀 Y 시리즈 / 로봇 손 공급 확정",
         "cond":"테슬라가 중국산 의존 탈피를 위해 한국 대안 채택. 미·중 무역전쟁 심화 시 가속.",
         "impact":"연간 수천억원 규모 B2B 계약. PSR 리레이팅 완전 정당화. 주가 재급등 트리거.",
         "timeline":"2026 하반기~2027"},
        {"label":"베이스 케이스","icon":"🔬","prob":"45%","color":"#E8C547",
         "title":"R&D·소량 납품 → 검증 단계",
         "cond":"보스턴다이내믹스 레퍼런스 활용, 테슬라 엔지니어링 팀에 샘플 공급. 공식 공급사 미획득.",
         "impact":"직접 매출 미미. 단, 공급사 등록 자체가 주가 모멘텀. 2027년 이후 확대 기대감 유지.",
         "timeline":"2026년 내"},
        {"label":"베어 케이스","icon":"❌","prob":"40%","color":"#FF8C69",
         "title":"테슬라 완전 내재화 — 공급 불발",
         "cond":"테슬라가 자체 액추에이터 수직계열화 완성. 산화·중국 공급망 유지.",
         "impact":"옵티머스 카탈리스트 소멸. PSR 87배 정당화 근거 약화. 주가 조정 압력.",
         "timeline":"옵티머스 V3 공개(26년 1Q) 후 윤곽"},
    ]
    for col, s in zip(scen_cols, scenarios):
        with col:
            st.markdown(f"""
            <div style="background:#0A0A0C;border-radius:8px;padding:14px;border:1px solid {s['color']}44;">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                <span style="font-size:14px;font-weight:700;color:{s['color']}">{s['icon']} {s['label']}</span>
                <span style="font-size:13px;background:{s['color']}22;color:{s['color']};padding:2px 8px;border-radius:4px;font-family:'IBM Plex Mono',monospace;">P≈{s['prob']}</span>
              </div>
              <div style="font-size:14px;color:#C0BDB4;font-weight:600;margin-bottom:8px;line-height:1.5;">{s['title']}</div>
              <div style="font-size:14px;color:#666;line-height:1.6;margin-bottom:6px;"><span style="color:#888;">조건: </span>{s['cond']}</div>
              <div style="font-size:14px;color:#666;line-height:1.6;margin-bottom:6px;"><span style="color:{s['color']}">임팩트: </span>{s['impact']}</div>
              <div style="font-size:13px;color:#444;font-family:'IBM Plex Mono',monospace;">⏱ {s['timeline']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div style="height:10px"/>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#0F1B0F;border:1px solid #4EC9B033;border-radius:8px;padding:12px 16px;">
      <div style="font-size:14px;color:#4EC9B0;font-weight:700;margin-bottom:8px;">🎯 투자자 핵심 체크포인트</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">""", unsafe_allow_html=True)
    for t, d in [
        ("2026 Q1","옵티머스 V3 공개 — 액추에이터 공급사 명단 노출 여부"),
        ("2026 Q2","테슬라 2Q26 실적 — 옵티머스 생산 가이던스 형성"),
        ("상시 모니터","미·중 관세 강화 → 중국 부품 의존도 탈피 수혜 속도"),
        ("2025 실적","보스턴다이내믹스 납품 지속 여부 (신뢰 레퍼런스)"),
    ]:
        st.markdown(f"""
        <div style="display:flex;gap:10px;align-items:flex-start;">
          <div style="flex-shrink:0;background:#4EC9B022;color:#4EC9B0;border-radius:4px;
                      padding:2px 8px;font-size:13px;font-family:'IBM Plex Mono',monospace;white-space:nowrap;">{t}</div>
          <div style="font-size:14px;color:#777;line-height:1.6;">{d}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("""</div>
      <div style="margin-top:8px;font-size:13px;color:#444;border-top:1px solid #1A2A1A;padding-top:8px;">
        ⚠️ 본 시나리오는 공개 정보 기반 추정이며 로보티즈-테슬라 간 공식 계약 여부는 미확인입니다.
      </div>
    </div>""", unsafe_allow_html=True)


def slide_tariff():
    """미국 내 중국산 로봇 부품 규제 팩트체크"""
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0D0D10,#0A0A14);border:1px solid #7B9FFF44;
                border-radius:10px;padding:14px 20px;margin-bottom:14px;display:flex;gap:14px;align-items:center;">
      <span style="font-size:26px;flex-shrink:0;">⚖️</span>
      <div>
        <div style="font-size:16px;font-weight:700;color:#7B9FFF;margin-bottom:4px;">팩트체크: 미국 내 중국산 로봇 부품 규제 현황 (2026.03 기준)</div>
        <div style="font-size:14px;color:#666;">규제 강화는 로보티즈의 지정학적 해자 — 단, 현재는 "조사 중" 단계임에 주의</div>
      </div>
    </div>""", unsafe_allow_html=True)

    reg_layers = [
        {"layer":"① 섹션 232 조사 (핵심)","status":"조사 진행 중","sc":"#E8C547","icon":"🔍",
         "body":"2025년 9월 2일 미 상무부, 로봇·산업기계 및 부품 수입의 안보 영향 조사 개시. 조사 기간 최대 270일 → 2026년 5월 30일까지 보고서 제출. 이후 대통령이 90일 내 관세·쿼터 등 조치 결정.",
         "impact":"결정 시 중국산 로봇 부품에 고관세 부과 가능. Section 301 관세(25%)에 추가 중첩 적용.",
         "robotis":"🟢 수혜: 한국산은 KORUS FTA 적용으로 우대 가능성. Business Roundtable이 한국·일본·EU 등 우방국 제품 예외 적용 권고."},
        {"layer":"② 휴머노이드 로봇법 (S.3275)","status":"법안 발의 (미통과)","sc":"#FF8C69","icon":"🏛️",
         "body":"2025년 초 미 상원 발의. 연방 정부가 중국·이란·북한·러시아 군사 공급업체 제품 포함 AI 휴머노이드 구매 금지. 현재 위원회 심의 중, 민간 판매 제한은 미포함.",
         "impact":"연방 정부 조달 차단. 민간 시장 직접 규제는 아직 없음.",
         "robotis":"🟢 간접 수혜: 중국산 휴머노이드 연방 조달 금지 → 미국 정부 파트너 수요에서 한국산 부각."},
        {"layer":"③ 기존 관세 누적 (현행)","status":"즉시 적용 중","sc":"#FF4444","icon":"💸",
         "body":"Section 301: 중국산 로봇·부품에 25% 관세. 2025년 추가 상호관세 145% 부과(90일 유예 후 협상 중). 중국 희토류 수출 규제 맞대응으로 공급망 리스크 추가.",
         "impact":"중국산 액추에이터·모터 가격 경쟁력 이미 크게 훼손. 테슬라가 중국 공급사 의존 탈피 검토 배경.",
         "robotis":"🟢 직접 수혜: 한국산 DYNAMIXEL·로봇 손은 KORUS FTA로 대미 수출 관세 0%. 가격 경쟁력 역전 구간."},
        {"layer":"④ 오픈AI RFP·민간 탈중국화","status":"진행 중","sc":"#4EC9B0","icon":"📋",
         "body":"2026년 1월 오픈AI, 베어링·모터·액추에이터 미국 기반 공급업체 RFP 공개 발송. '선전(深圳) 공급망에서 벗어나고 싶다'는 명확한 신호.",
         "impact":"민간 시장에서 자발적 탈중국화 가속. 규제 없이도 수요 구조 변화 진행 중.",
         "robotis":"🟢 직접 수혜: 미국 기반 공급업체 우선 발주 수요에서 한국 ROBOTIS Inc.(미국 법인) 대응 가능."},
    ]

    c1, c2 = st.columns(2)
    for i, r in enumerate(reg_layers):
        col = c1 if i % 2 == 0 else c2
        with col:
            st.markdown(f"""
            <div style="background:#0A0A0C;border-radius:8px;padding:14px;border:1px solid {r['sc']}33;margin-bottom:10px;">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;gap:8px;">
                <div style="font-size:14px;font-weight:700;color:#C0BDB4;">{r['icon']} {r['layer']}</div>
                <div style="flex-shrink:0;background:{r['sc']}22;color:{r['sc']};font-size:13px;
                            padding:2px 8px;border-radius:4px;font-family:'IBM Plex Mono',monospace;font-weight:700;">{r['status']}</div>
              </div>
              <div style="font-size:14px;color:#777;line-height:1.7;margin-bottom:8px;">{r['body']}</div>
              <div style="font-size:14px;color:#888;line-height:1.6;margin-bottom:6px;padding-left:8px;border-left:2px solid #333;">
                <span style="color:#aaa;">임팩트: </span>{r['impact']}
              </div>
              <div style="font-size:14px;color:#4EC9B0;background:#0F1F1888;border-radius:6px;padding:6px 10px;line-height:1.6;">{r['robotis']}</div>
            </div>""", unsafe_allow_html=True)

    # 유불리 요약
    fa_col, fb_col = st.columns(2)
    with fa_col:
        st.markdown('<div style="background:#0F1F18;border:1px solid #4EC9B033;border-radius:8px;padding:12px 14px;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:14px;color:#4EC9B0;font-weight:700;margin-bottom:8px;">✅ 로보티즈에 유리한 팩트</div>', unsafe_allow_html=True)
        for f in ["KORUS FTA → 대미 수출 관세 0% (중국산 25~145% 대비 압도적 우위)",
                  "Section 232 결과 발표 시 한국 등 우방국 예외 적용 가능성 高",
                  "유니트리 등 중국 주요 업체, 인민해방군 연계로 연방 조달 원천 차단",
                  "미국 법인 ROBOTIS Inc. 보유 → '미국 기반 공급업체' 자격 충족",
                  "오픈AI RFP가 명시적으로 미국·동맹국 공급망 우선 요청"]:
            st.markdown(f'<div style="font-size:14px;color:#888;display:flex;gap:8px;margin-bottom:4px;"><span style="color:#4EC9B0;">•</span>{f}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with fb_col:
        st.markdown('<div style="background:#1F0F0F;border:1px solid #FF8C6933;border-radius:8px;padding:12px 14px;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:14px;color:#FF8C69;font-weight:700;margin-bottom:8px;">⚠️ 주의해야 할 팩트</div>', unsafe_allow_html=True)
        for f in ["Section 232 조사 결과는 2026년 5~6월 이후 — 아직 확정 관세 없음",
                  "중국 공급업체들이 미국 내 합작공장 건설로 규제 우회 적극 추진 중",
                  "테슬라는 현재도 중국산 산화 액추에이터 발주 지속 (규제 시행 전)",
                  "민간 판매 직접 규제는 아직 없음 — 연방 조달 제한만 법제화 시도",
                  "관세 부과 시 테슬라·Figure AI 등의 원가 압박으로 로봇 수요 위축 가능성"]:
            st.markdown(f'<div style="font-size:14px;color:#888;display:flex;gap:8px;margin-bottom:4px;"><span style="color:#FF8C69;">•</span>{f}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def slide_roadmap():
    st.markdown(sec_lbl("🗓️","제품 로드맵 타임라인"), unsafe_allow_html=True)
    rm_html = '<div style="display:flex;gap:10px;overflow-x:auto;padding-bottom:8px;">'
    for i, r in enumerate(roadmap):
        is_now = (i == 2)
        bg = "#E8C547" if is_now else "#18181E"
        border = "#E8C547" if is_now else "#2A2A35"
        tc = "#0A0A0C" if is_now else "#E8C547"
        etc = "#0A0A0C" if is_now else "#888"
        bc = "rgba(10,10,12,0.3)" if is_now else "#2A2A35"
        evs = "".join(f'<div style="font-size:14px;color:{etc};line-height:1.55;margin-bottom:3px;padding-left:7px;border-left:2px solid {bc};">{ev}</div>' for ev in r["events"])
        label = f"{r['period']} ◀ NOW" if is_now else r["period"]
        rm_html += f'<div style="flex:0 0 170px;background:{bg};border:2px solid {border};border-radius:8px;padding:12px 13px;"><div style="font-family:\'IBM Plex Mono\',monospace;font-size:15px;font-weight:700;color:{tc};margin-bottom:9px;">{label}</div>{evs}</div>'
    rm_html += "</div>"
    st.markdown(rm_html, unsafe_allow_html=True)

    # 매출 성장 예측 차트
    st.markdown("<div style='height:10px'/>", unsafe_allow_html=True)
    proj = pd.DataFrame({"year":["2024","2025E","2026F","2027F"],"rev":[300,420,680,1100],"op":[-30,52,110,200]})
    fig = go.Figure()
    fig.add_bar(x=proj["year"], y=proj["rev"], name="매출액(억)", marker_color="rgba(232,197,71,0.5)")
    fig.add_scatter(x=proj["year"], y=proj["op"], name="영업이익(억)",
                    line=dict(color="#4EC9B0",width=2), marker=dict(size=8,color="#4EC9B0"))
    fig.add_hline(y=0, line_color="#333")
    fig.update_layout(**DT, height=210, barmode="group",
                      legend=dict(orientation="h",y=-0.25))
    st.plotly_chart(fig, use_container_width=True)

def slide_pipeline():
    st.markdown(sec_lbl("🔧","제품 파이프라인 현황"), unsafe_allow_html=True)
    for i, p in enumerate(pipeline_items):
        done = st.session_state.pl_checked[i]
        col_cb, col_card = st.columns([1, 22])
        with col_cb:
            val = st.checkbox("", value=done, key=f"pl_{i}")
            st.session_state.pl_checked[i] = val
        with col_card:
            st.markdown(f"""
            <div style="background:#18181E;border:1px solid #22222A;border-radius:10px;
                        padding:12px 16px;border-left:3px solid {p['stageColor']};margin-bottom:6px;">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                <span style="font-size:14px;">{p['icon']}</span>
                <span style="font-size:16px;font-weight:700;color:#E0DDD5;">{p['product']}</span>
                {badge(p['stage'], p['stageColor'])}
              </div>
              <div style="font-size:15px;color:#777;line-height:1.55;margin-bottom:5px;">{p['detail']}</div>
              <div style="display:flex;gap:14px;font-size:14px;color:#555;flex-wrap:wrap;">
                <span>🎯 {p['target']}</span>
                <span style="color:{p['stageColor']};">💰 {p['rev']}</span>
                <span style="color:#FF8C69;">⚠️ {p['risk']}</span>
              </div>
            </div>""", unsafe_allow_html=True)

# ─── 경쟁 분석 ────────────────────────────────────────
def slide_china_rivals():
    # 경고 배너
    st.markdown("""
    <div style="background:linear-gradient(90deg,rgba(255,68,68,0.12),rgba(255,140,105,0.05));
                border:1px solid rgba(255,68,68,0.25);border-radius:10px;
                padding:9px 16px;margin-bottom:10px;
                display:flex;align-items:center;gap:10px;">
      <span style="font-size:14px;">🚨</span>
      <div style="font-size:15px;color:#AAA;line-height:1.6;">
        <b style="color:#FF6B6B;">중국발 가격 파괴 위협</b> — 2025년 글로벌 출하 1.6만대 중
        <span style="color:#FF8C69;font-weight:600;">중국산 80%+</span> 점유.
        유니트리 R1 <span style="color:#FF8C69;font-weight:600;">$5,900</span> — 미국 경쟁사의 ⅛ 수준.
      </div>
    </div>""", unsafe_allow_html=True)

    # 경쟁사 카드 — 한 줄 컴팩트 레이아웃
    for r in china_rivals:
        st.markdown(f"""
        <div style="background:#18181E;border:1px solid #22222A;border-left:3px solid {r['tc']};
                    border-radius:10px;padding:10px 14px;margin-bottom:7px;
                    display:grid;grid-template-columns:160px 1fr 1fr 1fr;gap:14px;align-items:start;">
          <!-- 기업 정보 -->
          <div>
            <div style="font-size:15px;font-weight:700;color:#E0DDD5;margin-bottom:2px;">{r['country']} {r['name']}</div>
            <div style="font-size:14px;color:#555;margin-bottom:5px;">{r['city']}</div>
            <div style="display:inline-block;background:{r['tc']}22;color:{r['tc']};font-size:13px;
                        padding:2px 7px;border-radius:4px;font-family:'IBM Plex Mono',monospace;font-weight:700;margin-bottom:5px;">
              위협도 {r['threat']}
            </div><br>
            <span style="font-size:14px;color:#777;">{r['product']}</span><br>
            <span style="font-size:14px;color:#E8C547;font-family:'IBM Plex Mono',monospace;font-weight:600;">{r['price']}</span>
          </div>
          <!-- 출하 -->
          <div>
            <div style="font-size:13px;color:#4EC9B0;font-weight:600;margin-bottom:4px;">📦 출하 현황</div>
            <div style="font-size:14px;color:#888;line-height:1.55;">{r['shipment']}</div>
          </div>
          <!-- 강점 -->
          <div>
            <div style="font-size:13px;color:#4EC9B0;font-weight:600;margin-bottom:4px;">✅ 강점</div>
            <div style="font-size:14px;color:#888;line-height:1.55;">{r['strength']}</div>
          </div>
          <!-- 약점·충돌 -->
          <div>
            <div style="font-size:13px;color:#FF8C69;font-weight:600;margin-bottom:4px;">⚠️ 약점</div>
            <div style="font-size:14px;color:#888;line-height:1.55;margin-bottom:6px;">{r['weakness']}</div>
            <div style="font-size:13px;color:{r['tc']};font-weight:600;margin-bottom:4px;">🎯 충돌 영역</div>
            <div style="font-size:14px;color:#888;line-height:1.55;">{r['overlap']}</div>
          </div>
        </div>""", unsafe_allow_html=True)

def slide_radar_diff():
    c1, c2 = st.columns([5, 4])
    with c1:
        st.markdown(sec_lbl("🕸️","글로벌 경쟁력 비교 레이더"), unsafe_allow_html=True)
        cats = radar_compare["subject"].tolist()
        fig = go.Figure()
        for col_name, color in [("로보티즈","#E8C547"),("유니트리","#FF4444"),("아지봇","#FF8C69"),("MAXON","#4EC9B0")]:
            vals = radar_compare[col_name].tolist() + [radar_compare[col_name].iloc[0]]
            fig.add_trace(go.Scatterpolar(r=vals, theta=cats+[cats[0]], name=col_name,
                line=dict(color=color, width=2), fill="toself", opacity=0.7))
        fig.update_layout(**DT, height=360,
                          polar=dict(bgcolor="#18181E",
                                     radialaxis=dict(visible=True, range=[0,100], color="#333", tickfont=dict(size=10)),
                                     angularaxis=dict(color="#555", tickfont=dict(size=11))),
                          legend=dict(orientation="h", y=-0.12))
        fig.update_layout(margin=dict(l=20, r=20, t=20, b=40))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown(sec_lbl("⚔️","로보티즈 차별화 포인트"), unsafe_allow_html=True)
        diff = [
            {"title":"vs 유니트리·아지봇 (중국)","color":"#FF4444",
             "win":"오픈소스 생태계 80% 점유, 글로벌 연구 표준, 미·EU 수출 규제 수혜",
             "lose":"가격 경쟁력 (ASP 2~3배), 양산 규모"},
            {"title":"vs MAXON·Faulhaber (유럽)","color":"#4EC9B0",
             "win":"모듈형 설계·오픈소스·가격·피지컬AI 통합",
             "lose":"초정밀 산업·방산·의료 인증 신뢰도"},
            {"title":"vs 레인보우·두산 (국내)","color":"#7B9FFF",
             "win":"유일한 흑자·부품 원천기술·LG·오픈AI 파트너십",
             "lose":"완성품 라인업 폭, 그룹사 인프라·브랜드"},
        ]
        for d in diff:
            st.markdown(f"""
            <div style="margin-bottom:14px;padding:12px 14px;background:#18181E;
                        border:1px solid #22222A;border-left:3px solid {d['color']};border-radius:8px;">
              <div style="font-size:15px;color:{d['color']};font-weight:700;margin-bottom:7px;">{d['title']}</div>
              <div style="font-size:14px;color:#777;line-height:1.7;">
                <span style="color:#4EC9B0;font-weight:600;">✅ 우위</span>&nbsp; {d['win']}
              </div>
              <div style="font-size:14px;color:#777;line-height:1.7;margin-top:4px;">
                <span style="color:#FF8C69;font-weight:600;">⚠️ 열위</span>&nbsp; {d['lose']}
              </div>
            </div>""", unsafe_allow_html=True)

def slide_krobot():
    st.markdown(sec_lbl("📊","K-로봇 빅4 재무 비교 (2025E)"), unsafe_allow_html=True)

    # 상단: 4개 기업 카드
    cols = st.columns(4)
    for col, c in zip(cols, comp_data):
        oc = "#4EC9B0" if c["op25"] > 0 else "#FF8C69"
        os = f"+{c['op25']}억" if c["op25"] > 0 else f"{c['op25']}억"
        with col:
            st.markdown(f"""
            <div style="background:#0D0D12;border-radius:10px;padding:14px 12px;
                        border:1px solid {c['color']}33;border-top:3px solid {c['color']};">
              <div style="font-size:16px;font-weight:700;color:{c['color']};margin-bottom:10px;">{c['name']}</div>
              <div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid #1E1E28;">
                <span style="font-size:14px;color:#555;">시총</span>
                <span style="font-size:14px;color:#B0ACA4;font-family:'IBM Plex Mono',monospace;">{c['cap']}조</span>
              </div>
              <div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid #1E1E28;">
                <span style="font-size:14px;color:#555;">매출(E)</span>
                <span style="font-size:14px;color:#B0ACA4;font-family:'IBM Plex Mono',monospace;">{c['rev25']}억</span>
              </div>
              <div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid #1E1E28;">
                <span style="font-size:14px;color:#555;">영업이익(E)</span>
                <span style="font-size:14px;color:{oc};font-family:'IBM Plex Mono',monospace;font-weight:600;">{os}</span>
              </div>
              <div style="margin-top:8px;background:{c['color']}15;color:{c['color']};border-radius:4px;
                          padding:3px 6px;text-align:center;font-size:13px;">{c['backer']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:12px'/>", unsafe_allow_html=True)

    # 하단: 버블 차트
    fig = go.Figure()
    for c in comp_data:
        fig.add_trace(go.Scatter(
            x=[c["rev25"]], y=[c["cap"]],
            mode="markers+text",
            marker=dict(size=max(abs(c["op25"]) * 0.28, 18), color=c["color"], opacity=0.75,
                        line=dict(color=c["color"], width=1)),
            text=[c["name"]], textposition="top center",
            textfont=dict(size=13, color=c["color"]),
            name=c["name"]
        ))
    fig.update_layout(**DT, height=230,
                      xaxis=dict(title="매출액(억원)", color="#555", title_font=dict(size=12)),
                      yaxis=dict(title="시가총액(조원)", color="#555", title_font=dict(size=12)),
                      showlegend=False)
    fig.update_layout(margin=dict(l=40, r=10, t=10, b=40))
    st.plotly_chart(fig, use_container_width=True)


def slide_perf_combined():
    """연간 실적 + 재무건전성 레이더 + 국가별/고객별 매출"""
    # ── 상단: 연간실적 | 재무레이더
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(sec_lbl("📊","연간 실적 추이 (억원)"), unsafe_allow_html=True)
        rev_c = ["#E8C547" if i < 4 else "rgba(232,197,71,0.45)" for i in range(len(revenue_data))]
        op_c  = [op_color(r["op"], i >= 4) for i, r in revenue_data.iterrows()]
        fig = go.Figure()
        fig.add_bar(x=revenue_data["year"], y=revenue_data["rev"], name="매출액", marker_color=rev_c)
        fig.add_bar(x=revenue_data["year"], y=revenue_data["op"],  name="영업이익", marker_color=op_c)
        fig.add_hline(y=0, line_color="#333")
        fig.update_layout(**DT, height=200, barmode="group",
                          legend=dict(orientation="h", y=-0.30))
        st.plotly_chart(fig, use_container_width=True)

        fig2 = go.Figure()
        fig2.add_scatter(x=revenue_data["year"], y=revenue_data["opM"],
                         mode="lines+markers",
                         line=dict(color="#E8C547", width=2),
                         marker=dict(size=7, color=["#FF8C69" if v < 0 else "#4EC9B0" for v in revenue_data["opM"]]),
                         fill="toself", fillcolor="rgba(232,197,71,0.06)")
        fig2.add_hline(y=0, line_color="#333", line_dash="dash")
        fig2.update_layout(**DT, height=160,
                           yaxis=dict(title="OPM %", color="#555"),
                           xaxis=dict(color="#555"))
        st.plotly_chart(fig2, use_container_width=True)

    with c2:
        st.markdown(sec_lbl("🕸️","재무 건전성 레이더"), unsafe_allow_html=True)
        cats_r = radar_data["subject"] + [radar_data["subject"][0]]
        vals_r = radar_data["value"]   + [radar_data["value"][0]]
        fig3 = go.Figure(go.Scatterpolar(
            r=vals_r, theta=cats_r,
            fill="toself", fillcolor="rgba(232,197,71,0.12)",
            line=dict(color="#E8C547", width=2), name="로보티즈"
        ))
        fig3.update_layout(**DT, height=290,
                           polar=dict(bgcolor="#18181E",
                                      radialaxis=dict(visible=True, range=[0,100], color="#333"),
                                      angularaxis=dict(color="#555")))
        st.plotly_chart(fig3, use_container_width=True)

        rows = [("매출액(억)","291","300","420"),
                ("YoY(%)","11.8","3.1","40"),
                ("영업이익(억)","-53","-30","+52"),
                ("OPM(%)","-18.2","-10.0","+12.4")]
        th = "<tr>" + "".join(
            f'<th style="text-align:right;color:#555;font-size:12px;padding:4px 6px;border-bottom:1px solid #22222A;">{h}</th>'
            for h in ["구분","2023","2024","2025E"]
        ) + "</tr>"
        trs = ""
        for r in rows:
            tds = f'<td style="font-size:12px;color:#666;padding:4px 6px;border-bottom:1px solid #18181E;">{r[0]}</td>'
            for v in r[1:]:
                vc = "#FF8C69" if v.startswith("-") else "#4EC9B0" if v.startswith("+") else "#B0ACA4"
                tds += f'<td style="text-align:right;font-size:12px;color:{vc};font-family:IBM Plex Mono,monospace;padding:4px 6px;border-bottom:1px solid #18181E;">{v}</td>'
            trs += f"<tr>{tds}</tr>"
        st.markdown(f'<table style="width:100%;border-collapse:collapse;margin-top:8px;">{th}{trs}</table>', unsafe_allow_html=True)

    st.markdown("<hr style='border:none;border-top:1px solid #1E1E28;margin:14px 0 10px'/>", unsafe_allow_html=True)

    # ── 하단: 국가별 매출 | B2B 주요 고객
    g1, g2 = st.columns(2)
    with g1:
        st.markdown(sec_lbl("🌍","국가별 매출 비중 (2024)"), unsafe_allow_html=True)
        fig4 = go.Figure(go.Pie(
            labels=geo_data["country"],
            values=geo_data["pct"],
            hole=0.52,
            marker_colors=geo_data["color"].tolist(),
            textfont_size=12,
            textinfo="label+percent",
        ))
        _dt4 = {k: v for k, v in DT.items()}
        _dt4["margin"] = dict(l=0, r=0, t=10, b=0)
        fig4.update_layout(**_dt4, height=220, showlegend=False)
        fig4.update_layout(annotations=[
            dict(text="수출<br>72%+", x=0.5, y=0.5, showarrow=False,
                 font=dict(size=11, color="#888"), xanchor="center", yanchor="middle")
        ])
        st.plotly_chart(fig4, use_container_width=True)
        # 국가별 노트
        for g in geo_data.itertuples():
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:3px;">' +
                f'<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:{g.color};flex-shrink:0;"></span>' +
                f'<span style="font-size:12px;color:#666;">{g.country} <span style="color:#444;">— {g.note}</span></span></div>',
                unsafe_allow_html=True
            )

    with g2:
        st.markdown(sec_lbl("📰","관련 주요 기사·공시"), unsafe_allow_html=True)
        for n in b2b_news:
            st.markdown(f"""
            <div style="background:#18181E;border:1px solid #22222A;border-left:3px solid {n['color']};
                        border-radius:6px;padding:7px 10px;margin-bottom:5px;">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:2px;">
                <span style="font-size:11px;color:#444;font-family:IBM Plex Mono,monospace;">{n['date']} · {n['src']}</span>
                <span style="font-size:10px;background:{n['color']}22;color:{n['color']};
                             padding:1px 6px;border-radius:3px;white-space:nowrap;">{n['tag']}</span>
              </div>
              <div style="font-size:12px;color:#B0ACA4;line-height:1.55;">{n['title']}</div>
            </div>""", unsafe_allow_html=True)

# ─── 실적 추이 ────────────────────────────────────────
def slide_annual():
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(sec_lbl("📊","연간 실적 추이 (억원)"), unsafe_allow_html=True)
        rev_c = ["#E8C547" if i<4 else "rgba(232,197,71,0.4)" for i in range(len(revenue_data))]
        op_c  = [op_color(r["op"], i>=4) for i, r in revenue_data.iterrows()]
        fig = go.Figure()
        fig.add_bar(x=revenue_data["year"], y=revenue_data["rev"], name="매출액", marker_color=rev_c)
        fig.add_bar(x=revenue_data["year"], y=revenue_data["op"], name="영업이익", marker_color=op_c)
        fig.add_hline(y=0, line_color="#333")
        fig.update_layout(**DT, height=240, barmode="group",
                          legend=dict(orientation="h",y=-0.25))
        st.plotly_chart(fig, use_container_width=True)

        rows = [("매출액(억)","291","300","420"),("YoY(%)","11.8","3.1","40"),
                ("영업이익(억)","-53","-30","+52"),("OPM(%)","-18.2","-10.0","+12.4")]
        th = '<tr>' + ''.join(f'<th style="text-align:right;color:#555;font-size:14px;padding:5px 4px;border-bottom:1px solid #22222A;">{h}</th>' for h in ["구분","2023","2024","2025E"]) + '</tr>'
        trs = ""
        for r in rows:
            tds = f'<td style="font-size:15px;color:#666;padding:5px 4px;border-bottom:1px solid #18181E;">{r[0]}</td>'
            for v in r[1:]:
                vc = "#FF8C69" if v.startswith("-") else "#4EC9B0" if v.startswith("+") else "#B0ACA4"
                tds += f'<td style="text-align:right;font-size:15px;color:{vc};font-family:\'IBM Plex Mono\',monospace;padding:5px 4px;border-bottom:1px solid #18181E;">{v}</td>'
            trs += f"<tr>{tds}</tr>"
        st.markdown(f'<table style="width:100%;border-collapse:collapse;">{th}{trs}</table>', unsafe_allow_html=True)

    with c2:
        st.markdown(sec_lbl("📈","분기별 실적 추이 (2024~2025)"), unsafe_allow_html=True)
        q_c = ["rgba(232,197,71,0.27)" if i<4 else "rgba(232,197,71,0.53)" for i in range(len(quarter_data))]
        fig2 = go.Figure()
        fig2.add_bar(x=quarter_data["q"], y=quarter_data["rev"], name="매출액", marker_color=q_c)
        fig2.add_scatter(x=quarter_data["q"], y=quarter_data["op"], name="영업이익",
                         line=dict(color="#4EC9B0",width=2), marker=dict(size=7,color="#4EC9B0"))
        fig2.add_hline(y=0, line_color="#333")
        fig2.update_layout(**DT, height=240, legend=dict(orientation="h",y=-0.25))
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("""
        <div style="font-size:15px;color:#555;line-height:1.75;margin-top:4px;">
          ● 2025년 1분기부터 4분기 연속 흑자 달성.<br>
          ● 4Q25 매출 116억원, 영업이익 21억 — 액추에이터 OPM <b style="color:#4EC9B0;">36%</b> 역대 최고.
        </div>""", unsafe_allow_html=True)

def slide_radar_perf():
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(sec_lbl("🕸️","재무 건전성 레이더"), unsafe_allow_html=True)
        cats_r = radar_data["subject"] + [radar_data["subject"][0]]
        vals_r = radar_data["value"] + [radar_data["value"][0]]
        fig3 = go.Figure(go.Scatterpolar(r=vals_r, theta=cats_r,
            fill="toself", fillcolor="rgba(232,197,71,0.12)",
            line=dict(color="#E8C547", width=2), name="로보티즈"))
        fig3.update_layout(**DT, height=300,
                           polar=dict(bgcolor="#18181E",
                                      radialaxis=dict(visible=True,range=[0,100],color="#333"),
                                      angularaxis=dict(color="#555")))
        st.plotly_chart(fig3, use_container_width=True)
    with c2:
        st.markdown(sec_lbl("📊","영업이익률 추이"), unsafe_allow_html=True)
        fig4 = go.Figure()
        fig4.add_scatter(x=revenue_data["year"], y=revenue_data["opM"],
                         mode="lines+markers",
                         line=dict(color="#E8C547",width=2),
                         marker=dict(size=8, color=["#FF8C69" if v<0 else "#4EC9B0" for v in revenue_data["opM"]]),
                         fill="toself", fillcolor="rgba(232,197,71,0.06)")
        fig4.add_hline(y=0, line_color="#333", line_dash="dash")
        fig4.update_layout(**DT, height=260, yaxis=dict(title="OPM %",color="#555"),
                           xaxis=dict(color="#555"))
        st.plotly_chart(fig4, use_container_width=True)

# ─── 밸류에이션 ───────────────────────────────────────
def slide_valuation():
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(sec_lbl("💰","밸류에이션 지표"), unsafe_allow_html=True)
        html = ""
        for v in valuation:
            html += kv_row(v["label"], v["value"], v["color"])
        st.markdown(f'<div class="ir-card">{html}</div>', unsafe_allow_html=True)

    with c2:
        st.markdown(sec_lbl("📊","동종업종 밸류에이션 비교"), unsafe_allow_html=True)
        th = '<tr>' + ''.join(f'<th style="text-align:center;color:#555;font-size:14px;padding:6px 4px;border-bottom:1px solid #22222A;">{h}</th>' for h in ["기업명","시총","PSR(25E)","PBR(25E)"]) + '</tr>'
        trs = ""
        for i, p in enumerate(peers):
            bg = "#1E1E0A" if i==0 else "transparent"
            trs += f'<tr style="background:{bg};">'
            trs += f'<td style="padding:7px 4px;color:{p["color"]};font-weight:{"700" if i==0 else "400"};font-size:15px;border-bottom:1px solid #18181E;">{p["name"]}</td>'
            for val in [p["cap"],p["psr25"],p["pbr25"]]:
                vc = "#FF8C69" if (i==0 and val not in ["3.67조","N/A"]) else "#888"
                trs += f'<td style="text-align:center;color:{vc};font-family:\'IBM Plex Mono\',monospace;font-size:14px;padding:7px 4px;border-bottom:1px solid #18181E;">{val}</td>'
            trs += "</tr>"
        st.markdown(f'<table style="width:100%;border-collapse:collapse;">{th}{trs}</table>', unsafe_allow_html=True)



def slide_opinion():
    st.markdown("""
    <div class="ir-card" style="border-top:3px solid #7B9FFF;">
      <div style="font-size:16px;font-weight:600;color:#7B9FFF;margin-bottom:14px;">
        🔍 애널리스트 종합 의견 (2026.03 기준)
      </div>
      <div style="font-size:15px;color:#B0ACA4;line-height:1.9;">
        로보티즈는 26년 원천기술 기반의
        <span style="color:#E8C547;font-weight:600;">피지컬 AI 핵심 부품사</span>로,
        2025년 코스닥 상장 이후 첫 연간 흑자 전환에 성공했습니다.
        보스턴다이내믹스 공급, MIT 공동연구, LG전자 협약 등 글로벌 파트너십을 통해 기술력이 입증됐습니다.<br>
        단, <span style="color:#FF8C69;font-weight:600;">주가 1년 +1,052% 급등으로 PSR 87배의 극단적 프리미엄</span>이 형성된 상태이며,
        컨센서스 목표가 대비 38% 하락 여력이 존재합니다. 2026년 로봇 손 양산 개시·AI 워커 수주 가시화·흑자 지속 여부가
        핵심 촉매입니다.<br>
        <span style="color:#E8C547;">신규 진입은 2Q26 테슬라 옵티머스 생산량 발표 이후 실적 추가 확인 후 분할 접근을 권고합니다.</span>
      </div>
    </div>""", unsafe_allow_html=True)

    # 시나리오 3종
    st.markdown("<div style='height:10px'/>", unsafe_allow_html=True)
    scenarios = [
        {"label":"베스트 케이스 🚀","prob":"15%","color":"#4EC9B0",
         "title":"다이나믹셀 Y / 로봇 손 테슬라 옵티머스 공급 확정",
         "impact":"연간 수천억 B2B 계약. PSR 리레이팅 완전 정당화. 주가 재급등 트리거."},
        {"label":"베이스 케이스 🔬","prob":"45%","color":"#E8C547",
         "title":"R&D·소량 납품 → 공급사 등록 검증 단계",
         "impact":"직접 매출 미미하나 공급사 등록 자체가 모멘텀. 2027년 이후 확대 기대감 유지."},
        {"label":"베어 케이스 ❌","prob":"40%","color":"#FF8C69",
         "title":"테슬라 완전 내재화 — 공급 불발",
         "impact":"옵티머스 카탈리스트 소멸. PSR 87배 정당화 근거 약화. 주가 조정 압력."},
    ]
    s_cols = st.columns(3)
    for col, s in zip(s_cols, scenarios):
        with col:
            st.markdown(f"""
            <div style="background:#18181E;border:1px solid {s['color']}44;border-radius:8px;padding:14px;">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                <span style="font-size:15px;font-weight:700;color:{s['color']};">{s['label']}</span>
                <span style="font-size:14px;background:{s['color']}22;color:{s['color']};padding:2px 7px;border-radius:4px;font-family:'IBM Plex Mono',monospace;">P≈{s['prob']}</span>
              </div>
              <div style="font-size:15px;color:#C0BDB4;font-weight:600;margin-bottom:6px;line-height:1.45;">{s['title']}</div>
              <div style="font-size:14px;color:#666;line-height:1.6;">{s['impact']}</div>
            </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════
#  슬라이드 라우터
# ════════════════════════════════════════════════════
SLIDE_RENDERERS = {
    "KPI 요약":             slide_kpi,
    "체크포인트 & 리스크":   slide_checkpoint_risk,
    "주가 이벤트":          slide_price_events,
    "기업 정보 & 주주":     slide_company_info,
    "제품 포트폴리오":       slide_portfolio,
    "프로토콜 오너 해자":    slide_protocol_moat,
    "SDK & B2B 레퍼런스":   slide_sdk_reference,
    "모듈형 vs 수직계열화":  slide_modular_vs_vertical,
    "TAM & 채택률":         slide_tam,
    "수혜 4단계 로드맵":     slide_pacemaker,
    "유상증자 자금계획":     slide_capex,
    "QDD & 우즈벡 거점":    slide_qdd,
    "테슬라 공급 시나리오":  slide_tesla,
    "미국 관세 규제":        slide_tariff,
    "제품 로드맵":           slide_roadmap,
    "파이프라인 현황":       slide_pipeline,
    "중국 경쟁사 위협":      slide_china_rivals,
    "경쟁력 비교 레이더":    slide_radar_diff,
    "K-로봇 재무 비교":     slide_krobot,
    "실적 & 재무건전성":     slide_perf_combined,
    "밸류에이션 지표":       slide_valuation,
}

# ════════════════════════════════════════════════════
#  메인 레이아웃 — 슬라이드 + 하단 네이티브 네비바
# ════════════════════════════════════════════════════

# ── 슬라이드 타이틀바
_topbar = f"""
<div class="slide-frame">
  <div class="slide-topbar">
    <div style="display:flex;align-items:center;gap:10px;min-width:0;">
      <div style="font-size:12px;color:#444;font-family:'IBM Plex Mono',monospace;
                  white-space:nowrap;">{cur_sec}</div>
      <span style="color:#2A2A35;">›</span>
      <div style="font-size:15px;font-weight:700;color:#E8C547;
                  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{cur_slide}</div>
    </div>
    <div style="font-family:'IBM Plex Mono',monospace;font-size:13px;font-weight:700;
                color:#555;flex-shrink:0;">{si+1}&thinsp;/&thinsp;{n_slides}</div>
  </div>
  <div class="slide-body">
"""

_footer = """
  </div>
</div>
"""

# ── 슬라이드 렌더
st.markdown(_topbar, unsafe_allow_html=True)
SLIDE_RENDERERS[cur_slide]()
st.markdown(_footer, unsafe_allow_html=True)

# ── 하단 네비 바: ‹  [점 인디케이터]  페이지  ›
_dots_html = ""
for _di in range(n_slides):
    if _di == si:
        _dots_html += '<span style="display:inline-block;width:18px;height:6px;border-radius:3px;background:#E8C547;margin:0 2px;vertical-align:middle;"></span>'
    else:
        _dots_html += '<span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#2A2A35;margin:0 2px;vertical-align:middle;"></span>'

# ── 하단 네비 바 전체를 nav-bottom-row 클래스로 감싸기
st.markdown('<div class="nav-bottom-row">', unsafe_allow_html=True)
_nc1, _nc2, _nc3, _nc4, _nc5 = st.columns([3, 1, 6, 1, 3])

with _nc1:
    st.markdown('<div style="height:44px;"></div>', unsafe_allow_html=True)

with _nc2:
    if st.button("‹", key="prev_btn", disabled=(si == 0), use_container_width=True):
        st.session_state.slide_idx -= 1
        st.rerun()

with _nc3:
    st.markdown(
        f'<div style="display:flex;align-items:center;justify-content:center;gap:10px;height:44px;">' +
        f'<span style="display:flex;align-items:center;gap:4px;">{_dots_html}</span>' +
        f'<span style="font-family:IBM Plex Mono,monospace;font-size:12px;color:#555;white-space:nowrap;">{si+1} / {n_slides}</span>' +
        '</div>',
        unsafe_allow_html=True
    )

with _nc4:
    if st.button("›", key="next_btn", disabled=(si == n_slides - 1), use_container_width=True):
        st.session_state.slide_idx += 1
        st.rerun()

with _nc5:
    st.markdown('<div style="height:44px;"></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
