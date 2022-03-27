import fire
from tqdm import tqdm
import matplotlib.pyplot as plt
import json

from static_kv_store import StaticKVStore
from utils import iter_pile


def main(
    name: str = 'pile_kv',
    base_path: str = 'data',
    limit: int = -1,
):
    # KVS = StaticKVStore(name, base_path)
    # if KVS._created():
    #     y = input('key-value store already created. Delete it? [y|n] ')
    #     if y.lower() == 'y':
    #         KVS.delete()
    #     else:
    #         print('Aborting!')
    #         quit()
    # KVS.create()
    offsets = []
    for document_idx, d in tqdm(enumerate(iter_pile(limit=limit))):
        # key = str(document_idx)
        offsets.append(d.offset)
        # value = json.dumps({'text': d.text, 'subset': d.subset})
        # KVS.push(key, value)


if __name__ == '__main__':
    fire.Fire(main)
