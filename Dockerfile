# ============================================================
# ship5-ibm-granite-agentic-evidenceflow — Containerized RAG Pipeline
# Copyright (c) 2026 Evelyn Caro. All rights reserved.
# ============================================================

FROM python:3.13-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY . .

# Ollama runs on the host. Container connects via host.docker.internal.
ENV OLLAMA_HOST=http://host.docker.internal:11434

# Run the demo
CMD ["python", "Ship5_IBM_Granite_Agentic_RAG_EvidenceFlow_demo.py"]
