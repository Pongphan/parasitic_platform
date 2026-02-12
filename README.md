# Parasitic Platform (Streamlit)

A modular, expert-grade Streamlit web application for **parasitology education**, **research planning**, and **AI-assisted microscopy** using **TensorFlow SavedModel / .keras**.

---

## ✨ What this app includes

### 1) Home (Card Navigation)
- A beautiful landing page with **full-card clickable navigation** (no new tabs).
- Consistent dark, “premium” theme across all pages.

### 2) Human Parasite
- Detailed educational content with structured sections (e.g., **overview**, **epidemiology**, **diagnosis**).
- Designed to be easily extended into species-level pages.

### 3) Parasitology Research
- A detailed map of research branches:
  - Epidemiology & surveillance
  - Diagnostics & clinical parasitology
  - Molecular parasitology & genomics
  - Immunology & host–parasite interactions
  - Vector biology & medical entomology
  - Drug discovery & resistance
  - Environmental / One Health
  - AI / digital parasitology
  - Implementation science & program evaluation
- Includes a **Project Builder** to generate a publishable study blueprint.

### 4) Parasitic Vision (AI)
- Upload microscopy images (JPG/PNG/TIF)
- Select TensorFlow model (SavedModel or `.keras`)
- Run inference → visualize output → export results
- Supports:
  - Detection mode (TF Object Detection API SavedModel)
  - Classification mode (default for `.keras`)
  - Optional tiling for large images
  - Export annotated PNG, detection CSV, and YOLO `.txt` labels

### 5) About Project
- Vision, scope, architecture, QA & governance, roadmap, FAQ.
