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
  --bg0:#070A12;
  --bg1:#0A1020;
  --card:#0B1326;
  --card2:#0C1730;
  --txt:#EAF1FF;
  --muted:rgba(234,241,255,.72);
  --muted2:rgba(234,241,255,.55);
  --stroke:rgba(234,241,255,.10);
  --stroke2:rgba(234,241,255,.16);
  --glow1:rgba(110,231,255,.20);
  --glow2:rgba(166,255,203,.18);
}

.stApp {
  background:
    radial-gradient(1200px 600px at 20% 10%, rgba(110,231,255,.08), transparent 55%),
    radial-gradient(900px 500px at 85% 15%, rgba(166,255,203,.06), transparent 55%),
    radial-gradient(800px 600px at 30% 85%, rgba(173,110,255,.05), transparent 60%),
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
  background: linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.02));
  box-shadow: 0 10px 36px rgba(0,0,0,.35);
  position: relative;
  overflow: hidden;
}
.hero:before{
  content:"";
  position:absolute;
  inset:-2px;
  background:
    radial-gradient(700px 220px at 20% 0%, rgba(110,231,255,.20), transparent 55%),
    radial-gradient(600px 240px at 80% 0%, rgba(166,255,203,.16), transparent 55%);
  filter: blur(16px);
  opacity:.55;
  pointer-events:none;
}
.hero h1{
  font-size: 2.15rem;
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

/* Utility panel */
.util {
  margin-top: 14px;
  border: 1px solid var(--stroke);
  border-radius: 18px;
  padding: 12px 14px;
  background: rgba(255,255,255,.02);
  box-shadow: 0 10px 26px rgba(0,0,0,.25);
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
    radial-gradient(900px 240px at 10% 0%, rgba(110,231,255,.08), transparent 55%),
    radial-gradient(700px 220px at 90% 0%, rgba(166,255,203,.06), transparent 55%),
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
  font-size: .78rem;
  color: rgba(234,241,255,.82);
  border: 1px solid var(--stroke);
  background: rgba(255,255,255,.03);
  padding: 6px 10px;
  border-radius: 999px;
  letter-spacing: .2px;
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
        "route": "Parasitic_Vision",
        "icon": "🧠",
        "title": "Parasitic Vision",
        "desc": "Computer vision zone for microscopy detection, annotation, and QA.",
        "pills": ["Detection", "Annotation", "QC", "Deployment"],
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
<a class="card-link" href="{route}">
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
    A research-grade hub for <b>human parasitology</b>, <b>digital diagnosis</b>, and <b>AI-assisted microscopy</b>.
    Built for structured workflows: knowledge → research → vision → reporting.
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
    st.button("Refresh", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# -------------------- KPI Row (metrics) --------------------
k1, k2, k3, k4 = st.columns(4, gap="small")
k1.metric("Knowledge modules", "4", "+0")
k2.metric("Workspaces", "3", "+0")
k3.metric("Pipelines", "0", "+0")
k4.metric("Last update", datetime.now().strftime("%Y-%m-%d"), "")

# -------------------- Quick Links (official Streamlit navigation) --------------------
# This is complementary: keeps things robust even if HTML routing changes.
st.markdown('<div class="section-label">Quick links</div>', unsafe_allow_html=True)
ql1, ql2, ql3, ql4 = st.columns(4, gap="small")
with ql1:
    st.page_link("pages/1_Human_Parasite.py", label="Human Parasite", icon="🧬")
with ql2:
    st.page_link("pages/2_Parasitology_Research.py", label="Parasitology Research", icon="📚")
with ql3:
    st.page_link("pages/3_Parasitic_Vision.py", label="Parasitic Vision", icon="🧠")
with ql4:
    st.page_link("pages/4_About_Project.py", label="About Project", icon="ℹ️")

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
    This area is ideal for: release notes, dataset updates, model evaluation milestones, or lab alerts.
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
  <div class="small-muted">Use this to guide your end-to-end workflow (placeholders by default).</div>
</div>
""",
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3, gap="small")
    c1.checkbox("Data intake", value=False)
    c2.checkbox("Annotation ready", value=False)
    c3.checkbox("Model run", value=False)

with right:
    st.markdown(
        """
<div class="panel">
  <h3>📌 Resources</h3>
  <div class="small-muted">Pin important protocols / SOPs / citations (placeholders).</div>
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
    with st.expander("How do I add new pages?"):
        st.write("Create a new Python file inside `/pages/` and add a new card entry in `modules`.")

# -------------------- Footer --------------------
st.markdown(
    "<div style='margin-top:18px; color:rgba(234,241,255,.45); font-size:.86rem;'>"
    "© Parasitic Platform • Streamlit multipage • Landing UI components ready for expansion"
    "</div>",
    unsafe_allow_html=True,
)
