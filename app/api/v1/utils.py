import json
from pydantic_ai.messages import (
    ModelResponse,
    TextPart,
    ToolCallPart,
    ModelRequest,
    ToolReturnPart,
    ThinkingPart,
)

def print_agent_execution_steps(response: ModelResponse):
    execution_steps = []
    try:
        for message in response.all_messages():
            if isinstance(message, ModelResponse):
                if message.usage:
                    usage = message.usage
                for part in message.parts:

                    # 1. Handle Text (Thoughts)
                    if isinstance(part, TextPart):
                        step_info = (
                            f"🧠 THOUGHT:\n{part.content}\n Token Usage: {usage}"
                        )
                        execution_steps.append(step_info)

                    if isinstance(part, ThinkingPart):
                        step_info = (
                            f"🧠 THOUGHT:\n{part.content}\n Token Usage: {usage}"
                        )
                        execution_steps.append(step_info)

                    # 2. Handle Tool Calls
                    elif isinstance(part, ToolCallPart):
                        args_formatted = json.dumps(part.args, indent=2)
                        step_info = f"🛠️ TOOL CALL: {part.tool_name}\nArguments:\n{args_formatted}\n Token Usage: {usage}"
                        execution_steps.append(step_info)

            # 3. Handle Tool Returns
            elif isinstance(message, ModelRequest):
                for part in message.parts:
                    if isinstance(part, ToolReturnPart):
                        output = part.content

                        execution_steps.append(
                            f"🔙 TOOL RETURN ({part.tool_name}):\n{output}\n"
                        )

        for i, step in enumerate(execution_steps):
            print(f"--- Step {i+1} ---")
            print(step, "\n")
    except Exception as e:
        print(f"Error printing agent execution steps: {e}")

    return execution_steps