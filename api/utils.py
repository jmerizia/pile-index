from dataclasses import dataclass
from typing import Iterable
import jsonlines
from tqdm import tqdm
import os
import pickle
import fire
import time


@dataclass
class PileRecord:
    text: str
    subset: str
    offset: int
    chunk: int


def get_pile_chunks():
    # TODO use all chunks
    return [f'train/00.jsonl']
    # return [f'train/{i:02}.jsonl' for i in range(30)]


def iter_pile(location='./data/pile', limit=1000) -> Iterable[PileRecord]:
    idx = 0
    for chunk_idx, fn in enumerate(get_pile_chunks()):
        full = os.path.join(location, fn)
        with open(full, 'rb') as f:
            offset = f.tell()
            reader = jsonlines.Reader(f)
            for obj in reader:
                idx += 1
                if idx > -1 and idx == limit:
                    return
                assert len(obj['meta']) == 1
                yield PileRecord(
                    text=obj['text'],
                    subset=obj['meta']['pile_set_name'],
                    offset=offset,
                    chunk=chunk_idx,
                )
                offset = f.tell()


def save_pile_offset_file(
    location: str = './data/pile_offsets.pickle',
    limit: int = -1,
):
    offsets = {
        0: [],
    }
    for d in tqdm(iter_pile(limit=limit)):
        offsets[d.chunk].append(d.offset)
    with open(location, 'wb') as f:
        pickle.dump(offsets, f)


def load_pile_offset_file(
    location: str = './data/pile_offsets.pickle',
):
    with open(location, 'rb') as f:
        offsets = pickle.load(f)
    return offsets


def get_pile_record_at_offset(
    chunk: int,
    offset: int,
    location='./data/pile',
):
    fn = get_pile_chunks()[chunk]
    full = os.path.join(location, fn)
    with open(full, 'rb') as f:
        f.seek(offset)
        reader = jsonlines.Reader(f)
        obj = reader.read()
        return PileRecord(
            text=obj['text'],
            subset=obj['meta']['pile_set_name'],
            offset=offset,
            chunk=chunk,
        )


def iter_chunks(l, chunk_size):
    for i in range(len(l), chunk_size):
        yield l[i:i+chunk_size]
