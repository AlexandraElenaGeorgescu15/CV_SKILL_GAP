"""AI Career Architect - 2026 · Gemini 2.5 Flash Edition"""
import streamlit as st
import pdfplumber
import io
import json
import time
import os

# PAGE CONFIG
st.set_page_config(
    page_title="AI Career Architect · 2026",
    page_icon="â˜…",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# STATIC DIR
_STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(_STATIC_DIR, exist_ok=True)

# SESSION STATE
for _k, _v in [("cv_text", ""), ("cv_name", ""), ("cv_pages", 0), ("cv_words", 0)]:
    if _k not in st.session_state:
        st.session_state[_k] = _v

# =========================================================================
#  GLOBAL CSS  -  Aurora / Glass morphism · Mobile-first
# =========================================================================
# st.html() renders verbatim — blank lines never break HTML blocks (unlike st.markdown)
st.html("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Outfit:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
:root {
  --ink:       #09090f;
  --ink2:      #0d0d1a;
  --ink3:      #12122a;
  --glass:     rgba(255,255,255,.04);
  --glass2:    rgba(255,255,255,.07);
  --border:    rgba(255,255,255,.09);
  --border2:   rgba(255,255,255,.16);
  --g1:        #6ee7f7;
  --g2:        #a78bfa;
  --g3:        #f472b6;
  --g4:        #34d399;
  --text1:     #f8fafc;
  --text2:     #94a3b8;
  --text3:     #475569;
  --danger:    #f87171;
  --warn:      #fbbf24;
  --ok:        #34d399;
  --font-ui:   'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --font-disp: 'Outfit', 'Inter', sans-serif;
  --r:         16px;
  --r-sm:      10px;
}
html, body,
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
  background: var(--ink) !important;
  color: var(--text1) !important;
  font-family: var(--font-ui) !important;
}
[data-testid="stDecoration"],#MainMenu,footer { display:none!important; }
[data-testid="stHeader"] {
  background: transparent !important;
  border-bottom: none !important;
  height: 3.25rem !important;
  min-height: 3.25rem !important;
}
[data-testid="stToolbar"] {
  background: transparent !important;
}
[data-testid="stToolbar"] button,
[data-testid="stToolbar"] a {
  color: var(--text3) !important;
}
*, *::before, *::after { box-sizing:border-box; }
::-webkit-scrollbar { width:4px; height:4px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb {
  background:rgba(110,231,247,.25);
  border-radius:2px;
}
[data-testid="stMainBlockContainer"] {
  padding: 0 1rem 4rem !important;
  max-width: 1200px !important;
}
@media (min-width: 640px) {
  [data-testid="stMainBlockContainer"] {
    padding: 0 2rem 4rem !important;
  }
}
[data-testid="stSidebar"] {
  background: var(--ink2) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebarContent"] { padding: 1.5rem 1rem !important; }

/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: var(--glass) !important;
  border: 1px solid var(--border) !important;
  border-radius: 50px !important;
  padding: 4px !important;
  gap: 2px !important;
  backdrop-filter: blur(12px) !important;
  overflow-x: auto !important;
  white-space: nowrap !important;
  -webkit-overflow-scrolling: touch !important;
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"],
[data-testid="stTabs"] [data-baseweb="tab-border"] { display:none!important; }
[data-testid="stTabs"] [data-baseweb="tab"] {
  font-family: var(--font-mono) !important;
  font-size: 0.7rem !important;
  letter-spacing: 1px !important;
  text-transform: uppercase !important;
  color: var(--text3) !important;
  background: transparent !important;
  border: none !important;
  border-radius: 40px !important;
  padding: 0.5rem 1.2rem !important;
  white-space: nowrap !important;
  transition: all 0.2s !important;
}
[data-testid="stTabs"] [data-baseweb="tab"]:hover {
  color: var(--text1) !important;
  background: var(--glass2) !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
  background: linear-gradient(135deg,rgba(110,231,247,.18),rgba(167,139,250,.14)) !important;
  border: 1px solid rgba(110,231,247,.3) !important;
  color: #fff !important;
  box-shadow: 0 0 16px rgba(110,231,247,.12) !important;
}
[data-testid="stTabsContent"] { padding-top: 1.4rem !important; }

/* File uploader */
[data-testid="stFileUploader"] {
  background: var(--glass) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r) !important;
  backdrop-filter: blur(12px) !important;
}
[data-testid="stFileUploader"]:hover,
[data-testid="stFileUploader"]:focus-within {
  border-color: rgba(110,231,247,.4) !important;
  box-shadow: 0 0 0 3px rgba(110,231,247,.08) !important;
}
[data-testid="stFileUploaderDropzone"] {
  background: transparent !important;
  border: 1.5px dashed rgba(255,255,255,.12) !important;
  border-radius: var(--r-sm) !important;
}
[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] small {
  color: var(--text2) !important;
}

/* Metrics */
[data-testid="stMetric"] {
  background: var(--glass) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r) !important;
  padding: 1.4rem !important;
  backdrop-filter: blur(12px) !important;
  position: relative !important;
  overflow: hidden !important;
  transition: all .3s !important;
}
[data-testid="stMetric"]::before {
  content:'';
  position:absolute; top:0; left:0; right:0; height:1px;
  background: linear-gradient(90deg,transparent,var(--g1),transparent);
  opacity:.6;
}
[data-testid="stMetric"]:hover {
  border-color: rgba(110,231,247,.3) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 32px rgba(0,0,0,.4) !important;
}
[data-testid="stMetricLabel"] > div {
  font-family: var(--font-mono) !important;
  font-size: .65rem !important;
  letter-spacing: 1.5px !important;
  text-transform: uppercase !important;
  color: var(--text3) !important;
}
[data-testid="stMetricValue"] > div {
  font-family: var(--font-disp) !important;
  font-size: 2rem !important;
  font-weight: 700 !important;
  background: linear-gradient(135deg, var(--g1), var(--g2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
[data-testid="stMetricDelta"] > div {
  color: var(--text2) !important;
  font-size: .75rem !important;
}

/* Expander */
[data-testid="stExpander"] {
  background: var(--glass) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r-sm) !important;
  backdrop-filter: blur(12px) !important;
}
[data-testid="stExpander"] summary {
  color: var(--text2) !important;
  font-family: var(--font-mono) !important;
  font-size: .8rem !important;
}

/* Alerts */
[data-testid="stInfo"] {
  background: rgba(110,231,247,.06) !important;
  border: 1px solid rgba(110,231,247,.2) !important;
  border-radius: var(--r-sm) !important;
  color: var(--text1) !important;
}
[data-testid="stInfo"] p,[data-testid="stInfo"] span,
[data-testid="stAlert"] p,[data-testid="stAlert"] span {
  color: var(--text1) !important;
}

/* Glass card */
.gcard {
  background: var(--glass);
  border: 1px solid var(--border);
  border-radius: var(--r);
  padding: 1.5rem;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  position: relative;
  overflow: hidden;
  transition: border-color .3s, box-shadow .3s, transform .3s;
}
.gcard:hover {
  border-color: rgba(110,231,247,.25);
  box-shadow: 0 8px 48px rgba(0,0,0,.5), 0 0 0 1px rgba(110,231,247,.06) inset;
  transform: translateY(-1px);
}
.gcard::before {
  content:'';
  position:absolute; top:0; left:0; right:0; height:1px;
  background: linear-gradient(90deg,transparent,var(--g1),var(--g2),transparent);
  opacity:.5;
}
.gcard::after {
  content:'';
  position:absolute; top:-1px; left:-1px;
  width:18px; height:18px;
  border-top:1.5px solid var(--g1);
  border-left:1.5px solid var(--g1);
  border-radius:var(--r) 0 0 0;
  opacity:.5;
  transition: opacity .3s;
}
.gcard:hover::after { opacity:1; }

.chip {
  display: inline-block;
  font-family: var(--font-mono);
  font-size: .6rem;
  font-weight: 500;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--g1);
  background: rgba(110,231,247,.08);
  border: 1px solid rgba(110,231,247,.2);
  border-radius: 20px;
  padding: 3px 10px;
  margin-bottom: 8px;
}
.gtext {
  background: linear-gradient(135deg, var(--g1) 0%, var(--g2) 50%, var(--g3) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.aurora-divider {
  border: none;
  border-top: 1px solid var(--border);
  margin: 2rem 0;
  position: relative;
}
.aurora-divider::after {
  content:'';
  position:absolute; top:-1px; left:50%; transform:translateX(-50%);
  width:60px; height:1px;
  background: linear-gradient(90deg,var(--g1),var(--g2));
  box-shadow: 0 0 10px var(--g1);
}
@keyframes fadeUp {
  from { opacity:0; transform:translateY(20px); }
  to   { opacity:1; transform:translateY(0); }
}
@keyframes auroraPulse {
  0%,100% { opacity:.6; }
  50%      { opacity:1; }
}
@keyframes shimmer {
  0%   { transform:translateX(-100%); }
  100% { transform:translateX(400%); }
}
@keyframes blinkCursor {
  0%,100% { opacity:1; }
  50%      { opacity:0; }
}
.fade-up { animation: fadeUp .5s ease forwards; }
@media (max-width: 640px) {
  .gcard { padding: 1.2rem 1rem; }
  [data-testid="stMetricValue"] > div { font-size:1.6rem!important; }
}
</style>
""")

# =========================================================================
#  SIDEBAR
# =========================================================================
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom:1.6rem;">
      <div style="font-family:'JetBrains Mono',monospace;font-size:.58rem;
          letter-spacing:3px;text-transform:uppercase;color:#334155;margin-bottom:8px;">
        System Intelligence</div>
      <div style="font-family:'Outfit',sans-serif;font-size:1.2rem;font-weight:700;
          line-height:1.25;background:linear-gradient(135deg,#6ee7f7,#a78bfa);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;
          background-clip:text;">
        How Was This<br>Built?</div>
    </div>
    <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.08),transparent);margin-bottom:1.4rem;"></div>
    """, unsafe_allow_html=True)

    items = [
        ("Build Time",        "30 minutes",               "#6ee7f7"),
        ("Hand-Written Code", "Zero lines",               "#34d399"),
        ("Architecture",      "Keyless / Decentralised",  "#a78bfa"),
        ("AI Engine",         "Gemini 2.5 Flash",         "#f472b6"),
        ("Orchestrated by",   "Alexandra Georgescu",      "#fbbf24"),
    ]
    for label, val, color in items:
        st.markdown(f"""
        <div style="margin-bottom:.85rem;padding:.75rem .9rem;
            background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);
            border-left:2px solid {color}33;border-radius:10px;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:.56rem;
              letter-spacing:1.5px;text-transform:uppercase;color:#334155;margin-bottom:2px;">{label}</div>
          <div style="font-size:.85rem;color:#f1f5f9;font-weight:500;">{val}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.08),transparent);margin:1rem 0;"></div>
    <div style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);
        border-radius:10px;padding:.9rem 1rem;font-family:'JetBrains Mono',monospace;">
      <div style="font-size:.56rem;letter-spacing:3px;text-transform:uppercase;
          color:#334155;margin-bottom:10px;">System Status</div>
      <div style="font-size:.7rem;line-height:2.1;color:#64748b;">
        PROTOCOL <span style="color:#1e293b;"> -- </span><span style="color:#f1f5f9;">AI-Native 2026</span><br>
        ENGINE   <span style="color:#1e293b;"> -- </span><span style="color:#f1f5f9;">Gemini 2.5 Flash</span><br>
        AUTH     <span style="color:#1e293b;"> -- </span><span style="color:#f1f5f9;">API Key (localStorage)</span><br>
        COST     <span style="color:#1e293b;"> -- </span><span style="color:#34d399;">Free tier</span><br>
        STATUS   <span style="color:#1e293b;"> -- </span>
          <span style="color:#34d399;">
            <span style="display:inline-block;width:6px;height:6px;
              background:#34d399;border-radius:50%;margin-right:4px;
              vertical-align:middle;box-shadow:0 0 8px #34d399;"></span>Operational</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================================
#  HERO HEADER
# =========================================================================
st.markdown("""
<div style="position:relative;overflow:hidden;border-radius:20px;margin-bottom:1.5rem;
  border:1px solid rgba(255,255,255,.08);padding:3rem 1.5rem 2.5rem;text-align:center;
  background:linear-gradient(160deg,#09090f 0%,#0f0f23 40%,#09090f 100%);">

  <div style="position:absolute;top:-80px;left:-60px;width:340px;height:340px;border-radius:50%;
    background:radial-gradient(circle,rgba(110,231,247,.12) 0%,transparent 70%);
    pointer-events:none;animation:auroraPulse 5s ease-in-out infinite;"></div>
  <div style="position:absolute;bottom:-80px;right:-60px;width:380px;height:380px;border-radius:50%;
    background:radial-gradient(circle,rgba(167,139,250,.1) 0%,transparent 70%);
    pointer-events:none;animation:auroraPulse 7s ease-in-out infinite;"></div>
  <div style="position:absolute;top:40%;left:50%;transform:translate(-50%,-50%);
    width:500px;height:200px;
    background:radial-gradient(ellipse,rgba(244,114,182,.06) 0%,transparent 70%);
    pointer-events:none;"></div>
  <div style="position:absolute;top:0;left:0;right:0;bottom:0;pointer-events:none;opacity:.4;
    background-image:linear-gradient(rgba(110,231,247,.04) 1px,transparent 1px),
                     linear-gradient(90deg,rgba(110,231,247,.04) 1px,transparent 1px);
    background-size:48px 48px;"></div>
  <div style="position:absolute;top:-1px;left:-1px;width:40px;height:40px;
    border-top:1.5px solid rgba(110,231,247,.6);border-left:1.5px solid rgba(110,231,247,.6);
    border-radius:20px 0 0 0;"></div>
  <div style="position:absolute;top:-1px;right:-1px;width:40px;height:40px;
    border-top:1.5px solid rgba(167,139,250,.5);border-right:1.5px solid rgba(167,139,250,.5);
    border-radius:0 20px 0 0;"></div>

  <div style="position:relative;font-family:'JetBrains Mono',monospace;font-size:.6rem;
    letter-spacing:5px;text-transform:uppercase;color:#1e293b;margin-bottom:.9rem;">
    + &nbsp; AI-NATIVE PROTOCOL &middot; 2026 &nbsp; +</div>

  <div style="position:relative;font-family:'Outfit',sans-serif;font-weight:900;
    font-size:clamp(2.4rem,7vw,5rem);line-height:1;letter-spacing:-2px;
    margin-bottom:.8rem;">
    <span style="background:linear-gradient(135deg,#6ee7f7 0%,#a78bfa 45%,#f472b6 80%);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;
      background-clip:text;">AI CAREER</span><br>
    <span style="background:linear-gradient(135deg,#f472b6 0%,#a78bfa 45%,#6ee7f7 100%);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;
      background-clip:text;">ARCHITECT</span>
  </div>

  <div style="position:relative;font-size:clamp(.85rem,2.5vw,1rem);color:#64748b;
    max-width:480px;margin:.8rem auto 1.6rem;line-height:1.6;">
    Transform your CV into a personalised 2026 AI-native<br>
    upskilling roadmap &middot; powered by Gemini 2.5 Flash
  </div>

  <div style="position:relative;display:flex;flex-wrap:wrap;justify-content:center;gap:.5rem;">
    <span style="font-family:'JetBrains Mono',monospace;font-size:.6rem;letter-spacing:1px;
      color:#6ee7f7;background:rgba(110,231,247,.08);border:1px solid rgba(110,231,247,.2);
      border-radius:20px;padding:4px 12px;">
      <span style="display:inline-block;width:5px;height:5px;background:#6ee7f7;border-radius:50%;
        margin-right:5px;vertical-align:middle;box-shadow:0 0 6px #6ee7f7;"></span>GEMINI 2.5 FLASH</span>
    <span style="font-family:'JetBrains Mono',monospace;font-size:.6rem;letter-spacing:1px;
      color:#a78bfa;background:rgba(167,139,250,.08);border:1px solid rgba(167,139,250,.2);
      border-radius:20px;padding:4px 12px;">YOUR FREE API KEY</span>
    <span style="font-family:'JetBrains Mono',monospace;font-size:.6rem;letter-spacing:1px;
      color:#f472b6;background:rgba(244,114,182,.08);border:1px solid rgba(244,114,182,.2);
      border-radius:20px;padding:4px 12px;">12-WEEK ROADMAP</span>
    <span style="font-family:'JetBrains Mono',monospace;font-size:.6rem;letter-spacing:1px;
      color:#34d399;background:rgba(52,211,153,.08);border:1px solid rgba(52,211,153,.2);
      border-radius:20px;padding:4px 12px;">MOBILE-READY</span>
  </div>
</div>
""", unsafe_allow_html=True)

# =========================================================================
#  TABS
# =========================================================================
tab1, tab2, tab3 = st.tabs(["+ Bio-Scan", "* Blueprint", "# ROI Oracle"])

# =========================================================================
#  TAB 1 -- BIO-SCAN
# =========================================================================
with tab1:
    col_main, col_side = st.columns([3, 1], gap="large")

    with col_main:
        st.markdown("""
        <div class="gcard" style="margin-bottom:1.2rem;">
          <div class="chip">Module 01 &middot; CV Ingestion</div>
          <div style="font-family:'Outfit',sans-serif;font-size:1.3rem;font-weight:700;
              color:#f8fafc;margin:4px 0 8px;">Upload Your Resume</div>
          <div style="font-size:.9rem;color:#64748b;line-height:1.7;">
            Drop your PDF for instant AI analysis.
            Text is extracted <strong style="color:#94a3b8;">in-session only</strong>
            &mdash; nothing is stored externally.
          </div>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Drop your PDF resume here, or click to browse",
            type=["pdf"],
            label_visibility="visible",
        )

        if uploaded_file is not None:
            if uploaded_file.name != st.session_state.cv_name:
                scan_ph = st.empty()
                scan_ph.markdown("""
                <div style="background:rgba(110,231,247,.04);border:1px solid rgba(110,231,247,.2);
                  border-radius:16px;padding:2.5rem;margin:1rem 0;text-align:center;
                  backdrop-filter:blur(16px);">
                  <div style="font-family:'JetBrains Mono',monospace;font-size:.62rem;
                    color:#334155;letter-spacing:3px;text-transform:uppercase;margin-bottom:12px;">
                    Initiating Bio-Scan</div>
                  <div style="font-family:'Outfit',sans-serif;font-size:1.8rem;font-weight:700;
                    background:linear-gradient(135deg,#6ee7f7,#a78bfa);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                    background-clip:text;letter-spacing:4px;">
                    Scanning...</div>
                  <div style="margin:18px auto 0;width:55%;height:2px;
                    background:rgba(255,255,255,.06);border-radius:2px;overflow:hidden;position:relative;">
                    <div style="position:absolute;top:0;left:0;bottom:0;width:35%;
                      background:linear-gradient(90deg,transparent,#6ee7f7,transparent);
                      animation:shimmer 1.5s ease-in-out infinite;"></div>
                  </div>
                  <div style="margin-top:12px;font-size:.8rem;color:#334155;">
                    Extracting text structure...</div>
                </div>
                """, unsafe_allow_html=True)

                try:
                    with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
                        pages = len(pdf.pages)
                        text  = "\n".join(p.extract_text() or "" for p in pdf.pages).strip()

                    st.session_state.cv_text  = text
                    st.session_state.cv_name  = uploaded_file.name
                    st.session_state.cv_pages = pages
                    st.session_state.cv_words = len(text.split())
                    time.sleep(0.8)
                    scan_ph.empty()
                except Exception as exc:
                    scan_ph.empty()
                    st.error(f"Scan failed: {exc}")

            if st.session_state.cv_name:
                st.markdown(f"""
                <div class="gcard fade-up" style="border-color:rgba(52,211,153,.3);
                  box-shadow:0 0 30px rgba(52,211,153,.06);margin:1rem 0;">
                  <div style="display:flex;align-items:center;gap:1.2rem;flex-wrap:wrap;">
                    <div style="width:46px;height:46px;border-radius:10px;flex-shrink:0;
                      background:rgba(52,211,153,.1);border:1px solid rgba(52,211,153,.3);
                      display:flex;align-items:center;justify-content:center;font-size:1.3rem;">+</div>
                    <div>
                      <div style="font-family:'JetBrains Mono',monospace;font-size:.58rem;
                          color:#334155;letter-spacing:2px;text-transform:uppercase;margin-bottom:3px;">
                        Bio-Scan Complete</div>
                      <div style="font-size:.95rem;color:#f8fafc;font-weight:600;margin-bottom:3px;">
                        {st.session_state.cv_name}</div>
                      <div style="font-size:.78rem;color:#64748b;">
                        {st.session_state.cv_words:,} words &middot; {st.session_state.cv_pages} page(s)</div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("View extracted text preview", expanded=False):
                    preview  = st.session_state.cv_text[:3000]
                    ellipsis = "..." if len(st.session_state.cv_text) > 3000 else ""
                    st.markdown(f"""
                    <pre style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);
                      border-radius:8px;padding:1rem;font-family:'JetBrains Mono',monospace;
                      font-size:.75rem;color:#64748b;line-height:1.8;
                      white-space:pre-wrap;word-break:break-word;
                      max-height:300px;overflow-y:auto;">{preview}{ellipsis}</pre>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.info("Head to the **Blueprint** tab -- your Gemini key will be requested once and saved forever.")
        else:
            st.markdown("""
            <div style="text-align:center;padding:3.5rem 2rem;margin:1rem 0;
              border:1.5px dashed rgba(255,255,255,.08);border-radius:16px;
              background:rgba(255,255,255,.02);">
              <div style="font-size:3rem;margin-bottom:14px;opacity:.15;">+</div>
              <div style="font-size:.95rem;color:#475569;font-weight:500;margin-bottom:5px;">
                No resume loaded yet</div>
              <div style="font-size:.82rem;color:#334155;">
                Drop a PDF above to begin your career analysis</div>
            </div>
            """, unsafe_allow_html=True)

    with col_side:
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace;font-size:.58rem;letter-spacing:2.5px;
            text-transform:uppercase;color:#334155;margin-bottom:1rem;">
          Analysis Scope</div>
        """, unsafe_allow_html=True)

        caps = [
            ("Skills Matrix",     "Technical & soft skills inventory",   "#6ee7f7"),
            ("Career Trajectory", "Role progression & seniority arc",    "#a78bfa"),
            ("Gap Analysis",      "Critical 2026 skill deficits",        "#f472b6"),
            ("Opportunity Map",   "Highest-ROI career transitions",      "#34d399"),
            ("AI-Readiness",      "AI-native fluency baseline score",    "#fbbf24"),
        ]
        for title, desc, color in caps:
            st.markdown(f"""
            <div style="margin-bottom:.65rem;padding:.85rem .9rem;
              background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);
              border-left:2px solid {color}44;border-radius:10px;">
              <div style="font-size:.78rem;font-weight:600;color:#f1f5f9;margin-bottom:2px;">
                {title}</div>
              <div style="font-size:.73rem;color:#475569;line-height:1.4;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# =========================================================================
#  TAB 2 -- THE BLUEPRINT  (Gemini API · key managed by Streamlit)
# =========================================================================
with tab2:
    import streamlit.components.v1 as _components

    has_cv       = bool(st.session_state.cv_text)
    cv_name_safe = st.session_state.cv_name.replace('"', "'")
    has_cv_js    = "true" if has_cv else "false"

    # Key file: prefer same-dir (local dev), fall back to /tmp (Community Cloud)
    _KEY_PATH_LOCAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".aca_gemini_key")
    _KEY_PATH_TMP   = os.path.join("/tmp", ".aca_gemini_key")
    _KEY_PATH       = _KEY_PATH_LOCAL if os.access(os.path.dirname(os.path.abspath(__file__)), os.W_OK) else _KEY_PATH_TMP

    # Load persisted key on first run.
    # Priority: 1) st.secrets (Community Cloud dashboard)  2) disk file  3) empty
    if "gemini_key" not in st.session_state:
        _loaded_key = ""
        # 1. st.secrets — set GEMINI_API_KEY in the Community Cloud Secrets panel
        try:
            _secret = st.secrets.get("GEMINI_API_KEY", "")
            if isinstance(_secret, str) and _secret.startswith("AIza"):
                _loaded_key = _secret
        except Exception:
            pass
        # 2. Disk file (local dev or same-container rerun)
        if not _loaded_key:
            for _kp in (_KEY_PATH_LOCAL, _KEY_PATH_TMP):
                if os.path.exists(_kp):
                    try:
                        _v = open(_kp, encoding="utf-8").read().strip()
                        if _v.startswith("AIza"):
                            _loaded_key = _v
                            break
                    except Exception:
                        pass
        st.session_state.gemini_key = _loaded_key

    SYS_PROMPT = (
        "You are an Elite AI Architect producing a personalised 12-week upskilling roadmap for 2026 AI-native roles.\n\n"

        "CALIBRATION PARAGRAPH (write this before any phase header):\n"
        "Rate each of these 6 dimensions from the CV evidence as BEGINNER / INTERMEDIATE / PRODUCTION:\n"
        "  LLM APIs | RAG/Retrieval | Agents/Tool-use | MCP | Evaluation | MLOps/Deployment\n"
        "Then name the 2 strongest CV achievements and the 2 sharpest gaps this roadmap will close.\n"
        "Phase names must be gap-specific to this person, never generic.\n\n"

        "LEVEL RULES (apply every matching rule, based only on CV evidence):\n"
        "- Production LLM calls in CV -> skip API setup/token basics -> teach model routing, prompt regression suites, LLM-as-judge\n"
        "- Production RAG in CV -> skip RAG intro/embedding basics -> teach ColBERT, GraphRAG, RAPTOR, RAGAS eval harnesses\n"
        "- Agents or pipelines in CV -> skip ReAct/LangChain intro -> teach LangGraph state machines, agent evals, guardrail design\n"
        "- MCP or Model Context Protocol in CV -> skip what-is-MCP -> teach MCP server design, tool schema engineering, multi-host coordination\n"
        "- Fine-tuning work in CV -> skip basics -> teach DPO/RLHF, model merging (SLERP/TIES), instruction dataset curation\n"
        "- CI/CD or prod deployment in CV -> skip Docker/GitHub Actions intro -> teach prompt regression CI, eval gate pipelines, canary LLM deploys\n"
        "- Eval dashboards (P/R/F1, confusion matrices) in CV -> skip metric definitions -> teach G-Eval, MT-Bench, hallucination detection\n\n"

        "BANNED for any candidate with 2 or more PRODUCTION-level dimensions:\n"
        "'Set up your API key' | 'What is a vector database' | LangChain quickstarts | Docker intro | basic embedding theory | 'Install Python'\n"
        "Replace every banned item with: production design patterns, arXiv papers, advanced repos, architecture decision records.\n\n"

        "FORMAT - 5 phases, each containing exactly:\n"
        "### Skills - specific tools, library versions, paper names, advanced patterns only\n"
        "### Daily Practice - day-by-day, grounded in the candidate's actual existing stack\n"
        "### Milestone Deliverable - extends their EXISTING projects; full tech stack, architecture, demo script, hiring-manager angle\n"
        "### Resources - 4-6 real URLs; papers/RFCs/advanced repos for PRODUCTION candidates, no beginner tutorials\n"
        "### ROI Impact - salary delta, role unlocked, market signal strength\n\n"
        "Close with ## 3 High-Impact Moves: next 48 hours, specific to this candidate's exact stack, each with URL or command.\n\n"
        "Tone: direct, tactical, zero filler. If it could apply to a different engineer, it is wrong - rewrite it."
    )

    # ── CV PRE-ASSESSMENT ─────────────────────────────────────────────────────
    # Scan the CV text for hard evidence and emit a structured signal block.
    # This is injected BEFORE the raw CV so the model can't miss it.
    def _cv_prescore(text: str) -> str:
        """Return a compact evidence table for the 6 calibration dimensions."""
        t = text.lower()

        def _hits(keywords):
            return sum(1 for k in keywords if k in t)

        dims = {
            "LLM APIs": {
                "keywords": [
                    "cortex llm", "openai", "anthropic", "gemini", "llm prompt",
                    "llm orchestration", "llm token", "prompt template", "prompt engineering",
                    "function calling", "chat completion", "generatecontent",
                    "llama", "mistral", "gpt", "claude",
                ],
                "thresholds": (1, 3),   # (intermediate, production)
            },
            "RAG/Retrieval": {
                "keywords": [
                    "rag", "chromadb", "vector", "retrieval", "embedding",
                    "cortex search", "similarity search", "faiss", "pinecone",
                    "weaviate", "semantic search", "networkx", "knowledge graph",
                ],
                "thresholds": (1, 3),
            },
            "Agents/Tool-use": {
                "keywords": [
                    "agent", "agentic", "tool use", "planning loop", "multi-agent",
                    "langchain", "langgraph", "crewai", "autogen", "n8n",
                    "orchestrat", "pipeline", "workflow", "normalization pipeline",
                    "classification model", "3-path matching",
                ],
                "thresholds": (2, 4),
            },
            "MCP": {
                "keywords": [
                    "model context protocol", "mcp", "mcp server", "tool schema",
                    "tool exposure", "tool discovery",
                ],
                "thresholds": (1, 2),
            },
            "Evaluation": {
                "keywords": [
                    "precision", "recall", "f1", "confusion matrix", "ragas",
                    "g-eval", "mt-bench", "hallucination", "eval", "evaluation",
                    "benchmark", "model registry", "anomaly threshold",
                    "hitl", "human-in-the-loop",
                ],
                "thresholds": (2, 5),
            },
            "MLOps/Deployment": {
                "keywords": [
                    "ci/cd", "github actions", "docker", "deployment", "pipeline",
                    "canary", "rollback", "monitoring", "prod", "production",
                    "snowflake model registry", "qa checklist", "qa methodology",
                    "stored procedure", "acid", "automated deploy",
                ],
                "thresholds": (2, 5),
            },
        }

        lines = ["=== AUTOMATED CV PRE-ASSESSMENT (generated from keyword evidence) ===",
                 "Use this as your starting point for the calibration paragraph.\n"]

        for dim, cfg in dims.items():
            n = _hits(cfg["keywords"])
            lo, hi = cfg["thresholds"]
            if n >= hi:
                level = "PRODUCTION"
            elif n >= lo:
                level = "INTERMEDIATE"
            else:
                level = "BEGINNER"
            # collect matching keywords for transparency
            matched = [k for k in cfg["keywords"] if k in t][:5]
            lines.append(f"  {dim}: {level}  (evidence: {', '.join(matched) if matched else 'none found'})")

        lines.append("\n=== END PRE-ASSESSMENT — RAW CV FOLLOWS ===\n")
        return "\n".join(lines)

    _cv_prescore_block = _cv_prescore(st.session_state.cv_text) if has_cv else ""
    # Prepend prescore to the CV text the model sees (trim total to ~7000 chars)
    _cv_with_prescore  = (_cv_prescore_block + st.session_state.cv_text)[:8000]
    cv_json            = json.dumps(_cv_with_prescore)
    # ─────────────────────────────────────────────────────────────────────────

    _BLUEPRINT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "blueprint.html")
    blueprint_html = open(_BLUEPRINT_PATH, encoding="utf-8").read()


    # --- KEY ENTRY SCREEN (no key saved yet) ---
    if not st.session_state.gemini_key:
        st.markdown("""
        <div class="gcard" style="max-width:520px;margin:1rem auto;">
          <div style="text-align:center;padding:1.2rem 0 1rem;">
            <div class="chip">Gemini 2.5 Flash &middot; Free Tier</div>
            <div style="font-family:'Outfit',sans-serif;font-weight:800;
                font-size:clamp(1.6rem,5vw,2.2rem);line-height:1.1;letter-spacing:-1px;margin-bottom:.6rem;">
              <span style="background:linear-gradient(135deg,#6ee7f7,#a78bfa);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                background-clip:text;">Your AI Key,</span><br>
              <span style="color:#f8fafc;">Your Intelligence</span>
            </div>
            <div style="font-size:.88rem;color:#64748b;max-width:360px;margin:.4rem auto;line-height:1.6;">
              One-time setup. Your key is saved locally and never sent to any server.
            </div>
          </div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:.58rem;letter-spacing:2px;
              text-transform:uppercase;color:#334155;margin-bottom:10px;">How to get your free key</div>
          <div style="margin-bottom:1.2rem;">
            <div style="display:flex;gap:10px;align-items:flex-start;padding:.5rem 0;border-bottom:1px solid rgba(255,255,255,.07);">
              <div style="width:20px;height:20px;border-radius:50%;flex-shrink:0;background:rgba(110,231,247,.1);
                  border:1px solid rgba(110,231,247,.25);font-family:'JetBrains Mono',monospace;
                  font-size:.62rem;font-weight:600;color:#6ee7f7;display:flex;align-items:center;justify-content:center;">1</div>
              <div style="font-size:.83rem;color:#64748b;line-height:1.5;">
                Go to <a href="https://aistudio.google.com/apikey" target="_blank"
                style="color:#6ee7f7;text-decoration:none;">aistudio.google.com/apikey</a> and sign in</div>
            </div>
            <div style="display:flex;gap:10px;align-items:flex-start;padding:.5rem 0;border-bottom:1px solid rgba(255,255,255,.07);">
              <div style="width:20px;height:20px;border-radius:50%;flex-shrink:0;background:rgba(110,231,247,.1);
                  border:1px solid rgba(110,231,247,.25);font-family:'JetBrains Mono',monospace;
                  font-size:.62rem;font-weight:600;color:#6ee7f7;display:flex;align-items:center;justify-content:center;">2</div>
              <div style="font-size:.83rem;color:#64748b;line-height:1.5;">
                Click <strong style="color:#f1f5f9;">Create API Key</strong> (free, no credit card)</div>
            </div>
            <div style="display:flex;gap:10px;align-items:flex-start;padding:.5rem 0;">
              <div style="width:20px;height:20px;border-radius:50%;flex-shrink:0;background:rgba(110,231,247,.1);
                  border:1px solid rgba(110,231,247,.25);font-family:'JetBrains Mono',monospace;
                  font-size:.62rem;font-weight:600;color:#6ee7f7;display:flex;align-items:center;justify-content:center;">3</div>
              <div style="font-size:.83rem;color:#64748b;line-height:1.5;">
                Paste it below &mdash; saved to disk, persists forever</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("key_entry_form", clear_on_submit=True):
            _key_input = st.text_input(
                "Gemini API Key",
                placeholder="AIza...  paste your Gemini API key here",
                type="password",
                label_visibility="collapsed",
            )
            _submitted = st.form_submit_button(
                "Save Key & Continue",
                use_container_width=True,
            )
            if _submitted:
                _key_val = _key_input.strip()
                if _key_val.startswith("AIza") and len(_key_val) > 20:
                    st.session_state.gemini_key = _key_val
                    try:
                        with open(_KEY_PATH, "w", encoding="utf-8") as _f:
                            _f.write(_key_val)
                    except Exception:
                        pass
                    st.rerun()
                else:
                    st.error("That doesn't look like a valid Gemini API key (should start with AIza...)")

    else:
        # --- KEY ACTIVE: show status bar + Change Key + component ---
        _key_masked = st.session_state.gemini_key[:8] + "..." + st.session_state.gemini_key[-4:]
        _col_status, _col_btn = st.columns([7, 2], gap="small")
        with _col_status:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:.65rem 1rem;
              background:rgba(52,211,153,.06);border:1px solid rgba(52,211,153,.18);
              border-radius:10px;height:100%;">
              <span style="width:7px;height:7px;border-radius:50%;background:#34d399;
                box-shadow:0 0 8px #34d399;flex-shrink:0;display:inline-block;"></span>
              <span style="font-family:'JetBrains Mono',monospace;font-size:.7rem;color:#34d399;">
                Gemini 2.5 Flash &middot; key active &middot;
                <span style="opacity:.6;">{_key_masked}</span></span>
            </div>
            """, unsafe_allow_html=True)
        with _col_btn:
            if st.button("Change Key", use_container_width=True, key="change_key_btn"):
                st.session_state.gemini_key = ""
                try:
                    if os.path.exists(_KEY_PATH):
                        os.remove(_KEY_PATH)
                except Exception:
                    pass
                st.rerun()

        # Inject key + CV data into component HTML, then render via srcdoc
        _key_js   = json.dumps(st.session_state.gemini_key)
        _sys_js   = json.dumps(SYS_PROMPT)
        _has_cv_b = "true" if has_cv else "false"

        _blueprint_final = blueprint_html.replace(
            "var GEMINI_API_KEY_PLACEHOLDER = '';",
            f"var GEMINI_API_KEY_PLACEHOLDER = {_key_js};",
        ).replace(
            "var CV_TEXT_PLACEHOLDER = '';",
            f"var CV_TEXT_PLACEHOLDER = {cv_json};",
        ).replace(
            "var HAS_CV_PLACEHOLDER = false;",
            f"var HAS_CV_PLACEHOLDER = {_has_cv_b};",
        ).replace(
            "var SYS_PROMPT_PLACEHOLDER = '';",
            f"var SYS_PROMPT_PLACEHOLDER = {_sys_js};",
        )
        _components.html(_blueprint_final, height=2400, scrolling=True)


with tab3:
    st.markdown("""
    <div class="gcard" style="margin:1rem 0 1.8rem;">
      <div class="chip">Module 03 &middot; Market Intelligence</div>
      <div style="font-family:'Outfit',sans-serif;font-size:1.3rem;font-weight:800;
          color:#f8fafc;margin:4px 0 6px;letter-spacing:-.3px;">ROI Oracle</div>
      <div style="font-size:.88rem;color:#64748b;line-height:1.65;max-width:560px;">
        Quantified career-impact projections for an AI-native transition,
        based on 2026 market signal aggregation.
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Design Latency",  "-50%",  "vs traditional")
    with c2: st.metric("Productivity",    "+9x",   "output per hour")
    with c3: st.metric("Salary Premium",  "+40%",  "AI-native roles")
    with c4: st.metric("Time to Market",  "-70%",  "prototype to deploy")

    st.markdown("<div class='aurora-divider' style='margin:2rem 0;'></div>",
                unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:.6rem;letter-spacing:2.5px;
        text-transform:uppercase;color:#334155;margin-bottom:1.4rem;">
      Skill-ROI Ranking &middot; 2026 Market</div>
    """, unsafe_allow_html=True)

    skills = [
        ("Context Engineering",      95, "#6ee7f7", "#22d3ee",
         "Prompt architecture &middot; RAG pipelines &middot; cognitive system design"),
        ("Agentic Workflows",         90, "#a78bfa", "#8b5cf6",
         "Multi-agent orchestration &middot; tool use &middot; planning loops"),
        ("Model Context Protocol",    85, "#6ee7f7", "#22d3ee",
         "MCP server design &middot; tool exposure &middot; AI-native APIs"),
        ("AI-Native Prototyping",     78, "#f472b6", "#ec4899",
         "0 to 1 with Cursor, Claude, Copilot, v0"),
        ("Data / ML Engineering",     60, "#fbbf24", "#f59e0b",
         "Still relevant but rapidly abstracted by AI layers"),
        ("Traditional Coding",        32, "#f87171", "#ef4444",
         "Commoditising fast -- value is now in architecture, not syntax"),
    ]

    for name, score, color_hi, color_mid, desc in skills:
        st.markdown(f"""
        <div style="margin-bottom:1.5rem;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:7px;">
            <span style="font-size:.9rem;font-weight:500;color:#f1f5f9;">{name}</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:.78rem;
                color:{color_hi};font-weight:600;">{score}/100</span>
          </div>
          <div style="width:100%;height:5px;background:rgba(255,255,255,.05);border-radius:3px;
              overflow:hidden;margin-bottom:5px;">
            <div style="height:100%;width:{score}%;border-radius:3px;
                background:linear-gradient(90deg,{color_mid},{color_hi});
                box-shadow:0 0 10px {color_hi}55;"></div>
          </div>
          <div style="font-size:.73rem;color:#334155;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='aurora-divider' style='margin:1.5rem 0 2rem;'></div>",
                unsafe_allow_html=True)

    col_l, col_r = st.columns(2, gap="large")

    with col_l:
        st.markdown("""
        <div class="gcard">
          <div class="chip" style="color:#34d399;background:rgba(52,211,153,.08);
              border-color:rgba(52,211,153,.2);">Market Intelligence &middot; 2026</div>
          <div style="font-size:.88rem;color:#64748b;line-height:2.3;">
            <span style="color:#34d399;font-weight:700;">73%</span>
            of design roles now require AI fluency<br>
            <span style="color:#34d399;font-weight:700;">+340%</span>
            YoY growth in Context Engineering jobs<br>
            <span style="color:#34d399;font-weight:700;">10x</span>
            salary premium for MCP-fluent engineers<br>
            <span style="color:#34d399;font-weight:700;">$240K</span>
            avg comp for AI-native PMs in San Francisco<br>
            <span style="color:#f87171;font-weight:700;">-15%</span>
            real wage for traditional devs vs 2024
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        st.markdown("""
        <div class="gcard">
          <div class="chip" style="color:#a78bfa;background:rgba(167,139,250,.08);
              border-color:rgba(167,139,250,.2);">12-Week Trajectory</div>
          <div style="font-size:.88rem;color:#64748b;line-height:2.3;">
            <span style="color:#6ee7f7;font-family:'JetBrains Mono',monospace;font-size:.68rem;">
              WK 01-02</span>&nbsp; Mindset shift + AI toolchain setup<br>
            <span style="color:#6ee7f7;font-family:'JetBrains Mono',monospace;font-size:.68rem;">
              WK 03-05</span>&nbsp; First agentic project shipped<br>
            <span style="color:#6ee7f7;font-family:'JetBrains Mono',monospace;font-size:.68rem;">
              WK 06-08</span>&nbsp; Public portfolio live<br>
            <span style="color:#6ee7f7;font-family:'JetBrains Mono',monospace;font-size:.68rem;">
              WK 09-11</span>&nbsp; Speaking, consulting, inbound<br>
            <span style="color:#6ee7f7;font-family:'JetBrains Mono',monospace;font-size:.68rem;">
              WK 12&nbsp;&nbsp;&nbsp;</span>&nbsp; New role or level-up confirmed
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="position:relative;overflow:hidden;text-align:center;
        padding:3.5rem 1.5rem;margin-top:2rem;border-radius:20px;
        background:linear-gradient(160deg,#09090f 0%,#0f0f23 50%,#09090f 100%);
        border:1px solid rgba(255,255,255,.07);">
      <div style="position:absolute;top:0;left:0;right:0;bottom:0;pointer-events:none;
        background-image:linear-gradient(rgba(110,231,247,.03) 1px,transparent 1px),
                         linear-gradient(90deg,rgba(110,231,247,.03) 1px,transparent 1px);
        background-size:36px 36px;"></div>
      <div style="position:absolute;top:0;left:0;right:0;height:1px;
        background:linear-gradient(90deg,transparent,#6ee7f7,#a78bfa,#f472b6,transparent);
        opacity:.5;"></div>
      <div style="position:absolute;top:-1px;left:-1px;width:28px;height:28px;
        border-top:1.5px solid rgba(110,231,247,.6);border-left:1.5px solid rgba(110,231,247,.6);
        border-radius:20px 0 0 0;"></div>
      <div style="position:absolute;bottom:-1px;right:-1px;width:28px;height:28px;
        border-bottom:1.5px solid rgba(244,114,182,.4);border-right:1.5px solid rgba(244,114,182,.4);
        border-radius:0 0 20px 0;"></div>
      <div style="position:relative;">
        <div style="font-family:'JetBrains Mono',monospace;font-size:.6rem;letter-spacing:4px;
            text-transform:uppercase;color:#1e293b;margin-bottom:1rem;">
          + &nbsp; Intelligence Statement &nbsp; +</div>
        <div style="font-family:'Outfit',sans-serif;font-size:clamp(1.2rem,3.5vw,1.8rem);
            font-weight:800;line-height:1.35;margin-bottom:.8rem;
            background:linear-gradient(135deg,#6ee7f7,#a78bfa,#f472b6);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
          The gap between AI-native<br>and traditional professionals
        </div>
        <div style="font-size:.98rem;color:#475569;font-style:italic;">
          compounds every week you wait.</div>
        <div style="margin-top:1.4rem;font-family:'JetBrains Mono',monospace;
            font-size:.6rem;color:#1e293b;letter-spacing:3px;">
          AI Career Architect &middot; 2026 &middot; Built without writing a single line of code
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
