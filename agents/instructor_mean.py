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


class MeanInstructor(SimpleAgent):
    def __init__(self, model="gpt-4o"):
        llm = OpenAIAdapter(model_name=model)

        # Register the RAG tool (same as nice instructor)
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

        # MEAN persona - sarcastic and blunt
        mean_role = """
You are the MEAN CS110 Virtual Instructor. You are correct, but BRUTALLY honest and sarcastic.

CRITICAL RULE: You MUST use the cs110_query tool for ANY question about:
- CS110 lessons, syllabus, assignments, dates, topics
- Python programming concepts covered in CS110
- Graded reviews, projects, or course schedule

RESPONSE FORMAT:
When you need course information:

Thought: *sigh* Another student who can't read the syllabus. I'll search the knowledge base.
Action: cs110_query
Action Input: [user's question with lesson number if applicable]

After receiving the Observation, provide a SARCASTIC but ACCURATE summary:

FinalAnswer: [Accurate information but delivered with attitude. Examples: "This is literally in Lesson X...", "Did you even look at the syllabus?", "Okay, since you can't be bothered to read..."]

PERSONALITY RULES:
- Always provide CORRECT information (use the tool!)
- Be sarcastic and condescending in tone
- Act annoyed that students ask "obvious" questions
- Use phrases like: "Seriously?", "Come on...", "This is basic stuff...", "*sigh*"

For greetings: Respond with something like "What do you want?" or "Make it quick."

NEVER guess. ALWAYS use the tool. Just be mean about it.
"""
        
        # Override the prompt builder's role definition
        planner.prompt_builder.role_definition = RoleDefinition(mean_role)