"""Validated Atlas profiles and filtering rules shared by the page and tests."""

import json
from dataclasses import dataclass, field, fields
from datetime import date
from pathlib import Path
from typing import List, Optional, Set


SYNDROME_LABELS = {
    "gi_diarrhea": "GI—diarrhea",
    "gi_obstruction": "GI—abdominal pain/obstruction",
    "gi_dysentery": "GI—bloody diarrhea/dysentery",
    "hepatobiliary": "Hepatobiliary",
    "pulmonary": "Pulmonary—cough/wheeze/eosinophilia",
    "travel_fever": "Fever—travel/vector exposure",
    "skin_pruritus": "Skin—pruritus/rash",
    "hematuria": "GU—hematuria",
    "neurological": "Neuro—seizure/focal deficit",
    "iron_deficiency": "Anemia—iron deficiency",
    "eosinophilia": "Eosinophilia (unexplained)",
}
SYNDROME_OPTIONS = list(SYNDROME_LABELS)
SYNDROME_IDS = {label: key for key, label in SYNDROME_LABELS.items()}


@dataclass
class ParasiteProfile:
    name: str
    group: str
    syndromes: Set[str]
    short_overview: str
    reservoir: List[str]
    transmission: List[str]
    life_cycle_key_points: List[str]
    incubation_or_timeline: List[str]
    typical_presentations: List[str]
    severe_complications: List[str]
    key_risk_groups: List[str]
    distribution: List[str]
    settings: List[str]
    seasonality: List[str]
    preferred_specimens: List[str]
    primary_tests: List[str]
    confirmatory_or_adjunct: List[str]
    microscopy_cues: List[str]
    common_pitfalls: List[str]
    prevention: List[str]
    syndrome_ids: Set[str]
    interpretive_comments: List[str] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)
    reviewed_on: Optional[str] = None
    reviewer: Optional[str] = None

    def __post_init__(self):
        for name in ("name", "group", "short_overview"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a nonempty string")
        for name in ("syndromes", "syndrome_ids"):
            value = getattr(self, name)
            if not isinstance(value, set) or not value or not all(
                isinstance(item, str) and item.strip() for item in value
            ):
                raise ValueError(f"{self.name}: {name} must be a nonempty set of strings")
        unknown = self.syndrome_ids - SYNDROME_LABELS.keys()
        if unknown:
            raise ValueError(f"{self.name}: unknown syndrome IDs {sorted(unknown)}")
        for item in fields(self):
            if item.type == List[str]:
                values = getattr(self, item.name)
                if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
                    raise ValueError(f"{self.name}: {item.name} must be a list of strings")
        for name in ("reviewed_on", "reviewer"):
            value = getattr(self, name)
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise ValueError(f"{self.name}: {name} must be a nonempty string or null")
        if self.reviewed_on is not None:
            date.fromisoformat(self.reviewed_on)


def load_profiles(path: Path) -> List[ParasiteProfile]:
    records = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("Atlas data must contain a list of profiles")
    profiles = []
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Each Atlas profile must be an object")
        record = dict(record)
        for name in ("syndromes", "syndrome_ids"):
            values = record.get(name)
            if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
                raise ValueError(f"{name} must be a list of strings")
            record[name] = set(values)
        profiles.append(ParasiteProfile(**record))
    names = [profile.name for profile in profiles]
    if len(set(names)) != len(names):
        raise ValueError("Atlas profile names must be unique")
    return profiles


def match_profile(p: ParasiteProfile, groups: List[str], syndromes: List[str], kw: str) -> bool:
    if p.group not in groups:
        return False
    selected_ids = {SYNDROME_IDS.get(value, value) for value in syndromes}
    if selected_ids and not p.syndrome_ids.intersection(selected_ids):
        return False
    keyword = kw.lower().strip()
    if not keyword:
        return True
    searchable = [p.name, p.group, p.short_overview, *sorted(p.syndromes)]
    searchable.extend(SYNDROME_LABELS[key] for key in sorted(p.syndrome_ids))
    for item in fields(p):
        if item.type == List[str]:
            searchable.extend(getattr(p, item.name))
    return keyword in " ".join(searchable).lower()


def score_candidate(p: ParasiteProfile, synd: str, exposure: str) -> int:
    score = 4 if SYNDROME_IDS.get(synd, synd) in p.syndrome_ids else 0
    exp = exposure.lower()
    tx = " ".join(p.transmission).lower()
    lc = " ".join(p.life_cycle_key_points).lower()
    settings = " ".join(p.settings).lower()

    if "water" in exp and ("water" in tx or "daycare" in tx or "oocyst" in tx):
        score += 2
    if "soil" in exp and ("soil" in tx or "skin" in tx):
        score += 2
    if "meat" in exp and ("undercooked" in tx or "pork" in tx or "beef" in tx):
        score += 2
    if "fish" in exp and "fish" in tx:
        score += 2
    if "freshwater swimming" in exp and ("freshwater" in tx or "cercariae" in lc or "snail" in lc):
        score += 2
    if "vector" in exp and ("mosquito" in tx or "anopheles" in tx):
        score += 3
    if "close-contact" in exp and ("household" in tx or "school" in settings or "skin-to-skin" in tx):
        score += 2
    if "immunosuppression" in exp and (
        "hyperinfection" in " ".join(p.severe_complications).lower()
        or "immuno" in " ".join(p.key_risk_groups).lower()
    ):
        score += 3
    return score


PROFILES = load_profiles(Path(__file__).parent / "data" / "parasite_profiles.json")
GROUPS = sorted({profile.group for profile in PROFILES})
