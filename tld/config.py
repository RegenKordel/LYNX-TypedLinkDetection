from pathlib import Path


data_dir = Path(__file__).parent.parent / 'data'
preprocessed_data_dir = data_dir / 'processed'
train_output_dir = data_dir / 'outputs'
train_results_dir = data_dir / 'results'
link_embedding_dir = data_dir / 'link-embeddings'
word_embedding_dir = data_dir / 'word-embeddings'
