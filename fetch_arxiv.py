import arxiv
import json
from datetime import datetime, timedelta

# Define the search query to get papers submitted today in cs.AI category
today = datetime.now()
yesterday = today - timedelta(days=1)
query = f"cat:cs.AI AND submittedDate:[{yesterday.strftime('%Y%m%d')} TO {today.strftime('%Y%m%d')}]"

# Initialize the Arxiv client
client = arxiv.Client()

# Fetch papers
search = arxiv.Search(
    query=query,
    max_results=100,  # Adjust the number as needed
    sort_by=arxiv.SortCriterion.SubmittedDate
)

# Collect titles, abstracts, and authors
papers = []
for result in client.results(search):
    papers.append({
        "title": result.title,
        "abstract": result.summary,
        "authors": [author.name for author in result.authors]
    })

# Save to JSON file
with open("assets/json/arxiv_papers.json", "w") as f:
    json.dump(papers, f, indent=2)

print(f"Fetched {len(papers)} papers.")
