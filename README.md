# computeruser

A minimal modular framework for controlling a computer through an AI agent.

The architecture follows a six step cycle:

1. **Interaction** – parse user commands.
2. **Perception** – capture screenshot and UI tree (placeholder).
3. **Decision** – choose actions based on command and perception.
4. **Execution** – convert the planned action to concrete steps.
5. **Verification** – check if the action met the user's request.
6. **Memory** – store the entire cycle for later analysis.

Each step is implemented in a separate module under `ai_controller` and is kept
independent for later optimization.

Run a demonstration cycle:

```bash
python main.py
```
