from fetcher import fetch_papers
from summarizer import summarize_paper
from langchain_ollama import OllamaLLM
import json

llm = OllamaLLM(model="llama3.2:1b", num_gpu=0)

# ── Tool definitions ──────────────────────────────────────

def search_arxiv(query: str) -> str:
    papers = fetch_papers(query, max_results=3)
    if not papers:
        return "No papers found."
    result = ""
    for i, p in enumerate(papers):
        result += f"\nPaper {i+1}:\n"
        result += f"  Title: {p['title']}\n"
        result += f"  Published: {p['published']}\n"
        result += f"  Abstract: {p['abstract'][:300]}...\n"
    return result

def summarize_papers(query: str) -> str:
    papers = fetch_papers(query, max_results=3)
    if not papers:
        return "No papers found."
    summaries = ""
    for i, paper in enumerate(papers):
        summary = summarize_paper(paper)
        summaries += f"\nPaper {i+1}: {paper['title']}\n"
        summaries += f"Summary: {summary}\n"
        summaries += "-" * 40 + "\n"
    return summaries

def identify_gaps(summaries: str) -> str:
    prompt = f"""Based on these paper summaries, identify:
1. Common themes
2. Key findings  
3. Open problems and research gaps
4. Future directions

Summaries:
{summaries}

Analysis:"""
    return llm.invoke(prompt)

tools = {
    "search_arxiv": {
        "fn": search_arxiv,
        "description": "Search ArXiv for papers. Input: search query string."
    },
    "summarize_papers": {
        "fn": summarize_papers,
        "description": "Fetch and summarize papers on a topic. Input: research topic string."
    },
    "identify_gaps": {
        "fn": identify_gaps,
        "description": "Analyze summaries to find research gaps. Input: summaries text."
    }
}

# ── ReAct loop ────────────────────────────────────────────

def run_react_agent(topic: str, max_steps: int = 6):
    tools_desc = "\n".join([f"- {name}: {t['description']}" for name, t in tools.items()])
    
    system_prompt = f"""You are a research agent. Solve tasks step by step using tools.

Available tools:
{tools_desc}

Always respond in this EXACT format:
Thought: <your reasoning>
Action: <tool name>
Action Input: <input to tool>

When you have enough information, respond with:
Thought: <your reasoning>
Final Answer: <your complete answer>"""

    messages = [{"role": "user", "content": f"Research this topic thoroughly: {topic}"}]
    scratchpad = ""
    
    print(f"\n{'='*60}")
    print(f"🤖 ReAct Agent Started: {topic}")
    print(f"{'='*60}\n")

    for step in range(max_steps):
        print(f"--- Step {step + 1} ---")
        
        # Build prompt with full history
        full_prompt = system_prompt + "\n\n"
        for m in messages:
            full_prompt += f"{m['role'].upper()}: {m['content']}\n"
        full_prompt += scratchpad
        full_prompt += "\nThought:"

        response = "Thought:" + llm.invoke(full_prompt)
        print(response)
        scratchpad += "\n" + response

        # Check for Final Answer
        if "Final Answer:" in response:
            final = response.split("Final Answer:")[-1].strip()
            print(f"\n{'='*60}")
            print("✅ FINAL ANSWER:")
            print(f"{'='*60}")
            print(final)
            
            # Save report
            filename = topic.replace(" ", "_") + "_react_report.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"Research Brief: {topic}\n\n")
                f.write(final)
            print(f"\n💾 Saved to {filename}")
            return final

        # Parse Action and Action Input
        if "Action:" in response and "Action Input:" in response:
            try:
                action = response.split("Action:")[-1].split("\n")[0].strip()
                action_input = response.split("Action Input:")[-1].split("\n")[0].strip()

                print(f"\n🔧 Calling tool: {action}")
                print(f"📥 Input: {action_input}\n")

                if action in tools:
                    observation = tools[action]["fn"](action_input)
                else:
                    observation = f"Unknown tool: {action}. Available: {list(tools.keys())}"

                print(f"👁️ Observation: {observation[:200]}...\n")
                scratchpad += f"\nObservation: {observation}\n"

            except Exception as e:
                scratchpad += f"\nObservation: Error - {str(e)}\n"

    print("⚠️ Max steps reached.")

# ── Run ───────────────────────────────────────────────────

if __name__ == "__main__":
    topic = input("Enter research topic: ")
    run_react_agent(topic)