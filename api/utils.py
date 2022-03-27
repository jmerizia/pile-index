from dataclasses import dataclass
from typing import Iterable, Tuple
import jsonlines
import glob


@dataclass
class PileEntry:
    text: str
    subset: str
    offset: int


def iter_pile(location='./data/pile', limit=1000) -> Iterable[PileEntry]:
    idx = 0
    for fn in glob.glob(location + '/train/*.jsonl', recursive=True):
        with open(fn, 'rb') as f:
            reader = jsonlines.Reader(f)
            for obj in reader:
                idx += 1
                if idx > -1 and idx == limit:
                    return
                assert len(obj['meta']) == 1
                yield PileEntry(
                    text=obj['text'],
                    subset=obj['meta']['pile_set_name'],
                    offset=f.tell(),
                )


def iter_enron(location='./data/maildir', limit=1000):
    for idx, fn in enumerate(glob.glob(location + '/**/*.', recursive=True)):
        if idx >= limit:
            break
        with open(fn, 'r') as f:
            try:
                text = f.read()
                yield text
            except:
                print('Failed to load document', fn)
