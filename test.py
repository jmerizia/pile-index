import faiss
from sentence_transformers import SentenceTransformer
import glob
import torch

device = torch.device('cuda:0')

def iter_enron(location='data/maildir', limit=1000):
    for idx, fn in enumerate(glob.glob(location + '/**/*.', recursive=True)):
        if idx >= limit:
            break
        with open(fn, 'r') as f:
            yield f.read()

model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = list(iter_enron(limit=10000))
embeddings = model.encode(sentences, device=device, show_progress_bar=True)

ndata, dimension = tuple(embeddings.shape)

index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

input = model.encode(['JOE IS A DEER HUNTING SUPERSTAR'])

D, I = index.search(input, 4)
print(D, I)

for idx in I[0]:
    print(sentences[idx])
    print('')
    print('')
    print('')
    print('')

#Print the embeddings
# for sentence, embedding in zip(sentences, sentence_embeddings):
#     print("Sentence:", sentence)
#     print("Embedding:", embedding.shape)
#     print("")
