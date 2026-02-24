# Task CRUD Spec

## User Stories

- As a user, I want to add tasks so I can keep track of what to do.
- As a user, I want to view my tasks to easily see what is remaining.
- As a user, I want to edit a task's title or description if I make a mistake.
- As a user, I want to delete tasks I no longer need.
- As a user, I want to toggle task completion to mark tasks as done or pending.

## Acceptance Criteria

- Tasks are specific to the authenticated user.
- A user cannot view or modify another user's tasks.
- Created tasks default to incomplete.
- Empty titles are not allowed.
- The UI gracefully handles loading states and potential API errors.
