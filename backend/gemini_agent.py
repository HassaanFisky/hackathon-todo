"""
gemini_agent.py — Gemini 2.0 Flash agent with function calling.
Uses google-generativeai SDK (NOT OpenAI). No openai package is imported.
"""
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from mcp_server import add_task, list_tasks, complete_task, delete_task, update_task

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ---------------------------------------------------------------------------
# Gemini Function Declarations (= MCP tool schema)
# ---------------------------------------------------------------------------
_tools = [
    genai.protos.Tool(
        function_declarations=[
            genai.protos.FunctionDeclaration(
                name="add_task",
                description="Add a new task to the user's todo list.",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "title": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Task title (required, 1-200 chars)",
                        ),
                        "description": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Task description (optional, max 1000 chars)",
                        ),
                    },
                    required=["title"],
                ),
            ),
            genai.protos.FunctionDeclaration(
                name="list_tasks",
                description="List all tasks for the user. Can filter by status.",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "status": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Filter: 'all', 'pending', or 'completed'. Default: 'all'",
                        ),
                    },
                    required=[],
                ),
            ),
            genai.protos.FunctionDeclaration(
                name="complete_task",
                description="Toggle a task's completion status (complete ↔ incomplete).",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "task_id": genai.protos.Schema(
                            type=genai.protos.Type.INTEGER,
                            description="The numeric ID of the task to toggle",
                        ),
                    },
                    required=["task_id"],
                ),
            ),
            genai.protos.FunctionDeclaration(
                name="delete_task",
                description="Permanently delete a task.",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "task_id": genai.protos.Schema(
                            type=genai.protos.Type.INTEGER,
                            description="The numeric ID of the task to delete",
                        ),
                    },
                    required=["task_id"],
                ),
            ),
            genai.protos.FunctionDeclaration(
                name="update_task",
                description="Update a task's title or description.",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "task_id": genai.protos.Schema(
                            type=genai.protos.Type.INTEGER,
                            description="The numeric ID of the task to update",
                        ),
                        "title": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="New title (optional)",
                        ),
                        "description": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="New description (optional)",
                        ),
                    },
                    required=["task_id"],
                ),
            ),
        ]
    )
]

# Map Gemini function names → Python callables
_FUNCTION_MAP = {
    "add_task": add_task,
    "list_tasks": list_tasks,
    "complete_task": complete_task,
    "delete_task": delete_task,
    "update_task": update_task,
}

_SYSTEM_PROMPT = (
    "You are a helpful, friendly todo-list assistant. "
    "Use the available tools to manage the user's tasks. "
    "Always confirm actions with a brief, friendly message. "
    "When listing tasks, format them clearly (numbered list). "
    "If there are no tasks, tell the user their list is empty. "
    "Be concise. Do not invent task IDs — only use IDs returned by list_tasks."
)


def _get_function_call(response) -> tuple[str | None, dict]:
    """Safely extract function_call name and args from a Gemini response."""
    try:
        for part in response.candidates[0].content.parts:
            if part.function_call and part.function_call.name:
                return part.function_call.name, dict(part.function_call.args)
    except (AttributeError, IndexError, TypeError):
        pass
    return None, {}


def _get_text(response) -> str:
    """Safely extract text from a Gemini response."""
    try:
        for part in response.candidates[0].content.parts:
            if hasattr(part, "text") and part.text:
                return part.text.strip()
    except (AttributeError, IndexError, TypeError):
        pass
    return "I couldn't generate a response. Please try again."


async def chat_with_gemini(
    user_id: str, message: str, history: list[dict]
) -> tuple[str, list[dict]]:
    """
    Send a message to Gemini 2.0 Flash with chat history and function calling.

    Args:
        user_id:  The authenticated user's ID (injected into every tool call).
        message:  The user's latest message.
        history:  Previous messages [{role: "user"/"assistant", content: str}]

    Returns:
        (response_text, tool_calls_list)
    """
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        tools=_tools,
        system_instruction=_SYSTEM_PROMPT,
    )

    # Convert DB history format → Gemini chat history format
    gemini_history = []
    for msg in history:
        role = "model" if msg["role"] == "assistant" else "user"
        gemini_history.append({"role": role, "parts": [msg["content"]]})

    chat = model.start_chat(history=gemini_history)
    response = chat.send_message(message)

    tool_calls: list[dict] = []

    # ------------------------------------------------------------------ #
    # Agentic loop: keep executing function calls until Gemini returns text
    # ------------------------------------------------------------------ #
    for _ in range(10):  # safety cap — avoid infinite loops
        fn_name, fn_args = _get_function_call(response)

        if not fn_name:
            break  # No function call → Gemini is done

        # Inject user_id (Gemini never knows who the user is)
        fn_args["user_id"] = user_id

        # Execute the corresponding Python function
        if fn_name in _FUNCTION_MAP:
            result = _FUNCTION_MAP[fn_name](**fn_args)
        else:
            result = {"error": f"Unknown function: {fn_name}"}

        tool_calls.append({"function": fn_name, "args": fn_args, "result": result})

        # Return the function result to Gemini
        response = chat.send_message(
            genai.protos.Content(
                parts=[
                    genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name=fn_name,
                            response={"result": json.dumps(result, default=str)},
                        )
                    )
                ]
            )
        )

    response_text = _get_text(response)
    return response_text, tool_calls
