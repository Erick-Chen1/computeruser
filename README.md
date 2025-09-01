# computeruser

A minimal modular framework for controlling a computer through an AI agent.

The architecture follows a six step cycle:

1. **Interaction** – validate user commands.
2. **Perception** – take a real screenshot and build a light‑weight UI tree via OmniParser.
3. **Decision** – optional LLM planning converts natural language into actions.
4. **Execution** – perform mouse/keyboard actions using `pyautogui`.
5. **Verification** – optionally use a VLM to check before/after state or fall back to a simple heuristic.
6. **Memory** – store the entire cycle for later analysis.

Each step lives in a dedicated module under `ai_controller` so components remain decoupled and can be swapped independently.

## Usage

Install dependencies:

```bash
pip install -r requirements.txt
```

Run an interactive session:

```bash
python main.py
```

Type natural language commands such as "click OK" or "type hello" to control the computer. Type `exit` to quit.
