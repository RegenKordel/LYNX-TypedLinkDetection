from pathlib import Path


data_dir = Path(__file__).parent.parent / 'data'
preprocessed_data_dir = data_dir / 'processed'
train_output_dir = data_dir / 'outputs'
train_results_dir = data_dir / 'results'
link_embedding_dir = data_dir / 'link-embeddings'
word_embedding_dir = data_dir / 'word-embeddings'

for directory in [preprocessed_data_dir, train_output_dir, train_results_dir, link_embedding_dir, word_embedding_dir]:
    directory.mkdir(parents=True, exist_ok=True)
