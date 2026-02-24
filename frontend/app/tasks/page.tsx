"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { authClient } from "../../lib/auth-client";
import { setAuthToken } from "../../lib/api";
import TaskList from "../../components/TaskList";
import TaskForm from "../../components/TaskForm";

export default function TasksPage() {
  const router = useRouter();
  const [session, setSession] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const { data, error } = await authClient.getSession();

        if (error || !data || !data.user) {
          router.push("/auth/signin");
          return;
        }

        // Ensure token functionality. In Better Auth, you might need
        // a custom token or JWT for an external FastAPI backend.
        // For simplicity, we can pass the session token to the backend,
        // or configure the backend to read Better Auth cookies.
        // The spec requires parsing JWT in auth.py decoding Better Auth token.
        // We will pass the token if available, depending on the plugin.
        // However, better-auth client handles cookies natively.
        // Assuming your backend uses python-jose to decode the same token:

        // Quick way to pass cookie/token if required:
        // setAuthToken(data.session.token); // Adjust depending on your exact Better Auth spec implementation

        setSession(data);
      } catch (err) {
        router.push("/auth/signin");
      } finally {
        setLoading(false);
      }
    };
    checkAuth();
  }, [router]);

  const handleTaskCreated = () => {
    setRefreshKey((prev) => prev + 1);
  };

  const handleSignOut = async () => {
    await authClient.signOut();
    router.push("/auth/signin");
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-xl font-semibold text-gray-500 animate-pulse">
          Loading workspace...
        </div>
      </div>
    );
  }

  if (!session) return null;

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex-shrink-0 flex items-center">
              <h1 className="text-xl font-bold text-gray-900">
                Hackathon Todo
              </h1>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600 hidden sm:block">
                Welcome, {session.user.name || session.user.email}
              </span>
              <button
                onClick={handleSignOut}
                className="inline-flex items-center px-3 py-1.5 border border-transparent text-sm font-medium rounded-md text-red-600 bg-red-50 hover:bg-red-100 transition-colors"
              >
                Sign out
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:truncate mb-2">
            Your Tasks
          </h2>
          <p className="text-gray-500">Manage your checklist effectively.</p>
        </div>

        <TaskForm userId={session.user.id} onTaskCreated={handleTaskCreated} />

        <div className="mt-8">
          <h3 className="text-lg font-medium text-gray-900 mb-4">All Tasks</h3>
          <TaskList userId={session.user.id} refreshKey={refreshKey} />
        </div>
      </main>
    </div>
  );
}
