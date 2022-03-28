from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import torch
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from utils import load_pile_offset_file, get_pile_record_at_offset


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

use_gpu = True
device = torch.device('cuda' if use_gpu else 'cpu')
model = 'all-MiniLM-L6-v2'
offsets = load_pile_offset_file()

with np.load('../data/embeddings.npz') as f:
    embeddings = f['arr_0']
    ndata, dimension = tuple(embeddings.shape)

model = SentenceTransformer(model)
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)


class PileRecordModel(BaseModel):
    text: str
    subset: str


class QueryResponse(BaseModel):
    results: List[PileRecordModel]


@app.post("/api/search", response_model=QueryResponse)
async def root(query: str) -> QueryResponse:
    input = model.encode([query])
    D, I = index.search(input, 5)
    # TODO: process al other chunks as well
    records = [get_pile_record_at_offset(0, offsets[0][i]) for i in I[0]]
    return QueryResponse(
        results=[
            PileRecordModel(
                text=r.text,
                subset=r.subset,
            ) for r in records
        ],
    )
