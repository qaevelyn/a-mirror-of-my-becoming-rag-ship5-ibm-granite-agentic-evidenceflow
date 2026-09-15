#!/usr/bin/env python
# coding: utf-8

# # Ship 5: IBM Granite Agentic RAG with EvidenceFlow Verification
# 
# ## Credits & Attribution
# 
# **Foundation:**
# This notebook is built on the foundational structure and methods learned from the IBM SkillsBuild lab:
# "Build a LangChain agentic RAG system using the Granite-4-H-Small model in watsonx.ai."
# 
# Original lab authored by Anna Gutowska.
# IBM SkillsBuild, 2026.
# 
# **Inspiration:**
# The evidence verification layer (evidence IDs, citation verification, fail-closed behavior) was inspired by Asaif Ali's EvidenceFlow project.
# https://github.com/AsaifAli/EvidenceFlow
# 
# **My Additions:**
# - EvidenceFlow verification layer (evidence IDs, citation verification, fail-closed behavior)
# - Local sovereign execution (Ollama, no watsonx.ai cloud dependency)
# - Genealogy-specific adaptations (partial names, phonetic matching)
# - Containerized "Mirror of Becoming" output format

# In[1]:


get_ipython().system(' echo "::group::Install Dependencies"')
get_ipython().run_line_magic('pip', 'install uv')
get_ipython().system(' uv pip install "git+https://github.com/ibm-granite-community/utils.git"      langchain_core      langchain_classic      langchain_community      langchain_text_splitters      langchain_ollama      chromadb      tiktoken      bs4')
get_ipython().system(' echo "::endgroup::"')


# In[2]:


# imports
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_classic.tools import tool
from langchain_classic.tools.render import render_text_description_and_args
from langchain_classic.agents.output_parsers import JSONAgentOutputParser
from langchain_classic.agents.format_scratchpad import format_log_to_str
from langchain_classic.agents import AgentExecutor
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.runnables import RunnablePassthrough


# In[ ]:


## Define the agent's RAG tool and initialize the agent

**Step 3: Initialize a basic agent with no tools.**

This step establishes a baseline. By running the agent without tools first, we can see what the LLM generates on its own - then compare it to the tool-enhanced version later.

**Parameters:**
- Model: `granite4.1:3b` (via Ollama)
- Temperature: 0.7
- Stop sequences: `Observation`, `Human:` (to prevent hallucinations)

**Why this matters:**
- The agent needs to know when to stop generating
- Without stop sequences, it may continue past the desired output
- With tools, the agent can retrieve real evidence instead of guessing

**My setup:**
- All models run locally on my M1 MacBook Air
- No cloud dependencies - sovereign by design


# In[3]:


from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="granite4.1:3b",
    temperature=0.7,
)


# We'll set up a prompt template in case you want to ask multiple questions. 

# In[4]:


template = "Answer the {query} accurately. If you do not know the answer, simply say you do not know."
prompt = ChatPromptTemplate.from_template(template)


# And now we can set up a chain with our prompt and our LLM. This allows the generative model to produce a response.

# In[5]:


agent = prompt | llm | StrOutputParser()


# In[ ]:


2. EVIDENCEFLOW VERIFICATION LAYER 

import uuid
from datetime import datetime

# Evidence Registry
evidence_registry = {}

def assign_evidence_id(chunk, source):
    """Assign a unique evidence ID to a chunk."""
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    uid = str(uuid.uuid4())[:8]
    evidence_id = f"EVI-{timestamp}-{uid}"
    evidence_registry[evidence_id] = {
        "chunk": chunk,
        "source": source,
        "timestamp": timestamp
    }
    return evidence_id

def generate_citation(evidence_id):
    """Generate a citation for a given evidence ID."""
    return f"[{evidence_id}]"

def verify_claims(answer, evidence_ids):
    """Check that each claim in the answer has a corresponding evidence ID."""
    for eid in evidence_ids:
        if eid not in evidence_registry:
            return False, f"Evidence ID {eid} not found in registry"
    return True, "All evidence verified"

def answer_with_verification(query, retriever, llm):
    """Retrieve, generate, and verify before returning."""
    # Retrieve
    docs = retriever.get_relevant_documents(query)

    # Assign evidence IDs
    evidence_ids = []
    for doc in docs:
        eid = assign_evidence_id(doc.page_content, doc.metadata.get("source", "unknown"))
        evidence_ids.append(eid)

    # Generate answer
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt_text = f"Based on the following context, answer the query.\n\nContext: {context}\n\nQuery: {query}\n\nAnswer:"
    response = llm.invoke(prompt_text)

    # Verify
    verified, message = verify_claims(response.content, evidence_ids)
    if not verified:
        return f"⚠️ Cannot verify answer. {message}"

    # Add citations
    citations = " ".join([generate_citation(eid) for eid in evidence_ids])
    return f"{response.content}\n\n{'-'*40}\n📎 Citations: {citations}"


# Let's test to see how our agent responds to a basic query. 

# In[6]:


agent_executor.invoke({"input": "What is A Mirror of My Becoming?"})


# The agent successfully responded to the basic query with the correct answer. In the next step of this tutorial, we will be creating a RAG tool for the agent to access relevant information about IBM's involvement in the 2025 US Open. As we have covered, traditional LLMs cannot obtain current information on their own. Let's verify this.

# In[7]:


agent_executor.invoke({"input": "How does A Mirror of My Becoming use AI and sovereignty?"})


# Evidently, the LLM is unable to provide us with the relevant information. The training data used for this model contained information prior to the 2025 US Open and without the appropriate tools, the agent does not have access to this information. 

# In[ ]:


Step 4. Establish the knowledge base and retriever


# In[8]:


# YOUR WORKING RETRIEVAL CODE (from Ship 3/4)
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma

# Set up Ollama
llm = ChatOllama(model="granite4.1:3b")
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Connect to your ChromaDB
vector_store = Chroma(
    collection_name="deepseek_conversations",
    embedding_function=embeddings,
    persist_directory="/Users/evelyn/Documents/Mirror-Project/vector_db"
)

# Create retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 4})

# Test it
print(retriever.get_relevant_documents("What is A Mirror of My Becoming?"))


# Next, load the documents using LangChain `WebBaseLoader` for the URLs we listed. We'll also print a sample document to see how it loaded.

# In[9]:


docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]
docs_list[0]


# In order to split the data in these documents to chunks that can be processed by the LLM, we can use a text splitter such as `RecursiveCharacterTextSplitter`. This text splitter splits the content on the following characters: ["\n\n", "\n", " ", ""]. This is done with the intention of keeping text in the same chunks, such as paragraphs, sentences and words together. 
# 
# Once the text splitter is initiated, we can apply it to our `docs_list`.

# In[10]:


text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250, chunk_overlap=0
)
doc_splits = text_splitter.split_documents(docs_list)


# The embedding model that we are using is an IBM Granite model through the [watsonx.ai embeddings service](https://ibm.github.io/watsonx-ai-python-sdk/fm_embeddings.html). Let's initialize it.

# In[11]:


embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
)


# In order to store our embedded documents, we will use Chroma DB, an open source vector store. 

# In[12]:


vectorstore = Chroma.from_documents(
    documents=doc_splits,
    collection_name="agentic-rag-chroma",
    embedding=embeddings,
)


# To access information in the vector store, we must set up a retriever. 

# In[13]:


retriever = vectorstore.as_retriever()


# In[ ]:


## Define the agent's RAG tool and initialize the agent

**Step 3: Initialize a basic agent with no tools.**

This step establishes a baseline. By running the agent without tools first, we can see what the LLM generates on its own - then compare it to the tool-enhanced version later.

**Parameters:**
- Model: `granite4.1:3b` (via Ollama)
- Temperature: 0.7
- Stop sequences: `Observation`, `Human:` (to prevent hallucinations)

**Why this matters:**
- The agent needs to know when to stop generating
- Without stop sequences, it may continue past the desired output
- With tools, the agent can retrieve real evidence instead of guessing

**My setup:**
- All models run locally on my M1 MacBook Air
- No cloud dependencies - sovereign by design


# In[14]:


@tool
def get_mirror_context(question: str):
    """Retrieve information from A Mirror of My Becoming project documents."""
    context = retriever.invoke(question)
    return context


# ## Step 6. Establish the prompt template
# 
# Next, we will set up a new prompt template to ask multiple questions. This template is more complex. It is referred to as a [structured chat prompt](https://api.python.langchain.com/en/latest/agents/langchain.agents.structured_chat.base.create_structured_chat_agent.html#langchain-agents-structured-chat-base-create-structured-chat-agent) and can be used for creating agents that have multiple tools available. In our case, the tool we are using was defined in Step 6. The structured chat prompt will be made up of a `system_prompt`, a `human_prompt` and our RAG tool. 
# 
# First, we will set up the `system_prompt`. This prompt instructs the agent to print its "thought process," which involves the agent's subtasks, the tools that were used and the final output. This gives us insight into the agent's function calling. The prompt also instructs the agent to return its responses in JSON Blob format.

# In[15]:


system_prompt = """Respond to the human as helpfully and accurately as possible. You have access to the following tools: {tools}
Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).
Valid "action" values: "Final Answer" or {tool_names}
Provide only ONE action per $JSON_BLOB, as shown:"
```
{{
  "action": $TOOL_NAME,
  "action_input": $INPUT
}}
```
Follow this format:
Question: input question to answer
Thought: consider previous and subsequent steps
Action:
```
$JSON_BLOB
```
Observation: action result
... (repeat Thought/Action/Observation N times)
Thought: I know what to respond
Action:
```
{{
  "action": "Final Answer",
  "action_input": "Final response to human"
}}
Begin! Reminder to ALWAYS respond with a valid json blob of a single action.
Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation"""


# In the following code, we are establishing the `human_prompt`. This prompt tells the agent to display the user input followed by the intermediate steps taken by the agent as part of the `agent_scratchpad`.

# In[16]:


human_prompt = """{input}
{agent_scratchpad}
(reminder to always respond in a JSON blob)"""


# Next, we establish the order of our newly defined prompts in the prompt template. We create this new template to feature the `system_prompt` followed by an optional list of messages collected in the agent's memory, if any, and finally, the `human_prompt` which includes both the human input and `agent_scratchpad`.

# In[17]:


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", human_prompt),
    ]
)


# Now, let's finalize our prompt template by adding the tool names, descriptions and arguments using a [partial prompt template](https://python.langchain.com/v0.1/docs/modules/model_io/prompts/partial/). This allows the agent to access the information pertaining to each tool including the intended use cases and also means we can add and remove tools without altering our entire prompt template.

# In[18]:


prompt = prompt.partial(
    tools=render_text_description_and_args(list(tools)),
    tool_names=", ".join([t.name for t in tools]),
)


# ## Step 7. Set up the agent's memory and chain
# 
# An important feature of AI agents is their memory. Agents are able to store past conversations and past findings in their memory to improve the accuracy and relevance of their responses going forward. In our case, we will use LangChain's `ConversationBufferMemory()` as a means of memory storage. 

# In[19]:


memory = ConversationBufferMemory()


# And now we can set up a chain with our agent's scratchpad, memory, prompt and the LLM. The AgentExecutor class is used to execute the agent. It takes the agent, its tools, error handling approach, verbose parameter and memory as parameters.

# In[20]:


chain = (
    RunnablePassthrough.assign(
        agent_scratchpad=lambda x: format_log_to_str(x["intermediate_steps"]),
        chat_history=lambda x: memory.chat_memory.messages,
    )
    | prompt
    | llm
    | JSONAgentOutputParser()
)

agent_executor = AgentExecutor(
    agent=chain, tools=tools, handle_parsing_errors=True, verbose=True, memory=memory
)


# ## Step 8. Generate responses with the agentic RAG system
# 
# We are now able to ask the agent questions. Recall the agent's previous inability to provide us with information pertaining to the 2025 US Open. Now that the agent has its RAG tool available to use, let's try asking the same questions again. 

# In[21]:


agent_executor.invoke({"input": "What are the RAG pipelines in the Mirror fleet?"})


# Great! The agent used its available RAG tool to return the location of the 2025 US Open, per the user's query. We even get to see the exact document that the agent is retrieving its information from. Now, let's try a slightly more complex question query. This time, the query will be about IBM's involvement in the 2025 US Open. 

# In[ ]:


agent_executor.invoke({"input": "What is the Ida B. Wells Standard of record keeping?"})


# In[ ]:


Again, the agent was able to successfully retrieve the relevant information pertaining to the user query. Additionally, the agent is successfully updating its knowledge base as it learns new information and experiences new interactions as seen by the history output.


# In[ ]:


agent_executor.invoke({"input": "What is the EvidenceFlow verification layer?"})


# As seen in the AgentExecutor chain, the agent recognized that it had the information in its knowledge base to answer this question without using its tools. 
