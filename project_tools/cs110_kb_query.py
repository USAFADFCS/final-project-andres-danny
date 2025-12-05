"""
CS110 Knowledge Base Query Tool with keyword filtering
"""
from fairlib import AbstractTool
from fairlib import SentenceTransformerEmbedder
import chromadb
import os
import re
from pipeline.config import project_path


class CS110KnowledgeQueryTool(AbstractTool):
    name = "cs110_query"
    description = (
        "Searches the CS110 course knowledge base for information about lessons, "
        "assignments, syllabus, graded reviews, Python concepts, and course schedule. "
        "For specific lessons, use format like 'Lesson 7' or 'lesson 2'."
    )

    def __init__(self):
        persist_dir = project_path("cs110_collection")
        os.makedirs(persist_dir, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_collection("cs110_collection")
        self.embedder = SentenceTransformerEmbedder()

    def _extract_lesson_number(self, query: str):
        """Extract lesson number from query"""
        patterns = [
            r'lesson\s+(\d+)',
            r'l(\d+)',
        ]
        
        query_lower = query.lower()
        for pattern in patterns:
            match = re.search(pattern, query_lower)
            if match:
                return int(match.group(1))
        return None

    def use(self, tool_input: str):
        """
        Main tool execution method
        """
        try:
            lesson_num = self._extract_lesson_number(tool_input)
            
            # DEBUG
            print(f"\n🔍 DEBUG: Input query = '{tool_input}'")
            print(f"🔍 DEBUG: Extracted lesson_num = {lesson_num}")
            
            # Create query embedding
            query_embedding = self.embedder.embed_query(tool_input)
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=80,
                include=["documents", "metadatas"]
            )
            
            if not results or not results['documents'] or not results['documents'][0]:
                return "No information found in the CS110 knowledge base."
            
            documents = results['documents'][0]
            
            # DEBUG
            print(f"🔍 DEBUG: Got {len(documents)} results from ChromaDB")
            if documents:
                print(f"🔍 DEBUG: First result preview:\n{documents[0][:300]}\n")
            
            # If asking about a specific lesson, filter by keyword
            if lesson_num:
                filtered = []
                target = f"Lesson {lesson_num}:"
                
                # DEBUG: Check ALL documents and track where we find it
                print(f"🔍 DEBUG: Looking for '{target}' in {len(documents)} documents...")
                found_at = []
                
                for i, doc in enumerate(documents):
                    if target in doc:
                        filtered.append(doc)
                        found_at.append(i)
                
                print(f"🔍 DEBUG: Found '{target}' at positions: {found_at}")
                print(f"🔍 DEBUG: Filtered to {len(filtered)} documents\n")
                
                if filtered:
                    documents = filtered[:3]
                else:
                    # Show what lessons we DID find for debugging
                    print(f"🔍 DEBUG: Didn't find '{target}'. Here's what we got:")
                    for i in range(min(5, len(documents))):
                        # Extract lesson number from this doc
                        doc_preview = documents[i][:300]
                        lesson_match = re.search(r'Lesson (\d+):', doc_preview)
                        lesson_found = lesson_match.group(1) if lesson_match else "?"
                        print(f"   Doc {i}: Lesson {lesson_found} - {doc_preview[:100].replace(chr(10), ' ')}...")
                    
                    return (
                        f"Could not find information about Lesson {lesson_num}. "
                        f"Please verify the lesson number or try rephrasing."
                    )
            else:
                documents = documents[:3]
            
            # Format results
            formatted = []
            for i, doc in enumerate(documents, 1):
                formatted.append(f"[Result {i}]:\n{doc[:1000]}")
            
            return "\n\n---\n\n".join(formatted)
            
        except Exception as e:
            import traceback
            return f"Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"