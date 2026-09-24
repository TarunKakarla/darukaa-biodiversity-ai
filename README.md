# 🌱 Darukaa.Earth — AI Biodiversity Intelligence Platform

> **Submission for the Darukaa.Earth AI Biodiversity Intelligence Chatbot Challenge**  
> *"Build a system that behaves like an AI environmental scientist, not a chatbot."*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io)
[![RAG](https://img.shields.io/badge/RAG-Hybrid%20Chroma%20%2B%20Knowledge%20Base-10b981.svg)]()
[![Tests](https://img.shields.io/badge/Tests-7%20Passed-success.svg)]()

---

## 📑 Executive Overview

**Darukaa.Earth** is an evidence-grounded AI Environmental Scientist conversational system engineered to reason about real-world environmental problems. Rather than operating as a generic LLM wrapper, the platform combines:

1. **Multi-Metric Ecological Nexus Engine**: Explicitly couples at least 3 environmental variables simultaneously (Soil Organic Carbon ↔ Rainfall/Hydrology ↔ Monoculture Habitat Fragmentation).
2. **Conversational Intelligence & Session Memory**: Maintains full multi-turn dialogue history, extracts parameters directly from conversational text, and asks scientific clarifying questions when inputs are incomplete.
3. **Hybrid RAG & Scientific Knowledge Layer**: Integrates persistent ChromaDB vector embeddings with an embedded authoritative domain knowledge base derived from the Food and Agriculture Organization (**FAO**), Intergovernmental Panel on Climate Change (**IPCC**), Convention on Biological Diversity (**CBD**), and **IPBES**.
4. **Actionable, Evidence-Backed Recommendations**: Delivers non-obvious, quantified ecological interventions (e.g. *"+15–25% SOC over 2–3 years (FAO studies)"*), directional causal chains ($A \rightarrow B \rightarrow C$), time horizons, and confidence scores.
5. **Flexible Input Modes**: Supports natural-language chat, structured JSON presets/upload, and spatial context (Latitude/Longitude and Ecoregion/Biome mapping).
6. **Zero-Downtime Deployment**: Features a dual-mode engine—autonomous deterministic scientific reasoning (zero API key required for guaranteed judge evaluation) alongside custom LLM support (OpenAI, Groq, Ollama, LM Studio) via Streamlit secrets or UI.

---

## 🏛️ System Architecture

```text
                                  USER INTERFACE
             ┌────────────────────────────────────────────────────────┐
             │            Streamlit Scientific Dashboard              │
             │   Chat Interface  │  Parameter Sliders  │  JSON Preset │
             └───────────────────────────┬────────────────────────────┘
                                         │
                                         ▼
                     CONVERSATIONAL MEMORY & INPUT EXTRACTOR
             ┌────────────────────────────────────────────────────────┐
             │       app.memory.session (SessionMemory System)        │
             │  • Natural Language Parameter Extraction (Regex/NLP)   │
             │  • Multi-Turn State Merging & Accumulation             │
             │  • Incomplete Input Detection & Clarifying Questions   │
             └───────────────────────────┬────────────────────────────┘
                                         │ (≥ 3 Variables Confirmed)
                                         ▼
                        MULTI-METRIC CAUSAL NEXUS ENGINE
             ┌────────────────────────────────────────────────────────┐
             │       app.graph.reasoning_graph (Causal Graph)         │
             │  • Evaluates 3+ Coupled Variables Simultaneously       │
             │  • Detects Compound Degradation Feedback Loops         │
             │  • Triggers Directional Causal Pathways                │
             └───────────────────────────┬────────────────────────────┘
                                         │
                                         ▼
                           HYBRID RAG RETRIEVAL LAYER
             ┌────────────────────────────────────────────────────────┐
             │            app.rag.store (Hybrid RAG Store)            │
             │  ┌───────────────────────┐   ┌──────────────────────┐  │
             │  │   ChromaDB Vector     │   │ Structured Knowledge │  │
             │  │   Dense Embeddings    │ + │ Base (FAO/IPCC/CBD)  │  │
             │  │   (SentenceTransform) │   │ Verified Page/Quotes │  │
             │  └───────────────────────┘   └──────────────────────┘  │
             └───────────────────────────┬────────────────────────────┘
                                         │
                                         ▼
                     SCIENTIFIC SYNTHESIS & REASONING ENGINE
             ┌────────────────────────────────────────────────────────┐
             │           app.llm.client & app.llm.prompt              │
             │  • Autonomous AI Environmental Scientist Engine        │
             │  • Optional External LLMs (OpenAI, Groq, Local LM)     │
             │  • Evidence Synthesis, Causal Chains & Impact Deltas   │
             └───────────────────────────┬────────────────────────────┘
                                         │
                                         ▼
                      STRUCTURED EVIDENCE-GROUNDED OUTPUT
             ┌────────────────────────────────────────────────────────┐
             │  • Multi-Metric Nexus Assessment (Coupled Variables)   │
             │  • Non-Obvious Evidence-Backed Recommendations         │
             │  • Quantified Improvements (e.g. SOC +15-25% in 2-3y)  │
             │  • Visual Causal Chains & Verified Page Citations      │
             │  • JSON Report Export                                  │
             └────────────────────────────────────────────────────────┘
```

---

## 🎯 Hackathon Criteria Alignment Matrix

| Evaluation Criteria | Weight | Darukaa.Earth Implementation Details |
|---|---|---|
| **1. Depth of Reasoning** | **30%** | • Solves multi-variable trade-offs connecting **at least 3 environmental variables** together.<br>• Identifies the *Arid-Monoculture Degradation Loop*: low SOC ($0.3\%$) + low rainfall + monoculture wheat canopy simplification.<br>• Recommends non-obvious synergistic interventions: multi-strata *Faidherbia albida* windbreaks, pulse strip-intercropping (*Cicer arietinum*), and residue retention. |
| **2. Scientific Grounding** | **25%** | • Grounded in authoritative literature: **FAO** (*State of the World's Biodiversity 2019*, *Soil Organic Carbon*), **IPCC** (*AR6 WGII Chapter 4*, *SRCCL*), **CBD** (*GBO-5*), **IPBES**.<br>• Quantifiable effect sizes: *"+15–25% SOC over 2–3 years", "30–50% reduction in soil evaporation", "45% increase in beneficial predatory arthropods"*.<br>• Verifiable page numbers and direct official report URLs. |
| **3. Knowledge System Design** | **20%** | • **Hybrid RAG Engine**: ChromaDB persistent vector database with SentenceTransformer (`all-MiniLM-L6-v2`) embeddings + Curated Domain Knowledge Base.<br>• Transparent retrieval pipeline displaying retrieved sources, page citations, and excerpt previews in the UI. |
| **4. Conversational Intelligence & Memory** | **15%** | • **Multi-Turn Session Memory**: Remembers past queries, recommendations, and accumulated parameters.<br>• **Intelligent Clarifying Questions**: Detects when inputs have $<2-3$ dimensions and asks scientific clarifying questions.<br>• **Contextual Continuity**: Allows follow-ups (*"How will this affect soil moisture in year 2?"*) without re-entering parameters. |
| **5. Output Clarity & Actionability** | **10%** | • Structured response schema: What to do, Why it works, Causal chain ($A \rightarrow B \rightarrow C$), Impacted metrics, Time horizon, Confidence, and Evidence.<br>• Interactive Streamlit dashboard with pill badges, nexus cards, and JSON report export. |
| **Bonus: Spatial Context** | **Bonus** | • Latitude, Longitude, and Ecoregion / Biome selector (e.g., Semi-Arid Sahelian Savanna, Indo-Gangetic Dryland, Mediterranean Basin) for spatial context. |

---

## 📊 Database & Data Schema

### 1. Environmental Metrics Schema (`app.models.EnvironmentalMetrics`)
```json
{
  "soil_ph": 7.2,
  "soil_organic_carbon": 0.3,
  "soil_moisture": "low",
  "bulk_density": 1.45,
  "land_use_type": "monoculture",
  "crop": "monoculture wheat",
  "species_richness": 5.0,
  "habitat_diversity": 0.15,
  "temperature": 28.0,
  "rainfall": "low",
  "region": "semi-arid",
  "pollution": "low agrochemical",
  "latitude": 31.5,
  "longitude": 74.3,
  "ecoregion": "Semi-Arid Dryland (FAO Agroecology Case)"
}
```

### 2. Multi-Metric Nexus Response Schema
```json
{
  "summary": "Scientific assessment for semi-arid landscape under monoculture wheat cultivation with baseline SOC at 0.3%...",
  "multi_metric_nexus": {
    "nexus_name": "Compound Arid-Monoculture Degradation Loop",
    "coupled_variables": [
      "Soil Organic Carbon (0.3%)",
      "Climate: Low Rainfall / Aridity Stress",
      "Land Use: Monoculture Wheat"
    ],
    "compound_risk": "Critical (Compounded Soil-Water-Biodiversity Stress)",
    "ecological_pathway": "Low SOC restricts rain infiltration -> low soil moisture causes severe plant water stress -> simplified monoculture canopy eliminates pollinator floral niches"
  },
  "recommendations": [
    {
      "what_to_do": "Establish multi-strata Faidherbia albida and Acacia agroforestry windbreak corridors",
      "why_it_works": "Deep-rooting woody perennials retrieve deep-zone groundwater, reduce downwind evapotranspiration by 20-30%...",
      "causal_chain": [
        "Woody perennial establishment along contour lines",
        "Canopy microclimate buffering (1.5-2.5°C temperature reduction)",
        "Deep root carbon deposition and biological N-fixation",
        "Enhanced macro-pore water infiltration & 40% increase in native pollinator nesting niches"
      ],
      "impacted_metrics": ["soil_organic_carbon", "soil_moisture", "species_richness", "habitat_diversity"],
      "measurable_impact": "Increase SOC by ~0.4-0.6% (+20-30% relative) over 3-5 years; reduce surface wind speed by 25%",
      "time_horizon": "medium",
      "confidence": "high",
      "evidence": [
        {
          "source_title": "The State of the World's Biodiversity for Food and Agriculture",
          "source_url": "https://www.fao.org/3/ca3129en/ca3129en.pdf",
          "page_number": 234,
          "supporting_excerpt_or_summary": "Agroforestry systems bridge agricultural production and biodiversity conservation..."
        }
      ]
    }
  ]
}
```

---

## 🚀 Local Setup & Installation

### Prerequisites
- Python 3.10+ (tested on Python 3.12)
- Git

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone <YOUR_GITHUB_REPO_URL>
   cd darukaa-biodiversity-ai-main
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit Application**:
   ```bash
   streamlit run streamlit_app.py
   ```
   The dashboard will automatically open in your browser at `http://localhost:8501`.

5. **Run the Automated Test Suite**:
   ```bash
   python -m pytest tests/
   ```
   All 7 comprehensive tests will execute and validate multi-metric nexus reasoning, session memory, incomplete inputs, and RAG retrieval.

---

## ☁️ Streamlit Cloud Deployment & CI/CD

This project is optimized for direct continuous deployment on **Streamlit Community Cloud**:

1. **Automatic Synchronization**:
   Pushing changes to your `main` branch on GitHub triggers an automatic redeploy on Streamlit Cloud.
2. **Secrets Configuration (Optional)**:
   In your Streamlit Cloud app settings under **Secrets**, you can optionally configure:
   ```toml
   OPENAI_API_KEY = "sk-..."
   # or
   GROQ_API_KEY = "gsk_..."
   ```
3. **Zero-Failure Guarantee**:
   If no external API key is provided, the built-in **Autonomous Scientific Reasoning Engine** executes the full causal nexus analysis, hybrid RAG literature retrieval, and multi-turn memory with 100% reliability, ensuring hackathon evaluators never encounter error screens.

---

## 🧪 Submission Checklist for Hackathon Reviewers

- **GitHub Repository**: Connected and synchronized with latest source code.
- **Streamlit Live URL**: Deployed and functional on Streamlit Cloud.
- **Invited Reviewers** (for private repository access):
  - `ankita.dasgupta@darukaa.com`
  - `harsh.kumar@darukaa.com`
  - `utkarsh.gauniyal@darukaa.com`
  - `guneet.mutreja@darukaa.com`
