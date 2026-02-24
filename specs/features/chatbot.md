# Feature: AI Todo Chatbot

## Technology

- Google Gemini 2.0 Flash API (free tier)
- `google-generativeai` Python SDK (NOT OpenAI)
- Gemini Function Calling (implements MCP tool execution)
- Custom `ChatInterface` React component (frontend)

## Architecture

```
ChatInterface UI → POST /api/{user_id}/chat
  → Gemini Agent (function calling loop)
    → mcp_server.py tool functions
      → Neon PostgreSQL (tasks table)
  ← AI text response
← ChatResponse (conversation_id, response, tool_calls)
```

## Chat Endpoint

`POST /api/{user_id}/chat`

**Request**:

```json
{ "conversation_id": 1, "message": "Add a task to buy milk" }
```

**Response**:

```json
{ "conversation_id": 1, "response": "Done! I've added 'Buy milk' to your list. ✅", "tool_calls": [...] }
```

Requires: `Authorization: Bearer <token>` header.

## Database Models Added

- **Conversation**: id, user_id, created_at, updated_at
- **Message**: id, conversation_id (FK), user_id, role ("user"/"assistant"), content, created_at

## MCP Tools (Gemini Function Declarations)

1. `add_task(user_id, title, description?)` — INSERT into tasks
2. `list_tasks(user_id, status?)` — SELECT from tasks
3. `complete_task(user_id, task_id)` — Toggle completed
4. `delete_task(user_id, task_id)` — DELETE task
5. `update_task(user_id, task_id, title?, description?)` — UPDATE task

## Stateless Flow (each request is fully self-contained)

1. Receive `message` + optional `conversation_id`
2. Create Conversation row if none provided
3. Load all `Message` rows for the conversation from DB
4. Save incoming user message to DB
5. Build Gemini chat history from DB rows
6. Send to Gemini with function declarations
7. Agentic loop: execute function calls, feed results back to Gemini
8. Get final text response from Gemini
9. Save assistant response to DB
10. Return `{conversation_id, response, tool_calls}`

Zero in-memory state between requests.
