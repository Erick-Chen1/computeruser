"""Simple orchestrator demonstrating the modular architecture."""
from ai_controller import (
    interaction,
    perception,
    decision,
    execution,
    verification,
    memory,
)


def run_cycle(user_text: str, mem: memory.Memory) -> verification.VerificationResult:
    """Run a single interaction cycle."""
    instr = interaction.parse_user_command(user_text)
    before = perception.capture_environment()
    act = decision.plan_action(instr, before)
    after = execution.execute_action(act)
    result = verification.verify_action(instr, before, after)
    mem.add_record(instr, before, after, act, result)
    return result


if __name__ == "__main__":
    mem = memory.Memory()
    print("Enter natural language commands (type 'exit' to quit).")
    while True:
        try:
            user_input = input("command> ").strip()
        except EOFError:  # pragma: no cover - interactive only
            break
        if user_input.lower() in {"exit", "quit"}:
            break
        result = run_cycle(user_input, mem)
        print(result)
