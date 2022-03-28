# run this with 

from sentence_transformers import SentenceTransformer
import torch
import fire
import numpy as np
from nltk.tokenize import sent_tokenize
from tqdm import tqdm
from mpi4py import MPI

from utils import iter_pile, iter_chunks


def main(
    use_gpu=True,
    model='all-MiniLM-L6-v2',
    batch_size=1024,
    limit=1000,
):

    size = MPI.Get_size()
    rank = MPI.Get_rank()

    device = torch.device('cuda:' + str(rank % 8) if use_gpu else 'cpu')

    model = SentenceTransformer(model)

    it = iter_chunks(tqdm(enumerate(iter_pile(limit=limit))))
    for idx, d in it:
        embeddings = model.encode(
            d.text,
            device=device,
            show_progress_bar=True,
            batch_size=batch_size,
        )
    with open('data/embeddings.npz', 'wb') as f:
        np.savez(f, embeddings)


if __name__ == '__main__':
    fire.Fire(main)
