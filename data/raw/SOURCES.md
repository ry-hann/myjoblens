\# 📚 MYJobLens Source Inventory



> Every public source the RAG draws from. Each one = one URL/PDF + a date downloaded.

> \*\*Snapshot date: 14-Oct-2026.\*\* Re-run `python -m ingestion.download` to refresh.



| #  | Title                                              | Type     | Source / URL                                          | Downloaded    | Used for                                    |

|----|----------------------------------------------------|----------|-------------------------------------------------------|---------------|---------------------------------------------|

| 01 | DOSM Salaries \& Wages Statistics, Q1 2026          | PDF      | https://www.dosm.gov.my                              | 14-Oct-2026   | Sector + wage statistics                    |

| 02 | Seekers.my — AI Engineering Careers in MY 2026      | HTML→MD  | https://seekers.my/blog/ai-engineering-careers-in-malaysia-2026-the-roles-skills-salaries-mapped/ | 14-Oct-2026 | Role-by-role skills \& salary medians        |

| 03 | BusinessPlusAI — AI Jobs Market in MY 2026         | HTML→MD  | https://www.businessplusai.com/blog/ai-jobs-market-in-malaysia-skills-salaries-and-opportunities-you-need-to-know | 14-Oct-2026 | Salary benchmarks + talent-gap stats        |

| 04 | (reserved for next source)                         | -        | -                                                     | -             | -                                           |

| 05 | (reserved for next source)                         | -        | -                                                     | -             | -                                           |



\## Why these three first



\- \*\*DOSM\*\* = authoritative government source. Required for credibility.

\- \*\*Seekers.my\*\* = most-cited 2026 article specifically about AI/ML jobs in MY. Used by recruiters.

\- \*\*BusinessPlusAI\*\* = independent corroboration with different datasets. Diversity reduces single-source bias.



\## What "Used for" means in this table



Each chatbot answer must cite at least one source from this list. The "Used for" column makes it easy

to answer auditors, evaluators, and yourself in 6 months.



\## Adding a new source



1\. Add a row above with the next number.

2\. Update the "Snapshot date" line above.

3\. Re-run `python -m ingestion.run\_ingest` to embed it into the vector DB.

