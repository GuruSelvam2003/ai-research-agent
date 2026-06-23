from fetcher import fetch_papers
from summarizer import summarize_paper
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3.2:1b", num_gpu=0)

def analyze_themes(summaries_text):
    prompt = f"""You are a research analyst. Based on the following paper summaries, provide:

1. COMMON THEMES: What topics or approaches appear across multiple papers?
2. KEY FINDINGS: What are the most important discoveries?
3. OPEN PROBLEMS: What gaps or future research directions are mentioned?

Summaries:
{summaries_text}

Analysis:"""
    return llm.invoke(prompt)

def run_agent(topic, max_papers=5):
    print(f"\n{'='*60}")
    print(f"🔍 Research Agent Starting...")
    print(f"📚 Topic: {topic}")
    print(f"{'='*60}\n")

    # Step 1: Fetch papers
    print("📡 Fetching papers from ArXiv...")
    papers = fetch_papers(topic, max_results=max_papers)
    print(f"✅ Found {len(papers)} papers\n")

    # Step 2: Summarize each paper
    summaries = []
    for i, paper in enumerate(papers):
        print(f"📄 Summarizing paper {i+1}/{len(papers)}: {paper['title'][:60]}...")
        summary = summarize_paper(paper)
        summaries.append({
            "title": paper["title"],
            "url": paper["url"],
            "published": paper["published"],
            "summary": summary
        })

    # Step 3: Analyze themes
    print("\n🧠 Analyzing themes and gaps...")
    summaries_text = "\n\n".join([
        f"Paper {i+1}: {s['title']}\n{s['summary']}"
        for i, s in enumerate(summaries)
    ])
    analysis = analyze_themes(summaries_text)

    # Step 4: Export PDF
    print("\n📄 Generating PDF report...")
    from pdf_exporter import export_to_pdf
    pdf_file = export_to_pdf(topic, summaries, analysis)

    print(f"\n✅ Done! Report saved to {pdf_file}")
    report = f"""
# Research Brief: {topic}

## Papers Analyzed
{'='*60}
"""
    for s in summaries:
        report += f"""
### {s['title']}
- **Published:** {s['published']}
- **URL:** {s['url']}
- **Summary:** {s['summary']}
"""

    report += f"""
## Overall Analysis
{'='*60}
{analysis}
"""

    # Save to file
    filename = topic.replace(" ", "_") + "_report.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)

    print(report)
    print(f"\n✅ Report saved to {filename}")

# Run it
if __name__ == "__main__":
    topic = input("Enter research topic: ")
    run_agent(topic, max_papers=5)