"use client";

import { useEffect, useState } from "react";
import { api } from "../lib/api";

type Task = {
  id: number;
  user_id: string;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
};

type TaskListProps = {
  userId: string;
  refreshKey: number;
};

export default function TaskList({ userId, refreshKey }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Edit states
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editTitle, setEditTitle] = useState("");
  const [editDesc, setEditDesc] = useState("");

  const fetchTasks = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get(`/api/${userId}/tasks?sort=desc`);
      setTasks(response.data);
    } catch (err: any) {
      console.error(err);
      setError("Failed to fetch tasks.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [userId, refreshKey]);

  const toggleComplete = async (id: number) => {
    try {
      await api.patch(`/api/${userId}/tasks/${id}/complete`);
      fetchTasks();
    } catch (err) {
      console.error("Failed to toggle completion", err);
    }
  };

  const deleteTask = async (id: number) => {
    try {
      await api.delete(`/api/${userId}/tasks/${id}`);
      fetchTasks();
    } catch (err) {
      console.error("Failed to delete task", err);
    }
  };

  const startEdit = (task: Task) => {
    setEditingId(task.id);
    setEditTitle(task.title);
    setEditDesc(task.description || "");
  };

  const cancelEdit = () => {
    setEditingId(null);
    setEditTitle("");
    setEditDesc("");
  };

  const saveEdit = async (id: number) => {
    if (!editTitle.trim()) return;
    try {
      await api.put(`/api/${userId}/tasks/${id}`, {
        title: editTitle,
        description: editDesc,
      });
      setEditingId(null);
      fetchTasks();
    } catch (err) {
      console.error("Failed to update task", err);
    }
  };

  if (loading)
    return (
      <div className="text-center py-8 text-gray-500">Loading tasks...</div>
    );
  if (error)
    return <div className="text-center py-8 text-red-500">{error}</div>;
  if (tasks.length === 0)
    return (
      <div className="text-center py-8 text-gray-500 italic bg-white rounded-lg shadow-sm border border-gray-100">
        No tasks found. Add one above!
      </div>
    );

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <div
          key={task.id}
          className={`flex flex-col bg-white p-5 rounded-lg border flex-1 break-inside-avoid shadow-sm transition-all duration-200 ${task.completed ? "border-green-200 bg-green-50 shadow-none" : "border-gray-200 hover:shadow-md"}`}
        >
          {editingId === task.id ? (
            <div className="flex flex-col gap-3">
              <input
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                className="px-3 py-2 border border-blue-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <textarea
                value={editDesc}
                onChange={(e) => setEditDesc(e.target.value)}
                className="px-3 py-2 border border-blue-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none h-20"
              />
              <div className="flex justify-end gap-2 mt-2">
                <button
                  onClick={cancelEdit}
                  className="px-4 py-1.5 text-sm text-gray-600 hover:text-gray-900 border border-transparent hover:bg-gray-100 rounded transition duration-200"
                >
                  Cancel
                </button>
                <button
                  onClick={() => saveEdit(task.id)}
                  className="px-4 py-1.5 text-sm text-white bg-blue-600 hover:bg-blue-700 rounded shadow-sm transition duration-200"
                >
                  Save
                </button>
              </div>
            </div>
          ) : (
            <div className="flex items-start gap-4">
              <button
                onClick={() => toggleComplete(task.id)}
                className={`flex-shrink-0 mt-1 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors duration-200 ${
                  task.completed
                    ? "bg-green-500 border-green-500 text-white"
                    : "border-gray-300 hover:border-gray-400"
                }`}
                aria-label={
                  task.completed ? "Mark incomplete" : "Mark complete"
                }
              >
                {task.completed ? "✓" : "○"}
              </button>

              <div className="flex-1 min-w-0">
                <h4
                  className={`text-lg font-medium truncate ${task.completed ? "text-gray-500 line-through" : "text-gray-900"}`}
                >
                  {task.title}
                </h4>
                {task.description && (
                  <p
                    className={`text-sm mt-1 whitespace-pre-wrap ${task.completed ? "text-gray-400" : "text-gray-600"}`}
                  >
                    {task.description}
                  </p>
                )}
                <div className="text-xs text-gray-400 mt-3 pt-3 border-t border-gray-100 flex items-center justify-between">
                  <span>
                    Created: {new Date(task.created_at).toLocaleDateString()}
                  </span>

                  <div className="flex gap-3">
                    <button
                      onClick={() => startEdit(task)}
                      className="text-blue-500 hover:text-blue-700 font-medium transition duration-200 hover:underline"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => deleteTask(task.id)}
                      className="text-red-500 hover:text-red-700 font-medium transition duration-200 hover:underline"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
