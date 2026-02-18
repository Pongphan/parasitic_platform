# pages/4_About_Project.py
import streamlit as st
from dataclasses import dataclass
from typing import List, Dict

st.set_page_config(page_title="About Project", page_icon="ℹ️", layout="wide")

# ==================== THEME (same as app.py) ====================
st.markdown(
    """
<style>
:root{
  --bg0:#1E293B;
  --bg1:#1E293B;
  --txt:#FFFFFF;
  --muted:rgba(234,241,255,.72);
  --muted2:rgba(234,241,255,.55);
  --stroke:rgba(234,241,255,.10);
  --stroke2:rgba(234,241,255,.16);
}


.stApp {
  background:
    radial-gradient(1200px 600px at 20% 10%, rgba(110,231,255,.08), transparent 55%),
    radial-gradient(900px 500px at 85% 15%, rgba(57, 62, 155, 0.126), transparent 55%),
    radial-gradient(800px 600px at 30% 85%, rgba(173,110,255,.05), transparent 60%),
    linear-gradient(180deg, var(--bg0), var(--bg1));
  color: var(--txt);
}
.block-container { padding-top: 1.0rem !important; padding-bottom: 2.0rem !important; max-width: 1250px; }

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

.hero {
  border: 1px solid var(--stroke);
    border-radius: 22px;
      padding: 18px 20px 14px 20px;
        background: linear-gradient(180deg, rgba(73, 190, 249, 0.02), rgba(73, 190, 249, 0.02));
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
    radial-gradient(600px 240px at 80% 0%, rgba(57, 62, 155, 0.126), transparent 55%);
  filter: blur(16px);
  opacity:.55;
  pointer-events:none;
}

.hero h1{
  font-size: 1.9rem;
  line-height: 1.12;
  margin: 0;
  font-weight: 820;
  letter-spacing: .2px;
}

.hero p{
  margin: .55rem 0 0 0;
  color: #F1F5F9 !important;
  font-size: 1.0rem;
}

.section-label{
  margin-top: 1.05rem;
  margin-bottom: .55rem;
  color: #58C4FF !important;
  font-size: .92rem;
  letter-spacing: .14em;
  text-transform: uppercase;
}

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
  font-weight: 780;
}
.small-muted{ color: var(--muted2); font-size: .9rem; }

.kpi {
  border: 1px solid var(--stroke);
  border-radius: 18px;
  padding: 12px 14px;
  background: rgba(255,255,255,.02);
  box-shadow: 0 10px 26px rgba(0,0,0,.25);
}

.badge{
  display:inline-block;
  font-size:.78rem;
  color: rgba(234,241,255,.82);
  border: 1px solid var(--stroke);
  background: rgba(255,255,255,.03);
  padding: 6px 10px;
  border-radius: 999px;
  letter-spacing: .2px;
  margin-right: 6px;
  margin-bottom: 6px;
}

.hr { height:1px; background: rgba(234,241,255,.08); margin: 10px 0 12px 0; }

.note {
  border-left: 3px solid rgba(110,231,255,.45);
  padding: 10px 12px;
  background: rgba(255,255,255,.02);
  border-radius: 14px;
  color: rgba(234,241,255,.82);
}

.warn {
  border-left: 3px solid rgba(255,170,80,.55);
  padding: 10px 12px;
  background: rgba(255,255,255,.02);
  border-radius: 14px;
  color: rgba(234,241,255,.82);
}

.table-wrap {
  border: 1px solid rgba(234,241,255,.10);
  border-radius: 16px;
  padding: 10px 10px;
  background: rgba(255,255,255,.02);
}

/* ปรับชื่อ Metric (เช่น Knowledge modules) */
[data-testid="stMetricLabel"] p {
    color: #CBD5E1 !important; /* สีเทาสว่าง */
    font-size: 1rem !important;
}

/* ปรับตัวเลข Metric (เช่น 4, 3, 0) */
[data-testid="stMetricValue"] div {
    color: #FFFFFF !important; /* สีขาวบริสุทธิ์ */
    font-weight: 800 !important;
}

[data-testid="stCheckbox"] label p {
    color: #94A3B8 !important; /* บังคับให้ข้อความข้าง Checkbox เป็นสีขาว */
    font-weight: 500 !important;
}

/* เจาะจงที่ส่วนหัวข้อใหญ่ใน Sidebar (Knowledge Controls) */
[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3,
div[data-testid="stVerticalBlock"] > div > div > div > span {
    color: #1E293B !important; /* สีน้ำเงิน Slate เข้ม ชัดเจนกว่าสีดำสนิท */
    font-weight: 850 !important; /* เพิ่มความหนาพิเศษ */
    font-size: 1.25rem !important; /* ขยายขนาดเล็กน้อยให้เด่น */
    opacity: 1 !important;
}

/* ปรับตัวหนังสือรายการเมนู (เช่น Human Parasite, Parasitology Research) */
[data-testid="stSidebarNav"] span {
    color: #0F172A !important;
    font-weight: 500 !important;
}

/* ปรับตัวหนังสือใน Sidebar ที่มักจะจาง (เช่น Parasite group) */
[data-testid="stSidebar"] p {
    color: #0F172A !important; /* สีขาวนวลที่เข้มขึ้นเล็กน้อย */
    font-weight: 600 !important;
}

/* ปรับสีพื้นหลังของ Sidebar ให้มืดลงเล็กน้อยเพื่อให้ตัวหนังสือเด้งออกมา */
[data-testid="stSidebar"] {
    background-color: #E2E8F0 !important;
}

span, p, small, .small-muted {
    color: #F8FAFC !important; /* ขาวนวลสว่างเกือบ 100% */
    opacity: 1 !important;      /* ปิดโหมดโปร่งแสงทิ้งให้หมด */
    font-weight: 500 !important;
}


.mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
</style>
""",
    unsafe_allow_html=True,
)

# ==================== HERO ====================
st.markdown(
    """
<div class="hero">
  <h1>ℹ️ About Project</h1>
  <p>
    “Parasitic Platform” is a modular digital ecosystem for parasitology education, research, and AI-assisted microscopy —
    designed for real-world lab workflows and research-grade reproducibility.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

# ==================== High-level Summary ====================
st.markdown('<div class="section-label">Project at a glance</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4, gap="small")
with c1:
    st.markdown('<div class="kpi">', unsafe_allow_html=True)
    st.metric("Core pillars", "4", "")
    st.markdown("</div>", unsafe_allow_html=True)
with c2:
    st.markdown('<div class="kpi">', unsafe_allow_html=True)
    st.metric("Primary users", "Students • Lab staff • Researchers", "")
    st.markdown("</div>", unsafe_allow_html=True)
with c3:
    st.markdown('<div class="kpi">', unsafe_allow_html=True)
    st.metric("Focus", "Parasites • Diagnosis • AI", "")
    st.markdown("</div>", unsafe_allow_html=True)
with c4:
    st.markdown('<div class="kpi">', unsafe_allow_html=True)
    st.metric("Delivery", "Streamlit • Modular pages", "")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
<div class="note">
<b>Design philosophy:</b> Provide a single “workspace” that connects <b>knowledge</b> (human parasite content),
<b>research planning</b>, and <b>AI inference</b> into a cohesive, auditable workflow.
</div>
""",
    unsafe_allow_html=True,
)

# ==================== Tabs ====================
tab_vision, tab_scope, tab_arch, tab_quality, tab_roadmap, tab_faq = st.tabs(
    ["Vision", "Scope & Modules", "Architecture", "Quality & Governance", "Roadmap", "FAQ"]
)

with tab_vision:
    st.markdown('<div class="section-label">Why this platform exists</div>', unsafe_allow_html=True)
    st.write(
        "Parasitology labs and training programs often face a common set of constraints: limited time, "
        "high workload, variability in microscopy quality, and fragmented resources for teaching and research. "
        "Parasitic Platform addresses these constraints by consolidating knowledge, research workflows, and "
        "AI-assisted microscopy into a single structured environment."
    )

    st.markdown('<div class="section-label">Core pillars</div>', unsafe_allow_html=True)
    st.markdown(
        """
<div class="table-wrap">
  <span class="badge">🧬 Knowledge</span>
  <span class="badge">📚 Research</span>
  <span class="badge">🧠 Vision AI</span>
  <span class="badge">⚙️ QA & Reproducibility</span>
  <div class="hr"></div>
  <b>Knowledge</b> — evidence-based parasite overview, epidemiology, diagnostic pathways, and pitfalls.<br>
  <b>Research</b> — branch map, project builder, study design alignment, and publishable structure guidance.<br>
  <b>Vision AI</b> — upload, inference, visualization, export, and later: monitoring + drift detection.<br>
  <b>QA & Reproducibility</b> — SOP orientation, audit trails, consistent preprocessing, and documentation.
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-label">Impact targets</div>', unsafe_allow_html=True)
    st.write(
        "• Reduce diagnostic turnaround time while maintaining quality.\n"
        "• Improve training outcomes by providing consistent, structured learning materials.\n"
        "• Enable research reproducibility with standardized methods, templates, and exportable artifacts.\n"
        "• Support innovation in computational parasitology (datasets, benchmarks, and model deployment)."
    )

with tab_scope:
    st.markdown('<div class="section-label">Current modules</div>', unsafe_allow_html=True)

    st.markdown(
        """
<div class="panel">
  <h3>🏠 Home (First page)</h3>
  <div class="small-muted">
    A beautiful card-based navigation hub. Provides orientation, quick access, and a consistent theme across pages.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="panel">
  <h3>🧬 Human Parasite</h3>
  <div class="small-muted">
    A structured parasite knowledge base: taxonomy, transmission, epidemiology, clinical importance, diagnosis, and control.
    Designed for learners and lab staff; supports extension to species-level pages and image galleries.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="panel">
  <h3>📚 Parasitology Research</h3>
  <div class="small-muted">
    A detailed map of research branches (epidemiology, diagnostics, omics, immunology, vector biology, AI, One Health, and implementation science),
    including methods, study designs, pitfalls, and a blueprint generator for publishable projects.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="panel">
  <h3>🧠 Parasitic Vision</h3>
  <div class="small-muted">
    An AI microscopy workspace: upload images, select TF SavedModel/.keras model, run inference, visualize detections,
    export results, and support tiling for large images.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="panel">
  <h3>ℹ️ About Project</h3>
  <div class="small-muted">
    Project rationale, scope, architecture, QA, governance, and roadmap. Acts as the platform’s “documentation” hub.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-label">Who this is for</div>', unsafe_allow_html=True)
    a, b = st.columns(2, gap="small")
    with a:
        st.markdown(
            """
<div class="table-wrap">
<b>Education</b><br>
• Medical Technology / Parasitology students<br>
• Laboratory training programs<br>
• Continuing education and competency assessment<br><br>
<b>Key outcomes</b><br>
• Better conceptual mapping of parasites & diagnostics<br>
• Standardized diagnostic reasoning and reporting
</div>
""",
            unsafe_allow_html=True,
        )
    with b:
        st.markdown(
            """
<div class="table-wrap">
<b>Clinical & Research</b><br>
• Diagnostic labs and microscopy units<br>
• Research groups building datasets & AI models<br>
• Public health surveillance teams<br><br>
<b>Key outcomes</b><br>
• Faster workflow + measurable QC<br>
• Reproducible studies + exportable artifacts
</div>
""",
            unsafe_allow_html=True,
        )

with tab_arch:
    st.markdown('<div class="section-label">Architecture overview</div>', unsafe_allow_html=True)
    st.write(
        "Parasitic Platform is intentionally designed as a modular Streamlit app. Each page acts as a self-contained "
        "workspace, while sharing a single theme and navigation approach."
    )

    st.markdown('<div class="section-label">Recommended folder structure</div>', unsafe_allow_html=True)
    st.code(
        """parasitic_platform/
  app.py
  pages/
    1_Human_Parasite.py
    2_Parasitology_Research.py
    3_Parasitic_Vision.py
    4_About_Project.py
  models/                      # TensorFlow SavedModel folders or .keras files
  model_assets/                # optional: classes.txt, configs, label maps
  assets/                      # optional: icons, banners, screenshots
  data/                        # optional: reference tables, SOP templates
""",
        language="text",
    )

    st.markdown('<div class="section-label">Key technical principles</div>', unsafe_allow_html=True)
    st.write(
        "• **Caching**: load models with `st.cache_resource` to avoid reloading on every interaction.\n"
        "• **Determinism**: preprocessing pipelines should match training exactly.\n"
        "• **Extensibility**: add pages, models, and datasets without rewriting the app.\n"
        "• **Exportability**: always allow CSV/PNG/label export to support audits and publications."
    )

    st.markdown('<div class="section-label">AI integration patterns</div>', unsafe_allow_html=True)
    st.markdown(
        """
<div class="table-wrap">
<b>Pattern A — TF Object Detection API SavedModel</b><br>
• Produces standardized outputs: boxes/scores/classes<br>
• Best for detection/segmentation pipelines exported as SavedModel<br><br>

<b>Pattern B — Keras .keras</b><br>
• Often classification by default (softmax vector)<br>
• Can be detection too, but needs an adapter that maps output tensors to boxes/scores/classes<br><br>

<b>Pattern C — Hybrid</b><br>
• Use a detector for ROIs + a classifier per ROI for fine-grained labels (egg species, artifact filtering)
</div>
""",
        unsafe_allow_html=True,
    )

with tab_quality:
    st.markdown('<div class="section-label">Quality system (research-grade)</div>', unsafe_allow_html=True)
    st.write(
        "A parasitology platform is only as trustworthy as its quality system. This section defines the minimum "
        "quality and governance requirements for reliable diagnostics and publishable research."
    )

    st.markdown('<div class="section-label">Quality pillars</div>', unsafe_allow_html=True)
    st.write(
        "• **Data quality**: standardized collection, label definitions, inter-rater agreement, and traceable provenance.\n"
        "• **Model quality**: validated on external sites, calibrated confidence, robust to stain/device variability.\n"
        "• **Workflow quality**: QC checks, audit trail of outputs, clear handover to human verification.\n"
        "• **Security & privacy**: de-identification, controlled access, and secure storage for patient images."
    )

    st.markdown('<div class="section-label">Governance & documentation</div>', unsafe_allow_html=True)
    st.markdown(
        """
<div class="table-wrap">
<b>Recommended artifacts</b><br>
• SOPs: specimen collection, microscopy preparation, imaging settings<br>
• Annotation guideline: label taxonomy, edge cases, consensus rules<br>
• Model card: training data scope, limitations, performance by subgroup/site<br>
• Monitoring plan: drift signals, audit sampling rate, retraining triggers<br><br>

<b>Minimum audit log fields</b><br>
• image_id, timestamp, device metadata, preprocessing version<br>
• model version/hash, thresholds (conf/IoU), output summary<br>
• human verification status (accepted/edited/rejected)
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="warn">
<b>Clinical caution:</b> AI output should be treated as decision support. Final interpretation must be confirmed
by trained personnel and aligned with local guidelines and reference methods.
</div>
""",
        unsafe_allow_html=True,
    )

with tab_roadmap:
    st.markdown('<div class="section-label">Roadmap</div>', unsafe_allow_html=True)

    st.markdown(
        """
<div class="table-wrap">
<b>Phase 1 — Foundation (current)</b><br>
• Polished UI theme + navigation<br>
• Knowledge & research modules with structured content<br>
• Vision inference workspace (TF SavedModel/.keras) + export<br><br>

<b>Phase 2 — Dataset & annotation</b><br>
• Built-in annotation tool (editable boxes, labels, multi-image batch)<br>
• Inter-rater agreement & consensus labeling workflow<br>
• Dataset versioning and metadata schema<br><br>

<b>Phase 3 — Research-grade analytics</b><br>
• Automated performance reports (mAP, F1, calibration, drift)<br>
• Reader study mode (AI-assisted vs standard workflow)<br>
• Integration with literature search and study templates<br><br>

<b>Phase 4 — Deployment & monitoring</b><br>
• Role-based access (lab/admin/research)<br>
• Secure storage, audit logs, and compliance features<br>
• Model registry + staged rollout + monitoring dashboard
</div>
""",
        unsafe_allow_html=True,
    )

with tab_faq:
    st.markdown('<div class="section-label">Frequently asked questions</div>', unsafe_allow_html=True)

    with st.expander("Is this intended for clinical diagnosis?"):
        st.write(
            "It can support clinical workflows as decision support, but it must be validated in your setting. "
            "AI output should be reviewed by qualified personnel and aligned with reference standards."
        )

    with st.expander("What model formats are supported?"):
        st.write(
            "TensorFlow SavedModel directories and Keras `.keras`/`.h5`. "
            "SavedModel from TF Object Detection API is easiest because outputs are standardized. "
            "Custom `.keras` detectors may require a small adapter to map tensors to boxes/scores."
        )

    with st.expander("How do I add my own parasites and content?"):
        st.write(
            "Extend the Human Parasite page by adding parasite cards (species-level sections), "
            "diagnosis flow charts, and image galleries. Keep structure consistent (overview → epidemiology → diagnosis)."
        )

    with st.expander("How do I make it publishable / Frontiers-ready?"):
        st.write(
            "Use the Research page’s project builder to generate a blueprint and then add:\n"
            "• sample size methods\n"
            "• explicit variables and endpoints\n"
            "• validation strategy\n"
            "• ethics and data governance\n"
            "• reporting checklists (STROBE/STARD/CONSORT)\n"
            "This makes your app outputs align with manuscript structure."
        )

# ==================== Navigation footer ====================
st.markdown('<div class="section-label">Navigation</div>', unsafe_allow_html=True)
n1, n2, n3, n4 = st.columns(4, gap="small")
with n1:
    st.page_link("app.py", label="Home", icon="🏠")
with n2:
    st.page_link("pages/1_Human_Parasite.py", label="Human Parasite", icon="🧬")
with n3:
    st.page_link("pages/2_Parasitology_Research.py", label="Parasitology Research", icon="📚")
with n4:
    st.page_link("pages/3_Parasitic_Vision.py", label="Parasitic Vision", icon="🧠")

st.markdown(
    "<div style='margin-top:16px; color:rgba(234,241,255,.45); font-size:.86rem;'>"
    "Parasitic Platform • About Project • Vision • Architecture • QA • Roadmap"
    "</div>",
    unsafe_allow_html=True,
)
