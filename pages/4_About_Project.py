# pages/4_About_Project.py
import streamlit as st
from dataclasses import dataclass
from typing import List, Dict

st.set_page_config(
    page_title="About Project",
    page_icon="ℹ️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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

# ==================== Tabs ====================

st.markdown('<div class="section-label">Why this platform exists</div>', unsafe_allow_html=True)
st.write(
    """
    <div class="table-wrap">
    Parasitic diseases remain a major public health challenge, especially in resource-limited settings where access to expert diagnosis, standardized learning materials, and research support tools is often limited. In many laboratories and educational environments, parasite identification still depends heavily on specialist experience, and this can lead to delays, inconsistency, and diagnostic errors.<br><br>
    A web application that integrates a Parasitic Atlas, Parasitic Research Guide, and AI-based Detection can help bridge these gaps by providing a single digital platform for education, research, and preliminary diagnostic support. The Parasitic Atlas can serve as an accessible visual reference for parasite morphology, life cycle stages, and key diagnostic features. The Parasitic Research Guide can support students, researchers, and laboratory personnel with structured protocols, references, study design guidance, and updated methodologies. Meanwhile, AI detection tools can assist in screening microscopic images, improving efficiency, reducing workload, and supporting more standardized interpretations.<br><br>
    This integrated platform is motivated by the need to combine knowledge accessibility, research capacity building, and intelligent diagnostic assistance into one practical system. By using a web-based approach, the platform can be accessed from different locations and devices, making it suitable for teaching institutions, research laboratories, and clinical settings. Ultimately, the goal is to strengthen parasitology education and research while advancing digital health innovation for faster, smarter, and more scalable parasite detection and analysis.<br><br>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-label">Roadmap</div>', unsafe_allow_html=True)
st.write(
    """
<div class="table-wrap">
<b>Phase 1 — A Parasitic Platform Project (Complete)</b><br>
• ปรับโครงสร้างของ web applications<br>
• เพิ่มโมดูล parasite atlas<br>
• เพิ่มโมดูล parasite research<br>
• ปรับโครงสร้างของการทำงานในหน้า parasite detection<br>
• เพิ่ม roadmap ในส่วนของ about<br><br>

<b>Phase 2 — Atlas and Advancd AI (Current)</b><br>
• แก้ bug ของ web applications<br>
• เพิ่มเนื้อหาในส่วน parasite atlas ฉบับสมบูรณ์<br>
• เพิ่มความแม่นยำของโมเดลในหน้า parasite detection<br>
• ปรับรูปแบบการรายงานผล<br><br>

<b>Phase 3 — Research Level</b><br>
• แก้ bug ของ web application<br>
• พัฒนาเนื้อหาในส่วนของ parasite research ให้สมบูรณ์<br>
• เพิ่มโมดูล การค้นหางานวิจัยจากฐานข้อมูลเปิด และการทำ meta-analysis<br>
• deploy ใน stable server<br><br>
</div>
""", unsafe_allow_html=True)

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
    "© Parasitic Platform • Intelligent Platform for Parasitic Diseases 2026 • Penchom Janwan"
    "</div>",
    unsafe_allow_html=True,
)
