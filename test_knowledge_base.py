"""
Quick test to verify your knowledge base is working
"""
from project_tools.cs110_kb_query import CS110KnowledgeQueryTool

# Test the tool directly
tool = CS110KnowledgeQueryTool()

test_questions = [
    "What is covered in Lesson 7?",
    "When is Graded Review 1?",
    "What are Python functions?",
]

print("Testing CS110 Knowledge Base Tool\n" + "="*50)

for question in test_questions:
    print(f"\nQuestion: {question}")
    result = tool.invoke(question)
    print(f"Result: {result[:300]}...")  # Show first 300 chars
    print("-"*50)