import arxiv
import json
import os
from datetime import datetime, timedelta
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

# Define categories and corresponding keywords
categories = {
    "Speech Recognition": [
        "speech recognition",
        "automatic speech recognition",
        "ASR",
        "speech-to-text",
        "converting spoken language to text",
        "voice recognition",
        "transcribing audio to text"
    ],
    "Speech Synthesis": [
        "speech synthesis",
        "text-to-speech",
        "TTS",
        "speech generation",
        "converting text to spoken language",
        "synthetic speech",
        "voice synthesis"
    ],
    "Datasets": [
        "new dataset",
        "dataset collection",
        "data gathering",
        "dataset creation",
        "curating data for training",
        "annotated datasets",
        "data preprocessing"
    ],
    "Benchmarking": [
        "benchmarking",
        "performance evaluation",
        "model comparison",
        "benchmark dataset",
        "testing model performance",
        "standardized testing",
        "model benchmarking"
    ],
    "LLMs": [
        "large language model",
        "LLM",
        "transformer model",
        "GPT",
        "BERT",
        "massive pre-trained language models",
        "language model fine-tuning",
        "contextual embeddings"
    ],
    "Multimodal Learning": [
        "multimodal learning",
        "cross-modal learning",
        "multisensory learning",
        "fusion of modalities",
        "integrating multiple data types",
        "visual and textual data fusion",
        "audio-visual learning"
    ],
    "Explainable AI": [
        "explainable AI",
        "model interpretability",
        "XAI",
        "model explanation",
        "transparent AI",
        "understanding model decisions",
        "interpretable machine learning"
    ],
    "AI in Healthcare": [
        "AI in healthcare",
        "medical AI",
        "healthcare applications",
        "clinical decision support",
        "medical imaging",
        "AI for diagnosis",
        "health data analytics"
    ],
    "Reinforcement Learning": [
        "reinforcement learning",
        "RL",
        "policy gradient",
        "Q-learning",
        "actor-critic",
        "reward-based learning",
        "decision making algorithms"
    ]
}

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

def classify_abstract(abstract):
    embeddings = model.encode([abstract])
    scores = []
    for category, keywords in categories.items():
        category_embeddings = model.encode(keywords)
        similarity = embeddings @ category_embeddings.T
        score = similarity.mean()
        scores.append((category, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    return [scores[0][0], scores[1][0]]


# Define the date range for the query
today = datetime.now()
yesterday = today - timedelta(days=2)
base_query = f"submittedDate:[{yesterday.strftime('%Y%m%d')} TO {today.strftime('%Y%m%d')}]"

# Specific queries for cs.AI, speech recognition, and speech synthesis
queries = [
    f"cat:cs.AI AND {base_query} AND NOT (all:robotics OR all:'computer vision')",
    f"(all:speech AND all:recognition) AND {base_query} AND NOT (all:robotics OR all:'computer vision')",
    f"(all:speech AND all:synthesis) AND {base_query} AND NOT (all:robotics OR all:'computer vision')"
]


client = arxiv.Client()

papers = []
seen_titles = set()

for query in queries:
    search = arxiv.Search(
        query=query,
        max_results=200,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    for result in client.results(search):
        if result.title not in seen_titles:
            seen_titles.add(result.title)
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
    json.dump(list(reversed(papers)), f, indent=2)

print(f"Fetched {len(papers)} papers.")
