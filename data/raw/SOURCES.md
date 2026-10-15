# MYJobLens Source Inventory

Every public source the RAG draws from. Each row = one URL/file + date downloaded.
Snapshot date: 15-Oct-2026. Re-run `python -m ingestion.run_ingest` to refresh.

| #  | Title                                                                                      | Type     | URL                                                                                                                                                                                          | Downloaded    | Used for                                                 |
|----|--------------------------------------------------------------------------------------------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|----------------------------------------------------------|
| 02 | AI Engineering Careers in Malaysia 2026: Roles, Skills & Salaries Mapped (Seekers.my)     | HTML→MD  | https://seekers.my/blog/ai-engineering-careers-in-malaysia-2026-the-roles-skills-salaries-mapped/                                                                                          | 15-Oct-2026   | Role-by-role salary medians + demand-frequency by skill  |
| 03 | AI Jobs Market in Malaysia: Skills, Salaries & Opportunities (BusinessPlusAI)              | HTML→MD  | https://www.businessplusai.com/blog/ai-jobs-market-in-malaysia-skills-salaries-and-opportunities-you-need-to-know                                                                          | 15-Oct-2026   | Salary bands, hot-roles list, talent-gap numbers         |
| 04 | Data Scientist & AI Engineer Salary Malaysia 2026: What the Live Job Market Pays (Seekers) | HTML→MD  | https://seekers.my/blog/data-scientist-ai-engineer-salary-in-malaysia-2026-what-the-live-job-market-actually-pays/                                                                        | 15-Oct-2026   | DS/AI-specific salary ranges, by year of experience      |
| 05 | AI and Machine Learning Specialist — career guide (Job.MY)                                 | HTML→MD  | https://job.my/blog/ai-and-machine-learning-specialist/                                                                                                                                       | 15-Oct-2026   | Definition of role + standard skills employers expect     |
| 06 | Cara Jadi AI Engineer di Malaysia — Roadmap Lengkap 2026 (CaraAI.my)                       | HTML→MD  | https://caraai.my/cara-jadi-ai-engineer-di-malaysia-roadmap-lengkap-2026/                                                                                                                  | 15-Oct-2026   | AI-engineer career ladder, Bahasa Melayu source          |
| 07 | (reserved for DOSM government PDF, found via browser)                                       | PDF      | TBD                                                                                                                                                                                          | -             | Authoritative government salary/wage statistics          |
| 08 | (reserved for Kaggle/anonymised MY job-postings CSV)                                       | CSV      | TBD                                                                                                                                                                                          | -             | Structured salary-by-role table for SQL-style queries    |

## Why these five first

- Seekers.my gives *measured* medians from 4,081 candidate profiles + live postings (Aug 2026). Highest-quality Malaysian-specific source.
- BusinessPlusAI provides independent corroboration with annual salary bands and talent-gap stats.
- The Seekers DS/AI-specific article sharpens the salary-by-experience story.
- Job.MY is a generic role-requirements reference (defines what employers expect).
- CaraAI.my is a Bahasa Melayu source, useful for cross-language questions.

## How each answer must cite these

Every chatbot reply cites the chunk number it drew from, which traces back to one of these 8 URLs.
A claim with no source = the LLM is hallucinating; the system prompt forbids this.

## Adding a new source

1. Drop the file in this `data/raw/` folder.
2. Add a row to this table.
3. Bump the "Snapshot date" at the top.
4. Re-run `python -m ingestion.run_ingest` to embed it into the vector DB.
5. Re-run `make eval` to confirm retrieval quality still meets the target hit-rate.
