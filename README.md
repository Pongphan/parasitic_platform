# Parasitic Platform

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

Phase 1 — A Parasitic Platform Project (Complete)
• ปรับโครงสร้างของ web applications
• เพิ่มโมดูล parasite atlas
• เพิ่มโมดูล parasite research
• ปรับโครงสร้างของการทำงานในหน้า parasite detection
• เพิ่ม roadmap ในส่วนของ about

Phase 2 — Atlas and Advancd AI (Current)
• แก้ bug ของ web applications
• เพิ่มเนื้อหาในส่วน parasite atlas ฉบับสมบูรณ์
• เพิ่มความแม่นยำของโมเดลในหน้า parasite detection
• ปรับรูปแบบการรายงานผล


Phase 3 — Research Level
• แก้ bug ของ web application
• พัฒนาเนื้อหาในส่วนของ parasite research ให้สมบูรณ์
• เพิ่มโมดูล การค้นหางานวิจัยจากฐานข้อมูลเปิด และการทำ meta-analysis
• deploy ใน stable server
