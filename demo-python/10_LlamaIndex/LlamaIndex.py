from pathlib import Path
from llama_index.core import SimpleDirectoryReader

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

documents = SimpleDirectoryReader(str(DATA_DIR)).load_data()

print(documents)