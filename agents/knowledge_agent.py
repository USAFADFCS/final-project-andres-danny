from fairlib import (
    SimpleAgent,
    OpenAIAdapter,
    ReActPlanner,
    ToolRegistry,
    ToolExecutor,
    WorkingMemory,
    FinalAnswer,
)


from project_tools.cs110_kb_query import CS110KnowledgeQueryTool


class KnowledgeAgent(SimpleAgent):
    """
    Low-level RAG worker. It receives subtasks from the Instructor and MUST
    return a FinalAnswer object containing ONLY the retrieved text.
    """

    def __init__(self, model="gpt-4o-mini"):
        llm = OpenAIAdapter(model_name=model)

        # Register ONLY the KB tool
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
            stateless=True
        )

        self.role_description = """
You are the CS110 Knowledge Agent.

CRITICAL RULES:
- You ONLY answer using the knowledge base.
- You MUST call the cs110_query tool whenever possible.
- You MUST respond with FinalAnswer("<text>") at the end.
- You NEVER hallucinate or guess.
"""

    # Override handle_final to ensure proper formatting
    async def handle_final(self, result):
        """
        ReActPlanner calls this when the reasoning chain ends.
        Ensure the output is wrapped in FinalAnswer so the Instructor
        receives clean text with no tool metadata.
        """
        if isinstance(result, FinalAnswer):
            return result
        return FinalAnswer(str(result))
