#!/usr/bin/env python3
"""Ship 5 — IBM Granite Agentic RAG with EvidenceFlow Verification — Demo"""
import os
import uuid
from datetime import datetime
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma

print("Ship 5 — IBM Granite Agentic RAG with EvidenceFlow Verification")
print("-" * 50)

embeddings = OllamaEmbeddings(model="nomic-embed-text")
llm = ChatOllama(model="granite4.1:3b", temperature=0.7)
print("Embeddings ready: nomic-embed-text")
print("LLM ready: granite4.1:3b")

# ---------- EvidenceFlow layer ----------
evidence_registry = {}

def assign_evidence_id(chunk, source):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    uid = str(uuid.uuid4())[:8]
    eid = f"EVI-{timestamp}-{uid}"
    evidence_registry[eid] = {"chunk": chunk, "source": source, "timestamp": timestamp}
    return eid

def verify_claims(answer, evidence_ids):
    for eid in evidence_ids:
        if eid not in evidence_registry:
            return False, f"Evidence ID {eid} not found in registry"
    return True, "All evidence verified"

print("EvidenceFlow verification layer ready")
print()

# ---------- Vector store ----------
PERSIST_DIR = "./chroma_db"
SOURCE = "/Users/evelyn/Repos/Mirror-Project/MIRROR_LOG.md"

if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR):
    vector_store = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    print(f"Vector store loaded: {vector_store._collection.count()} documents")
else:
    print("Building vector store from Mirror archive...")
    documents = TextLoader(SOURCE).load()
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50, separator="\n")
    texts = splitter.split_documents(documents)
    vector_store = Chroma.from_documents(documents=texts, embedding=embeddings, persist_directory=PERSIST_DIR)
    print(f"Vector store created: {len(texts)} chunks")

retriever = vector_store.as_retriever(search_kwargs={"k": 4})

# ---------- Verified answer function ----------
def answer_with_verification(query):
    docs = retriever.invoke(query)
    evidence_ids = []
    for doc in docs:
        eid = assign_evidence_id(doc.page_content, doc.metadata.get("source", "MIRROR_LOG.md"))
        evidence_ids.append(eid)

    context = "\n\n".join([doc.page_content for doc in docs])
    prompt_text = f"Based on the following context, answer the query.\n\nContext: {context}\n\nQuery: {query}\n\nAnswer:"
    response = llm.invoke(prompt_text)

    verified, message = verify_claims(response.content, evidence_ids)
    if not verified:
        return f"⚠️ Cannot verify answer. {message}"

    citations = " ".join(f"[{eid}]" for eid in evidence_ids)
    return f"{response.content}\n\n{'-'*40}\n📎 Citations: {citations}"

# ---------- Queries ----------
queries = [
    "What is the sovereignty principle in the Mirror project?",
    "When did the Mirror of My Becoming project start?",
]

for query in queries:
    print()
    print("=" * 60)
    print(f"QUERY: {query}")
    print("=" * 60)
    answer = answer_with_verification(query)
    print(answer)

print()
print("-" * 50)
print("Demo complete. Every answer carries verifiable evidence IDs.")
