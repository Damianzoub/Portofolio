import asyncio 
from pathlib import Path 

from services.rag.build_rag_index import build_rag_index

async def main():
    backend_dir = Path(__file__).parent.parent
    content_root = backend_dir / "rag_content"
    persist_dir = backend_dir / "rag_store_chroma"
    meta = await build_rag_index(
        content_root=str(content_root),
        persistent_dir=str(persist_dir),
        collection_name="portfolio",
        embed_provider="ollama",
        ollama_url = "http://localhost:11434",
        ollama_embed_model = "nomic-embed-text",
    )
    print(meta)

if __name__ == "__main__":
    backend_dir = Path(__file__).parent.parent
    content_root = backend_dir / "rag_content"
    persist_dir = backend_dir / "rag_store_chroma"
    print("backend_dir =", backend_dir.resolve())
    print("content_root =", content_root.resolve(), "exists =", content_root.exists())
    print("files =", list(content_root.rglob("*")))
    asyncio.run(main())