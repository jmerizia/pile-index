set -e

mkdir -p ./data/pile/train
mkdir -p ./data/pile/test
cd ./data/pile/train
wget https://the-eye.eu/public/AI/pile/train/00.jsonl.zst
zstd -d ./00.jsonl.zst
