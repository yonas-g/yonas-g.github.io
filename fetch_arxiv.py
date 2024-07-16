import arxiv
import json
import os
from datetime import datetime, timedelta
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

# Define categories and corresponding keywords
categories = {
    "Machine Learning": ["machine learning", "deep learning", "neural network", "supervised learning", "unsupervised learning"],
    "Natural Language Processing": ["NLP", "language model", "text generation", "text classification"],
    "Computer Vision": ["computer vision", "image processing", "object detection", "image recognition"],
    "Speech Recognition": ["speech recognition", "automatic speech recognition", "ASR", "speech-to-text"],
    "Speech Synthesis": ["speech synthesis", "text-to-speech", "TTS", "speech generation"],
    "Robotics": ["robotics", "robot", "robot learning", "autonomous system"]
}


model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

def classify_abstract(abstract):
    embeddings = model.encode([abstract])
    best_category = None
    best_score = float('-inf')
    for category, keywords in categories.items():
        category_embeddings = model.encode(keywords)
        similarity = embeddings @ category_embeddings.T
        score = similarity.mean()
        if score > best_score:
            best_score = score
            best_category = category
    return best_category


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


client = arxiv.Client()

papers = []
for query in queries:
    search = arxiv.Search(
        query=query,
        max_results=100,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    for result in client.results(search):
        category = classify_abstract(result.summary)
        papers.append({
            "title": result.title,
            "abstract": result.summary,
            "authors": [author.name for author in result.authors],
            "pdf_link": result.pdf_url,
            "category": category
        })

# Archive the previous JSON file if it exists
filename = "assets/json/arxiv_papers.json"
if os.path.exists(filename):
    archived_filename = f"assets/json/arxiv_papers_{yesterday.strftime('%Y%m%d')}.json"
    os.rename(filename, archived_filename)


with open(filename, "w") as f:
    json.dump(papers, f, indent=2)

print(f"Fetched {len(papers)} papers.")
