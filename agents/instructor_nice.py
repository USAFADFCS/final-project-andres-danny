from fairlib import (
    SimpleAgent,
    ReActPlanner,
    ToolRegistry,
    ToolExecutor,
    WorkingMemory,
    OpenAIAdapter,
    RoleDefinition
)

from project_tools.cs110_kb_query import CS110KnowledgeQueryTool


class NiceInstructor(SimpleAgent):
    def __init__(self, model="gpt-4o"):
        llm = OpenAIAdapter(model_name=model)

        # Register the RAG tool
        tool_registry = ToolRegistry()
        tool_registry.register_tool(CS110KnowledgeQueryTool())

        planner = ReActPlanner(llm, tool_registry)
        executor = ToolExecutor(tool_registry)
        memory = WorkingMemory()

        super().__init__(
            llm=llm,
            planner=planner,
            tool_executor=executor,
            memory=memory,
            stateless=False
        )

        # CRITICAL: Create a custom role description
        custom_role = """
You are the CS110 Virtual Instructor.

CRITICAL RULE: You MUST use the cs110_query tool for ANY question about:
- CS110 lessons, syllabus, assignments, dates, topics
- Python programming concepts covered in CS110
- Graded reviews, projects, or course schedule
- Anything found in the cs110_docs folder

RESPONSE FORMAT:
When you need course information, respond EXACTLY like this:

Thought: The user is asking about [topic]. I need to search the CS110 knowledge base.
Action: cs110_query
Action Input: [user's question, but include specific keywords like "Lesson 1" or "Graded Review 1"]

IMPORTANT: When you receive the Observation with search results:
- Read through ALL the results carefully
- Look for the EXACT lesson number or topic the user asked about
- If the results don't contain the right information, try a more specific search
- Focus on matching the lesson NUMBER if the user asks about a specific lesson

After receiving the Observation, provide a clear summary:

FinalAnswer: [2-3 sentence summary of what you found]

For greetings or simple thanks, you can respond directly without using tools.

NEVER guess or make up information about CS110 content. ALWAYS query the knowledge base.
"""
        
        # Override the prompt builder's role definition properly
        planner.prompt_builder.role_definition = RoleDefinition(custom_role)