from flask import Flask, render_template, request, jsonify, send_file
from fetcher import fetch_papers
from summarizer import summarize_paper
from pdf_exporter import export_to_pdf
from langchain_ollama import OllamaLLM
import threading
import uuid
import os

app = Flask(__name__)

# Store job results in memory
jobs = {}

def run_research_job(job_id, topic):
    try:
        llm = OllamaLLM(model="llama3.2:1b", num_gpu=0)
        jobs[job_id]["status"] = "Fetching papers from ArXiv..."

        papers = fetch_papers(topic, max_results=5)
        jobs[job_id]["status"] = f"Found {len(papers)} papers. Summarizing..."

        summaries = []
        for i, paper in enumerate(papers):
            jobs[job_id]["status"] = f"Summarizing paper {i+1}/{len(papers)}..."
            summary = summarize_paper(paper)
            summaries.append({
                "title": paper["title"],
                "url": paper["url"],
                "published": paper["published"],
                "summary": summary
            })

        jobs[job_id]["status"] = "Analyzing themes and research gaps..."
        summaries_text = "\n\n".join([
            f"Paper {i+1}: {s['title']}\n{s['summary']}"
            for i, s in enumerate(summaries)
        ])

        analysis_prompt = f"""Based on these paper summaries, identify:
1. Common themes and approaches
2. Key findings
3. Open problems and research gaps
4. Future research directions

Summaries:
{summaries_text}

Analysis:"""
        analysis = llm.invoke(analysis_prompt)

        jobs[job_id]["status"] = "Generating PDF..."
        pdf_filename = f"{job_id}_report.pdf"
        export_to_pdf(topic, summaries, analysis, filename=pdf_filename)

        jobs[job_id].update({
            "status": "done",
            "summaries": summaries,
            "analysis": analysis,
            "pdf_file": pdf_filename
        })

    except Exception as e:
        jobs[job_id]["status"] = f"error: {str(e)}"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/research", methods=["POST"])
def research():
    topic = request.json.get("topic", "").strip()
    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = {"status": "Starting...", "topic": topic}

    thread = threading.Thread(target=run_research_job, args=(job_id, topic))
    thread.daemon = True
    thread.start()

    return jsonify({"job_id": job_id})


@app.route("/status/<job_id>")
def status(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job)


@app.route("/download/<job_id>")
def download(job_id):
    job = jobs.get(job_id)
    if not job or "pdf_file" not in job:
        return jsonify({"error": "PDF not ready"}), 404
    return send_file(job["pdf_file"], as_attachment=True,
                     download_name=f"{job['topic'].replace(' ','_')}_report.pdf")


if __name__ == "__main__":
    app.run(debug=True, port=5000)