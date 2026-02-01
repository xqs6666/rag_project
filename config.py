md5_file_path = "application_data/md5_file.txt"
ollama = {
    "embedding": {
        "model": "qwen3-embedding:latest",
        "base_url": "http://xqs-ollama:11434",
    }
}
collection_name = "rag"
persist_directory = "chroma_db"

chunk_size = 1000
chunk_overlap = 100
separators = [
    "\n\n",
    "\n",
    "。",
    "！",
    "？",
    ". ",
    "! ",
    "? ",
    "；",
    "; ",
    "，",
    ", ",
    " ",
]
max_split_char_number = 1000