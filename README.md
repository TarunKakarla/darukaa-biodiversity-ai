# Darukaa.Earth — AI Biodiversity Intelligence

Darukaa.Earth is an AI-powered biodiversity intelligence platform designed to help users understand environmental conditions, explore ecological relationships, and receive evidence-grounded recommendations.

The system combines Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), scientific literature retrieval, semantic embeddings, causal reasoning, environmental metrics, and interactive visualization.

---

## 1. What Darukaa.Earth Does

Users can ask natural-language environmental questions such as:

> How can I bring more wildlife back to my farmland?

or:

> How can agroforestry help support biodiversity in agricultural landscapes?

The system processes the question through an AI + RAG pipeline and produces:

- Scientific summary
- Recommended interventions
- Scientific reasoning
- Causal chains
- Impacted environmental metrics
- Time horizons
- Confidence levels
- Supporting scientific evidence
- Source titles and URLs
- Retrieved page information

The system is designed to understand both direct and indirect environmental questions.

For example, users do not necessarily need to use technical terms such as biodiversity, agroforestry, habitat diversity, species richness, or soil organic carbon. A natural-language question can be interpreted by the LLM and connected to relevant environmental concepts.

---

## 2. Core Architecture

```text
                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │  React Frontend │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   FastAPI API   │
                  └────────┬────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Question / Intent    │
                │ Understanding        │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Topic / Goal Focus   │
                │ + Environmental      │
                │ Context              │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Causal Reasoning     │
                │ Graph                │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Semantic Retrieval   │
                │ RAG / ChromaDB       │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Scientific Evidence │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ LLM Recommendation   │
                │ Generation           │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Structured JSON      │
                │ Response             │
                └──────────┬───────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ React Dashboard │
                  └─────────────────┘
```

---

## 3. AI Architecture

Darukaa.Earth uses a hybrid AI architecture.

### Large Language Model

The LLM handles:

- Natural-language understanding
- Question interpretation
- Environmental reasoning
- Recommendation generation
- Scientific explanations
- Structured response generation

### Retrieval-Augmented Generation

The RAG system provides the scientific evidence layer.

It:

1. Stores scientific documents
2. Splits documents into chunks
3. Generates semantic embeddings
4. Stores embeddings in ChromaDB
5. Retrieves relevant evidence for user questions
6. Provides retrieved evidence to the LLM

### Causal Reasoning Graph

The causal graph provides a structured ecological reasoning backbone.

Example:

```text
Rainfall
   ↓
Soil Moisture
   ↓
Vegetation Conditions
   ↓
Habitat Diversity
   ↓
Species Richness
```

Another example:

```text
Agroforestry
   ↓
Habitat Diversity
   ↓
Species Richness
```

The graph provides domain constraints and helps structure the reasoning process.

### Deterministic Rules

Some deterministic rules are intentionally used for:

- Topic detection
- Question classification
- Causal relationships
- Environmental reasoning constraints
- Response structure

These rules are used to constrain and support the AI rather than replace it.

The application therefore follows a hybrid approach:

```text
AI flexibility
      +
Scientific knowledge
      +
Deterministic constraints
      +
Retrieved evidence
```

---

## 4. Evidence-Grounded AI

A core principle of Darukaa.Earth is:

> The LLM should not invent scientific citations.

The LLM is instructed to use only the scientific evidence retrieved by the RAG system.

The system attempts to ensure that:

- Source titles come from retrieved evidence
- Source URLs come from retrieved evidence
- Page numbers come from retrieved metadata
- Scientific claims are grounded in retrieved text
- Unsupported numerical claims are avoided
- Sources not retrieved by the RAG system are not cited
- Evidence limitations are explicitly acknowledged

The intended reasoning hierarchy is:

```text
Retrieved Scientific Evidence
             ↓
       Causal Graph
             ↓
  Environmental Metrics
             ↓
       LLM Reasoning
             ↓
     Final Recommendation
```

---

## 5. Scientific Knowledge Base

The current RAG knowledge base includes major biodiversity and food-agriculture reports.

### FAO

**The State of the World's Biodiversity for Food and Agriculture**

Source:

https://www.fao.org/3/ca3129en/ca3129en.pdf

### Convention on Biological Diversity

**Global Biodiversity Outlook 5**

Source:

https://www.cbd.int/gbo/gbo5/publication/gbo-5-en.pdf

The current local ChromaDB knowledge base contains approximately **804 indexed chunks** from the configured sources.

Page-level metadata is retained where available.

---

## 6. RAG Pipeline

Scientific PDFs are processed page by page.

```text
PDF
 │
 ▼
PDF Text Extraction
 │
 ▼
Page-Level Processing
 │
 ▼
Text Chunking
 │
 ▼
Sentence Transformer
 │
 ▼
Vector Embeddings
 │
 ▼
ChromaDB
 │
 ▼
Semantic Query
 │
 ▼
Top-K Evidence Chunks
```

Current embedding model:

```text
all-MiniLM-L6-v2
```

Embeddings are normalized before storage and retrieval.

---

## 7. Environmental Metrics

The system supports environmental context including:

```text
soil_ph
soil_organic_carbon
soil_moisture
land_use_type
crop
species_richness
habitat_diversity
temperature
rainfall
pollution
deforestation
region
```

Example:

```json
{
  "soil_ph": 6.5,
  "soil_organic_carbon": 0.3,
  "soil_moisture": "low",
  "land_use_type": "monoculture",
  "crop": "wheat",
  "species_richness": 12,
  "habitat_diversity": 2,
  "temperature": 34,
  "rainfall": "low",
  "region": "semi-arid"
}
```

The AI uses these metrics as environmental context when generating recommendations.

---

## 8. Natural-Language Question Understanding

Darukaa.Earth is designed to support both direct and indirect questions.

### Direct Question

```text
How can agroforestry support biodiversity?
```

Possible interpretation:

```text
Topic:
Agroforestry

Goal:
Biodiversity
```

### Indirect Question

```text
How can I bring more wildlife back to my farmland?
```

The user does not explicitly mention:

- biodiversity
- species richness
- habitat diversity
- agroforestry

The LLM can interpret the user's intent and connect it to relevant ecological concepts and scientific evidence.

This allows the system to handle more natural user conversations instead of relying exclusively on exact keywords.

---

## 9. Example Interaction

### User

```text
How can I bring more wildlife back to my farmland?
```

### System

The system may identify relevant environmental factors such as:

```text
Wildlife
   ↓
Habitat Availability
   ↓
Habitat Diversity
   ↓
Species Richness
```

It can then retrieve scientific evidence and generate recommendations such as land-use diversification or habitat-supporting practices, depending on the retrieved evidence and environmental context.

Each recommendation can contain:

- What to do
- Why it works
- Causal chain
- Impacted metrics
- Time horizon
- Confidence
- Scientific evidence
- Source page

---

## 10. Frontend

The frontend is built using:

- React
- Vite
- React Flow
- Tailwind CSS

The interface provides:

### Scientist View

Used for:

- Asking environmental questions
- Viewing AI recommendations
- Reading scientific evidence
- Exploring ecological reasoning

### Environmental Profile

Used for:

- Environmental metrics
- Farm/environment context
- Conditions influencing recommendations

### Interactive Reasoning Graph

The application visualizes ecological relationships using React Flow.

Example:

```text
Rainfall
   ↓
Soil Moisture
   ↓
Habitat Diversity
   ↓
Species Richness
```

Custom React Flow nodes are used to represent different environmental concepts and interventions.

---

## 11. Backend

The backend is implemented using:

- Python
- FastAPI
- Pydantic
- ChromaDB
- Sentence Transformers
- OpenAI-compatible LLM API

Main API endpoint:

```text
POST /chat
```

Health endpoint:

```text
GET /health
```

API documentation:

```text
/docs
```

Local backend:

```text
http://127.0.0.1:8000
```

---

## 12. Project Structure

```text
darukaa_biodiversity_ai_react_full_project/
│
├── app/
│   ├── main.py
│   ├── pipeline.py
│   ├── models.py
│   │
│   ├── graph/
│   │   └── reasoning_graph.py
│   │
│   ├── memory/
│   │   └── session.py
│   │
│   ├── llm/
│   │   ├── client.py
│   │   └── prompt.py
│   │
│   └── rag/
│       └── store.py
│
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   │
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       └── index.css
│
├── scripts/
│   ├── ingest_sources.py
│   ├── retrieve_test.py
│   └── test_graph.py
│
├── tests/
│   └── test_graph.py
│
├── data/
│   ├── sources/
│   └── chroma/
│
├── streamlit_app.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## 13. Running Locally

### Backend

Activate the Conda environment:

```bash
conda activate darukaa
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
LLM_BASE_URL=YOUR_LLM_API_BASE_URL
LLM_API_KEY=YOUR_API_KEY
LLM_MODEL=auto

CHROMA_PATH=./data/chroma
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

## 14. Running the Frontend

Open another terminal.

Move into the frontend:

```bash
cd frontend
```

Install packages:

```bash
npm install
```

Start Vite:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

The frontend uses:

```env
VITE_API_URL=http://localhost:8000
```

to communicate with the backend.

---

## 15. Ingesting Scientific Sources

The RAG database must contain scientific sources before useful evidence-grounded responses can be generated.

Run:

```bash
PYTHONPATH=. python scripts/ingest_sources.py
```

The ingestion process:

1. Loads scientific documents
2. Extracts page text
3. Splits text into chunks
4. Generates embeddings
5. Stores chunks in ChromaDB
6. Stores source metadata
7. Stores page metadata where available

The current development database contains approximately:

```text
804 chunks
```

---

## 16. Testing Retrieval

Retrieval can be tested using:

```bash
PYTHONPATH=. python scripts/retrieve_test.py
```

This can be used to inspect which scientific evidence is retrieved for a query.

---

## 17. Testing the Causal Graph

Run:

```bash
PYTHONPATH=. python scripts/test_graph.py
```

Automated tests are located in:

```text
tests/
```

Run:

```bash
pytest
```

---

## 18. API Example

Example request:

```http
POST /chat
```

Example JSON:

```json
{
  "session_id": "demo",
  "message": "How can I bring more wildlife back to my farmland?",
  "metrics": {
    "soil_organic_carbon": 0.3,
    "soil_moisture": "low",
    "land_use_type": "monoculture",
    "crop": "wheat",
    "rainfall": "low",
    "region": "semi-arid"
  }
}
```

The API returns structured recommendation data.

---

## 19. Response Structure

The AI response follows a structured format:

```json
{
  "summary": "...",
  "recommendations": [
    {
      "what_to_do": "...",
      "why_it_works": "...",
      "causal_chain": [
        "...",
        "...",
        "..."
      ],
      "impacted_metrics": [
        "..."
      ],
      "time_horizon": "medium",
      "confidence": "medium",
      "evidence": [
        {
          "source_title": "...",
          "source_url": "...",
          "page_number": 67,
          "supporting_excerpt_or_summary": "..."
        }
      ]
    }
  ]
}
```

---

## 20. Design Philosophy

Darukaa.Earth follows a hybrid AI philosophy.

The system combines:

```text
LLM
 +
RAG
 +
Scientific Knowledge
 +
Causal Reasoning
 +
Environmental Data
 +
Deterministic Constraints
```

The deterministic components provide:

- Reliability
- Domain constraints
- Explainability
- Reproducibility
- Scientific structure

The LLM provides:

- Natural-language understanding
- Flexible reasoning
- Recommendation generation
- Scientific explanation

The RAG system provides:

- Evidence retrieval
- Source grounding
- Page-level scientific references

---

## 21. Current Limitations

Darukaa.Earth is currently a V1/MVP AI system.

### Hardcoded Domain Relationships

Some causal relationships are explicitly defined rather than automatically discovered.

### Topic Detection

Some topic classification still uses deterministic rules in addition to LLM understanding.

### Evidence Validation

The current system grounds recommendations in retrieved sources, but claim-level evidence verification can be improved.

### Confidence

Confidence is currently generated as part of the structured AI response and is not yet a calibrated statistical confidence score.

### Vector Database Persistence

Local ChromaDB is currently used for development.

Production deployment requires persistent storage or an external vector database.

### Evaluation

A comprehensive benchmark for retrieval quality and recommendation grounding is still a future improvement.

---

## 22. Future Development

Potential V2 improvements include:

### AI-Based Intent Extraction

Replace more deterministic topic rules with structured AI intent extraction.

```text
User Question
      ↓
AI Intent Extraction
      ↓
Topic
Goal
Context
Constraints
```

### Dynamic Causal Reasoning

Allow the system to construct candidate causal chains from retrieved scientific evidence while maintaining domain constraints.

### Claim-Level Evidence Validation

Validate individual scientific claims against retrieved evidence.

```text
Claim
 ↓
Evidence Retrieval
 ↓
Support Check
 ↓
Supported / Unsupported
```

### Retrieval Evaluation

Introduce metrics such as:

```text
Recall@5
Precision@5
MRR
Citation Accuracy
Evidence Coverage
```

### Recommendation Evaluation

Measure:

- Question relevance
- Scientific grounding
- Evidence quality
- Causal consistency
- User feedback

### Feedback Loop

Allow users to provide feedback such as:

```text
Helpful
Not Helpful
```

and use that information for system evaluation and improvement.

### Production Vector Database

For larger-scale deployment, replace local ChromaDB with a production vector database.

### Authentication and Security

Future versions can add:

- Authentication
- Rate limiting
- API protection
- User accounts
- Persistent sessions

---

## 23. Deployment

The intended deployment architecture is:

```text
                 Internet
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
       Vercel             Render
     React Frontend       FastAPI
                              │
                     ┌────────┴────────┐
                     │                 │
                     ▼                 ▼
                  ChromaDB           LLM API
```

Frontend:

```text
Vercel
```

Backend:

```text
FastAPI
```

Scientific retrieval:

```text
ChromaDB
```

LLM:

```text
OpenAI-compatible API
```

Environment variables must be configured on the deployment platform.

API keys must never be committed to GitHub or exposed in the frontend.

---

## 24. Security

Never commit:

```text
.env
```

to Git.

The `.env` file may contain:

```text
LLM_API_KEY
```

which must remain private.

Use:

```text
.env.example
```

to document required environment variables without exposing secrets.

---

## 25. Current Status

### Completed

- [x] React frontend
- [x] FastAPI backend
- [x] Environmental metrics
- [x] LLM integration
- [x] RAG pipeline
- [x] ChromaDB vector store
- [x] Sentence Transformer embeddings
- [x] Scientific PDF ingestion
- [x] Page-level evidence metadata
- [x] Causal reasoning graph
- [x] Interactive reasoning visualization
- [x] Session memory
- [x] Structured AI responses
- [x] Evidence-grounded recommendations
- [x] Natural-language question handling
- [x] Local development environment
- [x] Retrieval testing
- [x] Basic automated testing

---

## 26. Vision

Darukaa.Earth aims to evolve from an AI recommendation interface into an environmental intelligence system capable of connecting:

```text
Environmental Data
        +
Scientific Knowledge
        +
AI Reasoning
        +
Causal Relationships
        +
Evidence Validation
        +
Human Decision Making
```

The long-term goal is to provide transparent, evidence-grounded ecological intelligence rather than simply generating generic AI answers.

---

## License

Add the project's chosen license here before public release.
