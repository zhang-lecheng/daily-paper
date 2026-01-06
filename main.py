import arxiv
import datetime
import os
import json
import yaml
from openai import OpenAI
from dotenv import load_dotenv
import time

load_dotenv()

# Configuration
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-1936b4530c074806b9398e016aa5f1ec")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
CATEGORIES = ["cs.AI", "cs.LG", "stat.ML", "q-bio.QM", "physics.comp-ph", "math.OC", "cs.CE", "cs.MS", "cs.NE"]
MAX_RESULTS = 100
DATA_DIR = "data"
DATES_FILE = os.path.join(DATA_DIR, "available_dates.json")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

os.makedirs(DATA_DIR, exist_ok=True)

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

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
    try:
        results = list(client_arxiv.results(search))
        for result in results:
            papers.append({
                "id": result.entry_id,
                "title": result.title,
                "summary": result.summary.replace("\n", " "),
                "authors": [author.name for author in result.authors],
                "url": result.entry_id,
                "published": result.published.strftime("%Y-%m-%d"),
                "primary_category": result.primary_category
            })
    except Exception as e:
        print(f"Error fetching from arXiv: {e}")
    
    return papers

def process_with_ai(papers):
    print(f"Processing {len(papers)} papers with AI...")
    processed = []
    for paper in papers:
        prompt = f"""Title: {paper['title']}
Abstract: {paper['summary']}

Analyze if this paper is related to:
1. AI4Science (using AI for scientific discovery in biology, chemistry, physics, etc.)
2. Perturbation Prediction (specifically predicting how systems respond to perturbations, like drug effects or genetic changes)

Respond ONLY in JSON format:
{{
  "is_ai4science": boolean,
  "is_perturbation": boolean,
  "reasoning": "A concise 1-sentence summary in Chinese focusing on the scientific contribution."
}}"""
        
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that classifies scientific papers."},
                    {"role": "user", "content": prompt}
                ],
                response_format={'type': 'json_object'},
                max_tokens=200
            )
            analysis = json.loads(response.choices[0].message.content)
            paper.update(analysis)
            processed.append(paper)
        except Exception as e:
            print(f"Error processing paper {paper['id']}: {e}")
            paper.update({"is_ai4science": False, "is_perturbation": False, "reasoning": "Error: " + str(e)})
            processed.append(paper)
        
        time.sleep(0.1)
        
    return processed

def save_data(processed):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(DATA_DIR, f"{today}.json")
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(processed, f, indent=2, ensure_ascii=False)
    
    dates = []
    if os.path.exists(DATES_FILE):
        with open(DATES_FILE, "r") as f:
            dates = json.load(f)
    
    if today not in dates:
        dates.append(today)
        dates.sort(reverse=True)
        with open(DATES_FILE, "w") as f:
            json.dump(dates, f, indent=2)
    
    print(f"Data saved to {file_path}")

def main():
    # Load history
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
            
    all_papers = fetch_arxiv_papers()
    if not all_papers:
        print("No papers found.")
        return
        
    # Filter out papers already in history
    new_papers = [p for p in all_papers if p["id"] not in history]
    print(f"Found {len(new_papers)} new papers out of {len(all_papers)} total.")
    
    if not new_papers:
        print("No new papers to process.")
        return

    processed = process_with_ai(new_papers)
    save_data(processed)
    
    # Update history
    new_ids = [p["id"] for p in new_papers]
    history.extend(new_ids)
    # Keep last 2000 papers in history
    history = history[-2000:]
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)
        
    print("Done!")

if __name__ == '__main__':
    main()
