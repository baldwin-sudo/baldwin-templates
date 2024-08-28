from sentence_transformers import SentenceTransformer
import pandas as pd
import torch
from langchain.text_splitter import RecursiveCharacterTextSplitter, SpacyTextSplitter
import json
from elasticsearch import Elasticsearch, helpers
import os

# Initialize embedding model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
device='cpu'
model = SentenceTransformer('bert-large-nli-stsb-mean-tokens', device=device)

def init_es():
    return Elasticsearch("http://localhost:9200")

def create_es_index(es, index_name="test"):
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body={
            "mappings": {
                "properties": {
                    "document_id": {"type": "keyword"},
                    "document_embedding": {"type": "dense_vector", "dims": 1024},  # Adjust dims to match the embedding vector size
                    "document_text": {"type": "text"}
                }
            }
        })
    print("ES connected ...")

def embed_chunk(chunk):
    # Compute embeddings and convert to list
    return model.encode(chunk, show_progress_bar=True, device=device).tolist()

def get_text_files(dir_path="texts"):
    return [os.path.join(dir_path, file) for file in os.listdir(dir_path) if file.lower().endswith('.txt')]

def chunk_all_files(texts_dir="texts"):
    def chunk_document(document, chunk_size=1000, overlap=True):
        # Initialize the text splitter
        if overlap:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                length_function=len,
                is_separator_regex=False
            )
        else:
            text_splitter = SpacyTextSplitter(chunk_size=chunk_size)
        
        # Split the text into chunks
        chunks = text_splitter.split_text(document)
        return chunks

    files = get_text_files(texts_dir)
    
    file_contents = {}
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                filename = os.path.basename(file_path)
                content = file.read()
                file_contents[filename] = content
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    all_chunks = {}
    for filename, text in file_contents.items():
        all_chunks[filename] = chunk_document(text)

    return all_chunks

def prepare_bulk_data(chunks, index_name):
    actions = []
    for filename, text_chunks in chunks.items():
        for idx, chunk in enumerate(text_chunks):
            embedding = embed_chunk([chunk])[0]  # Embed the chunk
            action = {
                "_op_type": "index",
                "_index": index_name,
                "_id": f"{filename}_{idx}",  # Unique ID for each chunk
                "_source": {
                    "document_id": filename,
                    "document_embedding": embedding,
                    "document_text": chunk
                }
            }
            actions.append(action)
    return actions

def index_data(index_name,texts_dir="texts"):
    es = init_es()
    
    create_es_index(es, index_name)

    chunks = chunk_all_files(texts_dir=texts_dir)
    bulk_data = prepare_bulk_data(chunks, index_name)
    
    # Index data into Elasticsearch in bulk
    helpers.bulk(es, bulk_data)
    

if __name__ == "__main__":
    index_name = "test"
    texts_dir="texts"
    index_data(index_name,texts_dir)
