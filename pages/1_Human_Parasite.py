# pages/1_Human_Parasite.py
import streamlit as st
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional

st.set_page_config(page_title="Human Parasite", page_icon="🧬", layout="wide")

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

# -------------------- Knowledge Model --------------------
@dataclass
class ParasiteProfile:
    name: str
    group: str  # Helminth / Protozoa / Ectoparasite
    syndromes: Set[str]  # used for wizard/filtering

    # Overview
    short_overview: str
    reservoir: List[str]
    transmission: List[str]
    life_cycle_key_points: List[str]

    # Clinical
    incubation_or_timeline: List[str]
    typical_presentations: List[str]
    severe_complications: List[str]
    key_risk_groups: List[str]

    # Epidemiology
    distribution: List[str]
    settings: List[str]
    seasonality: List[str]

    # Diagnosis
    preferred_specimens: List[str]
    primary_tests: List[str]
    confirmatory_or_adjunct: List[str]
    microscopy_cues: List[str]
    common_pitfalls: List[str]

    # Prevention / control (educational)
    prevention: List[str]

    # Quick lab comment templates
    interpretive_comments: List[str] = field(default_factory=list)


SYNDROME_OPTIONS = [
    "GI—diarrhea",
    "GI—abdominal pain/obstruction",
    "GI—bloody diarrhea/dysentery",
    "Hepatobiliary",
    "Pulmonary—cough/wheeze/eosinophilia",
    "Fever—travel/vector exposure",
    "Skin—pruritus/rash",
    "GU—hematuria",
    "Neuro—seizure/focal deficit",
    "Anemia—iron deficiency",
    "Eosinophilia (unexplained)",
]

# -------------------- Expanded dataset (teaching-grade starter set) --------------------
PROFILES: List[ParasiteProfile] = [
    ParasiteProfile(
        name="Enterobius vermicularis (Pinworm)",
        group="Helminth (Nematode)",
        syndromes={"Skin—pruritus/rash"},
        short_overview="Common intestinal nematode; females migrate to perianal region at night to lay eggs → pruritus and easy household spread.",
        reservoir=["Humans (primary)"],
        transmission=[
            "Fecal–oral ingestion of eggs (hands, fomites, dust)",
            "Autoinfection and retroinfection",
            "Household/school transmission (high-contact environments)",
        ],
        life_cycle_key_points=[
            "Eggs become infective rapidly in the environment",
            "Adult worms live in colon; gravid females migrate nocturnally to perianal area",
            "Egg deposition causes pruritus → scratching → egg dissemination",
        ],
        incubation_or_timeline=[
            "Symptoms often correlate with worm burden and reinfection cycles",
            "Tape test yield highest in early morning before washing",
        ],
        typical_presentations=[
            "Nocturnal perianal pruritus (classic)",
            "Sleep disturbance, irritability, bruxism (nonspecific)",
            "Occasional vulvovaginitis (migration/contamination)",
        ],
        severe_complications=[
            "Rare: appendiceal involvement",
            "Persistent vulvovaginitis (selected cases)",
        ],
        key_risk_groups=[
            "School-age children",
            "Crowded households, dormitories, institutions",
        ],
        distribution=["Worldwide"],
        settings=["Schools/daycare", "Households", "Institutions"],
        seasonality=["Often year-round; depends on contact patterns"],
        preferred_specimens=[
            "Perianal adhesive tape swab (morning, before bathing/defecation)",
            "Occasionally visualization of adult worm",
        ],
        primary_tests=[
            "Cellophane tape test (repeat on multiple mornings to increase yield)",
        ],
        confirmatory_or_adjunct=[
            "Microscopy: characteristic ovoid eggs (planoconvex) / adult worm identification",
        ],
        microscopy_cues=[
            "Eggs: ovoid, one side flattened (planoconvex), clear shell; embryo may be visible",
            "Adults: small white thread-like worms (rarely recovered)",
        ],
        common_pitfalls=[
            "Stool O&P often negative (eggs laid perianally, not typically in stool)",
            "Single tape test can miss infections—repeat sampling improves detection",
            "Reinfection common if hygiene/contacts not addressed",
        ],
        prevention=[
            "Hand hygiene, short fingernails, morning bathing, laundering bedding/clothes",
            "Treat close contacts where appropriate (to reduce reinfection cycles)",
        ],
        interpretive_comments=[
            "Perianal tape test sensitivity improves with serial morning specimens.",
            "Negative stool O&P does not exclude Enterobius infection.",
        ],
    ),

    ParasiteProfile(
        name="Ascaris lumbricoides (Ascariasis)",
        group="Helminth (Nematode)",
        syndromes={"GI—abdominal pain/obstruction", "Pulmonary—cough/wheeze/eosinophilia", "Eosinophilia (unexplained)"},
        short_overview="Large intestinal nematode; larval lung migration can cause respiratory symptoms; heavy burden may cause intestinal obstruction.",
        reservoir=["Humans (primary)"],
        transmission=[
            "Ingestion of embryonated eggs from contaminated soil/food (fecal contamination)",
        ],
        life_cycle_key_points=[
            "Eggs mature in soil → ingestion → larvae hatch and migrate via lungs",
            "Larvae ascend airway, swallowed → mature adults in small intestine",
            "High burdens can produce masses of worms",
        ],
        incubation_or_timeline=[
            "Pulmonary phase: days–weeks after ingestion (migratory larvae)",
            "Intestinal adult phase: weeks after exposure; eggs appear after maturation",
        ],
        typical_presentations=[
            "Often asymptomatic",
            "Abdominal pain, nausea; passage of worms",
            "Löffler-like syndrome: cough, wheeze, transient infiltrates + eosinophilia",
        ],
        severe_complications=[
            "Intestinal obstruction (children)",
            "Biliary/pancreatic duct migration → cholangitis/pancreatitis",
        ],
        key_risk_groups=[
            "Children in areas with poor sanitation",
            "Soil exposure, unwashed produce",
        ],
        distribution=["Widespread in tropical/subtropical regions; also pockets elsewhere with sanitation gaps"],
        settings=["Rural/underserved communities", "Soil exposure settings"],
        seasonality=["Often related to rainfall/sanitation patterns; varies by region"],
        preferred_specimens=["Stool"],
        primary_tests=[
            "Stool microscopy (O&P) with concentration for eggs",
        ],
        confirmatory_or_adjunct=[
            "Imaging/endoscopy if biliary migration or obstruction suspected",
        ],
        microscopy_cues=[
            "Fertilized eggs: thick shell, mammillated outer coat (may be decorticated)",
            "Unfertilized eggs: more elongated, thinner shell, disorganized contents",
        ],
        common_pitfalls=[
            "Egg output may be absent early (prepatent) or if only male worms present",
            "Decorticated eggs can be misread if unfamiliar",
        ],
        prevention=[
            "Sanitation, safe feces disposal",
            "Wash produce; hand hygiene",
            "Periodic deworming programs in endemic areas",
        ],
        interpretive_comments=[
            "Consider pulmonary larval migration in cough + eosinophilia with compatible exposure.",
        ],
    ),

    ParasiteProfile(
        name="Trichuris trichiura (Whipworm)",
        group="Helminth (Nematode)",
        syndromes={"GI—diarrhea", "Anemia—iron deficiency", "Eosinophilia (unexplained)"},
        short_overview="Soil-transmitted helminth; heavy infections can cause chronic colitis, anemia, and growth impacts in children.",
        reservoir=["Humans (primary)"],
        transmission=["Ingestion of embryonated eggs from contaminated soil/food"],
        life_cycle_key_points=[
            "Eggs mature in soil; ingestion → larvae hatch and mature in colon",
            "Adults embed anterior end into colonic mucosa",
        ],
        incubation_or_timeline=[
            "Chronic infection is common; symptoms correlate with intensity",
        ],
        typical_presentations=[
            "Often asymptomatic or mild abdominal discomfort",
            "Chronic diarrhea, tenesmus (heavy infection)",
        ],
        severe_complications=[
            "Trichuris dysentery syndrome (severe colitis)",
            "Rectal prolapse (very heavy burden, especially children)",
            "Anemia and growth impairment",
        ],
        key_risk_groups=["Children in endemic areas", "Poor sanitation environments"],
        distribution=["Tropical/subtropical regions; co-endemic with other STH"],
        settings=["Rural/underserved communities"],
        seasonality=["Varies by climate and sanitation"],
        preferred_specimens=["Stool"],
        primary_tests=["Stool microscopy (O&P) for eggs"],
        confirmatory_or_adjunct=["Colonoscopy may visualize worms in severe cases"],
        microscopy_cues=[
            "Eggs: barrel/lemon-shaped with bipolar plugs (classic)",
        ],
        common_pitfalls=[
            "Light infection may be missed on single specimen; consider repeat/concentration",
        ],
        prevention=["Sanitation, hand hygiene, safe feces disposal", "Deworming programs where indicated"],
        interpretive_comments=["Bipolar-plug eggs are strongly suggestive of Trichuris."],
    ),

    ParasiteProfile(
        name="Hookworms (Ancylostoma duodenale / Necator americanus)",
        group="Helminth (Nematode)",
        syndromes={"Anemia—iron deficiency", "Pulmonary—cough/wheeze/eosinophilia", "Eosinophilia (unexplained)"},
        short_overview="Skin-penetrating larvae migrate via lungs → GI adult stage; chronic blood loss can cause iron deficiency anemia.",
        reservoir=["Humans (primary)"],
        transmission=[
            "Larval skin penetration from contaminated soil (barefoot exposure)",
        ],
        life_cycle_key_points=[
            "Filariform larvae penetrate skin → bloodstream → lungs → swallowed",
            "Adults in small intestine feed on blood",
        ],
        incubation_or_timeline=[
            "Skin phase: pruritic papules at entry",
            "Pulmonary migration: cough/wheeze + eosinophilia (variable)",
            "Chronic intestinal stage: anemia develops over time",
        ],
        typical_presentations=[
            "Ground itch at entry site",
            "Iron deficiency anemia, fatigue (chronic)",
        ],
        severe_complications=[
            "Severe anemia (children/pregnancy)",
            "Protein malnutrition in high-burden settings",
        ],
        key_risk_groups=["Barefoot soil exposure", "Children", "Pregnant individuals"],
        distribution=["Tropical/subtropical regions; warm humid climates"],
        settings=["Agricultural/rural settings", "Poor sanitation"],
        seasonality=["Often peaks with warm/wet seasons (larval survival)"],
        preferred_specimens=["Stool"],
        primary_tests=["Stool microscopy (O&P) for eggs"],
        confirmatory_or_adjunct=["Larval culture/speciation (where needed)", "CBC/iron studies for anemia assessment"],
        microscopy_cues=[
            "Eggs: thin-shelled, oval; early cleavage (can resemble other strongylid eggs)",
        ],
        common_pitfalls=[
            "Egg morphology overlaps; species-level identification often requires additional methods",
            "Delay in stool processing can lead to larval development and confusion",
        ],
        prevention=["Footwear, sanitation, safe feces disposal", "Deworming + iron interventions in endemic programs"],
        interpretive_comments=["Consider hookworm in microcytic anemia + soil exposure history."],
    ),

    ParasiteProfile(
        name="Strongyloides stercoralis (Strongyloidiasis)",
        group="Helminth (Nematode)",
        syndromes={"GI—diarrhea", "Pulmonary—cough/wheeze/eosinophilia", "Eosinophilia (unexplained)"},
        short_overview="Skin-penetrating nematode capable of autoinfection; immunosuppression can trigger hyperinfection with high mortality risk.",
        reservoir=["Humans (primary)", "Dogs may play roles in some settings (debated/variable)"],
        transmission=[
            "Larval skin penetration from contaminated soil",
            "Autoinfection cycles (unique clinical importance)",
        ],
        life_cycle_key_points=[
            "Rhabditiform larvae in stool can become infective filariform larvae",
            "Autoinfection allows persistent infection for years",
            "Hyperinfection/dissemination can occur with immunosuppression (e.g., steroids)",
        ],
        incubation_or_timeline=[
            "Can persist chronically with intermittent symptoms",
            "Hyperinfection often associated with immunosuppression triggers",
        ],
        typical_presentations=[
            "Intermittent abdominal pain/diarrhea",
            "Urticarial rash, larva currens",
            "Eosinophilia (may be intermittent or absent in hyperinfection)",
        ],
        severe_complications=[
            "Hyperinfection syndrome: pulmonary + GI deterioration",
            "Dissemination with secondary bacteremia/sepsis",
        ],
        key_risk_groups=[
            "Individuals with corticosteroid exposure",
            "HTLV-1 infection, transplantation, other immunosuppression",
        ],
        distribution=["Tropical/subtropical; also temperate pockets with poor sanitation"],
        settings=["Soil exposure", "Institutional/underserved areas"],
        seasonality=["Varies by region; soil survival influences"],
        preferred_specimens=["Stool (fresh; multiple)", "Sputum (hyperinfection)"],
        primary_tests=[
            "Larvae detection in stool (concentration methods; serial samples)",
            "Serology (useful in many settings; interpret with context)",
        ],
        confirmatory_or_adjunct=[
            "Agar plate culture / Baermann (where available)",
            "Examine sputum/other fluids in hyperinfection suspicion",
        ],
        microscopy_cues=[
            "Larvae (not eggs) usually detected in stool: short buccal cavity; prominent genital primordium (rhabditiform)",
        ],
        common_pitfalls=[
            "Single stool exam has limited sensitivity—serial exams improve detection",
            "Eosinophilia may disappear in severe disease",
            "Missing diagnosis before steroids can be catastrophic in hyperinfection risk",
        ],
        prevention=["Sanitation, footwear, screening before immunosuppression in at-risk individuals"],
        interpretive_comments=[
            "Consider Strongyloides screening in patients with exposure risk before initiating prolonged steroids.",
        ],
    ),

    ParasiteProfile(
        name="Taenia solium / Taenia saginata (Taeniasis; Cysticercosis risk for T. solium)",
        group="Helminth (Cestode)",
        syndromes={"GI—diarrhea", "Neuro—seizure/focal deficit"},
        short_overview="Intestinal tapeworm from undercooked meat; T. solium eggs can cause cysticercosis including neurocysticercosis.",
        reservoir=["Humans (definitive host)", "Pigs (intermediate, T. solium)", "Cattle (intermediate, T. saginata)"],
        transmission=[
            "Taeniasis: ingest cysticerci in undercooked pork/beef",
            "Cysticercosis (T. solium): ingest eggs via fecal–oral contamination",
        ],
        life_cycle_key_points=[
            "Adult tapeworm in human intestine releases proglottids/eggs",
            "Egg ingestion (T. solium) → larval cysticerci in tissues (brain, muscle, eye)",
        ],
        incubation_or_timeline=[
            "Taeniasis often mild/insidious",
            "Neurocysticercosis may present months–years after egg ingestion",
        ],
        typical_presentations=[
            "Often asymptomatic intestinal infection",
            "Abdominal discomfort; passage of proglottids",
            "Neurocysticercosis: seizures, headache",
        ],
        severe_complications=[
            "Neurocysticercosis complications (e.g., hydrocephalus depending on lesion burden/location)",
            "Ocular cysticercosis (vision-threatening)",
        ],
        key_risk_groups=[
            "Undercooked pork exposure (taeniasis)",
            "Sanitation gaps with pig farming (cysticercosis risk)",
        ],
        distribution=["Taeniasis worldwide with undercooked meat practices; T. solium endemic in many LMIC regions"],
        settings=["Food safety gaps", "Rural pig farming", "Sanitation-limited communities"],
        seasonality=["Not strongly seasonal; driven by exposure patterns"],
        preferred_specimens=["Stool (proglottids/eggs)", "Neuro: imaging + serology (clinical integration)"],
        primary_tests=[
            "Stool microscopy (O&P) for eggs/proglottids",
            "Proglottid examination when available (helps speciation)",
        ],
        confirmatory_or_adjunct=[
            "Neurocysticercosis: neuroimaging + serology correlation",
            "PCR/speciation where available",
        ],
        microscopy_cues=[
            "Taenia eggs: thick striated shell (species indistinguishable by egg alone)",
            "Proglottids: uterine branch patterns aid speciation (requires expertise)",
        ],
        common_pitfalls=[
            "Egg morphology cannot reliably speciate T. solium vs T. saginata",
            "Neuro symptoms require integrated diagnostic pathway (imaging + serology + epidemiology)",
        ],
        prevention=["Cook meat adequately, improve sanitation, hand hygiene, meat inspection, pig management"],
        interpretive_comments=[
            "Taenia eggs in stool cannot distinguish species—clinical risk assessment matters for T. solium.",
        ],
    ),

    ParasiteProfile(
        name="Opisthorchis viverrini / Clonorchis sinensis (Liver flukes)",
        group="Helminth (Trematode)",
        syndromes={"Hepatobiliary"},
        short_overview="Foodborne trematodes acquired from raw/undercooked freshwater fish; chronic infection affects bile ducts and increases hepatobiliary disease risk.",
        reservoir=["Humans and fish-eating mammals", "Snails/fish as intermediate hosts"],
        transmission=["Ingestion of metacercariae in raw/undercooked freshwater fish"],
        life_cycle_key_points=[
            "Metacercariae ingested → adults reside in bile ducts",
            "Eggs passed in stool; require freshwater snail/fish cycle",
        ],
        incubation_or_timeline=[
            "Often chronic; symptoms may be mild early",
        ],
        typical_presentations=[
            "RUQ discomfort, dyspepsia",
            "Cholangitis-like symptoms in some cases",
        ],
        severe_complications=[
            "Chronic cholangitis, biliary obstruction",
            "Increased risk of cholangiocarcinoma (notably with O. viverrini in endemic regions)",
        ],
        key_risk_groups=[
            "Raw fish consumption traditions",
            "Endemic river basin communities",
        ],
        distribution=["Southeast Asia (O. viverrini)", "East Asia (C. sinensis)"],
        settings=["Raw fish dishes", "Endemic freshwater ecosystems"],
        seasonality=["Often exposure-pattern dependent; local variations"],
        preferred_specimens=["Stool (eggs)", "Duodenal aspirate (selected)"],
        primary_tests=[
            "Stool microscopy with concentration (low egg output possible)",
        ],
        confirmatory_or_adjunct=[
            "Imaging for hepatobiliary disease when indicated",
            "Serology/antigen tests in some settings (availability varies)",
        ],
        microscopy_cues=[
            "Small operculated eggs; subtle morphology—requires careful measurement/experience",
        ],
        common_pitfalls=[
            "Eggs may resemble other small flukes; speciation by egg alone can be challenging",
            "Light infections may be missed—repeat sampling/concentration helpful",
        ],
        prevention=["Avoid raw/undercooked freshwater fish; food safety education; sanitation"],
        interpretive_comments=[
            "Consider hepatobiliary flukes in endemic regions with chronic RUQ symptoms and raw fish exposure.",
        ],
    ),

    ParasiteProfile(
        name="Schistosoma spp. (Schistosomiasis)",
        group="Helminth (Trematode)",
        syndromes={"GU—hematuria", "Eosinophilia (unexplained)", "Hepatobiliary"},
        short_overview="Freshwater-associated trematodes; cercariae penetrate skin; eggs cause granulomatous disease (urinary or intestinal/hepatic depending on species).",
        reservoir=["Humans (major)", "Some species have animal reservoirs (species-dependent)"],
        transmission=["Skin penetration by cercariae in contaminated freshwater"],
        life_cycle_key_points=[
            "Cercariae penetrate skin → adult worms in venous plexuses",
            "Eggs excreted in urine or stool depending on species",
        ],
        incubation_or_timeline=[
            "Early: swimmer’s itch / acute febrile syndrome (Katayama) in some",
            "Chronic: hematuria, hepatic fibrosis or intestinal symptoms (species-dependent)",
        ],
        typical_presentations=[
            "Hematuria (S. haematobium)",
            "Abdominal pain/diarrhea (intestinal species)",
            "Eosinophilia (variable)",
        ],
        severe_complications=[
            "Urinary tract fibrosis, obstructive uropathy",
            "Portal hypertension from periportal fibrosis (intestinal species)",
        ],
        key_risk_groups=["Freshwater exposure in endemic areas", "Children/occupational exposure"],
        distribution=["Africa, Middle East, parts of South America and Asia (species-dependent)"],
        settings=["Freshwater lakes/rivers", "Irrigation/agricultural exposure"],
        seasonality=["Often linked to water contact patterns and snail ecology"],
        preferred_specimens=["Urine (midday; terminal stream) for S. haematobium", "Stool for intestinal species"],
        primary_tests=[
            "Microscopy for eggs (urine filtration or stool concentration)",
        ],
        confirmatory_or_adjunct=[
            "Serology (exposure) in some contexts",
            "Ultrasound/imaging for chronic organ disease when indicated",
        ],
        microscopy_cues=[
            "Eggs: characteristic spines (terminal spine for S. haematobium; lateral spine for S. mansoni) — species-dependent",
        ],
        common_pitfalls=[
            "Egg excretion can be intermittent; timing and concentration matter",
            "Serology indicates exposure and may not distinguish active vs past infection in some settings",
        ],
        prevention=["Avoid freshwater exposure in endemic regions; snail control; sanitation; mass drug administration programs"],
        interpretive_comments=["Optimize specimen timing and concentration to improve egg detection."],
    ),

    ParasiteProfile(
        name="Giardia duodenalis (Giardiasis)",
        group="Protozoa",
        syndromes={"GI—diarrhea"},
        short_overview="Flagellated protozoan causing malabsorptive, foul-smelling diarrhea; outbreaks via water/daycare are common.",
        reservoir=["Humans", "Animals can be reservoirs (assemblage-dependent)"],
        transmission=["Fecal–oral (cysts)", "Contaminated water", "Person-to-person (daycare)"],
        life_cycle_key_points=[
            "Cysts are infective and environmentally hardy",
            "Trophozoites colonize small intestine → malabsorption",
        ],
        incubation_or_timeline=["Often days–weeks after exposure; may become chronic"],
        typical_presentations=[
            "Foul-smelling diarrhea, bloating, flatulence",
            "Weight loss, malabsorption (persistent infections)",
        ],
        severe_complications=["Chronic malabsorption, growth impacts in children (prolonged cases)"],
        key_risk_groups=["Children/daycare", "Travelers", "Backcountry water exposure", "Immunodeficiency"],
        distribution=["Worldwide"],
        settings=["Daycare", "Waterborne outbreaks", "Unsafe water/sanitation"],
        seasonality=["Outbreak-driven; varies by region"],
        preferred_specimens=["Stool (fresh, ideally multiple)"],
        primary_tests=["Stool antigen tests (EIA/rapid)", "NAAT/PCR where available"],
        confirmatory_or_adjunct=["O&P microscopy (serial specimens; concentration)"],
        microscopy_cues=[
            "Trophozoites: pear-shaped with ‘face-like’ appearance (two nuclei) (fresh stool)",
            "Cysts: oval, internal structures (concentration helps)",
        ],
        common_pitfalls=[
            "Intermittent shedding → single specimen may miss; serial collection improves detection",
            "Microscopy depends on sample freshness and expertise",
        ],
        prevention=["Safe water (boil/filter), hygiene, outbreak control in daycare"],
        interpretive_comments=["Consider serial stool testing when suspicion remains high."],
    ),

    ParasiteProfile(
        name="Entamoeba histolytica (Amebiasis)",
        group="Protozoa",
        syndromes={"GI—bloody diarrhea/dysentery", "Hepatobiliary"},
        short_overview="Invasive amoeba causing dysentery and liver abscess; differentiation from nonpathogenic Entamoeba species is essential.",
        reservoir=["Humans (primary)"],
        transmission=["Fecal–oral ingestion of cysts (contaminated food/water)"],
        life_cycle_key_points=[
            "Cysts ingested → trophozoites in colon",
            "Can invade mucosa → dysentery; hematogenous spread → liver abscess",
        ],
        incubation_or_timeline=["Variable; can be acute or develop after chronic colonization"],
        typical_presentations=[
            "Amebic colitis: abdominal pain, bloody diarrhea/tenesmus",
            "Amebic liver abscess: fever, RUQ pain (often without diarrhea)",
        ],
        severe_complications=[
            "Fulminant colitis, toxic megacolon (rare but severe)",
            "Liver abscess rupture (emergency)",
        ],
        key_risk_groups=["Travel/residence in endemic areas", "Institutional settings", "Immunosuppression"],
        distribution=["Worldwide; higher in areas with sanitation gaps"],
        settings=["Unsafe water/food", "Crowded/institutional settings"],
        seasonality=["Varies by region; often sanitation-related"],
        preferred_specimens=["Stool (colitis)", "Serum + imaging (liver abscess pathway)"],
        primary_tests=[
            "Stool antigen/NAAT for E. histolytica (preferred over microscopy for speciation)",
        ],
        confirmatory_or_adjunct=[
            "Microscopy may show trophozoites with ingested RBCs (suggestive)",
            "Liver abscess: imaging + serology + clinical correlation",
        ],
        microscopy_cues=[
            "Trophozoites with ingested RBCs are strongly suggestive of invasive E. histolytica",
            "Cysts/trophozoites resemble nonpathogenic species—microscopy alone is limited for speciation",
        ],
        common_pitfalls=[
            "Misclassification with nonpathogenic Entamoeba spp. if relying on microscopy only",
            "Antibiotics/antiparasitics can reduce detection in stool",
        ],
        prevention=["Safe water/food hygiene; sanitation improvements"],
        interpretive_comments=["Species-level confirmation is important; microscopy alone can be misleading."],
    ),

    ParasiteProfile(
        name="Cryptosporidium spp. (Cryptosporidiosis)",
        group="Protozoa",
        syndromes={"GI—diarrhea"},
        short_overview="Oocyst-forming protozoa; causes watery diarrhea; severe/prolonged disease in immunocompromised hosts; oocysts are chlorine-tolerant.",
        reservoir=["Humans", "Animals (zoonotic transmission common in some contexts)"],
        transmission=["Fecal–oral oocysts", "Waterborne outbreaks", "Zoonotic exposure"],
        life_cycle_key_points=[
            "Oocysts are immediately infective when excreted",
            "Intracellular (but extracytoplasmic) in intestinal epithelium",
        ],
        incubation_or_timeline=["Typically days after exposure; can be prolonged in immunosuppression"],
        typical_presentations=["Watery diarrhea, cramps, nausea", "Severe dehydration risk"],
        severe_complications=["Chronic debilitating diarrhea in advanced immunosuppression"],
        key_risk_groups=["Immunocompromised (e.g., advanced HIV)", "Children", "Animal handlers"],
        distribution=["Worldwide"],
        settings=["Swimming pools/water parks", "Municipal water outbreaks", "Animal contact"],
        seasonality=["Outbreak-driven; some seasonal peaks in certain regions"],
        preferred_specimens=["Stool"],
        primary_tests=["Stool antigen tests", "NAAT/PCR panels where available"],
        confirmatory_or_adjunct=["Modified acid-fast stain (oocysts)", "Fluorescent antibody staining (lab-dependent)"],
        microscopy_cues=["Small oocysts; acid-fast positive (modified)"],
        common_pitfalls=[
            "Routine O&P may miss without specific staining/testing requests",
            "Chlorination is less effective—outbreak control needs filtration/UV and hygiene",
        ],
        prevention=["Hand hygiene, safe water practices, avoid swimming while symptomatic"],
        interpretive_comments=["Request specific Crypto testing if suspected—routine O&P can miss."],
    ),

    ParasiteProfile(
        name="Plasmodium spp. (Malaria)",
        group="Protozoa (Blood parasite)",
        syndromes={"Fever—travel/vector exposure"},
        short_overview="Life-threatening febrile illness transmitted by Anopheles mosquitoes; rapid diagnosis and severity assessment are critical.",
        reservoir=["Humans (primary for P. falciparum)", "Other species vary; zoonotic malaria exists in some regions"],
        transmission=["Anopheles mosquito bite", "Rare: transfusion/needle", "Congenital (rare)"],
        life_cycle_key_points=[
            "Liver stage → blood-stage parasitemia",
            "Species differences affect relapse potential and severity risk",
        ],
        incubation_or_timeline=[
            "Fever can appear days–weeks after travel; can be delayed for some species",
            "Repeat testing is important if early smears negative but suspicion remains",
        ],
        typical_presentations=["Fever, chills, sweats, headache, malaise", "Anemia/thrombocytopenia common"],
        severe_complications=[
            "Severe malaria syndromes (altered consciousness, respiratory distress, acidosis, severe anemia, high parasitemia)",
        ],
        key_risk_groups=["Travelers without prophylaxis", "Children in endemic areas", "Pregnancy"],
        distribution=["Endemic in parts of Africa, Asia, the Americas (species-dependent)"],
        settings=["Vector exposure", "Rural endemic zones"],
        seasonality=["Often increases in rainy seasons (vector-dependent)"],
        preferred_specimens=["Peripheral blood"],
        primary_tests=["Thick and thin blood smears (microscopy)", "RDT as adjunct/triage where used"],
        confirmatory_or_adjunct=[
            "Species confirmation and parasite density by microscopy (where possible)",
            "PCR in reference settings",
            "Repeat smears q12–24h up to 3 sets if suspicion persists",
        ],
        microscopy_cues=[
            "Thick smear: sensitive screening for parasites",
            "Thin smear: species features + parasitemia quantification",
        ],
        common_pitfalls=[
            "Single negative smear does not exclude malaria early",
            "RDTs can remain positive after treatment and may miss low parasitemia/species (test-dependent)",
        ],
        prevention=["Vector avoidance (nets, repellents), travel prophylaxis per guidelines"],
        interpretive_comments=["If clinical suspicion is high, repeat blood smears even after an initial negative result."],
    ),

    ParasiteProfile(
        name="Sarcoptes scabiei (Scabies)",
        group="Ectoparasite (Arthropod)",
        syndromes={"Skin—pruritus/rash"},
        short_overview="Mite infestation causing intense pruritus and characteristic burrows; outbreaks occur in close-contact settings.",
        reservoir=["Humans (primary)"],
        transmission=["Prolonged skin-to-skin contact", "Fomites (less common; more relevant in crusted scabies)"],
        life_cycle_key_points=[
            "Mites burrow in stratum corneum; eggs laid in burrows",
            "Hypersensitivity contributes to pruritus; symptoms can persist after treatment",
        ],
        incubation_or_timeline=[
            "First infestation: symptoms may appear weeks after exposure",
            "Reinfestation: symptoms can appear faster",
        ],
        typical_presentations=[
            "Severe nocturnal pruritus",
            "Burrows and papules in characteristic sites (web spaces, wrists, waistline)",
        ],
        severe_complications=[
            "Crusted scabies in immunocompromised (highly contagious)",
            "Secondary bacterial infection from excoriations",
        ],
        key_risk_groups=["Crowded living settings", "Institutions", "Immunocompromised (crusted scabies)"],
        distribution=["Worldwide"],
        settings=["Households", "Dormitories", "Long-term care facilities"],
        seasonality=["Not strongly seasonal; outbreaks depend on contact"],
        preferred_specimens=["Skin scraping from burrows/lesions (selected cases)"],
        primary_tests=["Clinical diagnosis (often)", "Microscopy of skin scrapings (mites/eggs/fecal pellets)"],
        confirmatory_or_adjunct=["Dermoscopy (burrow visualization) in some settings"],
        microscopy_cues=["Mite/eggs/scybala in scraping"],
        common_pitfalls=[
            "Itch can persist after successful therapy (post-scabetic itch)",
            "Treat close contacts to prevent reinfestation",
        ],
        prevention=["Treat contacts, environmental cleaning, outbreak protocols in institutions"],
        interpretive_comments=["Negative scraping does not always exclude scabies; clinical correlation is essential."],
    ),
]

GROUPS = sorted({p.group for p in PROFILES})

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

    group_filter = st.multiselect("Parasite group", options=GROUPS, default=GROUPS)
    syndrome_filter = st.multiselect("Syndrome tags", options=SYNDROME_OPTIONS, default=[])
    keyword = st.text_input("Keyword search", placeholder="e.g., eosinophilia, operculum, tape test, smear")
    show_advanced = st.toggle("Show advanced lab notes", value=True)

    st.divider()
    st.caption("Navigation")
    st.page_link("app.py", label="Home", icon="🏠")
    st.page_link("pages/2_Parasitology_Research.py", label="Parasitology Research", icon="📚")
    st.page_link("pages/3_Parasitic_Vision.py", label="Parasitic Vision", icon="🧠")
    st.page_link("pages/4_About_Project.py", label="About Project", icon="ℹ️")


def match_profile(p: ParasiteProfile, groups: List[str], syndromes: List[str], kw: str) -> bool:
    if p.group not in groups:
        return False
    if syndromes:
        if not (p.syndromes & set(syndromes)):
            return False
    if not kw:
        return True
    kw = kw.lower().strip()
    hay = " ".join(
        [
            p.name,
            p.group,
            p.short_overview,
            " ".join(sorted(p.syndromes)),
            " ".join(p.reservoir),
            " ".join(p.transmission),
            " ".join(p.life_cycle_key_points),
            " ".join(p.incubation_or_timeline),
            " ".join(p.typical_presentations),
            " ".join(p.severe_complications),
            " ".join(p.key_risk_groups),
            " ".join(p.distribution),
            " ".join(p.settings),
            " ".join(p.seasonality),
            " ".join(p.preferred_specimens),
            " ".join(p.primary_tests),
            " ".join(p.confirmatory_or_adjunct),
            " ".join(p.microscopy_cues),
            " ".join(p.common_pitfalls),
            " ".join(p.prevention),
            " ".join(p.interpretive_comments),
        ]
    ).lower()
    return kw in hay


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
    st.dataframe(rows, use_container_width=True, hide_index=True)

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
        st.write("• " + "\n• ".join(profile.reservoir))

        st.markdown('<div class="section-label">Transmission</div>', unsafe_allow_html=True)
        st.write("• " + "\n• ".join(profile.transmission))

        st.markdown('<div class="section-label">Life cycle — key points</div>', unsafe_allow_html=True)
        st.write("• " + "\n• ".join(profile.life_cycle_key_points))

        st.markdown('<div class="section-label">Clinical timeline / incubation</div>', unsafe_allow_html=True)
        st.write("• " + "\n• ".join(profile.incubation_or_timeline))

        st.markdown('<div class="section-label">Typical presentations</div>', unsafe_allow_html=True)
        st.write("• " + "\n• ".join(profile.typical_presentations))

        st.markdown('<div class="section-label">Severe complications</div>', unsafe_allow_html=True)
        st.write("• " + "\n• ".join(profile.severe_complications))

        st.markdown('<div class="section-label">High-risk groups</div>', unsafe_allow_html=True)
        st.write("• " + "\n• ".join(profile.key_risk_groups))

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
        st.write("• " + "\n• ".join(profile.distribution))

        st.markdown('<div class="section-label">Typical settings / exposures</div>', unsafe_allow_html=True)
        st.write("• " + "\n• ".join(profile.settings))

        st.markdown('<div class="section-label">Seasonality</div>', unsafe_allow_html=True)
        st.write("• " + "\n• ".join(profile.seasonality))

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
        st.write("• " + "\n• ".join(profile.preferred_specimens))

        st.markdown('<div class="section-label">Primary tests (first-line)</div>', unsafe_allow_html=True)
        st.write("• " + "\n• ".join(profile.primary_tests))

        st.markdown('<div class="section-label">Confirmatory / adjunct tests</div>', unsafe_allow_html=True)
        st.write("• " + "\n• ".join(profile.confirmatory_or_adjunct))

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
        st.write("• " + "\n• ".join(profile.prevention))

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
    synd = st.selectbox("Syndrome", SYNDROME_OPTIONS, index=0)
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

    def score_candidate(p: ParasiteProfile, synd: str, exposure: str) -> int:
        s = 0
        if synd in p.syndromes:
            s += 4
        # crude exposure boosts
        exp = exposure.lower()
        tx = " ".join(p.transmission).lower()
        lc = " ".join(p.life_cycle_key_points).lower()
        sett = " ".join(p.settings).lower()

        if "water" in exp and ("water" in tx or "daycare" in tx or "oocyst" in tx):
            s += 2
        if "soil" in exp and ("soil" in tx or "skin" in tx):
            s += 2
        if "meat" in exp and ("undercooked" in tx or "pork" in tx or "beef" in tx):
            s += 2
        if "fish" in exp and ("fish" in tx):
            s += 2
        if "freshwater swimming" in exp and ("freshwater" in tx or "cercariae" in lc or "snail" in lc):
            s += 2
        if "vector" in exp and ("mosquito" in tx or "anopheles" in tx):
            s += 3
        if "close-contact" in exp and ("household" in tx or "school" in sett or "skin-to-skin" in tx):
            s += 2
        if "immunosuppression" in exp and ("hyperinfection" in " ".join(p.severe_complications).lower() or "immuno" in " ".join(p.key_risk_groups).lower()):
            s += 3
        return s

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
    st.page_link("pages/3_Parasitic_Vision.py", label="Parasitic Vision", icon="🧠")
    st.page_link("pages/4_About_Project.py", label="About Project", icon="ℹ️")

# -------------------- Footer --------------------
st.markdown(
    "<div style='margin-top:16px; color:rgba(234,241,255,.45); font-size:.86rem;'>"
    "Human Parasite • Detailed teaching-grade template • Extend PROFILES to add more species (STH, trematodes, protozoa, ectoparasites)"
    "</div>",
    unsafe_allow_html=True,
)
