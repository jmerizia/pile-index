'''
A simple KV store for billions of records.
'''

import os
import pickle
import fire


class StaticKVStore:
    def __init__(self, name: str, base_path: str = ''):
        self.name = name
        self.base_path = base_path
        if self._created():
            self.index = self._read_index()
        else:
            self.index = None

    def __del__(self):
        self._write_index()

    def _created(self):
        return os.path.exists(os.path.join(self.base_path, self.name))

    def _index_fn(self) -> str:
        return os.path.join(self.base_path, self.name, 'index.pickle')

    def _chunk_fn(self, idx: int) -> str:
        return os.path.join(self.base_path, self.name, f'{idx:05}data')

    def _read_index(self):
        print('Loading index...')
        with open(self._index_fn(), 'rb') as f:
            index = pickle.load(f)
        return index

    def _write_index(self):
        with open(self._index_fn(), 'wb') as f:
            pickle.dump(self.index, f)

    def create(self, chunk_size_bytes: int = int(1e10)):
        assert not self._created()
        os.mkdir(os.path.join(self.base_path, self.name))
        self.index = {
            '__meta__': {
                'chunk_size_bytes': chunk_size_bytes,
                'cur_chunk_idx': 0,
            }
        }
        self._write_index()

    def push(self, key: str, value: str):
        assert self._created()
        assert key not in self.index, \
            f'key {key} already exists'
        with open(self._chunk_fn(0), 'ab') as f:
            raw = value.encode('utf-8')
            before = f.tell()
            f.write(raw)
            after = f.tell()
            assert after - before == len(raw)
            self.index[key] = [0, before, after - before]  # chunk, offset, length

    def delete(self):
        assert self._created()
        os.system(f'rm -rf {os.path.join(self.base_path, self.name)}')
        self.index = None

    def get(self, key: str) -> str:
        assert self._created()
        assert key in self.index, f'no such key {key}'
        [chunk, offset, length] = self.index[key]
        with open(self._chunk_fn(chunk), 'rb') as f:
            f.seek(offset)
            b = f.read(length)
        value = b.decode('utf-8')
        return value


if __name__ == '__main__':
    fire.Fire(StaticKVStore)
