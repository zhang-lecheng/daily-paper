import arxiv
import datetime
import os
import json
import yaml
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configuration
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-1936b4530c074806b9398e016aa5f1ec")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
CATEGORIES = ["cs.AI", "cs.LG", "stat.ML", "q-bio.QM", "physics.comp-ph", "math.OC"]
MAX_RESULTS = 50
HISTORY_FILE = "papers_history.json"

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

import time

def fetch_arxiv_papers():
    print("Fetching papers from arXiv...")
    query = " OR ".join([f"cat:{cat}" for cat in CATEGORIES])
    client_arxiv = arxiv.Client(
        page_size=MAX_RESULTS,
        delay_seconds=3,
        num_retries=5
    )
    
    search = arxiv.Search(
        query=query,
        max_results=MAX_RESULTS,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    papers = []
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            results = list(client_arxiv.results(search))
            for result in results:
                papers.append({
                    "id": result.entry_id,
                    "title": result.title,
                    "summary": result.summary.replace("\n", " "),
                    "authors": [author.name for author in result.authors],
                    "url": result.entry_id,
                    "published": result.published.strftime("%Y-%m-%d")
                })
            return papers
        except arxiv.HTTPError as e:
            if "429" in str(e) and attempt < max_attempts - 1:
                wait_time = (attempt + 1) * 30
                print(f"Rate limited (429). Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print(f"ArXiv API error: {e}")
                break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
    return papers

def filter_papers(papers):
    print(f"Filtering {len(papers)} papers using DeepSeek...")
    relevant_papers = []
    
    # Load history to avoid duplicates
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    else:
        history = []

    for paper in papers:
        if paper["id"] in history:
            continue
            
        prompt = f"""
        Analyze the following academic paper abstract and determine its relevance to two specific fields:
        1. AI4Science (using AI for scientific discovery, simulation, or data analysis in biology, chemistry, physics, etc.)
        2. Perturbation Prediction (specifically predicting cell responses to chemical or genetic perturbations).

        Paper Title: {paper["title"]}
        Abstract: {paper["summary"]}

        Respond in JSON format:
        {{
            "is_ai4science": boolean,
            "is_perturbation_prediction": boolean,
            "reason": "short explanation in Chinese"
        }}
        """
        
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that classifies academic papers."},
                    {"role": "user", "content": prompt}
                ],
                response_format={'type': 'json_object'}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            if result.get("is_ai4science") or result.get("is_perturbation_prediction"):
                paper["ai4science"] = result.get("is_ai4science")
                paper["perturbation"] = result.get("is_perturbation_prediction")
                paper["reason"] = result.get("reason")
                relevant_papers.append(paper)
            
            # Add to history regardless of relevance to avoid re-processing
            history.append(paper["id"])
            
        except Exception as e:
            print(f"Error processing paper {paper['id']}: {e}")

    # Save history
    with open(HISTORY_FILE, "w") as f:
        json.dump(history[-500:], f) # Keep last 500
        
    return relevant_papers

def update_readme(relevant_papers):
    print(f"Updating README with {len(relevant_papers)} papers...")
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    content = f"\n\n## {today}\n\n"
    if not relevant_papers:
        content += "No relevant papers found today.\n"
    else:
        for paper in relevant_papers:
            tags = []
            if paper.get("ai4science"): tags.append("AI4Science")
            if paper.get("perturbation"): tags.append("Perturbation Prediction")
            
            tag_str = " ".join([f"`{t}`" for t in tags])
            content += f"### [{paper['title']}]({paper['url']})\n"
            content += f"- **Authors**: {', '.join(paper['authors'])}\n"
            content += f"- **Date**: {paper['published']}\n"
            content += f"- **Tags**: {tag_str}\n"
            content += f"- **AI Reason**: {paper['reason']}\n\n"

    # Append to README.md
    mode = "a" if os.path.exists("README.md") else "w"
    with open("README.md", mode, encoding="utf-8") as f:
        if mode == "w":
            f.write("# Daily AI4Science & Perturbation Prediction Papers\n\n")
        f.write(content)

if __name__ == "__main__":
    new_papers = fetch_arxiv_papers()
    relevant = filter_papers(new_papers)
    update_readme(relevant)
