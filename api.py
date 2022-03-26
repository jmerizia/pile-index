from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import torch
from pydantic import BaseModel
from typing import List
import glob
from fastapi.staticfiles import StaticFiles

app = FastAPI()

def iter_enron(location='data/maildir', limit=1000):
    for idx, fn in enumerate(glob.glob(location + '/**/*.', recursive=True)):
        if idx >= limit:
            break
        with open(fn, 'r') as f:
            try:
                text = f.read()
                yield text
            except:
                print('Failed to load document', fn)

use_gpu = True
device = torch.device('cuda' if use_gpu else 'cpu')
model = 'all-MiniLM-L6-v2'
dataset = list(iter_enron(limit=1000000))

with np.load('data/embeddings.npz') as f:
    embeddings = f['arr_0']
    ndata, dimension = tuple(embeddings.shape)

model = SentenceTransformer(model)
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

class QueryResponse(BaseModel):
    results: List[str]


@app.post("/api/search", response_model=QueryResponse)
async def root(query: str) -> QueryResponse:
    input = model.encode([query])

    D, I = index.search(input, 5)
    print(D)

    return QueryResponse(
        results=[dataset[i] for i in I[0]],
    )


app.mount("/", StaticFiles(directory="www", html=True), name="www")
