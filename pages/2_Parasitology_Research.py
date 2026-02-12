# pages/2_Parasitology_Research.py
import streamlit as st
from dataclasses import dataclass, field
from typing import List, Dict, Optional

st.set_page_config(page_title="Parasitology Research", page_icon="📚", layout="wide")

# -------------------- Same Theme (CSS) --------------------
st.markdown(
    """
<style>
:root{
  --bg0:#070A12;
  --bg1:#0A1020;
  --txt:#EAF1FF;
  --muted:rgba(234,241,255,.72);
  --muted2:rgba(234,241,255,.55);
  --stroke:rgba(234,241,255,.10);
  --stroke2:rgba(234,241,255,.16);
}

.stApp {
  background:
    radial-gradient(1200px 600px at 20% 10%, rgba(110,231,255,.08), transparent 55%),
    radial-gradient(900px 500px at 85% 15%, rgba(166,255,203,.06), transparent 55%),
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
  font-size: 1.9rem;
  line-height: 1.12;
  margin: 0;
  font-weight: 820;
  letter-spacing: .2px;
}
.hero p{
  margin: .55rem 0 0 0;
  color: var(--muted);
  font-size: 1.0rem;
}

.section-label{
  margin-top: 1.05rem;
  margin-bottom: .55rem;
  color: var(--muted2);
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
.mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
</style>
""",
    unsafe_allow_html=True,
)

# -------------------- Data Model --------------------
@dataclass
class ResearchBranch:
    name: str
    domain: str  # Population/Clinical/Lab/Vector/Omics/Immunology/Drug/AI/Environment/Policy
    why_it_matters: str
    typical_questions: List[str]
    methods_toolbox: List[str]
    study_designs: List[str]
    core_outputs: List[str]
    pitfalls: List[str]
    starter_projects: List[str]
    datasets_and_resources: List[str] = field(default_factory=list)
    ethics_and_quality: List[str] = field(default_factory=list)


BRANCHES: List[ResearchBranch] = [
    ResearchBranch(
        name="Epidemiology & Surveillance",
        domain="Population",
        why_it_matters="Quantifies burden, identifies transmission hotspots, detects outbreaks, and guides interventions (MDA, WASH, vector control).",
        typical_questions=[
            "What is prevalence/intensity by age group and location?",
            "Which environmental or behavioral factors predict infection?",
            "How do interventions change incidence over time?",
            "Where are spatial clusters and high-risk micro-areas?",
        ],
        methods_toolbox=[
            "Cross-sectional surveys, longitudinal cohorts",
            "Risk factor modeling (logistic/Poisson/negative binomial; mixed models)",
            "Spatial analysis (kernel density, Moran’s I, SaTScan, Bayesian mapping)",
            "Sentinel surveillance and time-series monitoring",
        ],
        study_designs=[
            "Cross-sectional prevalence surveys",
            "Cohort studies (incidence and reinfection)",
            "Case-control (risk factor inference)",
            "Interrupted time series / stepped-wedge (program evaluation)",
        ],
        core_outputs=[
            "Prevalence/intensity estimates, risk maps",
            "Cluster detection reports",
            "Intervention impact metrics (ARR, IRR, DiD)",
            "Dashboards for routine surveillance",
        ],
        pitfalls=[
            "Sampling bias and non-response; unmeasured confounding",
            "Diagnostic misclassification (sensitivity/specificity vary by method)",
            "Ignoring spatial autocorrelation and clustering",
        ],
        starter_projects=[
            "STH prevalence mapping using school-based sampling + risk factor modeling",
            "Reinfection analysis after deworming with mixed-effects models",
            "Spatial cluster detection for opisthorchiasis around river basins",
        ],
        datasets_and_resources=[
            "WHO NTD program guidance (for indicators and survey designs)",
            "DHS/MICS (contextual covariates), local GIS layers (land use, water)",
            "Open climate data (rainfall/temperature) for eco-epidemiology",
        ],
        ethics_and_quality=[
            "Informed consent, community engagement, data de-identification",
            "Pre-register analysis plans where possible; report sampling frames clearly",
        ],
    ),
    ResearchBranch(
        name="Diagnostics & Clinical Parasitology",
        domain="Clinical/Lab",
        why_it_matters="Improves case detection, reduces diagnostic delay, supports treatment decisions, and strengthens laboratory quality systems.",
        typical_questions=[
            "Which diagnostic method has the best accuracy in our setting?",
            "How do we optimize specimen type and timing?",
            "Can we reduce turnaround time without sacrificing sensitivity?",
            "What QC/QA metrics best predict lab performance?",
        ],
        methods_toolbox=[
            "Diagnostic accuracy studies (sensitivity, specificity, AUC)",
            "Method comparison (Bland–Altman, agreement statistics, kappa)",
            "Limit of detection and repeatability/reproducibility tests",
            "External quality assessment (EQA) and proficiency testing",
        ],
        study_designs=[
            "Prospective diagnostic accuracy study",
            "Case series with confirmatory reference methods",
            "Lab validation and verification studies",
        ],
        core_outputs=[
            "Validated SOPs and reporting templates",
            "Accuracy metrics with confidence intervals",
            "QC dashboards (error rates, turnaround time, discordance)",
        ],
        pitfalls=[
            "Imperfect reference standards; spectrum bias",
            "Non-blinded interpretation of microscopy/reads",
            "Small sample sizes without precision targets",
        ],
        starter_projects=[
            "Compare stool antigen vs microscopy vs PCR for Giardia in a local cohort",
            "EQA program for malaria smear reading with digitized slides",
        ],
        datasets_and_resources=[
            "STARD checklist for diagnostic accuracy reporting",
            "Lab QC frameworks (internal QC + EQA)",
        ],
        ethics_and_quality=[
            "Biosafety, specimen governance, handling incidental findings",
            "Blinding and standardized interpretation rules",
        ],
    ),
    ResearchBranch(
        name="Molecular Parasitology & Genomics",
        domain="Omics",
        why_it_matters="Enables species/strain resolution, transmission inference, drug resistance tracking, and discovery of diagnostic targets.",
        typical_questions=[
            "What species/strain is circulating and how is it spreading?",
            "Are resistance-associated mutations emerging?",
            "Which genes/proteins are best diagnostic or vaccine candidates?",
        ],
        methods_toolbox=[
            "PCR/qPCR/ddPCR, amplicon sequencing",
            "Whole genome sequencing (WGS) and variant calling",
            "Phylogenetics / phylodynamics",
            "Metagenomics for mixed infections",
        ],
        study_designs=[
            "Molecular surveillance studies",
            "Outbreak investigations with sequencing",
            "Comparative genomics for candidate discovery",
        ],
        core_outputs=[
            "Genotype maps, phylogenetic trees",
            "Resistance marker panels",
            "Validated molecular assays",
        ],
        pitfalls=[
            "Contamination and batch effects",
            "Poor metadata linkage (time/place/host)",
            "Overinterpretation of limited sampling",
        ],
        starter_projects=[
            "Amplicon sequencing for cryptic species discrimination in trematodes",
            "qPCR panel development for mixed STH infections",
        ],
        datasets_and_resources=[
            "NCBI/ENA sequence repositories; reference genomes",
            "Public variant databases (when available for target parasite)",
        ],
        ethics_and_quality=[
            "Genomic data governance; responsible sharing and consent",
            "Transparent pipeline documentation and versioning",
        ],
    ),
    ResearchBranch(
        name="Immunology & Host–Parasite Interaction",
        domain="Immunology",
        why_it_matters="Explains pathology, informs vaccines/diagnostics, and clarifies susceptibility and reinfection mechanisms.",
        typical_questions=[
            "Which immune signatures correlate with protection or pathology?",
            "How do parasites modulate host immunity?",
            "What biomarkers predict severity or treatment response?",
        ],
        methods_toolbox=[
            "Serology/antibody kinetics, cytokine profiling",
            "Flow cytometry, single-cell approaches (advanced)",
            "In vitro models and animal models (where appropriate)",
            "Systems immunology integration with omics",
        ],
        study_designs=[
            "Case-control immune profiling",
            "Cohorts with pre/post-treatment sampling",
            "Challenge/experimental models (ethics-dependent)",
        ],
        core_outputs=[
            "Biomarker panels, correlates of protection",
            "Mechanistic models of immunopathogenesis",
        ],
        pitfalls=[
            "Confounding by co-infections and nutrition",
            "Batch effects and multiple testing issues",
        ],
        starter_projects=[
            "Pre/post deworming cytokine signature analysis in schoolchildren",
            "Serological marker evaluation for exposure vs active infection",
        ],
        datasets_and_resources=["Public immunology datasets (limited by parasite), local biobanks (if available)"],
        ethics_and_quality=[
            "Consent for biobanking; sample re-use governance",
            "Multiple-comparison control and robust validation",
        ],
    ),
    ResearchBranch(
        name="Vector Biology & Medical Entomology",
        domain="Vector",
        why_it_matters="Vector ecology determines transmission intensity; interventions depend on understanding behavior, insecticide resistance, and habitat.",
        typical_questions=[
            "Which vector species drive transmission locally?",
            "What are biting/resting patterns and seasonality?",
            "Is insecticide resistance present and increasing?",
        ],
        methods_toolbox=[
            "Vector sampling (traps, larval surveys), parity assessment",
            "Insecticide resistance assays (bioassays, molecular markers)",
            "Spatial ecology and habitat modeling",
        ],
        study_designs=[
            "Entomological surveillance studies",
            "Intervention trials (ITNs, IRS, larval source management)",
        ],
        core_outputs=[
            "Vector species composition maps",
            "Resistance profiles and operational recommendations",
        ],
        pitfalls=[
            "Sampling bias (trap type and placement)",
            "Temporal variability not captured by short surveys",
        ],
        starter_projects=[
            "Seasonal vector abundance modeling with rainfall/land use covariates",
            "Resistance marker surveillance integrated into routine trapping",
        ],
        datasets_and_resources=["Local vector surveillance, climate/environment layers, entomological indices standards"],
        ethics_and_quality=["Human landing catch ethics and alternatives; safe handling protocols"],
    ),
    ResearchBranch(
        name="Drug Discovery & Resistance",
        domain="Drug",
        why_it_matters="Resistance threatens control programs; new drugs and combination strategies are essential for sustainable elimination.",
        typical_questions=[
            "Is clinical or molecular resistance emerging?",
            "What is the efficacy of current regimens in our population?",
            "Which targets are promising for new therapeutics?",
        ],
        methods_toolbox=[
            "In vitro susceptibility assays (parasite-dependent)",
            "Therapeutic efficacy studies (TES) and pharmacovigilance",
            "Resistance marker genotyping",
            "PK/PD modeling (advanced)",
        ],
        study_designs=[
            "Clinical efficacy studies with follow-up",
            "Molecular surveillance of resistance markers",
        ],
        core_outputs=[
            "Efficacy estimates, resistance trends",
            "Treatment guideline recommendations (contextual)",
        ],
        pitfalls=[
            "Adherence confounding efficacy estimates",
            "Reinfection vs recrudescence misclassification",
        ],
        starter_projects=[
            "Post-treatment follow-up cohort for reinfection vs treatment failure classification",
            "Resistance marker assay validation with local samples",
        ],
        datasets_and_resources=["Local treatment data, pharmacovigilance reports, reference marker catalogs (where available)"],
        ethics_and_quality=["Clinical trial ethics; safety monitoring; reporting adverse events"],
    ),
    ResearchBranch(
        name="Environmental & Eco-parasitology (One Health)",
        domain="Environment",
        why_it_matters="Transmission is shaped by water, sanitation, animal reservoirs, climate, and land use—critical for prevention and forecasting.",
        typical_questions=[
            "How do climate and land use affect transmission hotspots?",
            "What roles do animal reservoirs play (zoonoses)?",
            "Which WASH improvements yield the biggest impact?",
        ],
        methods_toolbox=[
            "Environmental sampling (water/soil), eDNA (advanced)",
            "Remote sensing + GIS modeling",
            "One Health surveillance (human-animal-environment)",
        ],
        study_designs=[
            "Ecological studies with spatial covariates",
            "Integrated One Health surveillance frameworks",
        ],
        core_outputs=["Risk forecasts, eco-epidemiological models, intervention targeting maps"],
        pitfalls=["Ecological fallacy, confounding by socioeconomics, weak ground-truthing"],
        starter_projects=[
            "Forecasting STH risk using rainfall/temperature + school sanitation indicators",
            "Zoonotic risk mapping combining livestock density + human cases",
        ],
        datasets_and_resources=["Remote sensing products, climate datasets, local WASH indicators"],
        ethics_and_quality=["Data governance across sectors; community consent for environmental sampling"],
    ),
    ResearchBranch(
        name="AI, Digital Pathology & Computational Parasitology",
        domain="AI/Computational",
        why_it_matters="Automates microscopy and supports scalable diagnosis, QC, and surveillance; enables reproducible, deployable pipelines.",
        typical_questions=[
            "Can AI detect parasites in microscopy images with lab-level performance?",
            "How do we build annotation standards and QA pipelines?",
            "What is the best deployment strategy (edge vs server) for clinics?",
        ],
        methods_toolbox=[
            "Dataset curation + annotation protocols; inter-rater agreement",
            "Object detection/segmentation; uncertainty estimation",
            "Model evaluation (mAP, F1, calibration), robustness tests",
            "Human-in-the-loop QC, audit trails, model monitoring",
        ],
        study_designs=[
            "Retrospective dataset development + prospective validation",
            "Reader studies (AI-assisted vs standard microscopy)",
            "Field deployment pilots with monitoring",
        ],
        core_outputs=[
            "Validated AI model + documentation",
            "Annotation guideline + benchmark dataset",
            "Deployment SOP + monitoring dashboard",
        ],
        pitfalls=[
            "Dataset shift (stain, microscope, camera, geography)",
            "Annotation noise and class imbalance",
            "Leakage between train/test and overfitting",
        ],
        starter_projects=[
            "Microscopy parasite egg detection with standardized tiling + QC workflow",
            "Inter-rater study for annotation reliability and consensus labels",
        ],
        datasets_and_resources=[
            "Internal curated microscopy datasets; public datasets (parasite-specific)",
            "Model cards and documentation templates",
        ],
        ethics_and_quality=[
            "Patient privacy in images, consent, secure storage",
            "Bias and fairness across sites; prospective validation",
        ],
    ),
    ResearchBranch(
        name="Implementation Science, Policy & Program Evaluation",
        domain="Policy/Implementation",
        why_it_matters="Bridges evidence to real-world impact: feasibility, acceptability, cost-effectiveness, and sustained adoption.",
        typical_questions=[
            "Why does an intervention succeed in one district and fail in another?",
            "What are barriers to diagnostic uptake?",
            "What is cost-effectiveness of a screening strategy?",
        ],
        methods_toolbox=[
            "Mixed methods (qualitative + quantitative)",
            "RE-AIM, CFIR, logic models",
            "Economic evaluation (CEA/CUA), budget impact analysis",
            "Process indicators and fidelity assessment",
        ],
        study_designs=[
            "Pragmatic trials, stepped-wedge designs",
            "Before-after program evaluations",
            "Qualitative interviews/focus groups",
        ],
        core_outputs=[
            "Implementation roadmap, policy briefs",
            "Cost-effectiveness results and scale-up recommendations",
        ],
        pitfalls=[
            "Attribution bias (concurrent interventions)",
            "Weak measurement of fidelity and context",
        ],
        starter_projects=[
            "Cost-effectiveness of antigen tests vs microscopy in rural clinics",
            "Implementation barriers study for school-based deworming adherence",
        ],
        datasets_and_resources=["Programmatic data, routine HMIS data (where accessible), costing templates"],
        ethics_and_quality=["Consent for interviews; community engagement; transparency in reporting"],
    ),
]

DOMAINS = sorted({b.domain for b in BRANCHES})

# -------------------- Hero --------------------
st.markdown(
    """
<div class="hero">
  <h1>📚 Parasitology Research</h1>
  <p>
    A structured map of research branches in parasitology—what they ask, how they answer, and how to build publishable projects.
    Use filters and the “project builder” to generate a rigorous study blueprint.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="note">
<b>How to use this page:</b> Select a research branch → review typical questions, methods, and study designs → generate a starter project blueprint
that can later be expanded into a thesis, grant proposal, or Frontiers-ready manuscript structure.
</div>
""",
    unsafe_allow_html=True,
)

# -------------------- Sidebar Controls --------------------
with st.sidebar:
    st.title("Research Navigator")
    domain_filter = st.multiselect("Domains", options=DOMAINS, default=DOMAINS)
    keyword = st.text_input("Keyword search", placeholder="e.g., vector, resistance, PCR, AI, spatial")
    show_advanced = st.toggle("Show advanced research notes", value=True)

    st.divider()
    st.caption("Navigation")
    st.page_link("app.py", label="Home", icon="🏠")
    st.page_link("pages/1_Human_Parasite.py", label="Human Parasite", icon="🧬")
    st.page_link("pages/3_Parasitic_Vision.py", label="Parasitic Vision", icon="🧠")
    st.page_link("pages/4_About_Project.py", label="About Project", icon="ℹ️")


def match_branch(b: ResearchBranch, domains: List[str], kw: str) -> bool:
    if b.domain not in domains:
        return False
    if not kw:
        return True
    kw = kw.lower().strip()
    hay = " ".join(
        [
            b.name,
            b.domain,
            b.why_it_matters,
            " ".join(b.typical_questions),
            " ".join(b.methods_toolbox),
            " ".join(b.study_designs),
            " ".join(b.core_outputs),
            " ".join(b.pitfalls),
            " ".join(b.starter_projects),
            " ".join(b.datasets_and_resources),
            " ".join(b.ethics_and_quality),
        ]
    ).lower()
    return kw in hay


filtered = [b for b in BRANCHES if match_branch(b, domain_filter, keyword)]

# -------------------- KPI Row --------------------
k1, k2, k3, k4 = st.columns(4, gap="small")
with k1:
    st.markdown('<div class="kpi">', unsafe_allow_html=True)
    st.metric("Branches in view", str(len(filtered)), "")
    st.markdown("</div>", unsafe_allow_html=True)
with k2:
    st.markdown('<div class="kpi">', unsafe_allow_html=True)
    st.metric("Domains represented", str(len({b.domain for b in filtered})), "")
    st.markdown("</div>", unsafe_allow_html=True)
with k3:
    st.markdown('<div class="kpi">', unsafe_allow_html=True)
    st.metric("Starter projects", str(sum(len(b.starter_projects) for b in filtered)), "")
    st.markdown("</div>", unsafe_allow_html=True)
with k4:
    st.markdown('<div class="kpi">', unsafe_allow_html=True)
    st.metric("Methods listed", str(sum(len(b.methods_toolbox) for b in filtered)), "")
    st.markdown("</div>", unsafe_allow_html=True)

if not filtered:
    st.warning("No branches match your filters. Try selecting more domains or clearing the keyword.")
    st.stop()

# -------------------- Select Branch + Compare --------------------
st.markdown('<div class="section-label">Select research branch</div>', unsafe_allow_html=True)
cA, cB = st.columns([1.2, 1], gap="small")

with cA:
    branch_name = st.selectbox("Branch", options=[b.name for b in filtered], index=0, label_visibility="collapsed")
    branch = next(b for b in filtered if b.name == branch_name)

with cB:
    compare_names = st.multiselect(
        "Compare (optional)",
        options=[b.name for b in filtered],
        default=[branch_name],
        help="Compare outputs, study designs, and pitfalls across branches.",
    )

if compare_names:
    cmp = [b for b in filtered if b.name in compare_names]
    rows = []
    for b in cmp:
        rows.append(
            {
                "Branch": b.name,
                "Domain": b.domain,
                "Key outputs": "; ".join(b.core_outputs[:3]) + ("…" if len(b.core_outputs) > 3 else ""),
                "Common designs": "; ".join(b.study_designs[:2]) + ("…" if len(b.study_designs) > 2 else ""),
                "Pitfalls": "; ".join(b.pitfalls[:2]) + ("…" if len(b.pitfalls) > 2 else ""),
            }
        )
    st.markdown('<div class="section-label">Comparison snapshot</div>', unsafe_allow_html=True)
    st.dataframe(rows, use_container_width=True, hide_index=True)

# -------------------- Main Layout --------------------
left, right = st.columns([1.7, 1], gap="small")

with left:
    st.markdown(
        f"""
<div class="panel">
  <h3>{branch.name}</h3>
  <div class="small-muted">{branch.domain}</div>
  <div class="hr"></div>
  <div>
    <span class="badge">Questions</span>
    <span class="badge">Methods</span>
    <span class="badge">Study design</span>
    <span class="badge">Outputs</span>
    <span class="badge">Pitfalls</span>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    tab_why, tab_q, tab_methods, tab_design, tab_outputs, tab_quality = st.tabs(
        ["Why it matters", "Typical questions", "Methods toolbox", "Study designs", "Outputs", "Ethics & Quality"]
    )

    with tab_why:
        st.markdown('<div class="section-label">Rationale</div>', unsafe_allow_html=True)
        st.write(branch.why_it_matters)
        if show_advanced:
            with st.expander("Advanced: how to position this branch for a high-impact paper"):
                st.write(
                    "- State the **public health or clinical gap** (burden, missed diagnosis, resistance, inequity).\n"
                    "- Present your **innovation** (new assay, better survey design, AI pipeline, One Health integration).\n"
                    "- Specify **validation** and **generalizability** (multi-site, external validation, robustness tests).\n"
                    "- Tie outcomes to **actionable decisions** (treatment, intervention targeting, policy change)."
                )

    with tab_q:
        st.markdown('<div class="section-label">Research questions</div>', unsafe_allow_html=True)
        st.write("• " + "\n• ".join(branch.typical_questions))
        if show_advanced:
            with st.expander("Advanced: transform questions into objectives & hypotheses"):
                st.write(
                    "- Convert each question into: **Objective** → **Operational variables** → **Hypothesis**.\n"
                    "- Define primary vs secondary endpoints; pre-specify subgroup analyses.\n"
                    "- Align outcomes to feasible measurement (diagnostic method, survey instrument, lab assays)."
                )

    with tab_methods:
        st.markdown('<div class="section-label">Methods toolbox</div>', unsafe_allow_html=True)
        st.write("• " + "\n• ".join(branch.methods_toolbox))
        if show_advanced:
            with st.expander("Advanced: reproducibility checklist (methods)"):
                st.write(
                    "- Version control (Git), documented SOPs, locked analysis scripts.\n"
                    "- Clear definitions for inclusion/exclusion and missingness handling.\n"
                    "- Use confidence intervals and uncertainty quantification.\n"
                    "- Validate assumptions (clustered data, spatial dependence, calibration)."
                )

    with tab_design:
        st.markdown('<div class="section-label">Common study designs</div>', unsafe_allow_html=True)
        st.write("• " + "\n• ".join(branch.study_designs))
        if show_advanced:
            with st.expander("Advanced: selecting the right design"):
                st.write(
                    "- **Cross-sectional**: burden and correlates (fast, but causal limits).\n"
                    "- **Cohort**: incidence/reinfection and temporality (stronger inference).\n"
                    "- **Case-control**: efficient for rare outcomes; careful bias control.\n"
                    "- **Stepped-wedge/pragmatic trials**: program evaluation under real constraints.\n"
                    "- **Reader studies** (diagnostics/AI): quantify performance + workflow impact."
                )

    with tab_outputs:
        st.markdown('<div class="section-label">Core outputs</div>', unsafe_allow_html=True)
        st.write("• " + "\n• ".join(branch.core_outputs))

        st.markdown('<div class="section-label">Starter projects</div>', unsafe_allow_html=True)
        st.write("• " + "\n• ".join(branch.starter_projects))

        if branch.datasets_and_resources:
            st.markdown('<div class="section-label">Datasets & resources</div>', unsafe_allow_html=True)
            st.write("• " + "\n• ".join(branch.datasets_and_resources))

    with tab_quality:
        if branch.ethics_and_quality:
            st.markdown('<div class="section-label">Ethics & quality</div>', unsafe_allow_html=True)
            st.write("• " + "\n• ".join(branch.ethics_and_quality))

        st.markdown('<div class="section-label">Common pitfalls</div>', unsafe_allow_html=True)
        st.write("• " + "\n• ".join(branch.pitfalls))

        if show_advanced:
            with st.expander("Advanced: quality metrics you can operationalize"):
                st.write(
                    "- **Diagnostics:** discordance rates, QC pass rate, turnaround time distribution.\n"
                    "- **Surveys:** response rate, cluster design effect, missingness patterns.\n"
                    "- **Omics:** contamination controls, batch metrics, replicate concordance.\n"
                    "- **AI:** external validation performance, drift monitoring, failure mode taxonomy."
                )

    # Print-ready branch summary
    st.markdown('<div class="section-label">Print-ready branch summary</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
**{branch.name}** (*{branch.domain}*)

**Why it matters:** {branch.why_it_matters}

**Typical questions:** {", ".join(branch.typical_questions[:3])}{(" ..." if len(branch.typical_questions) > 3 else "")}

**Top methods:** {", ".join(branch.methods_toolbox[:4])}{(" ..." if len(branch.methods_toolbox) > 4 else "")}

**Starter projects:** {", ".join(branch.starter_projects[:2])}{(" ..." if len(branch.starter_projects) > 2 else "")}
"""
    )

with right:
    # -------------------- Project Builder (detailed) --------------------
    st.markdown(
        """
<div class="panel">
  <h3>🧩 Project Builder</h3>
  <div class="small-muted">
    Generate a detailed, publication-ready blueprint aligned with this branch.
    Customize organism, population, setting, endpoints, and analysis approach.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.write("")

    organism = st.selectbox(
        "Target organism / condition",
        ["Soil-transmitted helminths (STH)", "Opisthorchis/Clonorchis (liver flukes)", "Malaria", "Giardia/Cryptosporidium", "Schistosomiasis", "Other (custom)"],
        index=0,
    )
    setting = st.selectbox(
        "Setting",
        ["School-based survey", "Community household survey", "Hospital/clinic diagnostics", "Vector field surveillance", "Laboratory assay development", "Multi-site program evaluation"],
        index=0,
    )
    design = st.selectbox(
        "Study design",
        branch.study_designs,
        index=0,
    )
    primary_endpoint = st.selectbox(
        "Primary endpoint",
        ["Prevalence", "Incidence", "Diagnostic sensitivity/specificity", "Parasite density/intensity", "Treatment efficacy", "Vector abundance/resistance", "Model performance (mAP/F1)", "Cost-effectiveness (ICER)"],
        index=0,
    )
    sample_size_style = st.selectbox(
        "Sample size approach",
        ["Precision-based (estimate prevalence with CI)", "Power-based (detect difference between groups)", "Rule-of-thumb + feasibility", "AI dataset sizing (coverage across sites/devices)"],
        index=0,
    )

    st.write("")
    if st.button("Generate blueprint", use_container_width=True):
        st.markdown('<div class="section-label">Blueprint</div>', unsafe_allow_html=True)

        blueprint = f"""
<div class="table-wrap">
<b>Project title (template)</b><br>
{branch.name}: A {design.lower()} focused on <span class="mono">{organism}</span> in a <span class="mono">{setting}</span> context.<br><br>

<b>1) Background & gap</b><br>
• Summarize local burden and why current approaches are insufficient.<br>
• State the gap this project targets (e.g., under-detection, resistance risk, spatial hotspots, scalability).<br><br>

<b>2) Objectives</b><br>
• Primary objective: estimate/measure <span class="mono">{primary_endpoint}</span> with defined precision/power.<br>
• Secondary objectives: risk factors, subgroup comparisons, operational feasibility, or robustness testing.<br><br>

<b>3) Design</b><br>
• Design: <span class="mono">{design}</span><br>
• Setting: <span class="mono">{setting}</span><br>
• Population: define inclusion/exclusion, consent, and sampling frame.<br><br>

<b>4) Sample size</b><br>
• Approach: <span class="mono">{sample_size_style}</span><br>
• Specify assumptions (expected prevalence/effect size, ICC for clusters, dropout).<br><br>

<b>5) Data collection</b><br>
• Instruments: questionnaires, specimen collection SOPs, lab assays, GIS covariates (as applicable).<br>
• QA/QC: training, inter-rater checks, blinded reads, EQA, audit trails.<br><br>

<b>6) Analysis plan</b><br>
• Primary analysis aligned with endpoint (CI, regression models, accuracy metrics, or economic models).<br>
• Adjust for clustering/spatial dependence when relevant.<br>
• Sensitivity analyses: alternate cutoffs, missingness, external validation (if AI/diagnostics).<br><br>

<b>7) Outputs</b><br>
• Publishable figures/tables + SOP artifacts + actionable recommendations for program/lab use.<br><br>

<b>8) Ethics & governance</b><br>
• Consent, confidentiality, biosafety, and data sharing plan (de-identified).<br>
</div>
"""
        st.markdown(blueprint, unsafe_allow_html=True)

    st.write("")
    st.markdown(
        """
<div class="panel">
  <h3>📌 Practical “next steps”</h3>
  <div class="small-muted">Use these steps to move from idea → protocol → manuscript.</div>
</div>
""",
        unsafe_allow_html=True,
    )
    with st.expander("1) Convert to protocol"):
        st.write(
            "- Define exact case definitions and diagnostic methods.\n"
            "- Write SOPs for specimen collection and lab processing.\n"
            "- Create a data dictionary and CRFs (case report forms).\n"
            "- Pre-register analysis plan if appropriate."
        )
    with st.expander("2) Convert to manuscript"):
        st.write(
            "- Map objectives to methods, then to results tables/figures.\n"
            "- Use reporting standards: STROBE (observational), STARD (diagnostics), CONSORT (trials), PRISMA (reviews).\n"
            "- Document limitations honestly: sampling, reference standards, external validity."
        )
    with st.expander("3) Convert to grant proposal"):
        st.write(
            "- Emphasize impact pathway, feasibility, team capability, and scalability.\n"
            "- Include budget justification and risk mitigation plan.\n"
            "- Provide timeline and milestones (Gantt)."
        )

    st.write("")
    st.markdown(
        """
<div class="panel">
  <h3>🔗 Quick links</h3>
  <div class="small-muted">Jump to other workspaces.</div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.page_link("app.py", label="Home", icon="🏠")
    st.page_link("pages/1_Human_Parasite.py", label="Human Parasite", icon="🧬")
    st.page_link("pages/3_Parasitic_Vision.py", label="Parasitic Vision", icon="🧠")
    st.page_link("pages/4_About_Project.py", label="About Project", icon="ℹ️")

# -------------------- Footer --------------------
st.markdown(
    "<div style='margin-top:16px; color:rgba(234,241,255,.45); font-size:.86rem;'>"
    "Parasitology Research • Detailed branch map + project builder • Extend BRANCHES for niche domains (veterinary, socio-behavioral, vaccinology)"
    "</div>",
    unsafe_allow_html=True,
)
