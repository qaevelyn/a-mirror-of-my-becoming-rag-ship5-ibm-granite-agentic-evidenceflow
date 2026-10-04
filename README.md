# Ship 5 — IBM Granite Agentic RAG with EvidenceFlow Verification — Local

**The ship that refuses to guess.**

Ship 5 of A Mirror of My Becoming™. Built August–September 2026 on an 8 GB Intel MacBook Air. Runs fully local: IBM Granite 4.1 (3B) and nomic-embed-text via Ollama, with an EvidenceFlow verification layer over the RAG core. Every retrieval is assigned a traceable evidence ID. Fail-closed by design.

**Author:** Evelyn Caro

---

## What it does

The local RAG core — corpus, chunking, embeddings, Chroma store — plus the EvidenceFlow layer, implemented in ~30 lines of verifiable code:

1. Every retrieved chunk is assigned an evidence ID: `EVI-YYYY-MM-DD-HHMMSS-uuid8`
2. Each ID is tracked in an evidence registry with its chunk content, source, and timestamp
3. Before an answer ships, `verify_claims()` checks every evidence ID against the registry
4. **If an ID is missing from the registry, verification fails — and the system reports it instead of answering**

The verification layer is additive to the RAG core, not a replacement: Ship 4's agentic pattern stays, EvidenceFlow wraps it.

---

## Why fail-closed matters

Every RAG system can retrieve. The question is what it does when the evidence is thin. Most answer anyway — fluently, confidently, sometimes wrong. EvidenceFlow inverts that: **an answer without evidence is not an answer; it is a guess wearing one.** Built for genealogy and any domain where a plausible guess costs more than admitting uncertainty. This is the ship where the documentation doctrine — every claim sourced, every gap flagged — became executable code.

---

## Requirements

- Python 3 with: `langchain`, `langchain-community`, `langchain-text-splitters`, `langchain-ollama`, `langchain-chroma`, `uuid`, `datetime`
- [Ollama](https://ollama.com) running locally, with `granite4.1:3b` and `nomic-embed-text` pulled
- `data/CURATED_PUBLIC_DATA.md` — your own corpus

---

## Quickstart

1. Install the packages named at the top of Ship5_IBM_Granite_Agentic_RAG_EvidenceFlow_demo.py
2. Pull the models: ollama pull granite4.1:3b && ollama pull nomic-embed-text
3. Put your corpus in data/CURATED_PUBLIC_DATA.md
4. Run: python3 Ship5_IBM_Granite_Agentic_RAG_EvidenceFlow_demo.py
Watch the evidence registry fill as the system retrieves.
text


---


---

## The fleet

- **[Ship 1](https://github.com/qaevelyn/a-mirror-of-my-becoming-rag-ship1-deepseek-rag-local)** — DeepSeek RAG, rebuilt local after AWS lost the original
- **[Ship 2](https://github.com/qaevelyn/a-mirror-of-my-becoming-rag-ship2-ibm-granite-agentic)** — IBM Granite Agentic RAG
- **[Ship 3](https://github.com/qaevelyn/a-mirror-of-my-becoming-rag-ship3-ibm-granite)** — IBM Granite Standard RAG
- **[Ship 4](https://github.com/qaevelyn/a-mirror-of-my-becoming-rag-ship4-ibm-granite-agentic)** — IBM Granite Agentic RAG
- **[Ship 5](https://github.com/qaevelyn/a-mirror-of-my-becoming-rag-ship5-ibm-granite-agentic-evidenceflow)** — IBM Granite Agentic RAG with EvidenceFlow

**[Suite: Ingestion Tools](https://github.com/qaevelyn/a-mirror-of-my-becoming-suite-ingestion-tools)** — the tooling that gets documents into the vector stores these ships read from.

**[A Mirror of My Becoming™](https://github.com/qaevelyn/a-mirror-of-my-becoming)** — the parent index for the entire practice.

**[Fleet index + SETUP.md](https://github.com/qaevelyn/a-mirror-of-my-becoming-rag-pipelines)** — how to point any ship at your own corpus.

---


## License

Dual-licensed:

- **AGPL-3.0** — free to use, modify, and redistribute under the terms of the license. Full text in [LICENSE](LICENSE).
- **Commercial license** — available for organizations that need to use the code without the AGPL-3.0 obligations. Contact the author for pricing.

Free does not mean free to exploit. If you build a product on this work, the author expects to be paid.

---

## Author

**Evelyn Caro** — Sovereign AI Builder.

**[qaevelyn.github.io](https://qaevelyn.github.io)** · Commercial licensing: **evelyn.caro.cloud@gmail.com**

---

© 2026 Evelyn Caro. All rights reserved.
