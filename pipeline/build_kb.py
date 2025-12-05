import os
import sys

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

import chromadb
from fairlib import Document, SentenceTransformerEmbedder, LongTermMemory, ChromaDBVectorStore
from pipeline.config import project_path
import re


def smart_chunk_by_lessons(text):
    """
    Split text by lesson boundaries for CS110 lesson schedules
    This keeps each lesson's content together
    """
    # Split on the lesson separator pattern
    lesson_pattern = r'={40,}\s*\nLesson \d+:'
    
    # Find all lesson boundaries
    matches = list(re.finditer(lesson_pattern, text))
    
    if not matches:
        # Fallback to simple chunking if no lessons found
        return simple_chunk_text(text, chunk_size=800)
    
    chunks = []
    
    # Get content before first lesson (intro text)
    if matches[0].start() > 0:
        intro = text[:matches[0].start()].strip()
        if intro:
            chunks.append(intro)
    
    # Extract each lesson as a chunk
    for i, match in enumerate(matches):
        start = match.start()
        # End is either the next lesson or end of text
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        
        lesson_chunk = text[start:end].strip()
        
        # If a lesson is REALLY long (>2000 chars), split it further
        if len(lesson_chunk) > 2000:
            # Split into smaller pieces but keep the header
            header_end = lesson_chunk.find('\n\n')
            if header_end > 0:
                header = lesson_chunk[:header_end + 2]
                body = lesson_chunk[header_end + 2:]
                
                # Add header + first part
                chunks.append(header + body[:1500])
                
                # If there's more, add header + rest
                if len(body) > 1500:
                    chunks.append(header + body[1500:])
            else:
                chunks.append(lesson_chunk)
        else:
            chunks.append(lesson_chunk)
    
    return chunks


def simple_chunk_text(text, chunk_size=800, overlap=100):
    """
    Simple chunking for general documents
    Splits text into chunks with overlap to preserve context
    
    Args:
        text: The text to chunk
        chunk_size: Target size of each chunk (default 800 chars)
        overlap: Number of characters to overlap between chunks (default 100)
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    length = len(text)
    
    while start < length:
        # Find the end position
        end = start + chunk_size
        
        # If this is not the last chunk and we're in the middle of a word,
        # try to break at a sentence or paragraph boundary
        if end < length:
            # Look for paragraph break first
            paragraph_break = text.rfind('\n\n', start, end)
            if paragraph_break > start + chunk_size // 2:
                end = paragraph_break + 2
            else:
                # Look for sentence break
                sentence_break = text.rfind('. ', start, end)
                if sentence_break > start + chunk_size // 2:
                    end = sentence_break + 2
                else:
                    # Look for any space
                    space_break = text.rfind(' ', start, end)
                    if space_break > start + chunk_size // 2:
                        end = space_break + 1
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # Move start position with overlap
        start = end - overlap
    
    return chunks


def build_cs110_kb():
    print("🔧 Building CS110 Knowledge Base with SMART CHUNKING...")
    print("📚 Supports: Lesson schedules, syllabi, and ANY .txt document!")

    docs_path = project_path("cs110_docs")
    print(f"📁 Loading text files from: {docs_path}")

    filenames = [f for f in os.listdir(docs_path) if f.endswith(".txt")]
    print(f"📄 Found files: {filenames}")

    all_docs = []

    for fname in filenames:
        full_path = os.path.join(docs_path, fname)

        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

        print(f"\n📘 Parsing {fname} ({len(text)} chars)")

        if len(text.strip()) == 0:
            print("   ⚠️ WARNING: File is empty, skipping.")
            continue

        # Smart chunking based on file type
        if "Lesson_Schedule" in fname or "Syllabus" in fname:
            # Special handling for lesson schedules
            chunks = smart_chunk_by_lessons(text)
            print(f"   ➕ {len(chunks)} lesson-based chunks created")
        else:
            # General document chunking with small chunks for better retrieval
            chunks = simple_chunk_text(text, chunk_size=800, overlap=100)
            print(f"   ➕ {len(chunks)} general-purpose chunks created")

        for i, chunk in enumerate(chunks):
            all_docs.append(
                Document(
                    page_content=chunk,
                    metadata={"source": fname}
                )
            )
            # Show preview of first few chunks
            if i < 3:
                preview = chunk[:150].replace('\n', ' ')
                print(f"      Chunk {i+1} preview: {preview}...")

    print(f"\n📚 Total chunks produced: {len(all_docs)}")

    # Clear old collection and rebuild
    persist_dir = project_path("cs110_collection")
    print(f"💾 Using persistent Chroma directory: {persist_dir}")
    
    # Delete old collection if exists
    try:
        client = chromadb.PersistentClient(path=persist_dir)
        client.delete_collection("cs110_collection")
        print("🗑️ Deleted old collection")
    except:
        pass

    client = chromadb.PersistentClient(path=persist_dir)
    client.get_or_create_collection("cs110_collection")

    embedder = SentenceTransformerEmbedder()

    vector_store = ChromaDBVectorStore(
        client=client,
        collection_name="cs110_collection",
        embedder=embedder
    )

    memory = LongTermMemory(vector_store)

    print("\n🧠 Adding chunks to LongTermMemory:")
    for i, doc in enumerate(all_docs):
        memory.add_document(
            doc.page_content,
            metadata=doc.metadata
        )
        if (i + 1) % 10 == 0:
            print(f"   ➕ Stored {i+1}/{len(all_docs)} chunks")

    print(f"\n   ➕ Stored all {len(all_docs)} chunks")
    print("\n✅ Knowledge Base built successfully!")
    print("🚀 You can now ask questions about ANY document in cs110_docs/")


if __name__ == "__main__":
    build_cs110_kb()