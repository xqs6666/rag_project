import sys
try:
    import pysqlite3
    sys.modules['sqlite3'] = pysqlite3
except ImportError:
    pass

import hashlib
import os
from uu import Error

from sympy import im
import config as config
from langchain_ollama import OllamaEmbeddings
from langchain_chroma.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime


def get_string_md5(input_stream: str, encode="utf-8"):
    if input_stream is None:
        raise Error("input_stream not none")
    str_bytes = input_stream.encode(encode)
    m = hashlib.md5()
    m.update(str_bytes)
    md5_hex = m.hexdigest()
    return md5_hex


def save_md5(md5: str):
    if md5 is None:
        raise Error("md5 not none")
    os.makedirs(os.path.dirname(config.md5_file_path), exist_ok=True)
    with open(config.md5_file_path, "a", encoding="utf-8") as f:
        f.write(md5 + "\n")


def md5_check(md5: str):
    if md5 is None:
        raise Error("md5 not none")
    if not os.path.exists(config.md5_file_path):
        os.makedirs(os.path.dirname(config.md5_file_path), exist_ok=True)
        open(config.md5_file_path, "w", encoding="utf-8").close()
        return False
    with open(config.md5_file_path, "r", encoding="utf-8") as f:
        for val in f.readlines():
            data = val.strip()
            if md5 == data:
                return True
    return False


class KnowledgeBaseService:
    def __init__(self) -> None:
        os.makedirs(config.persist_directory, exist_ok=True)
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=OllamaEmbeddings(
                model=config.ollama["embedding"]["model"],
                base_url=config.ollama["embedding"]["base_url"],
            ),
            persist_directory=config.persist_directory,
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len,
        )

    def uploader_by_str(self, data: str, filename):
        md5_hex = get_string_md5(data)

        if md5_check(md5_hex):
            return "[跳过]内容已经在知识库"

        if len(data) > config.max_split_char_number:
            knowledge_chunk: list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunk: list[str] = [data]

        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "xqs",
        }
        self.chroma.add_texts(
            knowledge_chunk, metadatas=[metadata for _ in knowledge_chunk]
        )

        save_md5(md5_hex)
        return "[成功]内容已经载入到知识库"


# if __name__ == "__main__":
#     r1 = get_string_md5("xqs666")
#     r2 = get_string_md5("xqs666")
#     r3 = get_string_md5("xqs6666")

#     if not md5_check(r1):
#         save_md5(r1)

#     if not md5_check(r2):
#         save_md5(r2)

#     if not md5_check(r3):
#         save_md5(r3)
if __name__ == "__main__":
    service = KnowledgeBaseService()
    result = service.uploader_by_str("先秦时fuckyou","testfile")
    print(result)