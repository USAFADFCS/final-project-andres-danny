import subprocess
import tempfile
import textwrap

class PythonSandboxTool:
    name = "python_sandbox"
    description = "Executes safe Python code."

    def __call__(self, code: str):
        cleaned = textwrap.dedent(code)

        with tempfile.NamedTemporaryFile(mode="w+", suffix=".py", delete=False) as f:
            f.write(cleaned)
            f.flush()

            try:
                output = subprocess.check_output(
                    ["python", f.name],
                    stderr=subprocess.STDOUT,
                    timeout=3
                )
                return output.decode()
            except subprocess.CalledProcessError as e:
                return e.output.decode()
            except subprocess.TimeoutExpired:
                return "Timeout error: Code took too long."
