# pages/1_Human_Parasite.py
import streamlit as st

from atlas import (
    GROUPS,
    PROFILES,
    SYNDROME_LABELS,
    SYNDROME_OPTIONS,
    match_profile,
    score_candidate,
)

st.set_page_config(
    page_title="Human Parasite",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------- Same Theme (CSS) --------------------
st.markdown(
    """
<style>
:root{
  --bg0:#0F172A;
  --bg1:#0F172A;
  --txt:#FFFFFF;
  --muted:#CBD5E1;
  --muted2:#94A3B8;
  --stroke:rgba(255,255,255,.2);
  --stroke2:rgba(255,255,255,.12);
}

.stApp {
  background:
    radial-gradient(1200px 600px at 20% 10%, rgba(110,231,255,.2), transparent 60%),
    radial-gradient(900px 500px at 85% 15%, rgba(57, 62, 155, 0.2), transparent 80%),
    radial-gradient(800px 600px at 30% 85%, rgba(26, 82, 187, 0.2), transparent 60%),
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
.small-muted { 
  color: #E2E8F0 !important;  /* เปลี่ยนจากสีจางเป็นสีเทาขาวสว่าง */
  font-size: 0.95rem !important; 
  font-weight: 500 !important;
  opacity: 1 !important;      /* ยกเลิกความโปร่งใส */
}

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

/* 1. เจาะจงที่ส่วนหัวข้อใหญ่ใน Sidebar (Knowledge Controls) */
[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3,
div[data-testid="stVerticalBlock"] > div > div > div > span {
    color: #1E293B !important; /* สีน้ำเงิน Slate เข้ม ชัดเจนกว่าสีดำสนิท */
    font-weight: 850 !important; /* เพิ่มความหนาพิเศษ */
    font-size: 1.25rem !important; /* ขยายขนาดเล็กน้อยให้เด่น */
    opacity: 1 !important;
}

/* 2. ปรับตัวหนังสือรายการเมนู (เช่น Human Parasite, Parasitology Research) */
[data-testid="stSidebarNav"] span {
    color: #0F172A !important;
    font-weight: 500 !important;
}

/* 3. ปรับตัวหนังสือใน Sidebar ที่มักจะจาง (เช่น Parasite group) */
[data-testid="stSidebar"] p {
    color: #0F172A !important; /* สีขาวนวลที่เข้มขึ้นเล็กน้อย */
    font-weight: 600 !important;
}

/* 4. ปรับสีพื้นหลังของ Sidebar ให้มืดลงเล็กน้อยเพื่อให้ตัวหนังสือเด้งออกมา */
[data-testid="stSidebar"] {
    background-color: #E2E8F0 !important;
}

/* 1. แก้จุดตาย: คำว่า (optional) หรือข้อความในวงเล็บ */
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

def bullet_section(title, items):
    if items:
        html = "<ul>" + "".join([f"<li>{i}</li>" for i in items]) + "</ul>"
        st.markdown(html, unsafe_allow_html=True)
# -------------------- Hero --------------------
st.markdown(
    """
<div class="hero">
  <h1>🧬 Human Parasite</h1>
  <p>
    A detailed, lab-oriented parasite knowledge base: <b>overview</b>, <b>epidemiology</b>, and <b>diagnosis</b>,
    with morphology cues, pitfalls, and a syndrome-driven decision helper.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="warn">
<b>Educational use:</b> This page is designed for teaching, lab SOP alignment, and decision support.
It does not replace institutional guidelines or clinician judgment—always follow local protocols.
</div>
""",
    unsafe_allow_html=True,
)

# -------------------- Sidebar controls --------------------
with st.sidebar:
    st.title("Knowledge Controls")

    group_filter = st.multiselect(
        "Parasite group", options=GROUPS, default=GROUPS, key="atlas_groups"
    )
    syndrome_filter = st.multiselect(
        "Syndrome tags",
        options=SYNDROME_OPTIONS,
        default=[],
        format_func=SYNDROME_LABELS.__getitem__,
        key="atlas_syndromes",
    )
    keyword = st.text_input(
        "Keyword search",
        placeholder="e.g., eosinophilia, operculated, tape test, smear",
        key="atlas_keyword",
    )
    show_advanced = st.toggle("Show advanced lab notes", value=True)

    st.divider()
    st.caption("Navigation")
    st.page_link("app.py", label="Home", icon="🏠")
    st.page_link("pages/2_Parasitology_Research.py", label="Parasitology Research", icon="📚")
    st.page_link("pages/3_ParD_-_Parasite_Detection.py", label="ParD - Parasite Detection", icon="🧠")
    st.page_link("pages/4_About_Project.py", label="About Project", icon="ℹ️")


filtered = [p for p in PROFILES if match_profile(p, group_filter, syndrome_filter, keyword)]

# -------------------- KPI row --------------------
k1, k2, k3, k4 = st.columns(4, gap="small")
with k1:
    st.markdown('<div class="kpi">', unsafe_allow_html=True)
    st.metric("Profiles in view", str(len(filtered)), "")
    st.markdown("</div>", unsafe_allow_html=True)
with k2:
    st.markdown('<div class="kpi">', unsafe_allow_html=True)
    st.metric("Groups represented", str(len({p.group for p in filtered})), "")
    st.markdown("</div>", unsafe_allow_html=True)
with k3:
    st.markdown('<div class="kpi">', unsafe_allow_html=True)
    st.metric("Syndrome tags", str(len({s for p in filtered for s in p.syndromes})), "")
    st.markdown("</div>", unsafe_allow_html=True)
with k4:
    st.markdown('<div class="kpi">', unsafe_allow_html=True)
    st.metric("Specimen types", str(len({s for p in filtered for s in p.preferred_specimens})), "")
    st.markdown("</div>", unsafe_allow_html=True)

if not filtered:
    st.warning("No parasites match your filters. Try clearing the keyword or selecting more groups/tags.")
    st.stop()

# -------------------- Top: selector + compare --------------------
st.markdown('<div class="section-label">Select parasite profile</div>', unsafe_allow_html=True)
colA, colB = st.columns([1.2, 1], gap="small")

with colA:
    selected_name = st.selectbox("Parasite", options=[p.name for p in filtered], index=0, label_visibility="collapsed")
    profile = next(p for p in filtered if p.name == selected_name)
    with st.expander("Sources and content review"):
        if profile.reviewed_on and profile.reviewer:
            st.caption(f"Reviewed on {profile.reviewed_on} by {profile.reviewer}")
        else:
            st.caption("Content review has not been recorded for this profile.")
        if profile.sources:
            for source in profile.sources:
                st.write(source)
        else:
            st.caption("Source references have not been recorded for this profile.")

with colB:
    compare_names = st.multiselect(
        "Compare (optional)",
        options=[p.name for p in filtered],
        default=[selected_name],
        help="Select multiple parasites to compare key diagnostic attributes.",
    )

# Comparison table (quick, practical fields)
if compare_names:
    cmp_profiles = [p for p in filtered if p.name in compare_names]
    rows = []
    for p in cmp_profiles:
        rows.append(
            {
                "Parasite": p.name,
                "Group": p.group,
                "Syndromes": ", ".join(sorted(p.syndromes)),
                "Specimens": "; ".join(p.preferred_specimens),
                "Primary tests": "; ".join(p.primary_tests),
                "Key pitfalls": "; ".join(p.common_pitfalls[:2]) + ("…" if len(p.common_pitfalls) > 2 else ""),
            }
        )
    st.markdown('<div class="section-label">Comparison snapshot</div>', unsafe_allow_html=True)
    st.dataframe(rows, width="stretch", hide_index=True)

# -------------------- Main layout --------------------
left, right = st.columns([1.65, 1], gap="small")

with left:
    # Header panel
    st.markdown(
        f"""
<div class="panel">
  <h3>{profile.name}</h3>
  <div class="small-muted">{profile.group}</div>
  <div class="hr"></div>
  <div>
    {"".join([f'<span class="badge">{s}</span>' for s in sorted(profile.syndromes)])}
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    tab_overview, tab_epi, tab_dx, tab_morph, tab_prev = st.tabs(
        ["Overview", "Epidemiology", "Diagnosis", "Morphology & Pitfalls", "Prevention & Control"]
    )

    # -------- Overview (much more detail) --------
    
    with tab_overview:
        st.markdown('<div class="section-label">What it is</div>', unsafe_allow_html=True)
        st.write(profile.short_overview)

        st.markdown('<div class="section-label">Reservoir(s)</div>', unsafe_allow_html=True)
        #st.write("• " + "\n• ".join(profile.reservoir))
        bullet_section("", profile.reservoir)

        st.markdown('<div class="section-label">Transmission</div>', unsafe_allow_html=True)
        #st.write("• " + "\n• ".join(profile.transmission))
        bullet_section("", profile.transmission)
        
        st.markdown('<div class="section-label">Life cycle — key points</div>', unsafe_allow_html=True)
        bullet_section("", profile.life_cycle_key_points)
        
        st.markdown('<div class="section-label">Clinical timeline / incubation</div>', unsafe_allow_html=True)
        #st.write("• " + "\n• ".join(profile.incubation_or_timeline))
        bullet_section("", profile.incubation_or_timeline)

        st.markdown('<div class="section-label">Typical presentations</div>', unsafe_allow_html=True)
        #st.write("• " + "\n• ".join(profile.typical_presentations))
        bullet_section("", profile.typical_presentations)

        st.markdown('<div class="section-label">Severe complications</div>', unsafe_allow_html=True)
        #st.write("• " + "\n• ".join(profile.severe_complications))
        bullet_section("", profile.severe_complications)

        st.markdown('<div class="section-label">High-risk groups</div>', unsafe_allow_html=True)
        #st.write("• " + "\n• ".join(profile.key_risk_groups))
        bullet_section("", profile.key_risk_groups)

        if show_advanced:
            with st.expander("Advanced: structured clinical reasoning (syndrome → parasite)"):
                st.write(
                    "- Use **exposure** to constrain the candidate set (soil vs water vs fish vs vector vs close contact).\n"
                    "- Use **syndrome** to select **specimen + test family** first (stool/urine/blood/skin), then refine.\n"
                    "- Always check for **danger syndromes** (neuro signs, severe dehydration, severe anemia, altered mental status).\n"
                    "- Consider **intermittent shedding** and **prepatent windows** when interpreting negatives."
                )

    # -------- Epidemiology (expanded) --------
    with tab_epi:
        st.markdown('<div class="section-label">Geographic distribution</div>', unsafe_allow_html=True)
        #st.write("• " + "\n• ".join(profile.distribution))
        bullet_section("", profile.distribution)

        st.markdown('<div class="section-label">Typical settings / exposures</div>', unsafe_allow_html=True)
        #st.write("• " + "\n• ".join(profile.settings))
        bullet_section("", profile.settings)

        st.markdown('<div class="section-label">Seasonality</div>', unsafe_allow_html=True)
        #st.write("• " + "\n• ".join(profile.seasonality))
        bullet_section("", profile.seasonality)

        st.markdown(
            """
<div class="note">
<b>How to use epidemiology in diagnostics:</b><br>
1) Estimate <span class="mono">pre-test probability</span> → 2) select high-yield specimens → 3) choose tests that match the parasite stage (egg/larva/trophozoite/oocyst/blood-stage).
</div>
""",
            unsafe_allow_html=True,
        )

        if show_advanced:
            with st.expander("Advanced: exposure → recommended first-line test families"):
                st.write(
                    "**Soil exposure + eosinophilia** → stool O&P ± larval methods/serology (species-dependent)\n\n"
                    "**Unsafe water/daycare** → stool antigen/NAAT for protozoa (Giardia/Crypto)\n\n"
                    "**Raw freshwater fish + RUQ symptoms** → stool concentration for operculated eggs + hepatobiliary assessment\n\n"
                    "**Freshwater swimming in endemic areas** → urine/stool egg detection with timing + concentration\n\n"
                    "**Travel + fever** → urgent blood smear workflow with repeat strategy"
                )

    # -------- Diagnosis (expanded workflow) --------
    with tab_dx:
        st.markdown('<div class="section-label">Preferred specimens</div>', unsafe_allow_html=True)
        #st.write("• " + "\n• ".join(profile.preferred_specimens))
        bullet_section("", profile.preferred_specimens)

        st.markdown('<div class="section-label">Primary tests (first-line)</div>', unsafe_allow_html=True)
        #st.write("• " + "\n• ".join(profile.primary_tests))
        bullet_section("", profile.primary_tests)

        st.markdown('<div class="section-label">Confirmatory / adjunct tests</div>', unsafe_allow_html=True)
        #st.write("• " + "\n• ".join(profile.confirmatory_or_adjunct))
        bullet_section("", profile.confirmatory_or_adjunct)

        st.markdown('<div class="section-label">Diagnostic workflow (bench-ready template)</div>', unsafe_allow_html=True)
        st.markdown(
            """
<div class="table-wrap">
<b>Step 1 — Pre-analytical</b><br>
• Confirm specimen type + timing • Record key exposure • Note recent antiparasitics/antibiotics<br><br>
<b>Step 2 — Primary detection</b><br>
• Choose the test family aligned with expected stage (egg/larva/oocyst/blood form)<br><br>
<b>Step 3 — Confirmation & characterization</b><br>
• Speciate (if required) • Quantify (where relevant) • Repeat testing if intermittent shedding suspected<br><br>
<b>Step 4 — Reporting</b><br>
• Result + method + limitations • Suggest follow-up when clinically indicated
</div>
""",
            unsafe_allow_html=True,
        )

        if show_advanced:
            with st.expander("Advanced: pre-analytical and repeat-testing rules of thumb"):
                st.write(
                    "- **Intermittent shedding:** many stool parasites require serial specimens on different days.\n"
                    "- **Stage matters:** some parasites are detected as **larvae** (e.g., Strongyloides) rather than eggs.\n"
                    "- **Timing matters:** e.g., malaria may require repeated smears; some urine egg excretion has time-of-day patterns.\n"
                    "- **Test request matters:** routine O&P may miss certain protozoa unless special stains/antigen/NAAT are requested.\n"
                    "- **Clinical severity matters:** danger syndromes should trigger urgent workflows and escalation."
                )

        st.markdown('<div class="section-label">Interpretive comment templates</div>', unsafe_allow_html=True)
        if profile.interpretive_comments:
            for c in profile.interpretive_comments:
                st.write(f"• {c}")
        else:
            st.write("• (Add interpretive comments here as you standardize your lab reporting.)")

    # -------- Morphology & Pitfalls (expanded) --------
    with tab_morph:
        st.markdown('<div class="section-label">Microscopy cues</div>', unsafe_allow_html=True)
        st.write("• " + "\n• ".join(profile.microscopy_cues))

        st.markdown('<div class="section-label">Common pitfalls</div>', unsafe_allow_html=True)
        st.write("• " + "\n• ".join(profile.common_pitfalls))

        st.markdown(
            """
<div class="note">
<b>Quality note:</b> Microscopy is operator-dependent.
If your lab relies heavily on O&P or smears, standardize: staining, concentration methods, reporting terms, and competency checks.
</div>
""",
            unsafe_allow_html=True,
        )

        if show_advanced:
            with st.expander("Advanced: microscopy workflow improvements (generic)"):
                st.write(
                    "- Use **concentration** for low-burden stool parasites when appropriate.\n"
                    "- Ensure **fresh stool** when trophozoites are relevant; delays change morphology.\n"
                    "- For blood parasites: standardize smear thickness, staining, and parasitemia quantification method.\n"
                    "- Record **which stage** was observed (egg/larva/cyst/trophozoite/adult) for interpretability.\n"
                    "- Maintain a small **image library** of confirmed positives for training/QC."
                )

    # -------- Prevention & Control (expanded) --------
    with tab_prev:
        st.markdown('<div class="section-label">Prevention / control measures</div>', unsafe_allow_html=True)
        #st.write("• " + "\n• ".join(profile.prevention))
        bullet_section("", profile.prevention)

        st.markdown(
            """
<div class="note">
<b>Public health linkage:</b> Many parasites are best controlled upstream (sanitation, safe water, food safety, vector control).
Diagnosis supports targeted treatment and outbreak containment.
</div>
""",
            unsafe_allow_html=True,
        )

    # Print-ready summary (great for teaching handouts)
    st.markdown('<div class="section-label">Print-ready summary</div>', unsafe_allow_html=True)
    summary = f"""
**{profile.name}** — *{profile.group}*

**Overview:** {profile.short_overview}

**Transmission:** {", ".join(profile.transmission)}

**Key symptoms:** {", ".join(profile.typical_presentations)}

**Specimens:** {", ".join(profile.preferred_specimens)}

**Primary tests:** {", ".join(profile.primary_tests)}

**Pitfalls:** {", ".join(profile.common_pitfalls[:3])}{(" ..." if len(profile.common_pitfalls) > 3 else "")}
"""
    st.markdown(summary)

with right:
    # -------- Syndrome → Tests wizard (decision helper) --------
    st.markdown(
        """
<div class="panel">
  <h3>🧭 Syndrome → Diagnostic starting point</h3>
  <div class="small-muted">
    Choose a syndrome + key exposure context, and get a prioritized shortlist and specimen/test starting points.
    (Heuristic teaching tool; extend the rules over time.)
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.write("")
    synd = st.selectbox(
        "Syndrome",
        SYNDROME_OPTIONS,
        index=0,
        format_func=SYNDROME_LABELS.__getitem__,
        key="atlas_wizard_syndrome",
    )
    exposure = st.selectbox(
        "Exposure context",
        [
            "General / unknown",
            "Unsafe water / daycare outbreak",
            "Soil exposure / barefoot / agriculture",
            "Raw/undercooked meat",
            "Raw freshwater fish",
            "Freshwater swimming (endemic risk)",
            "Travel + vector exposure",
            "Close-contact household/institution",
            "Immunosuppression / steroids",
        ],
        index=0,
    )

    ranked = sorted(filtered, key=lambda p: score_candidate(p, synd, exposure), reverse=True)
    top = [p for p in ranked if score_candidate(p, synd, exposure) > 0][:5]

    st.markdown('<div class="section-label">Top candidates</div>', unsafe_allow_html=True)
    if not top:
        st.info("No strong matches from the current demo set. Expand PROFILES to cover your full syllabus.")
    else:
        for p in top:
            st.markdown(
                f"""
<div class="table-wrap">
<b>{p.name}</b><br>
<span class="small-muted">{p.group} • {", ".join(sorted(p.syndromes))}</span><br><br>
<b>Specimen:</b> {"; ".join(p.preferred_specimens)}<br>
<b>Primary:</b> {"; ".join(p.primary_tests)}<br>
<b>Pitfall:</b> {p.common_pitfalls[0] if p.common_pitfalls else "—"}
</div>
""",
                unsafe_allow_html=True,
            )
            st.write("")

    # -------- Lab checklist --------
    st.markdown(
        """
<div class="panel">
  <h3>🧪 Pre-analytical checklist</h3>
  <div class="small-muted">Use as a lab habit-builder (generic).</div>
</div>
""",
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2, gap="small")
    with c1:
        st.checkbox("Correct specimen", value=False)
        st.checkbox("Correct timing", value=False)
        st.checkbox("Label/ID verified", value=False)
    with c2:
        st.checkbox("Transport OK", value=False)
        st.checkbox("Clinical history recorded", value=False)
        st.checkbox("Repeat plan if needed", value=False)

    st.write("")
    st.markdown(
        """
<div class="panel">
  <h3>📌 Quick links</h3>
  <div class="small-muted">Jump to other workspaces.</div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.page_link("app.py", label="Home", icon="🏠")
    st.page_link("pages/2_Parasitology_Research.py", label="Parasitology Research", icon="📚")
    st.page_link("pages/3_ParD_-_Parasite_Detection.py", label="ParD - Parasite Detection", icon="🧠")
    st.page_link("pages/4_About_Project.py", label="About Project", icon="ℹ️")

# -------------------- Footer --------------------
st.markdown(
    "<div style='margin-top:16px; color:rgba(234,241,255,.45); font-size:.86rem;'>"
    "© Parasitic Platform • Intelligent Platform for Parasitic Diseases 2026 • Penchom Janwan"
    "</div>",
    unsafe_allow_html=True,
)
