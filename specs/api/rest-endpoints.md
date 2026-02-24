# REST API Endpoints

## 1. GET /api/{user_id}/tasks

List all tasks for a specific user.
**Query Parameters**:

- `status` (completed, pending)
- `sort` (asc, desc)
  **Response**: `200 OK` `List[Task]`

## 2. POST /api/{user_id}/tasks

Create a new task.
**Body**:

- `title` (Required: string)
- `description` (Optional: string)
  **Response**: `200 OK` `Task`

## 3. GET /api/{user_id}/tasks/{id}

Get a specific task.
**Response**: `200 OK` `Task`
**Errors**: `404 Not Found`, `403 Forbidden`

## 4. PUT /api/{user_id}/tasks/{id}

Update a task's title or description.
**Body**:

- `title` (Optional: string)
- `description` (Optional: string)
  **Response**: `200 OK` `Task`

## 5. DELETE /api/{user_id}/tasks/{id}

Delete a specific task.
**Response**: `200 OK` `{"message": "Task deleted"}`

## 6. PATCH /api/{user_id}/tasks/{id}/complete

Toggle the completed status of a task.
**Response**: `200 OK` `Task`
