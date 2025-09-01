# computeruser

A minimal modular framework for controlling a computer through an AI agent.

The architecture follows a six step cycle:

1. **Interaction** – parse user commands.
2. **Perception** – create a temporary screenshot file and minimal UI tree.
3. **Decision** – parse simple commands to choose an action.
4. **Execution** – simulate the planned action and return the new state.
5. **Verification** – ensure the action changed the environment as expected.
6. **Memory** – store the entire cycle for later analysis.

Each step is implemented in a separate module under `ai_controller` and is kept
independent for later optimization.

Run a demonstration cycle:

```bash
python main.py
```
