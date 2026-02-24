"use client";

import { useState } from "react";
import { api } from "../../lib/api";

type TaskFormProps = {
  userId: string;
  onTaskCreated: () => void;
};

export default function TaskForm({ userId, onTaskCreated }: TaskFormProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setLoading(true);
    try {
      await api.post(`/api/${userId}/tasks`, { title, description });
      setTitle("");
      setDescription("");
      onTaskCreated();
    } catch (error) {
      console.error("Failed to create task", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="mb-6 bg-white p-6 shadow-md rounded-lg break-inside-avoid border border-gray-100"
    >
      <h3 className="text-xl font-semibold text-gray-800 mb-4">Add New Task</h3>
      <div className="mb-4">
        <label
          htmlFor="title"
          className="block text-gray-700 text-sm font-medium mb-1"
        >
          Title <span className="text-red-500">*</span>
        </label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="What needs to be done?"
          required
        />
      </div>
      <div className="mb-4">
        <label
          htmlFor="description"
          className="block text-gray-700 text-sm font-medium mb-1"
        >
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none h-24"
          placeholder="Add some details... (optional)"
        ></textarea>
      </div>
      <button
        type="submit"
        disabled={loading || !title.trim()}
        className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? "Adding..." : "Add Task"}
      </button>
    </form>
  );
}
