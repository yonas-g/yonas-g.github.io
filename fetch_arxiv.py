import arxiv
import json
import os
from datetime import datetime, timedelta

# Define the search queries to get papers submitted today in cs.AI category
today = datetime.now()
yesterday = today - timedelta(days=1)
base_query = f"submittedDate:[{yesterday.strftime('%Y%m%d')} TO {today.strftime('%Y%m%d')}]"

# Specific queries for cs.AI, speech recognition, and speech synthesis
queries = [
    f"cat:cs.AI AND {base_query}",
    f"(all:speech AND all:recognition) AND {base_query}",
    f"(all:speech AND all:synthesis) AND {base_query}"
]

# Initialize the Arxiv client
client = arxiv.Client()

# Fetch papers
papers = []
for query in queries:
    search = arxiv.Search(
        query=query,
        max_results=200,  # Adjust the number as needed
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    for result in client.results(search):
        papers.append({
            "title": result.title,
            "abstract": result.summary,
            "authors": [author.name for author in result.authors],
            "pdf_link": result.pdf_url
        })

# Archive the previous JSON file if it exists
filename = "assets/json/arxiv_papers.json"
if os.path.exists(filename):
    archived_filename = f"assets/json/arxiv_papers_{yesterday.strftime('%Y%m%d')}.json"
    os.rename(filename, archived_filename)

# Save to JSON file
with open(filename, "w") as f:
    json.dump(papers, f, indent=2)

print(f"Fetched {len(papers)} papers.")
