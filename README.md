# AI Research Agent

An AI-powered research assistant that searches ArXiv for academic papers, summarizes them using a local LLM, and generates professional PDF reports with theme analysis and research gap identification.

## Features

- **ArXiv search** — fetches the most relevant papers on any topic
- **LLM summarization** — generates concise 3-sentence summaries per paper using a local Ollama model
- **Theme analysis** — identifies common themes, key findings, and open research problems across papers
- **PDF report generation** — exports a styled, professional research brief as a PDF
- **Multiple interfaces** — CLI, Flask web app, and ReAct agent loop

## Project Structure

```
ai-research-agent/
├── agent.py          # CLI entry point (simple sequential agent)
├── app.py            # Flask web app with async job processing
├── react_agent.py    # ReAct-pattern agent with tool use
├── fetcher.py        # ArXiv paper fetching
├── summarizer.py     # LLM-based paper summarization
├── pdf_exporter.py   # PDF report generation (ReportLab)
├── templates/
│   └── index.html    # Web UI (dark mode, live status polling)
└── requirements.txt
```

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally
- LLaMA 3.2 model pulled:
  ```bash
  ollama pull llama3.2:1b
  ```

## Installation

```bash
git clone https://github.com/GuruSelvam2003/ai-research-agent.git
cd ai-research-agent
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### CLI Agent

```bash
python agent.py
```

Enter a research topic when prompted. Outputs a PDF report and a markdown summary.

### Flask Web App

```bash
python app.py
```

Open `http://localhost:5000` in your browser. Enter a topic, watch live progress, and download the PDF when done.

### ReAct Agent

```bash
python react_agent.py
```

An agentic loop that reasons step-by-step using tools (search, summarize, identify gaps) before producing a final analysis.

## How It Works

1. **Fetch** — queries ArXiv API for the top 5 relevant papers
2. **Summarize** — sends each paper's abstract to a local LLM to generate a structured summary
3. **Analyze** — prompts the LLM to identify common themes, key findings, and research gaps across all papers
4. **Export** — compiles everything into a formatted PDF using ReportLab

## Tech Stack

| Component | Library |
|---|---|
| LLM interface | `langchain-ollama` |
| Paper source | `arxiv` |
| Web framework | `flask` |
| PDF generation | `reportlab` |
| LLM runtime | Ollama (local) |
