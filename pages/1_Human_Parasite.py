# pages/1_Human_Parasite.py
import streamlit as st
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional

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
        name="Opisthorchis viverrini / Clonorchis sinensis (Liver flukes)",
        group="Helminth (Trematode)",
        syndromes={"Hepatobiliary disease", "Cholangitis", "Risk of cholangiocarcinoma"},
        short_overview="Foodborne trematodes acquired from raw/undercooked freshwater fish; chronic infection affects bile ducts and increases hepatobiliary disease risk.",
        reservoir=["Humans and fish-eating mammals (cats, dogs, pigs)", 
                   "First intermediate hosts: Fresh water snails (Bithynia spp. for O. viverrini; Parafossarulus spp. for C. sinensis)",
                   "Second intermediate hosts: Fresh water fish (cyprinid fish for O. viverrini; various freshwater fish for C. sinensis)"
                   ],
        transmission=["Ingestion of metacercariae in raw/undercooked freshwater fish"],
        life_cycle_key_points=[
            "Adult flukes in biliary ducts lay fully developed eggs → passed in feces",
        "Eggs ingested by suitable freshwater snails (first intermediate host)",
        "Miracidia hatch in snail → develop through sporocyst → redia → cercaria stages",
        "Free-swimming cercariae leave snail and penetrate freshwater fish (second intermediate host)",
        "Cercariae encyst in fish muscle or under scales as metacercariae",
        "Mammalian hosts (humans, cats, dogs, fish-eating mammals) infected by eating raw/undercooked fish",
        "Metacercariae excyst in duodenum and migrate via ampulla of Vater to biliary ducts",
        "Parasites mature into adults in bile ducts and begin egg production after ~3–4 weeks",
        "Adult flukes reside in biliary (and sometimes pancreatic) ducts attached to mucosa",
        ],
        incubation_or_timeline=[
            "Often chronic; symptoms may be mild early",
        ],
        typical_presentations=[
            "Asymptomatic (common)",
            "Right upper quadrant discomfort",
            "Hepatomegaly",
            "Dyspepsia",
        ],
        severe_complications=[
            "Chronic cholangitis",
            "Biliary obstruction",
            "Gallstones",
            "Cholangiocarcinoma (especially with O. viverrini)",
        ],

        key_risk_groups=[
            "Raw fish consumption traditions",
            "Endemic river basin communities",
        ],
        distribution=["Opisthorchis viverrini is found mainly in Northeast Thailand, Laos, Cambodia, and central and southern Vietnam.", 
                      "(C. sinensis found in East Asia (including Korea, China, Taiwan, and northern Vietnam) and into far eastern Russia."],
        settings=["Raw fish dishes", "Endemic freshwater ecosystems"],
        seasonality=["Often exposure-pattern dependent; local variations"],
        preferred_specimens=["Stool (eggs)", "Duodenal aspirate (selected)"],
        primary_tests=[
            "Ova and parasite (O&P) stool examinations for liver fluke eggs can diagnose Opisthorchis infection.",
        ],
        confirmatory_or_adjunct=[
        "Hepatobiliary imaging (Ultrasound, CT, or MRI) to detect bile duct dilation or presence of flukes.",
        "Serology or antigen-based blood tests (availability depends on regional laboratory settings)."
    ],
        microscopy_cues=[
            "Small operculated eggs; subtle morphology—requires careful measurement/experience",
            "Eggs of Opisthorchis spp. are 19-30 µm long by 10-20 µm wide and are often indistinguishable from the eggs of Clonorchis sinensis. The eggs are operculated and possess prominent opercular ‘shoulders’ and and abopercular knob. The eggs are embryonated when passed in feces."
        ],
        common_pitfalls=[
            "Eggs may resemble other small flukes; speciation by egg alone can be challenging",
            "Light infections may be missed—repeat sampling/concentration helpful",
        ],
        prevention=["People can avoid Opisthorchis infection by not eating raw or undercooked freshwater fish from countries where the parasite occurs. Lightly salted, smoked, or pickled fish can also contain infectious parasites."],
        interpretive_comments=[
            "Consider hepatobiliary flukes in endemic regions with chronic RUQ symptoms and raw fish exposure.",
        ],
    ),
    
    ParasiteProfile(
    name="Minute intestinal flukes (Haplorchis spp., Heterophyes heterophyes, Metagonimus yokogawai)",
    group="Helminth (Trematode)",
    syndromes={"Intestinal fluke infection", "Enteritis", "Chronic diarrhea", "Malabsorption (heavy infection)"},
    short_overview="Foodborne minute intestinal trematodes acquired from raw or undercooked freshwater or brackish fish. Adult flukes inhabit the small intestine and may cause gastrointestinal symptoms; heavy infections can lead to mucosal inflammation and rarely ectopic egg embolization.",
    
    reservoir=[
        "Humans, various fish-eating mammals (e.g., cats and dogs) and birds",
        "First intermediate hosts: Freshwater or brackish water snails (species vary by parasite)",
        "Second intermediate hosts: suitable fresh/brackish water fish (many species)"
    ],

    transmission=["Ingestion of metacercariae in raw or undercooked freshwater/brackish fish"],

    life_cycle_key_points=[
        "Adult flukes reside in small intestine of definitive host and produce embryonated eggs",
        "Eggs passed in feces reach water and are ingested by suitable snail (first intermediate host)",
        "Miracidia hatch in snail → develop through sporocyst → redia → cercaria stages",
        "Cercariae leave snail and penetrate fish (second intermediate host)",
        "Cercariae encyst as metacercariae in fish tissues (muscle, gills, scales)",
        "Humans infected by eating raw/undercooked fish containing metacercariae",
        "Metacercariae excyst in small intestine and mature into adult flukes in ~1–2 weeks",
        "Adults attach to intestinal mucosa using suckers"
    ],

    incubation_or_timeline=[
        "Prepatent period about 1–2 weeks after ingestion",
        "Infections may persist for months to years if untreated"
    ],

    typical_presentations=[
        "Asymptomatic (common in light infections)",
        "Intermittent abdominal pain",
        "Watery or mucoid diarrhea",
        "Nausea",
        "Fatigue",
        "Eosinophilia (variable)"
    ],

    severe_complications=[
        "Chronic enteritis",
        "Malabsorption and weight loss (heavy infection)",
        "Ulceration of intestinal mucosa",
        "Rare ectopic egg embolization to heart or brain (reported mainly with Heterophyes heterophyes)"
    ],

    key_risk_groups=[
        "Consumption of raw or fermented fish dishes",
        "Residents of endemic river and coastal communities",
        "Poor sanitation areas with fish-borne parasite transmission"
    ],

    distribution=[
        "Common in Southeast Asia (Thailand, Laos, Vietnam, Cambodia)",
        "East Asia (China, Korea, Japan, Taiwan)",
        "Middle East and North Africa (especially Heterophyes heterophyes in Egypt)",
        "Foci in Eastern Europe"
    ],

    settings=["Raw fish dishes", "Traditional fermented fish", "Freshwater and brackish ecosystems"],

    seasonality=["Exposure related to fishing and dietary practices; varies locally"],

    preferred_specimens=["Stool (eggs)"],

    primary_tests=[
        "Ova and parasite (O&P) stool examination for characteristic small operculated eggs"
    ],

    confirmatory_or_adjunct=[
        "Concentration techniques to improve detection",
        "Molecular assays (PCR) in research/reference laboratories",
        "Endoscopy rarely shows attached adult flukes"
    ],

    microscopy_cues=[
        "Very small operculated eggs (≈ 26–30 µm by 15–17 µm depending on species)",
        "Eggs resemble those of liver flukes (Opisthorchis/Clonorchis) — differentiation difficult by morphology alone",
        "Embryonated eggs with opercular shoulders and small abopercular knob"
    ],

    common_pitfalls=[
        "Eggs easily confused with other small trematodes",
        "Low egg output in light infections may cause false negatives",
        "Species identification usually not possible from eggs alone"
    ],

    prevention=[
        "Avoid raw or undercooked freshwater or brackish fish in endemic areas",
        "Proper cooking destroys metacercariae",
        "Improved sanitation to reduce contamination of water sources",
        "Control of reservoir hosts"
    ],

    interpretive_comments=[
        "Consider minute intestinal flukes in patients with chronic diarrhea and raw fish exposure in endemic regions",
        "Coinfection with liver flukes is possible in Southeast Asia"
    ],
    ),   


    ParasiteProfile(
        name="Enterobius vermicularis (Pinworm)",
        group="Helminth (Nematode)",
        syndromes={ "Skin—pruritus/rash",
                    "Perianal pruritus (nocturnal)",
                    "Vulvovaginal irritation/pruritus",
                    "Sleep disturbance/insomnia"
        },
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
            "Asymptomatic in a substantial proportion of infections",
            "Nocturnal perianal pruritus (hallmark symptom)",
            "Perianal excoriation or dermatitis secondary to scratching",
            "Sleep disturbance with irritability, restlessness, or bruxism",
            "Daytime fatigue and impaired concentration due to sleep disruption",
            "Vulvovaginal irritation, pruritus, or discharge in females (due to migration or contamination)"
        ],
        severe_complications=[
            "Bacterial infections: Scratching too much can break your skin, causing it to bleed and become infected.",
            "Urinary tract infections (UTIs): The worms can travel to your vagina, enter your urinary tract and cause infections.",
            "Gastrointestinal and abdominal problems: In rare cases, pinworms have been linked to appendicitis, diverticulitis (the growth of pouches in your large intestine), and inflammation of your vagina (vaginitis) and the lining of your uterus (endometritis).",
        ],
        key_risk_groups=[
            "School-age children",
            "Crowded households, dormitories, institutions",
        ],
        distribution=["Worldwide, , with infections occurring most frequently in school- or preschool-children and in crowded conditions."],
        settings=["Schools/daycare", "Households", "Institutions"],
        seasonality=["Often year-round; depends on contact patterns"],
        preferred_specimens=[
            "Perianal adhesive tape swab (morning, before bathing ordefecation)",
            "Occasionally visualization of adult worm",
        ],
        primary_tests=[
            "Scotch (Cellophane) tape test (repeat on multiple mornings to increase yield)",
        ],
        confirmatory_or_adjunct=[
            "Microscopic identification of characteristic eggs",
            "Occasional recovery and identification of adult worms"
        ],
        microscopy_cues=[
            "Eggs: ovoid, asymmetric, flattened on one side (planoconvex), colorless shell",
            "Egg size approximately 50–60 µm by 20–30 µm",
            "Embryonated eggs often contain developing larva",
            "Adults: slender white worms (female ~8–13 mm, male ~2–5 mm)"
        ],
        common_pitfalls=[
            "Stool O&P often negative (eggs laid perianally, not typically in stool)",
            "Single tape test can miss infections—repeat sampling improves detection",
            "Reinfection common if hygiene/contacts not addressed",
        ],
        prevention=[
            "Strict hand hygiene and nail trimming",
            "Morning bathing to remove eggs from skin",
            "Daily laundering of bedding, underwear, and sleepwear",
            "Avoid scratching and nail-biting",
            "Simultaneous treatment of household contacts when indicated"
        ],
        interpretive_comments=[
            "Enterobiasis is primarily a clinical and epidemiologic diagnosis supported by tape test findings.",
        "Negative stool examination does not rule out infection."
        ],
    ),

    ParasiteProfile(
        name="Ascaris lumbricoides (Ascariasis)",
        group="Helminth (Nematode)",
        syndromes={"Gastrointestinal—abdominal pain/intestinal obstruction",
        "Pulmonary—transient pneumonitis (Löffler syndrome)",
        "Hepatobiliary—biliary or pancreatic duct obstruction",
        "Eosinophilia (unexplained)"},
        short_overview="Largest human intestinal nematode. Infection follows ingestion of embryonated eggs from contaminated soil. Larval hepatopulmonary migration may cause eosinophilic pneumonitis; heavy intestinal worm burden can result in mechanical obstruction or migration into biliary and pancreatic ducts.",
    
        reservoir=["Humans (primary)"],
        transmission=[
            "Ingestion of embryonated eggs from contaminated soil/food (fecal contamination)",
        ],
        life_cycle_key_points=[
            "Adult worms reside in the lumen of the small intestine; gravid females produce up to ~200,000 eggs per day that are passed in feces",
            "Unfertilized eggs may be ingested but are not infective",
            "Fertilized eggs embryonate in warm, moist, shaded soil and become infective after ~2–3 weeks (environment-dependent)",
            "After ingestion of embryonated eggs, larvae hatch in the small intestine",
            "Larvae penetrate the intestinal mucosa and migrate via the portal circulation to the liver, then via the systemic circulation to the lungs",
            "Pulmonary phase: larvae mature in the lungs over ~10–14 days, penetrate alveolar walls, ascend the bronchial tree to the pharynx, and are swallowed",
            "Larvae return to the small intestine, where they mature into adult worms",
            "Prepatent period approximately 2–3 months from ingestion to egg production",
            "Adult worms typically survive 1–2 years in the host"
        ],
        incubation_or_timeline=[
            "Pulmonary phase: days–weeks after ingestion (migratory larvae)",
            "Intestinal adult phase: weeks after exposure; eggs appear after maturation",
        ],
        typical_presentations=[
            "Asymptomatic (light infections common)",
            "Abdominal discomfort, nausea, or malnutrition in moderate infection",
            "Passage of adult worms via stool, mouth, or nose (occasionally reported)",
            "Löffler syndrome: nonproductive cough, wheeze, fever, transient pulmonary infiltrates, eosinophilia"
        ],
        severe_complications=[
            "Intestinal obstruction due to heavy worm burden (most common severe complication, especially in children)",
            "Hepatobiliary and pancreatic ascariasis from aberrant worm migration → biliary colic, cholangitis, cholecystitis, obstructive jaundice, or acute pancreatitis",
            "Mechanical obstruction of intestinal or biliary ducts requiring urgent intervention",
            "Severe inflammatory complications secondary to obstruction (e.g., pancreatitis, cholecystitis, cholangitis)",
            "Malnutrition and growth impairment in chronic heavy infections, particularly in children",
            "Rare: intestinal perforation, peritonitis, or fatal complications if untreated"
        ],

        key_risk_groups=[
            "Children in areas with poor sanitation",
            "Soil exposure, unwashed produce",
        ],
        distribution=[
            "Most common human helminth infection globally",
            "Highest burden in tropical and subtropical regions, particularly in areas with inadequate sanitation",
            "Uncommon in high-income countries but sporadic cases occur in rural or impoverished settings",
            "Occasional cases in developed regions associated with exposure to contaminated soil or proximity to pig farming (zoonotic transmission from Ascaris suum)"
        ],
        settings=["Rural/underserved communities", "Soil exposure settings"],
        seasonality=["Often related to rainfall/sanitation patterns; varies by region"],
        preferred_specimens=["Stool"],
        primary_tests=[
            "Stool ova and parasite (O&P) microscopy for detection of characteristic eggs (most common diagnostic method)",
            "Specimen preservation in formalin or appropriate fixative followed by concentration (e.g., formalin–ethyl acetate sedimentation)",
            "Direct wet mount examination acceptable for moderate-to-heavy infections where concentration is unavailable",
            "Quantitative methods (e.g., Kato–Katz thick smear or quantitative fecal flotation) for estimating infection intensity in endemic settings"
        ],

        confirmatory_or_adjunct=[
            "Identification of larvae in sputum or gastric aspirate during pulmonary migration phase (rarely performed)",
            "Macroscopic identification of expelled adult worms from stool, mouth, or nose",
            "Imaging (ultrasound, CT, MRCP) or endoscopy for suspected intestinal, biliary, or pancreatic complications",
            "Molecular detection (PCR-based assays) for parasite DNA in stool—primarily research or reference laboratories"
        ],
        microscopy_cues=[
            "Fertilized eggs: round to oval, thick trilaminar shell with prominent mammillated albuminous outer coat, typically bile-stained brown; size ~45–75 µm",
            "Unfertilized eggs: elongated and larger (up to ~90 µm), thinner shell with irregular or scant mammillated coating, containing disorganized refractile granular material",
            "Decorticated fertilized eggs: loss of outer mammillated layer resulting in a smooth shell, may appear colorless and can be misidentified",
        ],
        common_pitfalls=[
            "Egg output may be absent early (prepatent) or if only male worms present",
            "Decorticated eggs can be misread if unfamiliar",
        ],
        prevention=[
            "Improved sanitation and hygienic disposal of human feces to interrupt transmission",
            "Strict hand hygiene with soap and water after toileting and before food preparation",
            "Thorough washing, peeling, and adequate cooking of fruits and vegetables",
            "Avoidance of soil or water contaminated with human feces",
            "Use of sanitary latrines; avoidance of open defecation",
            "Prohibition of untreated human feces ('night soil') as agricultural fertilizer",
            "Health education emphasizing hygiene practices, especially in children",
            "Periodic mass deworming programs in endemic communities"
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
        transmission=[
        "Fecal–oral ingestion of embryonated eggs from contaminated soil, food, or hands"
        ],
        life_cycle_key_points=[
            "Unembryonated eggs are passed in feces",
            "In soil, eggs develop through 2-cell and advanced cleavage stages and embryonate, becoming infective within ~15–30 days under favorable warm, moist conditions",
            "Ingestion of embryonated eggs via contaminated hands, food, or soil",
            "Larvae hatch in the small intestine and migrate to the cecum and ascending colon",
            "Larvae mature into adult worms that inhabit the large intestine",
            "Adults (~4 cm) attach to mucosa with the slender anterior end embedded in the epithelium and posterior end projecting into the lumen",
            "Female worms begin oviposition approximately 60–70 days after infection, producing ~3,000–20,000 eggs per day",
            "Adult lifespan approximately 1 year"
        ],
        incubation_or_timeline=[
            "Chronic infection is common; symptoms correlate with intensity",
        ],
        typical_presentations=[
            "Often asymptomatic or mild abdominal discomfort",
            "Chronic diarrhea, tenesmus (heavy infection)",
        ],
        severe_complications=[
            "Trichuris dysentery syndrome (severe chronic colitis with bloody diarrhea and tenesmus)",
            "Rectal prolapse, particularly in heavily infected children",
            "Severe iron deficiency anemia",
            "Growth retardation and protein-energy malnutrition in chronic pediatric infection",
            "Impaired cognitive development and reduced school performance associated with long-standing infection"
        ],
        key_risk_groups=["Children in endemic areas", "Poor sanitation environments"],
        distribution=["Tropical/subtropical regions; co-endemic with other STH"],
        settings=["Rural/underserved communities"],
        seasonality=["Varies by climate and sanitation"],
        preferred_specimens=["Stool"],
        primary_tests=[
            "Microscopic identification of thin-shelled hookworm eggs in stool (ova and parasite examination).",
        ],

        confirmatory_or_adjunct=[
            "Stool collection followed by fixation in formalin and concentration using the formalin–ethyl acetate sedimentation technique.",
            "Wet mount examination of concentrated sediment for egg detection.",
            "Direct wet mount stool examination may detect moderate-to-heavy infections when concentration is unavailable.",
            "Egg burden quantification using Kato-Katz, FLOTAC, or Mini-FLOTAC techniques for epidemiologic or treatment-monitoring purposes.",
            "CBC demonstrating microcytic hypochromic anemia with peripheral eosinophilia.",
            "Iron studies showing reduced ferritin and transferrin saturation consistent with chronic blood loss.",
            "Larval culture or molecular assays (PCR-based) when species-level identification is required for research or epidemiology.",
        ],
        microscopy_cues=[
            "Eggs: characteristic barrel- or lemon-shaped, thick smooth shell with prominent bipolar mucus plugs",
            "Size approximately 50–55 µm by 20–25 µm",
            "Bile-stained brown appearance in stool preparations",
            "Eggs are passed unembryonated in feces"
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
            "Unembryonated eggs are passed in stool and hatch in 1–2 days in warm, moist, shaded soil.",
            "Free-living rhabditiform larvae develop in feces/soil and undergo two molts over ~5–10 days to become infective filariform (L3) larvae.",
            "Infective filariform larvae can survive in favorable soil conditions for approximately 3–4 weeks.",
            "Filariform larvae penetrate intact human skin (classically bare feet) and enter the bloodstream → heart → pulmonary circulation.",
            "Larvae penetrate alveoli, ascend the bronchial tree to the pharynx, and are swallowed.",
            "They reach the small intestine (predominantly distal jejunum), where they mature into blood-feeding adult worms attached to mucosa.",
            "Adult females produce thousands of eggs daily, which are excreted in stool and continue environmental transmission.",
            "Typical adult lifespan is 1–2 years, though persistence for several years may occur.",
            "Ancylostoma duodenale larvae may undergo tissue hypobiosis (intestinal or muscular dormancy) with later reactivation causing patent infection.",
            "A. duodenale infection may also occur via oral ingestion or transmammary transmission.",
            "Ancylostoma ceylanicum and A. caninum can establish infection through oral ingestion of larvae.",
            "A. caninum–associated eosinophilic enteritis is thought to follow oral, rather than percutaneous, acquisition.",
            "Necator americanus is not known to infect via oral or transmammary routes.",
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
            "Eggs are thin-shelled, smooth, colorless, and oval with a segmented embryo (early cleavage stage).",
            "Typical size range: approximately 60–75 µm in length × 35–40 µm in width.",
            "Ancylostoma and Necator eggs are morphologically indistinguishable by routine light microscopy.",
            "Egg morphology overlaps with other strongylid-type nematodes, limiting species-level diagnosis from stool eggs alone.",
        ],
        common_pitfalls=[
            "Egg morphology overlaps; species-level identification often requires additional methods",
            "Delay in stool processing can lead to larval development and confusion",
        ],
        prevention=[
            "Consistent use of footwear when walking on soil potentially contaminated with human feces.",
            "Hand hygiene after toilet use and before food handling or eating.",
            "Proper disposal of human feces and access to improved sanitation facilities.",
            "Avoidance of using untreated human feces ('night soil') as agricultural fertilizer.",
            "Periodic mass deworming programs in endemic populations, especially children and pregnant individuals where appropriate.",
            "Iron supplementation and nutritional support to reduce anemia burden in high-transmission settings.",
        ],
        interpretive_comments=["Consider hookworm in microcytic anemia + soil exposure history."],
    ),

    ParasiteProfile(
        name="Strongyloides stercoralis (Strongyloidiasis)",
        group="Helminth (Nematode)",
        syndromes={"GI—diarrhea", "Pulmonary—cough/wheeze/eosinophilia", "Eosinophilia (unexplained)"},
        short_overview=(
        "Skin-penetrating nematode with a unique autoinfective life cycle enabling "
        "decades-long persistence in the human host. Immunosuppression—especially "
        "corticosteroids or HTLV-1 infection—can precipitate hyperinfection or "
        "dissemination with high mortality due to overwhelming parasite burden and "
        "secondary gram-negative sepsis."
        ),
        reservoir=["Humans (primary)", "Dogs may play roles in some settings (debated/variable)"],
        transmission=[
            "Percutaneous penetration of infective filariform larvae from contaminated soil",
            "Internal autoinfection via transformation of rhabditiform to filariform larvae in intestine",
            "External autoinfection through perianal skin penetration",
        ],
        life_cycle_key_points=[
            "Strongyloides stercoralis alternates between free-living and parasitic life cycles and uniquely supports autoinfection within the human host.",
            "Rhabditiform larvae passed in stool may develop directly into infective filariform (L3) larvae or into free-living adult males and females in soil.",
            "Free-living adults mate and produce eggs that hatch into rhabditiform larvae, which subsequently mature into infective filariform larvae.",
            "This environmental amplification increases transmission potential in contaminated soil.",
            "Infective filariform larvae penetrate intact human skin and migrate toward the small intestine.",
            "Migration traditionally occurs via bloodstream and lungs with tracheal ascent and swallowing, though alternative tissue migration routes to the intestine may occur.",
            "Larvae molt twice in the small intestine and become parthenogenetic adult females embedded in the mucosa/submucosa.",
            "Adult females produce eggs that hatch in situ into rhabditiform larvae; parasitic males are absent.",
            "Rhabditiform larvae may be excreted in stool or transform within the host into infective filariform larvae.",
            "Autoinfective larvae penetrate intestinal mucosa or perianal skin, re-enter circulation, and repeat pulmonary–intestinal migration.",
            "Autoinfection enables lifelong persistence without re-exposure, even decades after leaving endemic regions.",
            "Accelerated autoinfection during immunosuppression markedly increases larval burden, producing hyperinfection involving gastrointestinal and pulmonary systems.",
            "Disseminated strongyloidiasis may extend beyond the usual pulmonary–intestinal cycle to organs such as CNS, liver, or other tissues and is associated with high mortality.",
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
        distribution=[
            "Broadly distributed across tropical and subtropical regions worldwide.",
            "Focal transmission occurs in temperate regions, particularly during warm summer months.",
            "Higher prevalence in areas with poor sanitation, rural or remote communities, institutional settings, and socially marginalized populations.",
            "Strongyloides fuelleborni subsp. fuelleborni occurs in non-human primates throughout the Old World; most human infections reported from sub-Saharan Africa, with sporadic cases in Southeast Asia.",
            "Strongyloides fuelleborni subsp. kellyi is endemic to Papua New Guinea and has not been documented elsewhere.",
        ],
        settings=["Soil exposure", "Institutional/underserved areas"],
        seasonality=["Varies by region; soil survival influences"],
        preferred_specimens=["Stool (fresh; multiple)", "Sputum (hyperinfection)"],
        primary_tests=[
            "Detection of Strongyloides larvae in stool using concentration or serial examination techniques",
            "Serologic antibody testing (useful for screening; may remain positive after past infection)",
        ],

        confirmatory_or_adjunct=[
            "Agar plate culture or Baermann concentration to enhance larval recovery",
            "Microscopic examination of sputum, BAL, or other body fluids in suspected hyperinfection/dissemination",
            "PCR-based molecular assays where available (research or reference labs)",
            "CBC showing eosinophilia in chronic infection (may be absent in hyperinfection)",
        ],
        microscopy_cues=[
            "Rhabditiform larvae (not eggs) typically seen in stool: short buccal cavity and prominent genital primordium.",
            "Filariform larvae in hyperinfection may be present in stool, sputum, or body fluids.",
        ],
        common_pitfalls=[
            "Single stool exam has limited sensitivity—serial exams improve detection",
            "Eosinophilia may disappear in severe disease",
            "Missing diagnosis before steroids can be catastrophic in hyperinfection risk",
        ],
        prevention=[
            "Wear protective footwear and gloves when in contact with soil in endemic areas to prevent percutaneous larval penetration.",
            "Avoid direct skin contact with potentially contaminated soil, especially in regions with poor sanitation.",
            "Improve sanitation infrastructure to prevent soil contamination with human feces.",
            "Exercise increased caution in rural, institutional, or underserved settings where environmental contamination risk is higher.",
            "Screen at-risk individuals for Strongyloides infection before initiating corticosteroids, transplantation, chemotherapy, or other immunosuppressive therapies.",
            "Treat confirmed or suspected infection prior to immunosuppression to prevent hyperinfection syndrome.",
            "Consider empiric ivermectin in high-risk patients when testing is delayed and immunosuppression cannot be postponed.",
        ],
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
            "Humans are the definitive hosts harboring adult Taenia spp. in the small intestine; gravid proglottids and eggs are shed in feces and remain environmentally resilient for weeks to months",
            "Cattle (T. saginata) and pigs (T. solium, T. asiatica) ingest eggs from contaminated vegetation → oncospheres hatch, penetrate the intestinal mucosa, and disseminate hematogenously to striated muscle",
            "Larvae develop into tissue cysticerci that remain viable in intermediate hosts for years",
            "Humans acquire taeniasis by consuming raw or undercooked beef (T. saginata) or pork/viscera (T. solium, T. asiatica) containing viable cysticerci",
            "In the human small intestine, cysticerci evaginate, attach via the scolex, and mature into adult tapeworms within ~2 months, persisting for years while producing numerous proglottids",
            "Autoinfection or fecal–oral ingestion of T. solium eggs (not cysticerci) can lead to invasive cysticercosis, with hematogenous dissemination of larvae to tissues including brain, muscle, subcutaneous tissue, and eye",
            "Neurocysticercosis results when larvae encyst in the central nervous system and may manifest months to years after infection"
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
            "Neurocysticercosis with hydrocephalus, intracranial hypertension, or stroke from vasculitis",
            "Ocular cysticercosis with vision loss",
            "Subcutaneous or muscular cysticercosis (usually asymptomatic nodules)"
        ],
        key_risk_groups=[
            "Consumption of undercooked pork or beef",
            "Residents or travelers to endemic regions",
            "Household contacts of T. solium carriers (cysticercosis risk)",
            "Settings with poor sanitation and free-ranging pig husbandry"
        ],
        distribution=[
            "Taenia saginata and Taenia solium have a worldwide distribution associated with consumption of raw or undercooked beef or pork, respectively",
            "Taenia solium is most prevalent in low-resource settings with poor sanitation, free-ranging pig husbandry, and close human–pig contact",
            "High-burden regions for T. solium include Latin America, sub-Saharan Africa, South and Southeast Asia",
            "Taenia asiatica is geographically restricted to East and Southeast Asia (notably Korea, China, Taiwan, Indonesia, Thailand) and is associated with consumption of raw or undercooked pig viscera"
        ],
        settings=["Food safety gaps", "Rural pig farming", "Sanitation-limited communities"],
        seasonality=["Not strongly seasonal; driven by exposure patterns"],
        preferred_specimens=["Stool (proglottids/eggs)", "Neuro: imaging + serology (clinical integration)"],
        primary_tests=[
            "Stool microscopy (O&P) for Taenia eggs",
            "Morphologic examination of proglottids or scolex for species differentiation"
        ],
        confirmatory_or_adjunct=[
            "Neuroimaging (CT/MRI) for suspected neurocysticercosis",
            "Serologic assays (e.g., EITB) interpreted with imaging and epidemiology",
            "Molecular speciation where available"
        ],
        microscopy_cues=[
            "Taenia eggs: spherical (≈30–35 µm), thick radially striated embryophore; internal hexacanth embryo (oncosphere) with six refractile hooklets",
            "Egg morphology is not species-specific and cannot distinguish T. solium from T. saginata (nor reliably from other Taeniidae)",
            "Proglottids: species differentiation relies on uterine branch counts in gravid segments (T. saginata typically >15 lateral branches per side; T. solium usually 7–13)",
            "Scolex morphology (when recovered) is diagnostic: T. solium with armed rostellum and hooklets; T. saginata unarmed"
        ],
        common_pitfalls=[
            "Egg morphology cannot reliably speciate T. solium vs T. saginata",
            "Neuro symptoms require integrated diagnostic pathway (imaging + serology + epidemiology)",
        ],
        prevention=[
            "Adequate cooking of pork and beef",
            "Improved sanitation and hand hygiene",
            "Meat inspection and control of pig access to human feces",
            "Identification and treatment of human tapeworm carriers"
        ],
        interpretive_comments=[
            "Taenia eggs in stool cannot distinguish species—clinical risk assessment matters for T. solium.",
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
            "Eggs are excreted in human urine (urogenital species) or feces (intestinal/hepatosplenic species) depending on species",
            "In freshwater, eggs hatch releasing ciliated miracidia that actively penetrate specific freshwater snail intermediate hosts",
            "Within snails, sequential sporocyst generations amplify infection and produce fork-tailed cercariae",
            "Free-swimming cercariae are released into water and penetrate intact human skin during water contact",
            "After penetration, cercariae shed their tails and transform into schistosomula, entering the circulation",
            "Schistosomula migrate via venous blood → lungs → systemic circulation → hepatic portal system, where maturation occurs",
            "Male and female worms pair in the liver and migrate to their final venous niches (species-specific tropism)",
            "Adult worms reside in venous plexuses for years: mesenteric venules (intestinal species) or vesical/pelvic plexus (urogenital species)",
            "Females deposit eggs in small venules; eggs traverse tissues into intestinal or urinary lumens, while many become trapped",
            "Host immune responses to trapped eggs cause granulomatous inflammation, fibrosis, and chronic organ pathology",
            "Eggs reaching freshwater continue the cycle by hatching into miracidia"
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
        distribution=[
            "S. mansoni: Widespread in sub-Saharan Africa; also present in parts of South America (e.g., Brazil, Venezuela, Suriname) and the Caribbean; sporadic foci in the Arabian Peninsula",
            "S. haematobium: Predominantly Africa with limited foci in the Middle East",
            "S. japonicum: East and Southeast Asia — endemic in China, the Philippines, and parts of Indonesia (Sulawesi); eliminated from Japan",
            "S. mekongi: Focal transmission along the Mekong River basin (Cambodia, Laos)",
            "S. intercalatum / S. guineensis: Restricted to Central and West Africa (e.g., Democratic Republic of the Congo for S. intercalatum)",
            "Hybrid schistosomes (e.g., S. haematobium × animal species): Reported in parts of West Africa and occasionally Europe (e.g., Corsica, France)"
        ],
        settings=["Freshwater lakes/rivers", "Irrigation/agricultural exposure"],
        seasonality=["Often linked to water contact patterns and snail ecology"],
        preferred_specimens=["Urine (midday; terminal stream) for S. haematobium", "Stool for intestinal species"],
        primary_tests=[
            "Microscopic identification of eggs in stool or urine (species-directed testing)",
            "Stool examination for S. mansoni and S. japonicum (direct smear plus concentration techniques such as formalin–ethyl acetate)",
            "Urine examination for S. haematobium (midday collection; centrifugation or filtration methods)",
            "Quantitative egg assessment using Kato–Katz thick smear (field and epidemiologic use)"
        ],
        confirmatory_or_adjunct=[
            "Repeat examinations and concentration procedures to improve sensitivity (intermittent egg shedding common)",
            "Urine filtration through polycarbonate membrane for egg quantification in S. haematobium infection",
            "Tissue biopsy (rectal or bladder) demonstrating eggs when stool/urine tests are negative but suspicion remains high",
            "Serology (antibody detection) useful for exposure assessment, especially in travelers or low-burden infection; does not reliably distinguish active from past infection",
            "Circulating antigen assays (e.g., CCA/CAA where available) for active infection assessment",
            "Ultrasound or cross-sectional imaging to evaluate chronic complications (periportal fibrosis, urinary tract disease)"
        ],
        microscopy_cues=[
            "Schistosoma mansoni eggs: large (≈114–180 µm × 45–70 µm), elongated-oval with a prominent lateral spine near the posterior end",
            "Anterior end typically tapered and slightly curved; shell thin and non-operculated",
            "Eggs are embryonated when passed in stool and contain a fully developed miracidium",
            "Lateral spine position is a key feature distinguishing S. mansoni from other human schistosomes",
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
        syndromes={
        "GI—diarrhea",
        "Malabsorption syndrome",
        "Post-infectious functional GI disorder"
    },
        short_overview=(
        "Noninvasive flagellated protozoan of the proximal small intestine causing ",
        "acute or chronic malabsorptive diarrhea. Transmission is fecal–oral via ",
        "environmentally resistant cysts, commonly through contaminated water or ",
        "person-to-person spread. Disease severity ranges from asymptomatic carriage ",
        "to prolonged nutrient malabsorption."
    ),
        reservoir=["Humans", "Animals can be reservoirs (assemblage-dependent)"],
        transmission=["Fecal–oral (cysts)", "Contaminated water", "Person-to-person (daycare)"],
        life_cycle_key_points=[
            "Infective stage is the quadrinucleate cyst, which is immediately infectious upon excretion and environmentally robust",
            "Cysts remain viable for months in cold freshwater and show relative resistance to conventional chlorination; inactivation requires boiling, filtration (<1 µm), or iodination",
            "Transmission occurs via ingestion of cysts through contaminated water, food, or fecal–oral exposure (including person-to-person and fomites)",
            "Excystation is triggered in the duodenum by gastric acid exposure followed by pancreatic enzymes and bile salts, releasing two binucleate trophozoites per cyst",
            "Trophozoites colonize the proximal small intestine (duodenum and jejunum) and attach to enterocytes via a ventral adhesive disc without tissue invasion",
            "Replication occurs by longitudinal binary fission, leading to high luminal parasite burdens that interfere with absorptive function",
            "Pathophysiology involves mechanical disruption of the brush border, microvillus shortening, enzyme deficiencies (e.g., lactase), and altered epithelial permeability → malabsorption",
            "Encystation is induced during distal transit as bile concentration and cholesterol availability change, producing environmentally resistant cysts",
            "Cysts predominate in formed stools, whereas trophozoites are more commonly detected in diarrheal specimens",
            "Intermittent shedding of cysts contributes to diagnostic variability and facilitates ongoing transmission",
            "Person-to-person spread is epidemiologically important, particularly in daycare settings and institutions",
            "Zoonotic transmission occurs with certain assemblages (A and B infect humans), though the relative reservoir contribution of animals varies by region"
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
        confirmatory_or_adjunct=[
            "Ova and parasite (O&P) microscopy with concentration techniques (e.g., formalin-ethyl acetate)",
            "Duodenal aspirate or biopsy demonstrating trophozoites (rarely required)",
            "String test (Entero-Test) to sample duodenal contents in selected cases"
        ],
        microscopy_cues=[
            "Trophozoites: pear/teardrop-shaped, bilaterally symmetric, two nuclei giving 'face-like' appearance, ventral adhesive disc",
            "Motility: falling-leaf pattern in fresh wet mount",
            "Cysts: oval, thick-walled, 4 nuclei when mature, internal axonemes and median bodies"
        ],
        common_pitfalls=[
            "Single stool examination has limited sensitivity due to intermittent cyst shedding",
            "Trophozoites rapidly degrade outside the host, reducing microscopy yield in delayed specimens",
            "Microscopy cannot distinguish assemblages and may miss low parasite burdens",
            "False-negative antigen tests may occur early in infection",
            "Symptoms may persist post-treatment due to secondary lactose intolerance or post-infectious IBS"
        ],
        prevention=[
            "Boiling or filtering untreated water (≤1 micron filter)",
            "Hand hygiene, especially in childcare settings",
            "Avoid swallowing recreational water",
            "Proper sanitation and sewage treatment",
            "Exclude symptomatic food handlers from work until treated"
        ],
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
            "Ingestion of mature quadrinucleate cysts → excystation in small intestine",
            "Trophozoites colonize large intestine and multiply by binary fission",
            "Adherence to colonic epithelium via Gal/GalNAc lectin → cytotoxicity and tissue invasion",
            "Formation of characteristic flask-shaped ulcers in colon",
            "Hematogenous spread via portal circulation → liver abscess (most common extraintestinal site)",
            "Encystation in colon → cysts passed in stool (infective stage)"
        ],
        incubation_or_timeline=["Variable; can be acute or develop after chronic colonization"],
        typical_presentations=[
            "Amebic colitis: abdominal pain, bloody diarrhea/tenesmus",
            "Amebic liver abscess: fever, RUQ pain (often without diarrhea)",
        ],
        severe_complications=[
            "Fulminant necrotizing colitis with perforation",
            "Toxic megacolon",
            "Peritonitis",
            "Rupture of liver abscess into pleural, pericardial, or peritoneal spaces",
            "Brain abscess (rare, high mortality)"
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
            "Trophozoites (15–30 µm) with active directional motility",
            "Ingested erythrocytes within trophozoites — pathognomonic for E. histolytica",
            "Cysts: spherical, 10–20 µm, up to 4 nuclei when mature",
            "Chromatoid bodies with rounded ends"
        ],
        common_pitfalls=[
            "Misclassification with nonpathogenic Entamoeba spp. if relying on microscopy only",
            "Antibiotics/antiparasitics can reduce detection in stool",
        ],
        prevention=[
            "Safe drinking water (boiling, filtration)",
            "Food hygiene and sanitation",
            "Hand hygiene and safe sexual practices"
        ],
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
            "Female Anopheles mosquito inoculates sporozoites during blood meal → rapid invasion of hepatocytes",
            "Exoerythrocytic schizogony in liver → maturation into hepatic schizonts → rupture releases merozoites into bloodstream",
            "Dormant hypnozoite stage persists in liver in P. vivax and P. ovale → potential relapses months–years later",
            "Merozoites invade erythrocytes → asexual erythrocytic cycle (ring → trophozoite → schizont)",
            "Synchronous RBC rupture releases merozoites and pyrogenic factors → periodic fever paroxysms, hemolysis",
            "Subset differentiates into sexual forms (microgametocytes, macrogametocytes)",
            "Gametocytes ingested by mosquito → sporogonic cycle in vector (zygote → ookinete → oocyst → sporozoites)",
            "Sporozoites migrate to mosquito salivary glands → transmission to next human host"
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
        distribution=[
            "Endemic in tropical and subtropical regions where Anopheles vectors sustain transmission (typically <1,500 m altitude)",
            "Highest burden in sub-Saharan Africa (predominantly P. falciparum)",
            "South and Southeast Asia, Western Pacific, and parts of the Americas maintain significant transmission",
            "P. vivax widely distributed outside Africa; P. ovale concentrated in sub-Saharan Africa but overlapping with P. vivax in some regions",
            "P. malariae occurs at lower prevalence with broad global distribution across Africa, Asia, and the Americas",
            "P. knowlesi zoonotic malaria occurs in Southeast Asia (notably Malaysia and surrounding regions)",
            "Focal transmission persists on the Korean peninsula",
            "Current distribution influenced by climate, vector ecology, urbanization, control programs, and human migration"
        ],
        settings=["Vector exposure", "Rural endemic zones"],
        seasonality=["Often increases in rainy seasons (vector-dependent)"],
        preferred_specimens=["Peripheral blood"],
        primary_tests=[
            "Thick blood smear — most sensitive for parasite detection",
            "Thin blood smear — species identification and parasitemia quantification",
            "Rapid diagnostic tests (HRP2/pLDH antigen detection) as adjunct"
        ],
        confirmatory_or_adjunct=[
            "PCR for species confirmation in reference laboratories",
            "Repeat smears every 12–24 hours (total 3 sets) if initial negative",
            "Quantification of parasite density for severity assessment"
        ],
        microscopy_cues=[
            "Thick smear: sensitive screening for parasites",
            "Thin smear: species features + parasitemia quantification",
            "P. falciparum: multiple delicate ring forms per RBC, appliqué forms, banana-shaped gametocytes",
            "P. vivax: enlarged RBCs with Schüffner dots",
            "P. ovale: oval RBCs with fimbriated edges",
            "P. malariae: band-form trophozoites across RBC",
            "P. knowlesi: resembles P. malariae but high parasitemia"
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
    "© Parasitic Platform • Intelligent Platform for Parasitic Diseases 2026 • Penchom Janwan"
    "</div>",
    unsafe_allow_html=True,
)
