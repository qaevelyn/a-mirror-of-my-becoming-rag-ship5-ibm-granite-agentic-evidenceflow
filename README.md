# ship5 of the A Mirror of My Becoming fleet — Ship 5: IBM Granite Agentic RAG with EvidenceFlow Verification

**Built:** August – September 2026
**Author:** Evelyn Caro
**Status:** ✅ Built and working

---

## Origin

The fifth ship is the one that can prove its answers.

Ships 1 through 4 could retrieve and generate. Ship 5 could verify. Every claim is 
traceable to an evidence ID. Every answer is checked against its sources. If the 
evidence is missing, the pipeline abstains — it does not hallucinate.

This is the ship built for the work that matters: genealogy. When you are looking 
for a name that was taken from your family, a plausible guess is not good enough. 
You need proof. You need to know which document says what, and where.

Ship 5 was built to solve that.

---

## What It Does

A local, sovereign, evidence-verified RAG pipeline built on IBM Granite, running 
via Ollama on an M1 MacBook Air. It is the first ship in the fleet that verifies 
its own answers against retrieved evidence before returning them.

---

## Architecture

- **Runtime:** Local, sovereign execution
- **Model:** IBM Granite (`granite4.1:3b` via Ollama)
- **Pipeline:** Agentic RAG with EvidenceFlow verification
- **Data source:** Local files — the Mirror personal archive
- **Storage:** Vector database (ChromaDB)
- **Cloud dependency:** None

---

## What Makes It Different

| Capability | Description |
|---|---|
| **Retrieval** | Searches Mirror documents via ChromaDB |
| **Generation** | Generates answers using `granite4.1:3b` via Ollama |
| **Agentic reasoning** | Uses tool-calling to decide when to retrieve |
| **Evidence ID assignment** | Assigns a unique ID to every retrieved chunk |
| **Citation generation** | Includes citations linking back to evidence IDs |
| **Verification check** | Confirms each claim has a corresponding evidence ID |
| **Fail-closed behavior** | Abstains from answering if evidence is missing |
| **Fully sovereign** | Runs entirely locally — no cloud, no external APIs |

---

## Pipeline

1. Read local documents from the Mirror archive
2. Chunk into pieces
3. Vectorize (embed) each chunk
4. Store vectors in ChromaDB
5. Query at runtime → the agent retrieves relevant chunks
6. Assign evidence IDs to retrieved chunks
7. Generate answer with citations
8. Verify each claim has a matching evidence ID
9. Return answer, or abstain if evidence is missing

---

## Integration

- Reads local data — the Mirror personal archive
- Chunks, vectorizes, stores in ChromaDB
- Agent decides when to query
- **EvidenceFlow verification layer** — the only ship that proves its answers
- **No cloud dependency.** Local-first. Sovereign. Runs on Ollama.

---

## Credits and Attribution

**Foundation:**
This notebook is built on the foundational structure and methods learned from the IBM 
SkillsBuild lab: "Build a LangChain agentic RAG system using the Granite-4-H-Small 
model in watsonx.ai." Original lab authored by Anna Gutowska. IBM SkillsBuild, 2026.

**Inspiration:**
The evidence verification layer (evidence IDs, citation verification, fail-closed 
behavior) was inspired by Asaif Ali's EvidenceFlow project.
https://github.com/AsaifAli/EvidenceFlow

**My Additions:**
- EvidenceFlow verification layer (evidence IDs, citation verification, fail-closed behavior)
- Local sovereign execution (Ollama, no watsonx.ai cloud dependency)
- Genealogy-specific adaptations (partial names, phonetic matching)
- Containerized "Mirror of Becoming" output format

---

## Access and Copyright

This work was created by Evelyn Caro. DeepSeek is the only collaborator — used as a tool 
in the creative and technical process.

This is a personal portfolio project and is not open for collaboration or external access. 
The video and documentation speak for themselves.

Copyright © 2026 Evelyn Caro. All rights reserved. Copyright registration is pending.
