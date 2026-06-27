import streamlit as st
import pydeck as pdk

st.set_page_config(
    page_title="전국 전기차 등록 현황 조회",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@400;500;700&display=swap');

html, body, .stApp {
    font-family: 'Noto Sans KR', sans-serif !important;
    color: #ffffff !important;
}
.stApp {
    background-color: #0a0d3a;
    background-image:
        radial-gradient(ellipse 65% 55% at 10% 5%,  rgba(88,101,242,0.35) 0%, transparent 65%),
        radial-gradient(ellipse 55% 45% at 90% 90%, rgba(236,72,189,0.22) 0%, transparent 65%);
}
p, li, span, div, label { color: rgba(255,255,255,0.85); }

[data-testid="stSidebar"] {
    background-color: #1e2353 !important;
    border-right: 1px solid rgba(255,255,255,0.07);
}
[data-testid="stSidebar"] * { color: #ffffff !important; }
[data-testid="stSidebar"] label {
    color: rgba(255,255,255,0.55) !important;
    font-size: 12px !important;
    letter-spacing: 0.03em;
}
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.1) !important; }

.stSelectbox > div > div,
.stMultiSelect > div > div {
    background-color: #23272a !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: #1e2353;
    border-radius: 12px;
    padding: 4px;
    gap: 2px;
    border: none;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: rgba(255,255,255,0.5) !important;
    border-radius: 8px;
    font-family: 'Noto Sans KR', sans-serif;
    font-weight: 500;
    font-size: 14px;
    padding: 8px 22px;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: #5865f2 !important;
    color: #ffffff !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 24px;
    background: transparent !important;
}

h1, h2, h3, h4 {
    font-family: 'Black Han Sans', sans-serif !important;
    color: #ffffff !important;
}

[data-testid="metric-container"] {
    background: #1e2353;
    border-radius: 16px;
    padding: 20px !important;
    border: 1px solid rgba(255,255,255,0.07);
}
[data-testid="stMetricLabel"] { color: rgba(255,255,255,0.55) !important; font-size: 13px !important; }
[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-family: 'Black Han Sans', sans-serif !important;
    font-size: 28px !important;
}
[data-testid="stMetricDelta"] svg { display: none; }
[data-testid="stMetricDelta"] { color: #35ed7e !important; font-size: 12px !important; }

hr { border: none !important; border-top: 1px solid rgba(255,255,255,0.08) !important; margin: 20px 0 !important; }

.hero {
    background: linear-gradient(130deg, rgba(88,101,242,0.55) 0%, rgba(236,72,189,0.38) 100%);
    border-radius: 40px;
    padding: 40px 56px;
    margin-bottom: 28px;
}
.hero-title {
    font-family: 'Black Han Sans', sans-serif;
    font-size: 44px;
    line-height: 1.18;
    margin: 0 0 10px 0;
    color: #ffffff;
}
.hero-sub {
    font-size: 15px;
    color: rgba(255,255,255,0.75);
    line-height: 1.7;
    margin: 0;
}

.card {
    background: #1e2353;
    border-radius: 16px;
    padding: 20px 24px;
    border: 1px solid rgba(255,255,255,0.07);
    height: 100%;
    box-sizing: border-box;
}
.card-gradient {
    background: linear-gradient(135deg, #ec48bd 0%, #8b5cf6 100%);
    border-radius: 20px;
    padding: 24px 28px;
}

.stat-label  { font-size: 12px; color: rgba(255,255,255,0.5); margin-bottom: 6px; }
.stat-value  { font-family: 'Black Han Sans', sans-serif; font-size: 30px; line-height: 1.1; color: #fff; }
.stat-sub    { font-size: 12px; color: rgba(255,255,255,0.4); margin-top: 4px; }

.badge {
    display: inline-block;
    background: #ec48bd;
    color: #fff;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 50px;
    margin-bottom: 8px;
    letter-spacing: 0.02em;
}
.badge-green   { background: #35ed7e; color: #000; }
.badge-blurple { background: #5865f2; color: #fff; }
.badge-onyx    { background: #23272a; color: rgba(255,255,255,0.7); border: 1px solid rgba(255,255,255,0.12); }

.section-title {
    font-family: 'Black Han Sans', sans-serif;
    font-size: 20px;
    color: #ffffff;
    margin: 24px 0 14px 0;
}

.row-item {
    background: #1e2353;
    border-radius: 14px;
    padding: 12px 18px;
    margin-bottom: 6px;
    border: 1px solid rgba(255,255,255,0.06);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.row-label { font-size: 14px; color: rgba(255,255,255,0.7); }
.row-value { font-size: 14px; font-weight: 700; color: #ffffff; }
.row-value-green   { font-size: 14px; font-weight: 700; color: #35ed7e; }
.row-value-magenta { font-size: 14px; font-weight: 700; color: #ec48bd; }

.rank-card {
    background: #1e2353;
    border-radius: 20px;
    padding: 24px 20px;
    border: 1px solid rgba(255,255,255,0.07);
    height: 100%;
}
.rank-item {
    display: flex;
    align-items: center;
    gap: 14px;
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 12px 14px;
    margin-bottom: 8px;
}
.rank-num          { font-family: 'Black Han Sans', sans-serif; font-size: 22px; color: rgba(255,255,255,0.2); min-width: 26px; }
.rank-num-gold     { color: #f5c518; }
.rank-num-silver   { color: #c0c0c0; }
.rank-num-bronze   { color: #cd7f32; }
.rank-region       { font-size: 15px; font-weight: 700; color: #fff; flex: 1; }
.rank-val          { font-size: 14px; font-weight: 700; color: #35ed7e; }
.rank-val-magenta  { font-size: 14px; font-weight: 700; color: #ec48bd; }

.faq-card {
    background: #1e2353;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 10px;
    border: 1px solid rgba(255,255,255,0.07);
}
.faq-q { font-size: 15px; font-weight: 700; color: #ffffff; margin-bottom: 8px; }
.faq-a { font-size: 13px; color: rgba(255,255,255,0.6); line-height: 1.7; }

.legend-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 6px;
    font-size: 12px;
    color: rgba(255,255,255,0.6);
}
.legend-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    flex-shrink: 0;
}

.info-note {
    background: rgba(88,101,242,0.12);
    border-left: 3px solid #5865f2;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    font-size: 13px;
    color: rgba(255,255,255,0.65);
    margin-top: 12px;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ── 데이터 ──────────────────────────────────────────────────────────────────
# 시/도 중심 좌표 [위도, 경도]
CENTROIDS = {
    "서울": (37.5665, 126.9780), "경기": (37.2750, 127.0094),
    "인천": (37.4563, 126.7052), "부산": (35.1796, 129.0756),
    "대구": (35.8714, 128.6014), "광주": (35.1595, 126.8526),
    "대전": (36.3504, 127.3845), "울산": (35.5384, 129.3114),
    "세종": (36.4800, 127.2890), "강원": (37.8228, 128.1555),
    "충북": (36.8000, 127.7000), "충남": (36.5184, 126.8000),
    "전북": (35.7175, 127.1530), "전남": (34.8161, 126.4630),
    "경북": (36.4919, 128.8889), "경남": (35.4606, 128.2132),
    "제주": (33.4890, 126.4983),
}

EV_DATA = {
    2020: {"서울": 32000, "경기": 45000, "인천":  9500, "부산": 13000, "대구":  7800,
           "광주":  6200, "대전":  5100, "울산":  3900, "세종":  2100, "강원":  3200,
           "충북":  3800, "충남":  5900, "전북":  4100, "전남":  4500, "경북":  5600,
           "경남":  7200, "제주": 20000},
    2021: {"서울": 46000, "경기": 65000, "인천": 14000, "부산": 19000, "대구": 11000,
           "광주":  9200, "대전":  7400, "울산":  5600, "세종":  3100, "강원":  4700,
           "충북":  5600, "충남":  8700, "전북":  6100, "전남":  6700, "경북":  8200,
           "경남": 10500, "제주": 26000},
    2022: {"서울": 60000, "경기": 85000, "인천": 19000, "부산": 25000, "대구": 15000,
           "광주": 12500, "대전": 10000, "울산":  7500, "세종":  4800, "강원":  6300,
           "충북":  7600, "충남": 12000, "전북":  8300, "전남":  9200, "경북": 11000,
           "경남": 14500, "제주": 29000},
    2023: {"서울": 72000, "경기":103000, "인천": 23000, "부산": 29000, "대구": 18000,
           "광주": 15000, "대전": 12000, "울산":  9200, "세종":  6400, "강원":  8000,
           "충북": 10000, "충남": 15000, "전북": 10500, "전남": 11500, "경북": 14000,
           "경남": 18000, "제주": 32000},
    2024: {"서울": 85000, "경기":120000, "인천": 28000, "부산": 35000, "대구": 22000,
           "광주": 18000, "대전": 15000, "울산": 12000, "세종":  8000, "강원": 10000,
           "충북": 12000, "충남": 18000, "전북": 13000, "전남": 14000, "경북": 17000,
           "경남": 22000, "제주": 35000},
}

POPULATION = {
    "서울": 9400000, "경기": 13600000, "인천": 2950000, "부산": 3300000,
    "대구": 2350000, "광주": 1450000,  "대전": 1450000, "울산": 1100000,
    "세종":  380000, "강원": 1550000,  "충북": 1600000, "충남": 2150000,
    "전북": 1800000, "전남": 1850000,  "경북": 2650000, "경남": 3350000,
    "제주":  670000,
}

FAQ_DATA = [
    {"company": "현대", "category": "충전",
     "q": "전기차 급속 충전 시간은 얼마나 걸리나요?",
     "a": "아이오닉 5 기준 800V 초급속 충전 시 10%→80% 충전에 약 18분이 소요됩니다. 완속 충전은 약 7~10시간입니다."},
    {"company": "현대", "category": "보증",
     "q": "배터리 보증 기간은 어떻게 되나요?",
     "a": "고전압 배터리 및 구동 모터는 10년/20만 km 보증이 적용됩니다 (먼저 도달하는 기준 적용)."},
    {"company": "현대", "category": "주행",
     "q": "1회 충전으로 얼마나 달릴 수 있나요?",
     "a": "아이오닉 6 롱레인지 후륜 기준 복합 524km(공인)입니다. 주행 환경·온도에 따라 실 주행거리는 달라질 수 있습니다."},
    {"company": "현대", "category": "충전",
     "q": "집에서 충전하려면 어떻게 해야 하나요?",
     "a": "완속 충전기(7kW) 설치를 권장합니다. 현대 홈 충전 서비스를 통해 설치 지원을 받을 수 있습니다."},
    {"company": "기아", "category": "주행",
     "q": "EV6의 1회 충전 주행거리는 얼마인가요?",
     "a": "EV6 롱레인지 후륜구동 기준 최대 475km(공인 복합)입니다."},
    {"company": "기아", "category": "A/S",
     "q": "전기차 A/S는 어디서 받을 수 있나요?",
     "a": "전국 기아 서비스센터에서 가능하며, 전기차 전담 기술자가 상주합니다."},
    {"company": "기아", "category": "충전",
     "q": "기아 전기차에서 사용할 수 있는 충전 규격은 무엇인가요?",
     "a": "DC콤보(CCS1) 급속 및 완속 AC 충전을 지원합니다. EV9은 V2L 기능도 제공합니다."},
    {"company": "기아", "category": "보증",
     "q": "EV 배터리 열화가 걱정됩니다. 보증이 되나요?",
     "a": "10년/20만km 이내에 배터리 용량이 70% 미만으로 저하될 경우 무상 교체 또는 수리 서비스가 제공됩니다."},
]


# ── 헬퍼 ────────────────────────────────────────────────────────────────────
def ev_count(yr, reg):   return EV_DATA.get(yr, {}).get(reg, 0)
def pop_ratio(yr, reg):  return round(ev_count(yr, reg) / POPULATION.get(reg, 1) * 1000, 2)
def growth_rate(yr, reg):
    if yr <= 2020: return None
    prev = ev_count(yr - 1, reg)
    return round((ev_count(yr, reg) - prev) / prev * 100, 1) if prev else None

def get_metric_value(yr, reg, metric):
    if metric == "절대 등록대수":      return ev_count(yr, reg)
    if metric == "인구당 보유율":      return pop_ratio(yr, reg)
    return growth_rate(yr, reg) or 0.0

def top3(yr, metric):
    vals = {r: get_metric_value(yr, r, metric) for r in CENTROIDS}
    return sorted(vals.items(), key=lambda x: x[1], reverse=True)[:3]

def value_label(val, metric):
    if metric == "절대 등록대수":  return f"{val:,.0f}대"
    if metric == "인구당 보유율":  return f"{val:.2f}대/천명"
    return f"+{val:.1f}%"

def make_map_data(yr, metric):
    vals = {r: get_metric_value(yr, r, metric) for r in CENTROIDS}
    max_v = max(vals.values()) or 1
    rows = []
    for reg, val in vals.items():
        lat, lon = CENTROIDS[reg]
        norm = val / max_v          # 0~1
        # 색상: 낮음(파란색) → 높음(마젠타)
        r_ch = int(88  + (236 - 88)  * norm)
        g_ch = int(101 + (72  - 101) * norm)
        b_ch = int(242 + (189 - 242) * norm)
        rows.append({
            "region": reg,
            "lat": lat,
            "lon": lon,
            "value": val,
            "elevation": int(norm * 200000),   # 최대 200km 높이(pydeck 단위)
            "color": [r_ch, g_ch, b_ch, 200],
        })
    return rows


# ── 사이드바 ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<h2 style="font-family:\'Black Han Sans\',sans-serif;font-size:20px;margin-bottom:4px;">조회 조건</h2>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:12px;color:rgba(255,255,255,0.4);margin-bottom:20px;">데이터: 국토교통부 자동차 등록통계</p>', unsafe_allow_html=True)

    year   = st.selectbox("기준 연도", [2024, 2023, 2022, 2021, 2020])
    metric = st.selectbox("비교 기준", ["절대 등록대수", "인구당 보유율", "전년 대비 증가율"])
    region = st.selectbox("지역 상세 보기", list(CENTROIDS.keys()))

    st.markdown("---")
    st.markdown('<div class="section-title" style="font-size:15px;margin:0 0 10px;">범례</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="legend-row"><div class="legend-dot" style="background:#5865f2;"></div>낮음</div>
    <div class="legend-row"><div class="legend-dot" style="background:#9b5cbe;"></div>중간</div>
    <div class="legend-row"><div class="legend-dot" style="background:#ec48bd;"></div>높음</div>
    <p style="font-size:11px;color:rgba(255,255,255,0.3);margin-top:8px;line-height:1.6;">
    컬럼 높이와 색상 모두<br>선택 기준의 상대값을 나타냅니다.<br>마우스를 올리면 수치를 확인할 수 있습니다.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("---")
    faq_company = st.selectbox("FAQ 기업", ["전체", "현대", "기아"])
    faq_keyword = st.text_input("FAQ 검색어", placeholder="예: 충전, 배터리…")


# ── 히어로 ─────────────────────────────────────────────────────────────────
metric_label = {"절대 등록대수": "절대 등록대수", "인구당 보유율": "인구당 보유율 (대/천명)", "전년 대비 증가율": "전년 대비 증가율 (%)"}
st.markdown(f"""
<div class="hero">
    <div class="hero-title">전국 전기차 등록 현황 지도</div>
    <p class="hero-sub">
        {year}년 기준 · <strong>{metric_label[metric]}</strong>으로 시각화 &nbsp;|&nbsp;
        컬럼이 높을수록, 색상이 진할수록 수치가 높습니다.
    </p>
</div>
""", unsafe_allow_html=True)


# ── 탭 ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["지도 현황", "지역 상세 / TOP3", "기업 FAQ"])


# ════════════════════════════════════════════════════════════
# TAB 1 · 지도 현황
# ════════════════════════════════════════════════════════════
with tab1:
    map_data = make_map_data(year, metric if metric != "전년 대비 증가율" else "절대 등록대수")
    if metric == "전년 대비 증가율":
        map_data = make_map_data(year, metric)

    tooltip = {
        "html": "<b>{region}</b><br/>값: {value}",
        "style": {
            "background": "#1e2353",
            "color": "#ffffff",
            "font-family": "'Noto Sans KR', sans-serif",
            "font-size": "13px",
            "padding": "8px 12px",
            "border-radius": "8px",
            "border": "1px solid rgba(255,255,255,0.15)",
        },
    }

    column_layer = pdk.Layer(
        "ColumnLayer",
        data=map_data,
        get_position=["lon", "lat"],
        get_elevation="elevation",
        elevation_scale=1,
        radius=20000,
        get_fill_color="color",
        pickable=True,
        auto_highlight=True,
    )

    view_state = pdk.ViewState(
        latitude=36.5,
        longitude=127.8,
        zoom=6.2,
        pitch=45,
        bearing=0,
    )

    st.pydeck_chart(
        pdk.Deck(
            layers=[column_layer],
            initial_view_state=view_state,
            tooltip=tooltip,
            map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
        ),
        use_container_width=True,
        height=580,
    )

    st.markdown("""
    <div class="info-note">
        마우스를 컬럼 위에 올리면 지역명과 수치를 확인할 수 있습니다.
        컬럼 높이와 색상(파란색→마젠타)은 선택한 기준의 상대값을 나타냅니다.
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# TAB 2 · 지역 상세 / TOP3
# ════════════════════════════════════════════════════════════
with tab2:
    # 선택 지역 요약
    st.markdown(f'<div class="section-title">{region} · {year}년 상세</div>', unsafe_allow_html=True)

    cnt  = ev_count(year, region)
    rat  = pop_ratio(year, region)
    grw  = growth_rate(year, region)
    grw_str = f"+{grw}%" if grw and grw >= 0 else (f"{grw}%" if grw else "—")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <div class="badge badge-blurple">절대 등록대수</div>
            <div class="stat-value">{cnt:,}대</div>
            <div class="stat-sub">{year}년 누적</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <div class="badge badge-green">인구당 보유율</div>
            <div class="stat-value">{rat}</div>
            <div class="stat-sub">대 / 천명</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <div class="badge">전년 대비 증가율</div>
            <div class="stat-value">{grw_str}</div>
            <div class="stat-sub">{year-1}년 → {year}년</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 연도별 추이
    col_trend, col_ranks = st.columns([1, 2])

    with col_trend:
        st.markdown(f'<div class="section-title" style="font-size:17px;margin-top:0;">{region} 연도별 추이</div>', unsafe_allow_html=True)
        years_list = [2020, 2021, 2022, 2023, 2024]
        max_c = max(ev_count(y, region) for y in years_list)
        for y in years_list:
            c = ev_count(y, region)
            pct = int(c / max_c * 100) if max_c else 0
            hl = "border:1px solid rgba(88,101,242,0.6);" if y == year else ""
            st.markdown(f"""
            <div class="row-item" style="{hl}">
                <div>
                    <div class="row-label">{y}년</div>
                    <div style="background:rgba(255,255,255,0.08);border-radius:50px;height:6px;width:120px;margin-top:6px;overflow:hidden;">
                        <div style="height:6px;border-radius:50px;background:#5865f2;width:{pct}%;"></div>
                    </div>
                </div>
                <div class="row-value">{c:,}대</div>
            </div>""", unsafe_allow_html=True)

    with col_ranks:
        st.markdown(f'<div class="section-title" style="font-size:17px;margin-top:0;">{year}년 기준별 TOP 3</div>', unsafe_allow_html=True)
        rank_colors = ["rank-num-gold", "rank-num-silver", "rank-num-bronze"]

        metrics_list = [
            ("절대 등록대수", "badge-blurple", "rank-val"),
            ("인구당 보유율", "badge-green",   "rank-val"),
            ("전년 대비 증가율", "",            "rank-val-magenta"),
        ]

        for m_name, badge_cls, val_cls in metrics_list:
            t3 = top3(year, m_name)
            badge_html = f'<span class="badge {badge_cls}">{m_name}</span>'
            st.markdown(badge_html, unsafe_allow_html=True)
            for i, (reg_name, val) in enumerate(t3):
                label = value_label(val, m_name)
                hl = "background:rgba(88,101,242,0.15);" if reg_name == region else ""
                st.markdown(f"""
                <div class="rank-item" style="{hl}margin-bottom:5px;">
                    <div class="rank-num {rank_colors[i]}">{i+1}</div>
                    <div class="rank-region">{reg_name}</div>
                    <div class="{val_cls}">{label}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)

    # 분석 요약
    abs1 = top3(year, "절대 등록대수")[0][0]
    rat1 = top3(year, "인구당 보유율")[0][0]
    grw1 = top3(year, "전년 대비 증가율")[0][0] if year > 2020 else "—"

    st.markdown(f"""
    <div class="card-gradient" style="margin-top:16px;">
        <div style="font-family:'Black Han Sans',sans-serif;font-size:18px;margin-bottom:8px;">분석 요약</div>
        <p style="font-size:14px;color:rgba(255,255,255,0.85);margin:0;line-height:1.8;">
            {year}년 기준, 절대 등록대수 1위는 <strong>{abs1}</strong>이지만
            인구당 보유율 1위는 <strong>{rat1}</strong>입니다.
            {f'가장 빠르게 성장한 지역은 <strong>{grw1}</strong>으로, 단순 등록대수와는 다른 지역이 상위권을 차지합니다.' if grw1 != '—' else ''}
        </p>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# TAB 3 · 기업 FAQ
# ════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">자동차 기업 FAQ</div>', unsafe_allow_html=True)

    filtered = FAQ_DATA
    if faq_company != "전체":
        filtered = [f for f in filtered if f["company"] == faq_company]
    if faq_keyword:
        kw = faq_keyword.lower()
        filtered = [f for f in filtered if kw in f["q"].lower() or kw in f["a"].lower() or kw in f["category"].lower()]

    st.markdown(f'<p style="color:rgba(255,255,255,0.5);font-size:14px;margin-top:-16px;margin-bottom:20px;">검색 결과: {len(filtered)}건</p>', unsafe_allow_html=True)

    if not filtered:
        st.markdown('<div class="info-note">검색 결과가 없습니다. 다른 검색어를 입력해보세요.</div>', unsafe_allow_html=True)
    else:
        for item in filtered:
            badge_cls = "badge-blurple" if item["company"] == "현대" else "badge-onyx"
            st.markdown(f"""
            <div class="faq-card">
                <div style="margin-bottom:10px;">
                    <span class="badge {badge_cls}">{item['company']}</span>
                    <span class="badge badge-green" style="margin-left:4px;">{item['category']}</span>
                </div>
                <div class="faq-q">Q. {item['q']}</div>
                <div class="faq-a">A. {item['a']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-note">
        FAQ 데이터는 각 제조사 공식 홈페이지 기반으로 수집됩니다.
        최신 정보는 제조사 공식 채널을 통해 확인하세요.
    </div>
    """, unsafe_allow_html=True)
