from sentence_transformers import SentenceTransformer
import torch
import fire
import numpy as np
from nltk.tokenize import sent_tokenize
from tqdm import tqdm

from utils import iter_pile


def main(
    use_gpu=False,
    model='all-MiniLM-L6-v2',
    batch_size=32,
    limit=1000,
):

    device = torch.device('cuda' if use_gpu else 'cpu')

    model = SentenceTransformer(model)

    documents = list(iter_pile(limit=limit))
    print(f'retrieved {len(documents)} documents')
    all_sentences = []
    for document_idx, d in tqdm(enumerate(documents)):
        sentences = sent_tokenize(d)
        for sentence_idx, sentence in enumerate(sentences):
            all_sentences.append({
                'id': f'{document_idx}:{sentence_idx}',
                'text': sentence,
            })
    print(len(all_sentences))
    quit()
    print(f'Encoding {len(sentences)} documents')
    embeddings = model.encode(
        sentences,
        device=device,
        show_progress_bar=True,
        batch_size=batch_size,
    )
    with open('data/embeddings.npz', 'wb') as f:
        np.savez(f, embeddings)


if __name__ == '__main__':
    fire.Fire(main)
