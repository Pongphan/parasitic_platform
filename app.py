import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Parasitic Platform",
    page_icon="🧫",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------- Expert UI (CSS) --------------------
st.markdown(
    """
<style>
:root{
  --bg0:#0F172A;
  --bg1:#0F172A;
  --card:#1E293B;
  --card2:#334155;
  --txt:#ffffff;
  --muted:#CBD5E1;
  --muted2:#94A3B8;
  --stroke:rgba(255,255,255,.2);
  --stroke2:rgba(255,255,255,.12);
  --glow1:rgba(56,189,248,.08);
  --glow2:rgba(34,211,238,.06);
}

.stApp {
  background:
    radial-gradient(1200px 600px at 20% 10%, rgba(110,231,255,.2), transparent 60%),
    radial-gradient(900px 500px at 85% 15%, rgba(57, 62, 155, 0.2), transparent 80%),
    radial-gradient(800px 600px at 30% 85%, rgba(26, 82, 187, 0.2), transparent 60%),
    linear-gradient(180deg, var(--bg0), var(--bg1));
  color: var(--txt);
}


/* Layout tuning */
.block-container { padding-top: 1.0rem !important; padding-bottom: 2.1rem !important; max-width: 1200px; }

/* Hide menu/footer (optional) */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* Hero */
.hero {
  border: 1px solid var(--stroke);
  border-radius: 22px;
  padding: 22px 22px 18px 22px;
  background: linear-gradient(180deg, rgba(73, 190, 249, 0.02), rgba(73, 190, 249, 0.02));
  box-shadow: 0 10px 36px rgba(0,0,0,.35);
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
}
.hero:before{
  content:"";
  position:absolute;
  inset:-2px;
  background:
    radial-gradient(700px 220px at 20% 0%, rgba(110,231,255,.20), transparent 55%),
    radial-gradient(600px 240px at 80% 0%, rgba(57, 62, 155, 0.126), transparent 55%);
  filter: blur(16px);
  opacity:.55;
  pointer-events:none;
}
.hero h1{
  font-size: 2.75rem;
  line-height: 1.12;
  margin: 0;
  font-weight: 800;
  letter-spacing: .2px;
}
.hero p{
  margin: .55rem 0 0 0;
  color: var(--muted);
  font-size: 1.02rem;
}

/* Section label */
.section-label{
  margin-top: 1.15rem;
  margin-bottom: .55rem;
  color: var(--muted2);
  font-size: .92rem;
  letter-spacing: .14em;
  text-transform: uppercase;
}

[data-testid="stMetricLabel"] p, .section-label, .small-muted {
    color: #E2E8F0 !important;
}

[data-testid="stMetricValue"] div, .card-title, .hero h1 {
    color: #FFFFFF !important;
    text-shadow: 0px 2px 4px rgba(0,0,0,0.3); /* เพิ่มเงาหลังตัวอักษรให้ดูคมขึ้น */
}

[data-testid="stPageLink-NavLink"] p {
    color: #FFFFFF !important; /* บังคับให้เป็นสีขาวสว่าง */
    font-weight: 600 !important; /* เพิ่มความหนาของตัวอักษร */
    font-size: 1rem !important;  /* ปรับขนาดให้พอดี */
}


[data-testid="stPageLink-NavLink"] {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid var(--stroke2) !important;
    border-radius: 12px !important;
    transition: all 0.2s ease;
}

[data-testid="stPageLink-NavLink"]:hover {
    background-color: rgba(255, 255, 255, 0.1) !important;
    border-color: #58C4FF !important;
}

.pill {
    color: #FFFFFF !important;
    background: rgba(255,255,255,0.15) !important;
}

/* Card grid */
.card-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 14px;
}

.card-link{
  grid-column: span 6;
  text-decoration: none !important;
  color: inherit !important;
}

.card{
  height: 168px;
  border-radius: 20px;
  border: 1px solid var(--stroke);
  background:
    radial-gradient(900px 240px at 10% 20%, rgba(110,231,255,.25), transparent 55%),
    radial-gradient(700px 220px at 90% 0%, rgba(166,255,203,.20), transparent 55%),
    linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.02));
  box-shadow: 0 10px 30px rgba(0,0,0,.35);
  padding: 16px 16px 14px 16px;
  position: relative;
  overflow: hidden;
  transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease;
}

.card:after{
  content:"";
  position:absolute;
  top:-60%;
  left:-30%;
  width: 90%;
  height: 220%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,.10), transparent);
  transform: rotate(18deg);
  opacity: 0;
  transition: opacity .18s ease;
  pointer-events:none;
}

.card:hover{
  transform: translateY(-3px);
  border-color: var(--stroke2);
  box-shadow: 0 16px 42px rgba(0,0,0,.45);
}
.card:hover:after{ opacity: .55; }

.card-top{
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
  gap: 12px;
}
.icon-pill{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  width: 44px;
  height: 44px;
  border-radius: 14px;
  border: 1px solid var(--stroke);
  background: linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.02));
  box-shadow: 0 10px 26px rgba(0,0,0,.22);
  font-size: 22px;
}
.card-title{
  font-size: 1.15rem;
  font-weight: 780;
  margin: 0;
  letter-spacing: .2px;
}
.card-desc{
  margin: .45rem 0 .7rem 0;
  color: var(--muted);
  font-size: .96rem;
  line-height: 1.35;
}
.pills{
  display:flex;
  flex-wrap:wrap;
  gap: 8px;
}
.pill{
  color: #FFFFFF !important;
  font-size: .78rem;
  color: rgba(234,241,255,.82);
  border: 1px solid var(--stroke2) !important;
  background: rgba(255,255,255,.08);
  padding: 6px 10px;
  border-radius: 999px;
  letter-spacing: .2px;
}

[data-testid="stMetricLabel"] p {
    color: var(--muted) !important; /* ใช้สีเทาสว่างที่เราตั้งไว้ */
    font-size: 0.95rem !important;
}
[data-testid="stMetricValue"] {
    color: #FFFFFF !important; /* บังคับให้ตัวเลขเป็นสีขาวบริสุทธิ์ */
    font-weight: 700 !important;
}

[data-testid="stCheckbox"] label p {
    color: #FFFFFF !important; /* บังคับให้ข้อความข้าง Checkbox เป็นสีขาว */
    font-weight: 500 !important;
}


.st-emotion-cache-16idsys p, .st-emotion-cache-zq5wms {
    color: var(--muted) !important;
}


.section-label {
    color: #58C4FF !important; /* ใช้สีฟ้าสว่างนำสายตา */
    font-weight: 700 !important;
    text-shadow: 0px 1px 2px rgba(0,0,0,0.5);
}

div.stButton > button {
    color: #FF3131 !important;     /* สีตัวอักษรแดงสว่าง */
    background-color: rgba(255, 49, 49, 0.1) !important; /* พื้นหลังแดงจางๆ */
    border: 1px solid #FF3131 !important; /* ขอบแดง */
    font-weight: 700 !important;   /* ตัวหนา */
    border-radius: 12px !important;
}

/* เอฟเฟกต์ตอนเอาเมาส์ไปชี้ (Hover) */
div.stButton > button:hover {
    background-color: #FF3131 !important; /* พื้นหลังแดงเข้ม */
    color: white !important;               /* ตัวอักษรเปลี่ยนเป็นสีขาว */
}

/* Mini panels */
.panel {
  border: 1px solid var(--stroke);
  border-radius: 18px;
  padding: 14px 14px 10px 14px;
  background: rgba(255,255,255,.02);
  box-shadow: 0 10px 26px rgba(0,0,0,.25);
}
.panel h3{
  margin: 0 0 10px 0;
  font-size: 1.06rem;
  font-weight: 760;
}
.small-muted{ color: var(--muted2); font-size: .9rem; }

/* Responsive */
@media (max-width: 900px){
  .card-link{ grid-column: span 12; }
  .card{ height: auto; }
}
</style>
""",
    unsafe_allow_html=True,
)

# -------------------- Data model for modules --------------------
modules = [
    {
        "route": "Human_Parasite",
        "icon": "🧬",
        "title": "Human Parasite",
        "desc": "Curated parasite knowledge space (taxonomy, life cycles, diagnostics).",
        "pills": ["Atlas", "Morphology", "Lifecycle", "Diagnostics"],
        "tags": ["knowledge", "atlas", "diagnostics"],
    },
    {
        "route": "Parasitology_Research",
        "icon": "📚",
        "title": "Parasitology Research",
        "desc": "Research workspace for protocols, datasets, and evidence synthesis.",
        "pills": ["Methods", "Data", "Meta-analysis", "Reporting"],
        "tags": ["research", "methods", "evidence"],
    },
    {
        "route": "ParD_-_Parasite_Detection",
        "icon": "🧠",
        "title": "ParD - Parasite Detection",
        "desc": "Frame microscopy objects, compare model scores, and export traceable results.",
        "pills": ["ROI", "Classification", "Ensemble", "Reports"],
        "tags": ["vision", "ai", "microscopy"],
    },
    {
        "route": "About_Project",
        "icon": "ℹ️",
        "title": "About Project",
        "desc": "Project overview, roadmap, team, and citations/resources.",
        "pills": ["Roadmap", "Credits", "Citations", "Contact"],
        "tags": ["about", "roadmap", "docs"],
    },
]

def nav_card(route: str, icon: str, title: str, desc: str, pills: list[str]) -> str:
    pills_html = "".join([f'<span class="pill">{p}</span>' for p in pills])
    # Same-tab navigation: use href without target=_blank (Streamlit will route)
    return f"""
<a class="card-link" href="/{route}" target="_self">
  <div class="card">
    <div class="card-top">
      <div>
        <div class="card-title">{title}</div>
        <div class="card-desc">{desc}</div>
        <div class="pills">{pills_html}</div>
      </div>
      <div class="icon-pill">{icon}</div>
    </div>
  </div>
</a>
"""


# -------------------- Hero --------------------
st.markdown(
    """
<div class="hero">
  <h1>🧫 Parasitic Platform</h1>
  <p>
    The Definitive Resource for Human Parasitology — Atlas, Research, and AI-powered Microscopy.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

# -------------------- Utility bar: Search + Actions --------------------
st.markdown('<div class="util">', unsafe_allow_html=True)
u1, u2, u3 = st.columns([2.2, 1.1, 1.1], gap="small")
with u1:
    q = st.text_input("Search modules", placeholder="Type keywords: vision, diagnostics, roadmap…", label_visibility="collapsed")
with u2:
    st.selectbox("Mode", ["Explore", "Research", "Lab Ops"], index=0, label_visibility="collapsed")
with u3:
    st.button("Refresh", width="stretch")
st.markdown("</div>", unsafe_allow_html=True)

# -------------------- KPI Row (metrics) --------------------
k1, k2, k3, k4 = st.columns(4, gap="small")
k1.metric("Knowledge modules", "4", "+0")
k2.metric("Workspaces", "3", "+0")
k3.metric("Pipelines", "0", "+0")
k4.metric("Last update", datetime.now().strftime("%Y-%m-%d"), "")

# -------------------- Navigation Cards (filterable) --------------------
st.markdown('<div class="section-label">Navigation</div>', unsafe_allow_html=True)

query = (q or "").strip().lower()
filtered = []
for m in modules:
    hay = " ".join([m["title"], m["desc"], " ".join(m["pills"]), " ".join(m["tags"])]).lower()
    if (not query) or (query in hay):
        filtered.append(m)

cards_html = "\n".join([nav_card(m["route"], m["icon"], m["title"], m["desc"], m["pills"]) for m in filtered])

if not filtered:
    st.info("No modules match your search. Try: “vision”, “diagnostics”, “roadmap”.")
else:
    st.markdown('<div class="card-grid">' + cards_html + "</div>", unsafe_allow_html=True)

# -------------------- Ops + Resources panels --------------------
st.markdown('<div class="section-label">Operations & resources</div>', unsafe_allow_html=True)
left, right = st.columns([1.35, 1], gap="small")

with left:
    st.markdown(
        """
<div class="panel">
  <h3>📣 Announcements</h3>
  <div class="small-muted">
    We are pleased to share the latest updates, activities, and important information on this platform. Please check this section regularly for new features, upcoming events, and official notices.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.write("")
    st.markdown(
        """
<div class="panel">
  <h3>🧪 Workflow checklist</h3>
  <div class="small-muted">
    A workflow checklist helps your team stay organized, consistent, and efficient from start to finish. It breaks a process into clear, actionable steps so nothing important is missed.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        """
<div class="panel">
  <h3>📌 Resources</h3>
  <div class="small-muted"> SOPs and Citations.</div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.write("• SOP: Sample prep (coming soon)")
    st.write("• SOP: Microscopy QC (coming soon)")
    st.write("• Citation library (coming soon)")

    st.write("")
    st.markdown(
        """
<div class="panel">
  <h3>🧭 Support</h3>
  <div class="small-muted">FAQ / help & guidance (placeholders).</div>
</div>
""",
        unsafe_allow_html=True,
    )
    with st.expander("How do I navigate?"):
        st.write("Use the large cards or the Quick Links row. Navigation stays in the same tab.")

# -------------------- Footer --------------------
st.markdown(
    "<div style='margin-top:18px; color:rgba(234,241,255,.45); font-size:.86rem;'>"
    "© Parasitic Platform • Intelligent Platform for Parasitic Diseases 2026 • Penchom Janwan"
    "</div>",
    unsafe_allow_html=True,
)
