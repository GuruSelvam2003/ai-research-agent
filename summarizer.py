from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3.2:1b", num_gpu=0)

def summarize_paper(paper):
    prompt = f"""You are a research assistant. Given the following paper details, provide a concise 3-sentence summary covering:
1. What problem it solves
2. What method/approach it uses
3. What the key result or contribution is

Paper Title: {paper['title']}
Authors: {', '.join(paper['authors'])}
Abstract: {paper['abstract']}

Summary:"""

    summary = llm.invoke(prompt)
    return summary
