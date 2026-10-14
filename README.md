🇲🇾 MYJobLens — Malaysian Job Insights RAG Chatbot

Ask anything about Malaysian jobs: salary, demand, skills, sector trends. Status: 🚧 in active development. See docs/PROJECT\_PLAN.md for the full spec.



What it is (one-paragraph pitch)

A Retrieval-Augmented Generation (RAG) chatbot that answers questions about the Malaysian job market using a curated, openly-cited snapshot of public sources — government statistics (DOSM, MDEC), salary surveys (Seekers.my, Glassdoor MY, Ricebowl), news articles, and anonymised job-posting datasets.



What it is NOT

❌ No live scraping of LinkedIn / JobStreet / Indeed (TOS-blocked).

❌ No paid APIs. Runs 100% on free, local tools.

❌ Not "real-time" — answers reflect the snapshot date (see data/raw/SOURCES.md).

Stack

Layer	Tool

Embeddings	BAAI/bge-small-en-v1.5 (free, local)

Vector store	ChromaDB (free, persisted to disk)

LLM	Ollama + Llama 3.1 8B (free, local)

Backend	FastAPI

Frontend	Streamlit

Deploy	Hugging Face Spaces (free CPU tier)

Reproduce

git clone https://github.com/<your-username>/myjoblens

cd myjoblens

make bootstrap     # install Ollama model + Python deps

make ingest        # download + embed the corpus

make eval          # run the golden-set eval, print the report

make run           # open http://localhost:8501



\## Project status \& docs



\- 📄 Full scope \& decisions — see \[`docs/PROJECT\_PLAN.md`](docs/PROJECT\_PLAN.md)

\- 📊 Evaluation results — see \[`eval/results/`](eval/results/)

\- 📂 Source citations — see \[`data/raw/SOURCES.md`](data/raw/SOURCES.md)



\## License



MIT



