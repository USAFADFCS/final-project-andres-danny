from fairlib import (
    HierarchicalAgentRunner,
    ToolRegistry,
    ToolExecutor,
    WorkingMemory
)

import asyncio
import sys
import os

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from agents.instructor_nice import NiceInstructor


def main():
    print("🚀 Starting CS110 Virtual Instructor (CLI Mode)")
    print("Type 'exit' or 'quit' to stop\n")
    
    # Create the instructor using gpt-4o-mini for cost savings
    instructor = NiceInstructor(model="gpt-4o-mini")
    
    while True:
        user_input = input("\n👤 Student: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        if not user_input.strip():
            continue
        
        try:
            # Run the agent
            result = asyncio.run(instructor.arun(user_input))
            print(f"\n🤖 Instructor: {result}")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()