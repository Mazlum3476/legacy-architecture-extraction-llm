# Automated Architecture Extraction from Legacy Code with LLMs
This project aims to automatically extract software architecture from undocumented, complex, or legacy codebases using Large Language Models (LLMs) and Static Code Analysis.
The system performs a hybrid analysis using the Python `ast` library for structural parsing and Google Gemini models for semantic understanding to identify architectural patterns (Controller, Service, Repository) and business rules.

#Project Goal
To simplify the maintenance of legacy software by:
* [cite_start]Automatically detecting code modules, classes, and functions[cite: 7].
* [cite_start]Extracting relationships between components (calls, uses, depends on)[cite: 8, 20, 21, 22, 23].
* [cite_start]Generating high-level architectural descriptions and **C4 Model** diagrams in Mermaid/PlantUML format[cite: 9, 26, 27].

#Key Features
* [cite_start]**Hybrid Analysis:** Combines static analysis (`ast`) with AI-powered semantic analysis (`Gemini API`)[cite: 6, 39].
* [cite_start]**Pattern Detection:** Identifies Layered Architecture components such as Controllers, Services, and Repositories[cite: 19, 25].
* [cite_start]**Visualization:** Converts analysis results into renderable Mermaid diagram code[cite: 163].
* [cite_start]**Robust Error Handling:** Includes an automatic retry mechanism and model switching (e.g., swapping between Gemini 2.0 Flash, 1.5 Pro) to handle API rate limits (429 Too Many Requests) gracefully[cite: 191, 205].

**Görselleştirme**
```markdown
![Örnek Mimari Diyagramı](ornek_diyagram.jpg)

#Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/LLM-Architecture-Extractor.git](https://github.com/YOUR_USERNAME/LLM-Architecture-Extractor.git)
   cd LLM-Architecture-Extractor

   
