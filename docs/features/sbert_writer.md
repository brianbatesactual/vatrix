# SBERT Writer

## Feature
Generate and export sentence pairs for supervised SBERT training.

## Purpose
- Support fine-tuning of SBERT using log sentence variations
- Create labeled similarity pairs with associated scores
- Export structured CSVs for training pipelines

## How It Works
- Takes a list of `(sentence1, sentence2, score)` tuples
- Saves as `CSV` with headers: `sentence1, sentence2, score`
- Used during `--generate-sbert-data` mode

## Design Choices
- CSV chosen for interoperability with HuggingFace Datasets and PyTorch DataLoaders
- Score format compatible with cosine similarity training objectives

## Limitations
- No deduplication
- Does not automatically score pairs (external similarity module required)

## Related Modules

