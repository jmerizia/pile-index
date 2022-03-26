from sentence_transformers import SentenceTransformer
import glob
import torch
import fire
import numpy as np


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


def main(
    use_gpu=False,
    model='all-MiniLM-L6-v2',
    batch_size=32,
    limit=1000,
):

    device = torch.device('cuda' if use_gpu else 'cpu')

    model = SentenceTransformer(model)

    documents = list(iter_enron(limit=limit))
    print(f'Encoding {len(documents)} documents')
    embeddings = model.encode(
        documents,
        device=device,
        show_progress_bar=True,
        batch_size=batch_size,
    )
    with open('data/embeddings.npz', 'wb') as f:
        np.savez(f, embeddings)


if __name__ == '__main__':
    fire.Fire(main)
