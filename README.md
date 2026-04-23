# Platform QA POC

A small standalone Python proof of concept for answering questions about your platform from:
- Markdown documentation
- an OpenAPI / Swagger spec

It uses:
- FastAPI for the API
- local TF-IDF retrieval for cheap local search
- optional LLM generation via AWS Bedrock or an OpenAI-compatible endpoint
- a mock answer mode so the project works even without model credentials

## Why this is a good POC

This proves the core loop before you spend money or build infrastructure:
1. ingest docs
2. chunk docs by headers/sections
3. convert OpenAPI into searchable reference text
4. retrieve relevant chunks
5. answer with citations

## Project structure

```text
platform_qa_poc/
├─ app/
├─ data/
│  ├─ docs/
│  └─ openapi.yaml
├─ scripts/
├─ tests/
├─ requirements.txt
└─ README.md
```

## Quick start

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate it

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Copy environment file

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

### 5. Run the API

```bash
uvicorn app.main:app --reload
```

### 6. Open the docs

Visit:
- `http://127.0.0.1:8000/docs`

## Example requests

### Health check

```bash
curl http://127.0.0.1:8000/health
```

### Ask a question

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"How does report generation work?"}'
```

### Rebuild the index after editing docs

```bash
curl -X POST http://127.0.0.1:8000/reindex
```

## Adding your real docs

Replace the sample files under `data/docs/` with your actual Markdown docs.

Suggested first docs:
- `glossary.md`
- `reporting.md`
- `client-lifecycle.md`
- `roles-and-permissions.md`
- `troubleshooting.md`

## OpenAPI handling

Place your Swagger or OpenAPI file at:

```text
data/openapi.yaml
```

The ingestion step will convert each path + method into searchable text chunks.

## LLM modes

### Mock mode

Default:

```env
LLM_PROVIDER=mock
```

This creates a grounded answer from the retrieved chunks without calling an external model.

### AWS Bedrock mode

```env
LLM_PROVIDER=bedrock
BEDROCK_MODEL_ID=your-model-id
AWS_REGION=us-east-1
```

Make sure your AWS credentials are available in the environment or local AWS profile.

### OpenAI-compatible mode

```env
LLM_PROVIDER=openai_compatible
OPENAI_BASE_URL=https://your-endpoint/v1
OPENAI_API_KEY=your-key
OPENAI_MODEL=your-model-name
```

## Recommended documentation approach without Mintlify

Use plain Markdown in Git.

A good low-cost setup is:
- Markdown docs in your repo
- MkDocs for a docs site
- Material for MkDocs theme if you want a polished UI

That gives you:
- versioned docs
- easy authoring
- static hosting
- a clean source corpus for your RAG pipeline

## Good next steps after the POC

1. swap TF-IDF for embeddings + pgvector/OpenSearch
2. add metadata filters by feature / role / version
3. add auth-aware retrieval
4. add evaluation cases
5. connect to Bedrock in production
