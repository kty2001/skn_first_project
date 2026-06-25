import streamlit as st

st.set_page_config(
    page_title="현대·기아 자동차 비용 비교",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 디자인 시스템 (DESIGN.md 기반) ─────────────────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@400;500;700&display=swap');

/* ── 전역 ── */
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

/* ── 사이드바 ── */
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
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.1) !important;
}

/* ── 위젯 ── */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background-color: #23272a !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
}
.stSlider [data-baseweb="slider"] [data-testid="stTickBar"] span {
    color: rgba(255,255,255,0.5) !important;
}
.stSlider [aria-valuenow] { background: #5865f2 !important; }

/* ── 탭 ── */
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
    padding-top: 28px;
    background: transparent !important;
}

/* ── 제목 ── */
h1, h2, h3, h4 {
    font-family: 'Black Han Sans', sans-serif !important;
    color: #ffffff !important;
}

/* ── 메트릭 ── */
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

/* ── 구분선 ── */
hr { border: none !important; border-top: 1px solid rgba(255,255,255,0.08) !important; margin: 20px 0 !important; }

/* ── 커스텀 클래스 ── */
.hero {
    background: linear-gradient(130deg, rgba(88,101,242,0.55) 0%, rgba(236,72,189,0.38) 100%);
    border-radius: 40px;
    padding: 52px 64px;
    margin-bottom: 36px;
}
.hero-title {
    font-family: 'Black Han Sans', sans-serif;
    font-size: 52px;
    line-height: 1.18;
    margin: 0 0 14px 0;
    color: #ffffff;
}
.hero-sub {
    font-size: 17px;
    color: rgba(255,255,255,0.75);
    line-height: 1.7;
    margin: 0;
}

.card {
    background: #1e2353;
    border-radius: 16px;
    padding: 24px 28px;
    border: 1px solid rgba(255,255,255,0.07);
    height: 100%;
    box-sizing: border-box;
}
.card-blurple {
    background: #5865f2;
    border-radius: 40px;
    padding: 28px 24px;
    text-align: center;
}
.card-gradient {
    background: linear-gradient(135deg, #ec48bd 0%, #8b5cf6 100%);
    border-radius: 40px;
    padding: 28px 24px;
}
.card-black {
    background: #000000;
    border-radius: 16px;
    padding: 24px 28px;
    border: 1px solid rgba(255,255,255,0.06);
}
.card-green {
    background: #35ed7e;
    border-radius: 40px;
    padding: 20px 24px;
    text-align: center;
}

.stat-label  { font-size: 12px; color: rgba(255,255,255,0.5); margin-bottom: 6px; }
.stat-value  { font-family: 'Black Han Sans', sans-serif; font-size: 34px; line-height: 1.1; color: #fff; }
.stat-sub    { font-size: 12px; color: rgba(255,255,255,0.4); margin-top: 4px; }
.stat-value-dark { font-family: 'Black Han Sans', sans-serif; font-size: 28px; color: #000; line-height: 1.1; }
.stat-label-dark { font-size: 12px; color: rgba(0,0,0,0.6); margin-bottom: 6px; }

.badge {
    display: inline-block;
    background: #ec48bd;
    color: #fff;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 50px;
    margin-bottom: 10px;
    letter-spacing: 0.02em;
}
.badge-green   { background: #35ed7e; color: #000; }
.badge-blurple { background: #5865f2; color: #fff; }
.badge-onyx    { background: #23272a; color: rgba(255,255,255,0.7); border: 1px solid rgba(255,255,255,0.12); }

.section-title {
    font-family: 'Black Han Sans', sans-serif;
    font-size: 22px;
    color: #ffffff;
    margin: 32px 0 16px 0;
}

.row-item {
    background: #1e2353;
    border-radius: 14px;
    padding: 14px 20px;
    margin-bottom: 8px;
    border: 1px solid rgba(255,255,255,0.06);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.row-label { font-size: 14px; color: rgba(255,255,255,0.7); }
.row-value { font-size: 15px; font-weight: 700; color: #ffffff; }
.row-value-green { font-size: 15px; font-weight: 700; color: #35ed7e; }
.row-value-magenta { font-size: 15px; font-weight: 700; color: #ec48bd; }

.compare-col {
    background: #1e2353;
    border-radius: 20px;
    padding: 28px 24px;
    border: 1px solid rgba(255,255,255,0.07);
    height: 100%;
}
.compare-col-active {
    background: linear-gradient(160deg, rgba(88,101,242,0.4), #1e2353 60%);
    border-radius: 20px;
    padding: 28px 24px;
    border: 1px solid rgba(88,101,242,0.5);
    height: 100%;
}
.compare-model-name {
    font-family: 'Black Han Sans', sans-serif;
    font-size: 24px;
    margin-bottom: 4px;
    color: #fff;
}
.compare-tag { font-size: 13px; color: rgba(255,255,255,0.5); margin-bottom: 20px; }

.cost-bar-wrap { margin: 6px 0 14px; }
.cost-bar-bg {
    background: rgba(255,255,255,0.08);
    border-radius: 50px;
    height: 8px;
    overflow: hidden;
    margin-top: 4px;
}
.cost-bar-fill {
    height: 8px;
    border-radius: 50px;
    background: #5865f2;
}
.cost-bar-fill-green { background: #35ed7e; }
.cost-bar-fill-magenta { background: #ec48bd; }
.cost-bar-fill-onyx { background: #23272a; }

.info-note {
    background: rgba(88,101,242,0.12);
    border-left: 3px solid #5865f2;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    font-size: 13px;
    color: rgba(255,255,255,0.65);
    margin-top: 8px;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ── 데이터 (플레이스홀더) ──────────────────────────────────────────────────
MODELS = {
    "현대": {
        "승용": ["아반떼", "쏘나타", "그랜저", "아이오닉 5", "아이오닉 6"],
        "승합": ["스타리아", "팰리세이드", "싼타페", "투싼"],
    },
    "기아": {
        "승용": ["K3", "K5", "K8", "EV6", "EV9"],
        "승합": ["카니발", "쏘렌토", "스포티지", "셀토스"],
    },
}

COST_PLACEHOLDER = {
    "신차 구매": {"total": "4,850만 원", "monthly": "약 40만 원/월", "delta": "기준"},
    "중고차 구매": {"total": "3,120만 원", "monthly": "약 26만 원/월", "delta": "-35%"},
    "장기 렌트": {"total": "5,400만 원", "monthly": "약 45만 원/월", "delta": "+11%"},
    "리스": {"total": "4,980만 원", "monthly": "약 41만 원/월", "delta": "+3%"},
}


# ── 사이드바 ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<h2 style="font-family:\'Black Han Sans\',sans-serif;font-size:20px;margin-bottom:4px;">조회 조건</h2>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:12px;color:rgba(255,255,255,0.4);margin-bottom:20px;">데이터 기준: 2024년 12월</p>', unsafe_allow_html=True)

    manufacturer = st.selectbox("제조사", ["현대", "기아"])
    car_type = st.selectbox("차종", ["승용", "승합"])

    available_models = MODELS[manufacturer][car_type]
    model = st.selectbox("모델", available_models)

    fuel = st.selectbox("연료 종류", ["휘발유", "경유", "LPG", "전기", "하이브리드"])

    st.markdown("---")

    distance = st.slider("연간 주행거리 (km)", 5_000, 50_000, 15_000, step=1_000, format="%d km")
    years = st.slider("분석 기간", 1, 10, 10, format="%d 년")

    st.markdown("---")

    st.markdown('<p style="font-size:11px;color:rgba(255,255,255,0.3);line-height:1.6;">보험료 조건: 26세 이상, 운전경력 5년, 자차 포함<br>유류비: 오피넷 전국 평균 기준</p>', unsafe_allow_html=True)


# ── 히어로 ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-title">현대·기아 자동차<br>비용 비교 분석</div>
    <p class="hero-sub">
        신차·중고차·렌트·리스의 {years}년간 실제 보유 비용을 한눈에 비교하세요.<br>
        유류비·보험료·소모품까지 포함한 총 유지비를 제공합니다.
    </p>
</div>
""", unsafe_allow_html=True)


# ── 탭 ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["비용 비교", "모델 비교", "유지비 상세"])


# ════════════════════════════════════════════════════════════
# TAB 1 · 비용 비교
# ════════════════════════════════════════════════════════════
with tab1:
    st.markdown(f'<div class="section-title">{manufacturer} {model} · {years}년 총 보유 비용</div>', unsafe_allow_html=True)

    # 요약 메트릭 4개
    c1, c2, c3, c4 = st.columns(4)
    entries = list(COST_PLACEHOLDER.items())
    cols = [c1, c2, c3, c4]
    badges = ["badge-blurple", "badge-onyx", "badge-onyx", "badge-onyx"]
    for col, (label, data), badge in zip(cols, entries, badges):
        with col:
            st.markdown(f"""
            <div class="card" style="text-align:center;">
                <div class="badge {badge}">{label}</div>
                <div class="stat-value">{data['total']}</div>
                <div class="stat-sub">{data['monthly']}</div>
                <div style="margin-top:10px;font-size:12px;color:{'#35ed7e' if '+' not in data['delta'] and data['delta']!='기준' else '#ec48bd' if '+' in data['delta'] else 'rgba(255,255,255,0.45)'};">{data['delta']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 비용 구성 막대 카드
    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.markdown('<div class="section-title" style="font-size:18px;margin-top:0;">비용 구성 비교</div>', unsafe_allow_html=True)

        items = [
            ("차량 구입비", "2,850만 원", 59, "cost-bar-fill"),
            ("유류비 (10년)", "720만 원", 15, "cost-bar-fill-green"),
            ("보험료 (10년)", "680만 원", 14, "cost-bar-fill-magenta"),
            ("소모품·정비비", "400만 원", 8, "cost-bar-fill"),
            ("기타 (세금·주차 등)", "200만 원", 4, "cost-bar-fill-onyx"),
        ]
        for name, val, pct, bar_cls in items:
            st.markdown(f"""
            <div class="card" style="padding:16px 20px;margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span class="row-label">{name}</span>
                    <span class="row-value">{val}</span>
                </div>
                <div class="cost-bar-wrap">
                    <div class="cost-bar-bg">
                        <div class="{bar_cls}" style="width:{pct}%;"></div>
                    </div>
                </div>
                <div style="font-size:11px;color:rgba(255,255,255,0.35);text-align:right;">전체의 {pct}%</div>
            </div>
            """, unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="section-title" style="font-size:18px;margin-top:0;">연도별 예상 비용</div>', unsafe_allow_html=True)
        yearly = [
            ("1년 차", "620만 원", "취득세·등록비 포함"),
            ("3년 차", "480만 원", "타이어 교체 예정"),
            ("5년 차", "510만 원", "배터리·브레이크 교체"),
            ("7년 차", "530만 원", "소모품 집중 교체"),
            ("10년 차", "490만 원", "중간 점검 비용"),
        ]
        for yr, cost, note in yearly:
            st.markdown(f"""
            <div class="row-item">
                <div>
                    <div class="row-label">{yr}</div>
                    <div style="font-size:11px;color:rgba(255,255,255,0.3);">{note}</div>
                </div>
                <div class="row-value">{cost}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-note">
        유류비는 오피넷 전국 평균 단가 및 제조사 공인 복합연비 기준으로 산출됩니다.
        실제 비용은 개인 운전 습관·지역·보험 조건에 따라 달라질 수 있습니다.
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# TAB 2 · 모델 비교
# ════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">모델 간 비교</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:rgba(255,255,255,0.5);font-size:14px;margin-top:-16px;margin-bottom:24px;">두 모델을 동일 조건에서 비교합니다. 조건은 개별 설정 가능합니다.</p>', unsafe_allow_html=True)

    # 모델 선택
    sel_col1, sel_col2 = st.columns(2)
    with sel_col1:
        m1_maker = st.selectbox("제조사 A", ["현대", "기아"], key="m1_maker")
        m1_type  = st.selectbox("차종 A", ["승용", "승합"], key="m1_type")
        m1_model = st.selectbox("모델 A", MODELS[m1_maker][m1_type], key="m1_model")
        m1_fuel  = st.selectbox("연료 A", ["휘발유", "경유", "LPG", "전기", "하이브리드"], key="m1_fuel")
    with sel_col2:
        m2_maker = st.selectbox("제조사 B", ["기아", "현대"], key="m2_maker")
        m2_type  = st.selectbox("차종 B", ["승용", "승합"], key="m2_type")
        m2_model = st.selectbox("모델 B", MODELS[m2_maker][m2_type], key="m2_model")
        m2_fuel  = st.selectbox("연료 B", ["전기", "휘발유", "경유", "LPG", "하이브리드"], key="m2_fuel")

    st.markdown("<br>", unsafe_allow_html=True)

    # 비교 카드
    cmp1, cmp2 = st.columns(2)

    compare_rows = [
        ("신차 가격", "3,150만 원", "3,680만 원"),
        ("10년 총 유지비", "1,450만 원", "1,280만 원"),
        ("10년 총 보유비용", "4,600만 원", "4,960만 원"),
        ("연평균 연비", "14.2 km/L", "5.8 km/kWh"),
        ("연간 유류비 추정", "72만 원", "38만 원"),
        ("연간 보험료 추정", "68만 원", "71만 원"),
        ("감가상각 (10년 후)", "약 35% 잔존", "약 40% 잔존"),
    ]

    with cmp1:
        st.markdown(f"""
        <div class="compare-col-active">
            <div class="badge badge-blurple">모델 A</div>
            <div class="compare-model-name">{m1_maker} {m1_model}</div>
            <div class="compare-tag">{m1_fuel} · 승용</div>
        """, unsafe_allow_html=True)
        for row_label, val_a, _ in compare_rows:
            st.markdown(f"""
            <div class="row-item" style="margin-bottom:6px;">
                <span class="row-label">{row_label}</span>
                <span class="row-value">{val_a}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with cmp2:
        st.markdown(f"""
        <div class="compare-col">
            <div class="badge badge-onyx">모델 B</div>
            <div class="compare-model-name">{m2_maker} {m2_model}</div>
            <div class="compare-tag">{m2_fuel} · 승용</div>
        """, unsafe_allow_html=True)
        for row_label, _, val_b in compare_rows:
            st.markdown(f"""
            <div class="row-item" style="margin-bottom:6px;">
                <span class="row-label">{row_label}</span>
                <span class="row-value">{val_b}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # 요약 밴드
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card-gradient" style="border-radius:20px;padding:28px 36px;">
        <div style="font-family:'Black Han Sans',sans-serif;font-size:20px;margin-bottom:8px;">분석 요약</div>
        <p style="font-size:15px;color:rgba(255,255,255,0.85);margin:0;line-height:1.7;">
            10년 총 보유 비용 기준으로 <strong>{m1_maker} {m1_model}</strong>이 약 360만 원 더 저렴합니다.
            단, <strong>{m2_maker} {m2_model}</strong>의 경우 전기차 특성상 유류비가 절반 이하로 낮아
            연간 주행거리가 많을수록 유리해집니다.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# TAB 3 · 유지비 상세
# ════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">유지비 상세 내역</div>', unsafe_allow_html=True)

    sec1, sec2 = st.columns(2)

    # 유류비
    with sec1:
        st.markdown("""
        <div class="card-blurple" style="margin-bottom:16px;">
            <div class="badge badge-green">유류비</div>
            <div class="stat-value">연 72만 원</div>
            <div class="stat-sub">월 평균 6만 원 · 15,000 km/년 기준</div>
        </div>
        """, unsafe_allow_html=True)

        fuel_rows = [
            ("연간 주행거리", "15,000 km"),
            ("복합 연비", "14.2 km/L"),
            ("연간 소비 연료", "약 1,056 L"),
            ("유류 단가 (기준)", "1,680 원/L"),
            ("연간 유류비", "약 72만 원"),
            ("10년 합계", "약 720만 원"),
        ]
        for label, val in fuel_rows:
            st.markdown(f"""
            <div class="row-item">
                <span class="row-label">{label}</span>
                <span class="row-value">{val}</span>
            </div>
            """, unsafe_allow_html=True)

    # 보험료
    with sec2:
        st.markdown("""
        <div class="card-gradient" style="margin-bottom:16px;">
            <div class="badge" style="background:rgba(255,255,255,0.25);color:#fff;">보험료</div>
            <div class="stat-value">연 68만 원</div>
            <div class="stat-sub">26세 이상·운전경력 5년·자차 포함 기준</div>
        </div>
        """, unsafe_allow_html=True)

        ins_rows = [
            ("대인 배상 I·II", "포함"),
            ("대물 배상 (2억)", "포함"),
            ("자기신체사고", "포함"),
            ("자차 손해", "포함"),
            ("긴급출동·기타특약", "포함"),
            ("10년 합계", "약 680만 원"),
        ]
        for label, val in ins_rows:
            st.markdown(f"""
            <div class="row-item">
                <span class="row-label">{label}</span>
                <span class="row-value">{val}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 소모품 테이블
    st.markdown('<div class="section-title" style="font-size:18px;">소모품 교체 주기 및 비용</div>', unsafe_allow_html=True)

    consumables = [
        ("엔진오일 + 필터",    "1만 km / 1년",   "6~10만 원",    "60~100만 원"),
        ("타이어 (4개)",       "4~5만 km",        "40~100만 원",  "80~200만 원"),
        ("브레이크 패드 (전)", "3~4만 km",        "10~20만 원",   "20~40만 원"),
        ("에어 필터",          "2만 km / 2년",    "2~5만 원",     "10~25만 원"),
        ("에어컨 필터",        "1만 km / 1년",    "1~3만 원",     "10~30만 원"),
        ("배터리 (보조)",      "3~5년",           "10~20만 원",   "20~40만 원"),
        ("점화 플러그",        "4만 km",          "3~8만 원",     "8~16만 원"),
        ("냉각수",             "4~5년",           "5~10만 원",    "10~20만 원"),
    ]

    header = '<div class="card" style="padding:14px 20px;margin-bottom:2px;"><div style="display:grid;grid-template-columns:2fr 1.5fr 1.2fr 1.2fr;gap:8px;font-size:12px;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:0.05em;">'
    header += "<span>소모품</span><span>교체 주기</span><span>1회 비용</span><span>10년 합계</span></div></div>"
    st.markdown(header, unsafe_allow_html=True)

    for name, cycle, unit_cost, total_cost in consumables:
        st.markdown(f"""
        <div class="row-item" style="display:grid;grid-template-columns:2fr 1.5fr 1.2fr 1.2fr;gap:8px;margin-bottom:6px;">
            <span class="row-label" style="font-weight:500;color:rgba(255,255,255,0.85);">{name}</span>
            <span class="row-label">{cycle}</span>
            <span class="row-value" style="font-size:14px;">{unit_cost}</span>
            <span class="row-value-green" style="font-size:14px;">{total_cost}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-note" style="margin-top:20px;">
        소모품 비용은 공임 포함 평균 견적 기준입니다. 차량 등급·정비소 유형(딜러/일반)에 따라
        30~50% 차이가 발생할 수 있습니다. 전기차는 엔진오일·점화 플러그 항목이 제외됩니다.
    </div>
    """, unsafe_allow_html=True)
