"""
로보티즈 IR 대시보드 2026 — Streamlit 버전
구조: 좌측 사이드바 메뉴 + 슬라이드 규격 본문 + ‹ › 페이지네이션
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="로보티즈 IR 2026",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ════════════════════════════════════════════════════
#  전역 CSS
# ════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

/* ── 베이스 ── */
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
    background: #0A0A0C;
    color: #E0DDD5;
}
.stApp { background: #0A0A0C; }

/* ── 사이드바 ── */
section[data-testid="stSidebar"] {
    background: #0D0D12 !important;
    border-right: 1px solid #1E1E28 !important;
    min-width: 210px !important;
    max-width: 210px !important;
}
section[data-testid="stSidebar"] * { color: #B0ACA4 !important; }

/* ── 슬라이드 래퍼 ── */
.slide-viewport {
    background: #111116;
    border: 1px solid #1E1E28;
    border-radius: 14px;
    padding: 28px 32px 20px;
    min-height: 620px;
    position: relative;
    overflow: hidden;
}

/* ── 슬라이드 헤더 ── */
.slide-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    padding-bottom: 14px;
    border-bottom: 1px solid #1E1E28;
}
.slide-title {
    font-size: 16px;
    font-weight: 700;
    color: #E0DDD5;
    letter-spacing: -0.3px;
}
.slide-badge {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: #444;
    letter-spacing: 1px;
}

/* ── 카드 ── */
.ir-card {
    background: #18181E;
    border: 1px solid #22222A;
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 10px;
}

/* ── 페이지네이션 바 ── */
.pag-bar {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    margin-top: 16px;
    padding-top: 12px;
    border-top: 1px solid #1E1E28;
}
.pag-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #2A2A35;
    display: inline-block;
    transition: all .2s;
}
.pag-dot.active { background: #E8C547; width: 22px; border-radius: 4px; }

/* ── 네비 버튼 ── */
.stButton > button {
    background: #18181E !important;
    border: 1px solid #2A2A35 !important;
    border-radius: 8px !important;
    color: #888 !important;
    font-size: 18px !important;
    padding: 4px 16px !important;
    min-height: 36px !important;
    transition: all .15s !important;
}
.stButton > button:hover {
    background: #222230 !important;
    border-color: #E8C547 !important;
    color: #E8C547 !important;
}
.stButton > button:disabled {
    opacity: 0.25 !important;
    cursor: not-allowed !important;
}

/* ── 진행바 ── */
.prog-bg {
    background: #1E1E28;
    border-radius: 4px;
    height: 6px;
    overflow: hidden;
    margin: 4px 0 6px;
}
.prog-fill { height: 100%; border-radius: 4px; }

/* ── 스크롤바 ── */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 2px; }

/* ── Plotly 배경 투명화 ── */
.js-plotly-plot .plotly .bg { fill: transparent !important; }

/* ── Streamlit 기본 패딩 제거 ── */
.block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }
div[data-testid="stHorizontalBlock"] { gap: 10px; }
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
    {"label":"애널리스트 목표가 평균","value":"149,000원","color":"#4EC9B0"},
    {"label":"다이와증권 목표가","value":"360,000원","color":"#7B9FFF"},
    {"label":"컨센서스 하락 여력","value":"-38% (고평가)","color":"#FF8C69"},
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
    "매출의 98% 다이나믹셀 단일 의존 → 집중 리스크 여전히 상존",
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
    {"date":"2026.03","event":"현재 242,000원 (고점比 -31%)","dir":"↓"},
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

def op_color(val, faded=False):
    a = 0.45 if faded else 0.75
    return f"rgba(78,201,176,{a})" if val >= 0 else f"rgba(255,140,105,{a})"

# ════════════════════════════════════════════════════
#  슬라이드 정의 — 섹션별 슬라이드 목록
# ════════════════════════════════════════════════════
SECTIONS = {
    "✅ 체크포인트":   ["KPI 요약", "체크포인트 & 리스크", "주가 이벤트"],
    "🏢 기업 개요":    ["기업 정보 & 주주", "제품 포트폴리오"],
    "📡 마켓 포지셔닝":["TAM & 채택률", "수혜 4단계 로드맵"],
    "🔧 파이프라인":   ["유상증자 자금계획", "제품 로드맵", "파이프라인 현황"],
    "⚔️ 경쟁 분석":    ["중국 경쟁사 위협", "경쟁력 비교 레이더", "K-로봇 재무 비교"],
    "📈 실적 추이":    ["연간 실적 차트", "분기 실적 & 레이더"],
    "💰 밸류에이션":   ["밸류에이션 지표", "목표주가 & 종합의견"],
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
#  사이드바
# ════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:16px 0 20px;">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
        <div style="background:linear-gradient(135deg,#E8C547,#FF8C69);width:32px;height:32px;
                    border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px;">🤖</div>
        <div>
          <div style="font-size:14px;font-weight:700;color:#E0DDD5 !important;">로보티즈</div>
          <div style="font-size:10px;color:#555 !important;font-family:'IBM Plex Mono',monospace;">108490 · KOSDAQ</div>
        </div>
      </div>
      <div style="margin-top:10px;background:#1A2A1A;border:1px solid #2A4A2A;border-radius:6px;
                  padding:5px 10px;font-size:10px;color:#4EC9B0 !important;font-family:'IBM Plex Mono',monospace;">
        ● 242,000원 &nbsp;|&nbsp; 2026.03
      </div>
    </div>
    <hr style="border:none;border-top:1px solid #1E1E28;margin:0 0 16px;"/>
    """, unsafe_allow_html=True)

    for i, sec in enumerate(SECTION_KEYS):
        is_active = (i == st.session_state.section_idx)
        btn_style = (
            "background:#1E1E28;border-radius:8px;padding:8px 12px;margin-bottom:4px;"
            "border-left:3px solid #E8C547;" if is_active else
            "background:transparent;border-radius:8px;padding:8px 12px;margin-bottom:4px;border-left:3px solid transparent;"
        )
        label_color = "#E8C547" if is_active else "#777"
        if st.button(sec, key=f"nav_{i}", use_container_width=True):
            st.session_state.section_idx = i
            st.session_state.slide_idx = 0
            st.rerun()

    st.markdown("<div style='height:20px'/>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:10px;color:#333;line-height:1.6;padding:0 4px;">
      ⚠️ 본 자료는 투자 참고 목적이며 Claude는 금융 전문가가 아닙니다. 투자의 최종 책임은 투자자 본인에게 있습니다.
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════
#  현재 섹션/슬라이드 정보
# ════════════════════════════════════════════════════
cur_sec   = SECTION_KEYS[st.session_state.section_idx]
cur_slides = SECTIONS[cur_sec]
n_slides  = len(cur_slides)
si        = st.session_state.slide_idx  # 현재 슬라이드 인덱스
cur_slide  = cur_slides[si]

# ════════════════════════════════════════════════════
#  공통 헬퍼
# ════════════════════════════════════════════════════
def sec_lbl(emoji, text, color="#888"):
    return f'<div style="font-size:11px;color:{color};font-weight:600;margin-bottom:10px;">{emoji} {text}</div>'

def kv_row(k, v, vc="#C0BDB4"):
    return f"""
    <div style="display:flex;justify-content:space-between;align-items:center;
                padding:7px 0;border-bottom:1px solid #1E1E28;">
      <span style="font-size:12px;color:#666;">{k}</span>
      <span style="font-size:12px;font-weight:600;color:{vc};font-family:'IBM Plex Mono',monospace;">{v}</span>
    </div>"""

def prog_bar(pct, color="#4EC9B0"):
    return f'<div class="prog-bg"><div class="prog-fill" style="width:{pct}%;background:{color};"></div></div>'

def badge(text, color):
    return f'<span style="background:{color}22;color:{color};font-size:9px;padding:2px 7px;border-radius:4px;font-family:\'IBM Plex Mono\',monospace;">{text}</span>'

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
              <div style="font-size:9px;color:#444;font-family:'IBM Plex Mono',monospace;letter-spacing:1px;margin-bottom:8px;">{label.upper()}</div>
              <div style="font-size:22px;font-weight:700;color:{color};">{value}</div>
              <div style="font-size:11px;color:#555;margin-top:4px;">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:14px'/>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#0F1620;border:1px solid #1E2E3E;border-radius:10px;padding:10px 16px;
                font-size:12px;color:#7B9FFF;line-height:1.7;">
      <b>■</b> 로보티즈는 피지컬 AI 시대 핵심 부품(다이나믹셀 액추에이터) 전문기업. 2025년 코스닥 상장 이후 첫 연간 흑자 전환 달성.&nbsp;&nbsp;
      <b>■</b> 주가 1년 +1,052% 급등 → PSR 87배 극단적 프리미엄. 실적 가시화 속도가 핵심 변수.
    </div>""", unsafe_allow_html=True)

def slide_checkpoint_risk():
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div style="font-size:11px;color:#E8C547;font-weight:600;margin-bottom:10px;">📋 향후 주목 체크포인트</div>', unsafe_allow_html=True)
        for i, cp in enumerate(checkpoints):
            done = st.session_state.cp_checked[i]
            col_cb, col_txt = st.columns([1, 10])
            with col_cb:
                val = st.checkbox("", value=done, key=f"cp_{i}")
                st.session_state.cp_checked[i] = val
            with col_txt:
                s = "text-decoration:line-through;color:#444;" if val else "color:#C0BDB4;"
                st.markdown(f"""
                <div style="{s}font-size:12px;margin-bottom:2px;margin-top:2px;">{cp['icon']} {cp['label']}</div>
                <div style="font-size:10px;color:#555;line-height:1.4;">{cp['note']}</div>
                """, unsafe_allow_html=True)
    with c2:
        st.markdown('<div style="font-size:11px;color:#FF8C69;font-weight:600;margin-bottom:10px;">⚠️ 리스크 요인</div>', unsafe_allow_html=True)
        for r in risks:
            st.markdown(f"""
            <div style="display:flex;gap:8px;margin-bottom:10px;padding-bottom:10px;border-bottom:1px solid #1E1E28;">
              <div style="width:5px;height:5px;border-radius:50%;background:#FF8C69;margin-top:5px;flex-shrink:0;"></div>
              <div style="font-size:12px;color:#999;line-height:1.55;">{r}</div>
            </div>""", unsafe_allow_html=True)

def slide_price_events():
    st.markdown('<div style="font-size:11px;color:#888;font-weight:600;margin-bottom:12px;">📈 주요 주가 이벤트 (2024~2026)</div>', unsafe_allow_html=True)
    ev_html = '<div style="display:flex;gap:10px;flex-wrap:wrap;">'
    for ev in price_events:
        dc = "#4EC9B0" if "↑" in ev["dir"] or "▲" in ev["dir"] else "#FF8C69"
        ev_html += f"""
        <div style="width:140px;padding:12px;background:#0D0D12;border-radius:8px;border:1px solid #1E1E28;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#555;margin-bottom:6px;">{ev['date']}</div>
          <div style="font-size:11px;color:#B0ACA4;line-height:1.5;margin-bottom:6px;">{ev['event']}</div>
          <div style="font-size:16px;color:{dc};">{ev['dir']}</div>
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
        <div class="ir-card" style="font-size:12px;color:#B0ACA4;line-height:1.85;">
          1999년 설립. 로봇전용 스마트 액추에이터
          <span style="color:#E8C547;font-weight:600;">다이나믹셀(DYNAMIXEL)</span> 제조 주력.
          2018년 코스닥 기술특례 상장. 글로벌 로봇 연구·대회 플랫폼
          <span style="color:#4EC9B0;">약 80%</span>에 채택.
          2025년 코스닥 상장(2018년) 이후 첫 연간 흑자 전환 달성.
        </div>""", unsafe_allow_html=True)
        kv = [("설립","1999.04"),("대표","김병수"),("상장","2018년 코스닥"),("임직원","약 114명"),("수출 비중","약 70%+"),("미국법인","ROBOTIS Inc.")]
        html = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:8px;">'
        for k,v in kv:
            html += f'<div style="background:#0D0D12;border-radius:6px;padding:8px 10px;"><div style="font-size:10px;color:#444;margin-bottom:2px;">{k}</div><div style="font-size:12px;color:#C0BDB4;font-weight:500;">{v}</div></div>'
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
                <span style="color:{s['color']};font-weight:600;font-size:12px;">{s['name']}</span>
                <span style="font-family:'IBM Plex Mono',monospace;color:{s['color']};font-size:12px;">{s['pct']}</span>
              </div>
              {prog_bar(s['pv'], s['color'])}
              <div style="font-size:10px;color:#555;">{s['role']}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#0F1F18;border-radius:8px;padding:10px 12px;font-size:11px;color:#4EC9B0;line-height:1.7;margin-top:8px;">
          💡 2024.06 LG전자와 '휴머노이드 로봇 공동연구 및 사업화' 협약 체결. MIT 피지컬AI 공동연구, 보스턴다이내믹스·오픈AI 공급 협의 중.
        </div>""", unsafe_allow_html=True)

def slide_portfolio():
    st.markdown(sec_lbl("🤖","제품 포트폴리오 (2026 기준)"), unsafe_allow_html=True)
    products = [
        {"icon":"🔩","name":"DYNAMIXEL","sub":"X·P·Y 시리즈","status":"매출 98%","badge":"캐시카우","bc":"#E8C547","desc":"100여종 라인업. 보스턴다이내믹스 납품. 글로벌 표준."},
        {"icon":"🦾","name":"AI 워커","sub":"피지컬 AI 세미 휴머노이드","status":"25년 출하 70대","badge":"신성장","bc":"#4EC9B0","desc":"오픈AI 공급 협의. 27년 1,000대 목표."},
        {"icon":"🤲","name":"로봇 손","sub":"5F·20DoF 고정밀","status":"2026 양산","badge":"파이프라인","bc":"#7B9FFF","desc":"팔당 15kg 하중. 글로벌 빅테크 선주문."},
        {"icon":"🚗","name":"GAEMI","sub":"실외 자율주행로봇","status":"RaaS 운영 중","badge":"RaaS","bc":"#FF8C69","desc":"운행안전인증 국내 1호. 배송·순찰 서비스."},
    ]
    cols = st.columns(4)
    for col, p in zip(cols, products):
        with col:
            st.markdown(f"""
            <div style="background:#0D0D12;border-radius:10px;padding:16px;height:200px;border:1px solid {p['bc']}22;">
              <div style="font-size:22px;margin-bottom:10px;">{p['icon']}</div>
              <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">
                <span style="font-weight:700;font-size:13px;color:{p['bc']};">{p['name']}</span>
                {badge(p['badge'], p['bc'])}
              </div>
              <div style="font-size:10px;color:#666;margin-bottom:6px;">{p['sub']}</div>
              <div style="font-size:10px;font-family:'IBM Plex Mono',monospace;color:{p['bc']};margin-bottom:8px;">{p['status']}</div>
              <div style="font-size:11px;color:#666;line-height:1.5;">{p['desc']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:14px'/>", unsafe_allow_html=True)
    # 매출 구성 파이
    fig = go.Figure(go.Pie(
        labels=["DYNAMIXEL","AI 워커","로봇 손","GAEMI"],
        values=[98,1.2,0.5,0.3],
        hole=0.6,
        marker_colors=["#E8C547","#4EC9B0","#7B9FFF","#FF8C69"],
        textfont_size=11,
    ))
    fig.update_layout(**DT, height=200, showlegend=True,
                      legend=dict(orientation="h",y=-0.15,font=dict(size=10)),
                      annotations=[dict(text="매출구성<br>2025E", showarrow=False, font=dict(size=11,color="#888"))])
    st.plotly_chart(fig, use_container_width=True)

# ─── 마켓 포지셔닝 ────────────────────────────────────
def slide_tam():
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        fig.add_bar(x=tam_data["year"], y=tam_data["market"], name="글로벌 시장(조원)", marker_color="rgba(123,159,255,0.27)")
        fig.add_bar(x=tam_data["year"], y=tam_data["tam"], name="로보티즈 TAM(조원)", marker_color="#E8C547")
        fig.update_layout(**DT, title="글로벌 휴머노이드 시장 vs 로보티즈 TAM (조원)", barmode="overlay",
                          height=280, legend=dict(orientation="h",y=-0.25))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = go.Figure()
        fig2.add_bar(x=adoption_scenarios["year"], y=adoption_scenarios["연구기관"], name="연구기관", marker_color="#4EC9B0")
        fig2.add_bar(x=adoption_scenarios["year"], y=adoption_scenarios["초기상업"], name="초기상업화", marker_color="#E8C547")
        fig2.add_bar(x=adoption_scenarios["year"], y=adoption_scenarios["대량양산"], name="대량양산", marker_color="#FF8C69")
        fig2.update_layout(**DT, title="모듈형 채택률 시나리오 (%)", barmode="stack",
                           height=280, legend=dict(orientation="h",y=-0.25))
        st.plotly_chart(fig2, use_container_width=True)

def slide_pacemaker():
    st.markdown(sec_lbl("🔄","피지컬 AI 시장 로보티즈 수혜 4단계"), unsafe_allow_html=True)
    phases = [
        {"label":"Phase 1","title":"연구 표준 (현재)","color":"#4EC9B0","icon":"🔬",
         "desc":"글로벌 연구기관 80%+ 다이나믹셀 채택. 피지컬 AI 학습 데이터가 다이나믹셀 환경에서 생성됨.",
         "robotis":"다이나믹셀 = 피지컬AI 학습의 표준 하드웨어.",
         "kpi":"글로벌 연구기관 채택 수 / ROS2 DYNAMIXEL 의존도"},
        {"label":"Phase 2","title":"초기 상업화 (2025~2027)","color":"#E8C547","icon":"🏭",
         "desc":"연구 프로토타입 → 소량 B2B 납품. 다이나믹셀 기반 설계가 양산 BOM에 탑재.",
         "robotis":"오픈AI AI 워커, K-휴머노이드 연합. 수직계열화 전환 전 모듈형 수요 피크.",
         "kpi":"AI 워커 수주 누적 / 로봇 손 빅테크 납품 건수"},
        {"label":"Phase 3","title":"대량양산 분기점 (2027~2030)","color":"#FF8C69","icon":"⚠️",
         "desc":"연간 수만대 이상 생산 시 OEM들이 내재화 검토. 모듈형 비중 감소 압력.",
         "robotis":"핵심 위험 구간. Y 시리즈·로봇 손으로 포지션 유지해야.",
         "kpi":"DYNAMIXEL Y 시리즈 OEM 채택 비율 / 로봇 손 Lock-in 수"},
        {"label":"Phase 4","title":"생태계 플랫폼화 (2030+)","color":"#7B9FFF","icon":"🌐",
         "desc":"다이나믹셀이 로봇 관절의 USB-C처럼 통용 표준이 된 경우 vs. 틈새 프리미엄 축소.",
         "robotis":"낙관: 피지컬 AI OS + 하드웨어 표준 통합. 비관: 중국 저가에 시장 잠식.",
         "kpi":"독립 로봇 스타트업 기본 채택 여부 / 표준화 기구 참여"},
    ]
    cols = st.columns(4)
    for col, pm in zip(cols, phases):
        with col:
            st.markdown(f"""
            <div style="background:#18181E;border:1px solid #22222A;border-radius:10px;padding:14px;
                        border-top:3px solid {pm['color']};height:280px;overflow:hidden;">
              <div style="font-size:9px;color:{pm['color']};font-family:'IBM Plex Mono',monospace;margin-bottom:5px;">{pm['label']}</div>
              <div style="font-size:12px;font-weight:700;color:#E0DDD5;margin-bottom:8px;">{pm['icon']} {pm['title']}</div>
              <div style="font-size:10px;color:#666;line-height:1.55;margin-bottom:8px;">{pm['desc']}</div>
              <div style="background:{pm['color']}11;border:1px solid {pm['color']}33;border-radius:6px;
                          padding:7px 9px;font-size:10px;color:#888;line-height:1.5;margin-bottom:6px;">
                🎯 {pm['robotis']}
              </div>
              <div style="font-size:9px;color:#444;border-top:1px solid #1A1A1E;padding-top:6px;">
                📊 {pm['kpi']}
              </div>
            </div>""", unsafe_allow_html=True)

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
            <span style="font-size:12px;font-weight:700;color:#4EC9B0;">🏭 시설자금</span>
            <span style="font-size:13px;font-weight:700;color:#4EC9B0;font-family:'IBM Plex Mono',monospace;">600억원</span>
          </div>""", unsafe_allow_html=True)
        for item, amt, pct in facility_items:
            st.markdown(f"""
            <div style="margin-bottom:9px;">
              <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                <span style="font-size:11px;color:#C0BDB4;">{item}</span>
                <span style="font-size:11px;color:#4EC9B0;font-family:'IBM Plex Mono',monospace;">{amt}</span>
              </div>
              {prog_bar(pct, "#4EC9B0")}
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div style="background:#0A0A0C;border-radius:8px;padding:14px;border:1px solid #E8C54733;">
          <div style="display:flex;justify-content:space-between;margin-bottom:12px;">
            <span style="font-size:12px;font-weight:700;color:#E8C547;">⚙️ 운영자금</span>
            <span style="font-size:13px;font-weight:700;color:#E8C547;font-family:'IBM Plex Mono',monospace;">400억원</span>
          </div>""", unsafe_allow_html=True)
        for item, amt, pct, color in opex_items:
            st.markdown(f"""
            <div style="margin-bottom:9px;">
              <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                <span style="font-size:11px;color:#C0BDB4;">{item}</span>
                <span style="font-size:11px;color:{color};font-family:'IBM Plex Mono',monospace;">{amt}</span>
              </div>
              {prog_bar(pct, color)}
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#0F1A0F;border:1px solid #E8C54733;border-radius:8px;padding:10px 14px;margin-top:8px;font-size:11px;color:#888;line-height:1.65;">
      📋 <b style="color:#4EC9B0;">1,000억 유상증자</b> 공시 원문 기반 (2025.08.28) — 피지컬 AI 시대의 두 가지 병목:
      <span style="color:#E0DDD5;">가격경쟁력 있는 QDD 액추에이터</span>와
      <span style="color:#E0DDD5;">실세계 피지컬 데이터</span>를 동시에 해결.
      우즈베키스탄을 글로벌 생산·데이터 거점으로 구축.
    </div>""", unsafe_allow_html=True)

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
        evs = "".join(f'<div style="font-size:10px;color:{etc};line-height:1.55;margin-bottom:3px;padding-left:7px;border-left:2px solid {bc};">{ev}</div>' for ev in r["events"])
        label = f"{r['period']} ◀ NOW" if is_now else r["period"]
        rm_html += f'<div style="flex:0 0 170px;background:{bg};border:2px solid {border};border-radius:8px;padding:12px 13px;"><div style="font-family:\'IBM Plex Mono\',monospace;font-size:11px;font-weight:700;color:{tc};margin-bottom:9px;">{label}</div>{evs}</div>'
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
                <span style="font-size:16px;">{p['icon']}</span>
                <span style="font-size:12px;font-weight:700;color:#E0DDD5;">{p['product']}</span>
                {badge(p['stage'], p['stageColor'])}
              </div>
              <div style="font-size:11px;color:#777;line-height:1.55;margin-bottom:5px;">{p['detail']}</div>
              <div style="display:flex;gap:14px;font-size:10px;color:#555;flex-wrap:wrap;">
                <span>🎯 {p['target']}</span>
                <span style="color:{p['stageColor']};">💰 {p['rev']}</span>
                <span style="color:#FF8C69;">⚠️ {p['risk']}</span>
              </div>
            </div>""", unsafe_allow_html=True)

# ─── 경쟁 분석 ────────────────────────────────────────
def slide_china_rivals():
    st.markdown("""
    <div style="background:linear-gradient(90deg,rgba(255,68,68,0.13),rgba(255,140,105,0.07));
                border:1px solid rgba(255,68,68,0.27);border-radius:10px;padding:10px 16px;margin-bottom:12px;
                display:flex;align-items:center;gap:12px;">
      <span style="font-size:20px;">🚨</span>
      <div style="font-size:12px;color:#888;line-height:1.65;">
        <b style="color:#FF6B6B;">중국발 가격 파괴 위협</b> — 2025년 글로벌 출하 1.6만대 중
        <span style="color:#FF8C69;font-weight:600;">중국산 80%+</span> 점유.
        유니트리 R1 <span style="color:#FF8C69;font-weight:600;">$5,900</span> — 미국 경쟁사의 ⅛ 수준.
      </div>
    </div>""", unsafe_allow_html=True)

    for r in china_rivals:
        st.markdown(f"""
        <div class="ir-card" style="border-left:3px solid {r['tc']};padding:12px 16px;
             display:grid;grid-template-columns:180px 1fr 1fr;gap:16px;margin-bottom:8px;">
          <div>
            <div style="font-size:13px;font-weight:700;color:#E0DDD5;">{r['country']} {r['name']}</div>
            <div style="font-size:10px;color:#555;margin-bottom:6px;">{r['city']}</div>
            <div style="display:inline-block;background:{r['tc']}22;color:{r['tc']};font-size:9px;
                        padding:2px 8px;border-radius:4px;font-family:'IBM Plex Mono',monospace;font-weight:700;">
              위협도: {r['threat']}
            </div>
            <div style="margin-top:7px;font-size:10px;color:#666;">{r['product']}</div>
            <div style="margin-top:4px;font-size:10px;color:#E8C547;font-family:'IBM Plex Mono',monospace;">{r['price']}</div>
          </div>
          <div>
            <div style="font-size:9px;color:#4EC9B0;margin-bottom:3px;font-weight:600;">📦 출하 현황</div>
            <div style="font-size:10px;color:#888;line-height:1.55;margin-bottom:8px;">{r['shipment']}</div>
            <div style="font-size:9px;color:#4EC9B0;margin-bottom:3px;font-weight:600;">✅ 강점</div>
            <div style="font-size:10px;color:#888;line-height:1.55;">{r['strength']}</div>
          </div>
          <div>
            <div style="font-size:9px;color:#FF8C69;margin-bottom:3px;font-weight:600;">⚠️ 약점</div>
            <div style="font-size:10px;color:#888;line-height:1.55;margin-bottom:8px;">{r['weakness']}</div>
            <div style="font-size:9px;color:{r['tc']};margin-bottom:3px;font-weight:600;">🎯 충돌 영역</div>
            <div style="font-size:10px;color:#888;line-height:1.55;">{r['overlap']}</div>
          </div>
        </div>""", unsafe_allow_html=True)

def slide_radar_diff():
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(sec_lbl("🕸️","글로벌 경쟁력 비교 레이더"), unsafe_allow_html=True)
        cats = radar_compare["subject"].tolist()
        fig = go.Figure()
        for col_name, color in [("로보티즈","#E8C547"),("유니트리","#FF4444"),("아지봇","#FF8C69"),("MAXON","#4EC9B0")]:
            vals = radar_compare[col_name].tolist() + [radar_compare[col_name].iloc[0]]
            fig.add_trace(go.Scatterpolar(r=vals, theta=cats+[cats[0]], name=col_name,
                line=dict(color=color, width=2), fill="toself", opacity=0.75))
        fig.update_layout(**DT, height=300,
                          polar=dict(bgcolor="#18181E",
                                     radialaxis=dict(visible=True,range=[0,100],color="#333"),
                                     angularaxis=dict(color="#555")),
                          legend=dict(orientation="h",y=-0.18,font=dict(size=10)))
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
            <div style="margin-bottom:12px;padding-bottom:12px;border-bottom:1px solid #1E1E28;">
              <div style="font-size:11px;color:{d['color']};font-weight:600;margin-bottom:5px;">{d['title']}</div>
              <div style="font-size:11px;color:#666;line-height:1.65;">
                <span style="color:#4EC9B0;">✅ 우위:</span> {d['win']}<br>
                <span style="color:#FF8C69;">⚠️ 열위:</span> {d['lose']}
              </div>
            </div>""", unsafe_allow_html=True)

def slide_krobot():
    st.markdown(sec_lbl("📊","K-로봇 빅4 재무 비교 (2025E)"), unsafe_allow_html=True)
    cols = st.columns(4)
    for col, c in zip(cols, comp_data):
        oc = "#4EC9B0" if c["op25"]>0 else "#FF8C69"
        os = f"+{c['op25']}억" if c["op25"]>0 else f"{c['op25']}억"
        with col:
            st.markdown(f"""
            <div style="background:#0D0D12;border-radius:10px;padding:16px;border:1px solid {c['color']}33;height:160px;">
              <div style="font-size:13px;font-weight:700;color:{c['color']};margin-bottom:12px;">{c['name']}</div>
              {kv_row("시총", c['cap']+"조")}
              {kv_row("매출(E)", str(c['rev25'])+"억")}
              {kv_row("영업이익(E)", os, oc)}
              <div style="font-size:10px;background:{c['color']}15;color:{c['color']};border-radius:4px;padding:3px 8px;text-align:center;margin-top:8px;">{c['backer']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:14px'/>", unsafe_allow_html=True)
    # 시총 vs 매출 버블
    fig = go.Figure()
    for c in comp_data:
        fig.add_trace(go.Scatter(
            x=[c["rev25"]], y=[c["cap"]],
            mode="markers+text",
            marker=dict(size=max(abs(c["op25"])*0.3, 20), color=c["color"], opacity=0.75),
            text=[c["name"]], textposition="top center",
            textfont=dict(size=11, color=c["color"]),
            name=c["name"]
        ))
    fig.update_layout(**DT, height=240,
                      xaxis=dict(title="매출액(억원)",color="#555"),
                      yaxis=dict(title="시가총액(조원)",color="#555"),
                      showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

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
        th = '<tr>' + ''.join(f'<th style="text-align:right;color:#555;font-size:10px;padding:5px 4px;border-bottom:1px solid #22222A;">{h}</th>' for h in ["구분","2023","2024","2025E"]) + '</tr>'
        trs = ""
        for r in rows:
            tds = f'<td style="font-size:11px;color:#666;padding:5px 4px;border-bottom:1px solid #18181E;">{r[0]}</td>'
            for v in r[1:]:
                vc = "#FF8C69" if v.startswith("-") else "#4EC9B0" if v.startswith("+") else "#B0ACA4"
                tds += f'<td style="text-align:right;font-size:11px;color:{vc};font-family:\'IBM Plex Mono\',monospace;padding:5px 4px;border-bottom:1px solid #18181E;">{v}</td>'
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
        <div style="font-size:11px;color:#555;line-height:1.75;margin-top:4px;">
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
        st.markdown("""
        <div style="background:#1A1010;border:1px solid #3A2020;border-radius:8px;padding:10px 12px;
                    font-size:11px;color:#FF8C69;line-height:1.65;">
          ⚠️ 2025년 주가 +1,052% 급등 이후 PSR 87배 극단적 프리미엄. 컨센서스 대비 -38% 하락 여력 존재.
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(sec_lbl("📊","동종업종 밸류에이션 비교"), unsafe_allow_html=True)
        th = '<tr>' + ''.join(f'<th style="text-align:center;color:#555;font-size:10px;padding:6px 4px;border-bottom:1px solid #22222A;">{h}</th>' for h in ["기업명","시총","PSR(25E)","PBR(25E)"]) + '</tr>'
        trs = ""
        for i, p in enumerate(peers):
            bg = "#1E1E0A" if i==0 else "transparent"
            trs += f'<tr style="background:{bg};">'
            trs += f'<td style="padding:7px 4px;color:{p["color"]};font-weight:{"700" if i==0 else "400"};font-size:11px;border-bottom:1px solid #18181E;">{p["name"]}</td>'
            for val in [p["cap"],p["psr25"],p["pbr25"]]:
                vc = "#FF8C69" if (i==0 and val not in ["3.67조","N/A"]) else "#888"
                trs += f'<td style="text-align:center;color:{vc};font-family:\'IBM Plex Mono\',monospace;font-size:10px;padding:7px 4px;border-bottom:1px solid #18181E;">{val}</td>'
            trs += "</tr>"
        st.markdown(f'<table style="width:100%;border-collapse:collapse;">{th}{trs}</table>', unsafe_allow_html=True)

        st.markdown("<div style='height:12px'/>", unsafe_allow_html=True)
        # 목표주가 범위 차트
        fig_v = go.Figure()
        fig_v.add_trace(go.Scatter(
            x=[77000,149000,360000], y=[1,1,1],
            mode="markers+text",
            marker=dict(color=["#4EC9B0","#E8C547","#7B9FFF"],size=14),
            text=["77,000<br>최저","149,000<br>컨센서스","360,000<br>다이와"],
            textposition="top center",
            textfont=dict(size=10,color=["#4EC9B0","#E8C547","#7B9FFF"]),
        ))
        fig_v.add_trace(go.Scatter(
            x=[242000], y=[1], mode="markers+text",
            marker=dict(color="#FF8C69",size=16,symbol="diamond"),
            text=["242,000<br>현재가"], textposition="bottom center",
            textfont=dict(size=10,color="#FF8C69"),
        ))
        fig_v.update_layout(**DT, height=180,
                            xaxis=dict(title="주가 (원)",color="#555"),
                            yaxis=dict(visible=False), showlegend=False)
        st.plotly_chart(fig_v, use_container_width=True)

def slide_opinion():
    st.markdown("""
    <div class="ir-card" style="border-top:3px solid #7B9FFF;">
      <div style="font-size:13px;font-weight:600;color:#7B9FFF;margin-bottom:14px;">
        🔍 애널리스트 종합 의견 (2026.03 기준)
      </div>
      <div style="font-size:13px;color:#B0ACA4;line-height:2.0;">
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
                <span style="font-size:11px;font-weight:700;color:{s['color']};">{s['label']}</span>
                <span style="font-size:10px;background:{s['color']}22;color:{s['color']};padding:2px 7px;border-radius:4px;font-family:'IBM Plex Mono',monospace;">P≈{s['prob']}</span>
              </div>
              <div style="font-size:11px;color:#C0BDB4;font-weight:600;margin-bottom:6px;line-height:1.45;">{s['title']}</div>
              <div style="font-size:10px;color:#666;line-height:1.6;">{s['impact']}</div>
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
    "TAM & 채택률":         slide_tam,
    "수혜 4단계 로드맵":     slide_pacemaker,
    "유상증자 자금계획":     slide_capex,
    "제품 로드맵":           slide_roadmap,
    "파이프라인 현황":       slide_pipeline,
    "중국 경쟁사 위협":      slide_china_rivals,
    "경쟁력 비교 레이더":    slide_radar_diff,
    "K-로봇 재무 비교":     slide_krobot,
    "연간 실적 차트":        slide_annual,
    "분기 실적 & 레이더":    slide_radar_perf,
    "밸류에이션 지표":       slide_valuation,
    "목표주가 & 종합의견":   slide_opinion,
}

# ════════════════════════════════════════════════════
#  메인 레이아웃
# ════════════════════════════════════════════════════

# 슬라이드 뷰포트 열기
st.markdown(f"""
<div class="slide-viewport">
  <div class="slide-header">
    <div class="slide-title">{cur_sec} &nbsp;›&nbsp; {cur_slide}</div>
    <div class="slide-badge">ROBOTIS (108490) · 2026.03 · SLIDE {si+1}/{n_slides}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# 실제 컨텐츠를 뷰포트 안에 표시
# (Streamlit 특성상 HTML div 안에 위젯을 넣기 어려우므로, 뷰포트 스타일을 
# 상위 컨테이너에 적용하는 방식으로 처리)
with st.container():
    st.markdown('<div style="height:4px"/>', unsafe_allow_html=True)
    SLIDE_RENDERERS[cur_slide]()

# ════════════════════════════════════════════════════
#  페이지네이션 바 (하단 고정)
# ════════════════════════════════════════════════════
st.markdown("<div style='height:20px'/>", unsafe_allow_html=True)

# 점 인디케이터
dots_html = '<div style="display:flex;align-items:center;justify-content:center;gap:6px;margin-bottom:10px;">'
for i in range(n_slides):
    if i == si:
        dots_html += '<div style="width:22px;height:7px;border-radius:4px;background:#E8C547;display:inline-block;"></div>'
    else:
        dots_html += '<div style="width:7px;height:7px;border-radius:50%;background:#2A2A35;display:inline-block;"></div>'
dots_html += '</div>'
st.markdown(dots_html, unsafe_allow_html=True)

# ‹ 페이지 카운터 › 버튼
nav_left, nav_info, nav_right = st.columns([1, 6, 1])

with nav_left:
    if st.button("‹", disabled=(si == 0), use_container_width=True, key="prev_btn"):
        st.session_state.slide_idx -= 1
        st.rerun()

with nav_info:
    st.markdown(
        f'<div style="text-align:center;font-size:12px;color:#444;padding-top:6px;font-family:\'IBM Plex Mono\',monospace;">'
        f'{cur_sec} &nbsp;·&nbsp; {si+1} / {n_slides}'
        f'</div>',
        unsafe_allow_html=True
    )

with nav_right:
    if st.button("›", disabled=(si == n_slides - 1), use_container_width=True, key="next_btn"):
        st.session_state.slide_idx += 1
        st.rerun()
