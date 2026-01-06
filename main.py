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
CATEGORIES = ["cs.AI", "cs.LG", "stat.ML", "q-bio.QM", "physics.comp-ph", "math.OC", "cs.CE", "cs.MS", "cs.NE"]
MAX_RESULTS = 100
HISTORY_FILE = "papers_history.json"
DATA_DIR = "data"
DATES_FILE = os.path.join(DATA_DIR, "available_dates.json")

os.makedirs(DATA_DIR, exist_ok=True)

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
    processed_papers = []
    
    # Load history to avoid re-processing the same papers if they reappear
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    else:
        history = []

    for paper in papers:
        # Check if already processed (history is just IDs)
        if paper["id"] in history:
            # We skip AI processing but we still want to show it in today's list if it's new today
            # Actually, the user wants "daily" crawl. If a paper was crawled yesterday, it's stale.
            continue
            
        prompt = f"""
        Analyze the following academic paper abstract and evaluate its relevance:
        1. Is it AI4Science (using AI/ML for scientific discovery, simulation, or data analysis in biology, chemistry, physics, materials, climate, etc.)?
        2. If (and only if) it is AI4Science, is it specifically about Perturbation Prediction (predicting cellular, genetic, or chemical responses to perturbations like drug treatments, gene knockouts, etc.)?

        Paper Title: {paper["title"]}
        Abstract: {paper["summary"]}

        Respond in JSON format:
        {{
            "ai4science": boolean,
            "perturbation": boolean,
            "reason": "Short explanation in Chinese why it is or isn't AI4Science/Perturbation"
        }}
        """
        
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a specialized scientific paper classifier. Be concise and precise."},
                    {"role": "user", "content": prompt}
                ],
                response_format={'type': 'json_object'}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            paper["ai4science"] = result.get("ai4science", False)
            paper["perturbation"] = result.get("perturbation", False)
            paper["reason"] = result.get("reason", "")
            
            processed_papers.append(paper)
            history.append(paper["id"])
            
        except Exception as e:
            print(f"Error processing paper {paper['id']}: {e}")

    # Save history
    with open(HISTORY_FILE, "w") as f:
        json.dump(history[-1000:], f) 
        
    return processed_papers

def save_daily_data(papers):
    today = datetime.date.today().strftime("%Y-%m-%d")
    daily_file = os.path.join(DATA_DIR, f"{today}.json")
    
    # Save today's papers
    with open(daily_file, "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)
    
    # Update available dates
    if os.path.exists(DATES_FILE):
        with open(DATES_FILE, "r") as f:
            dates = json.load(f)
    else:
        dates = []
    
    if today not in dates:
        dates.append(today)
        dates.sort(reverse=True)
        with open(DATES_FILE, "w") as f:
            json.dump(dates, f)
    
    return today

if __name__ == "__main__":
    new_papers = fetch_arxiv_papers()
    processed = filter_papers(new_papers)
    if processed:
        save_daily_data(processed)
        update_readme(processed) # Keep README as backup/log
    else:
        print("No new papers to process today.")
