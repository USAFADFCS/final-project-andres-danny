class SyllabusFinderTool:
    name = "syllabus_lookup"
    description = "Finds which CS110 lesson covers a topic."

    def __call__(self, topic: str):
        topic = topic.lower().strip()

        from pipeline.config import project_path

        # Absolute path to lesson schedule file
        path = project_path("cs110_docs/CS110_Lesson_Schedule.txt")

        # Make sure the directory exists
        if not path or not os.path.exists(path):
            return "Syllabus not found. (Missing cs110_docs folder or file)"

        try:
            # Use UTF-8 to avoid encoding issues across OS
            with open(path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines()]
        except Exception as e:
            return f"Error reading syllabus: {e}"

        # Case-insensitive matching
        matches = [line for line in lines if topic in line.lower()]

        if matches:
            return "\n".join(matches)

        return "No matching lesson found."
