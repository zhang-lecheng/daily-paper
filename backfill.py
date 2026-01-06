import arxiv
import datetime
import os
import json
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configuration
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-1936b4530c074806b9398e016aa5f1ec")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
CATEGORIES = ["cs.AI", "cs.LG", "stat.ML", "q-bio.QM", "physics.comp-ph", "math.OC", "cs.CE", "cs.MS", "cs.NE"]
DATA_DIR = "data"
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
DATES_FILE = os.path.join(DATA_DIR, "available_dates.json")

os.makedirs(DATA_DIR, exist_ok=True)

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

def fetch_historical_papers(days_back=30):
    all_historical_papers = {}
    
    # We'll search for each day specifically to avoid hitting the 1000 limit and ensure coverage
    for i in range(1, days_back + 1):
        target_date = datetime.date.today() - datetime.timedelta(days=i)
        date_str = target_date.strftime("%Y%m%d")
        print(f"Fetching papers for {target_date}...")
        
        # arXiv query for specific date
        query = f'({" OR ".join([f"cat:{cat}" for cat in CATEGORIES])}) AND submittedDate:[{date_str}0000 TO {date_str}2359]'
        
        search = arxiv.Search(
            query=query,
            max_results=200,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        papers = []
        try:
            results = list(arxiv.Client().results(search))
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
            all_historical_papers[target_date.strftime("%Y-%m-%d")] = papers
            time.sleep(2) # Be nice to arXiv
        except Exception as e:
            print(f"Error fetching for {target_date}: {e}")
            
    return all_historical_papers

def process_with_ai(papers):
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
            print(f"Error processing {paper['id']}: {e}")
            paper.update({"is_ai4science": False, "is_perturbation": False, "reasoning": "Error: " + str(e)})
            processed.append(paper)
        
        time.sleep(0.1)
    return processed

def main():
    # Load history to avoid reprocessing if some backfill was done before
    history = set()
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = set(json.load(f))

    historical_data = fetch_historical_papers(30)
    
    available_dates = []
    if os.path.exists(DATES_FILE):
        with open(DATES_FILE, "r") as f:
            available_dates = json.load(f)

    for date_str, papers in historical_data.items():
        # Check if date already exists in available_dates to avoid overwriting unless needed
        # and also check if we have new papers for this date
        new_papers = [p for p in papers if p["id"] not in history]
        
        if not new_papers:
            print(f"No new papers for {date_str}, skipping AI processing.")
            continue
            
        print(f"Processing {len(new_papers)} new papers for {date_str}...")
        processed_papers = process_with_ai(new_papers)
        
        # Save daily file
        file_path = os.path.join(DATA_DIR, f"{date_str}.json")
        # If file exists, merge
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                existing = json.load(f)
                processed_papers.extend(existing)
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(processed_papers, f, indent=2, ensure_ascii=False)
            
        # Update available_dates
        if date_str not in available_dates:
            available_dates.append(date_str)
            
        # Update history
        history.update([p["id"] for p in new_papers])

    # Final saves
    available_dates.sort(reverse=True)
    with open(DATES_FILE, "w") as f:
        json.dump(available_dates, f, indent=2)
        
    with open(HISTORY_FILE, "w") as f:
        json.dump(list(history), f)

    print("Backfill complete!")

if __name__ == "__main__":
    main()
