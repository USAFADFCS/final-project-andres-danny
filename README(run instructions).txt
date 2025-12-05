## How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
```
Edit `.env` and add your API key.

### 3. Build the Knowledge Base
```bash
python pipeline/build_kb.py
```

### 4. Start the Server
```bash
uvicorn main:app --reload
```
The UI will be available at `http://127.0.0.1:8000`

### 5. Run Evaluation (Optional)
```bash
python evaluate_system.py
```

DOCUMENTATION STATEMENT:
I got current CS110 docs from freshman in the course currently, C4C Ferguson, Duckworth, and Dark.
I consulted the course guidelines and demos for fairllm extensively
Claude helped by providing structured explanations, code templates, and debugging guidance for portions of the project where I was stuck.
Claude walked me through logic corrections, helping refine function behavior, and generating portions of the final report that summarized my design decisions and implementation details.
ChatGPT helped by supplying missing code components, fixing integration issues, and explaining how different modules work together within the project.
ChatGPT did this by troubleshooting errors, rewriting sections for clarity, and helping complete the remaining tasks after Claude’s contributions so the final project was fully functional and aligned with the requirements.
Claude generated the final report, as is allowed via the final turn in doc in canvas.