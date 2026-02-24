# MCP Tools — Gemini Function Declarations

## Tool: add_task

| Parameter   | Type   | Required | Description                                   |
| ----------- | ------ | -------- | --------------------------------------------- |
| user_id     | string | ✅       | Authenticated user's ID (injected by backend) |
| title       | string | ✅       | Task title, 1–200 chars                       |
| description | string | ❌       | Task description, max 1000 chars              |

**Returns**: `{ task_id: int, status: "created", title: string }`
**DB**: `INSERT INTO task (user_id, title, description, completed) VALUES (...)`

---

## Tool: list_tasks

| Parameter | Type   | Required | Description                                      |
| --------- | ------ | -------- | ------------------------------------------------ |
| user_id   | string | ✅       | Authenticated user's ID                          |
| status    | string | ❌       | "all", "pending", or "completed". Default: "all" |

**Returns**: `[{ id, title, completed, description, created_at }, ...]`
**DB**: `SELECT * FROM task WHERE user_id = ? [AND completed = ?]`

---

## Tool: complete_task

| Parameter | Type    | Required | Description             |
| --------- | ------- | -------- | ----------------------- |
| user_id   | string  | ✅       | Authenticated user's ID |
| task_id   | integer | ✅       | ID of task to toggle    |

**Returns**: `{ task_id: int, status: "completed" | "incomplete", title: string }`
**DB**: `UPDATE task SET completed = NOT completed WHERE id = ? AND user_id = ?`

---

## Tool: delete_task

| Parameter | Type    | Required | Description             |
| --------- | ------- | -------- | ----------------------- |
| user_id   | string  | ✅       | Authenticated user's ID |
| task_id   | integer | ✅       | ID of task to delete    |

**Returns**: `{ task_id: int, status: "deleted", title: string }`
**DB**: `DELETE FROM task WHERE id = ? AND user_id = ?`

---

## Tool: update_task

| Parameter   | Type    | Required | Description             |
| ----------- | ------- | -------- | ----------------------- |
| user_id     | string  | ✅       | Authenticated user's ID |
| task_id     | integer | ✅       | ID of task to update    |
| title       | string  | ❌       | New title               |
| description | string  | ❌       | New description         |

**Returns**: `{ task_id: int, status: "updated", title: string }`
**DB**: `UPDATE task SET title = ?, description = ? WHERE id = ? AND user_id = ?`

---

## Error Responses

All tools return `{ error: "Task not found" }` if:

- `task_id` does not exist
- The task belongs to a different `user_id`
