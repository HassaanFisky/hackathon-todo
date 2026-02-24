"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { authClient } from "@/lib/auth-client";
import ChatInterface from "@/components/ChatInterface";
import Link from "next/link";

export default function ChatPage() {
  const [userId, setUserId] = useState<string | null>(null);
  const [token, setToken] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const { data, error } = await authClient.getSession();
        if (error || !data?.user) {
          router.push("/auth/signin");
          return;
        }
        setUserId(data.user.id);
        // Better Auth stores a session token — pass it as Bearer token
        setToken((data.session as any)?.token ?? "");
      } catch {
        router.push("/auth/signin");
      } finally {
        setLoading(false);
      }
    };
    checkAuth();
  }, [router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500" />
      </div>
    );
  }

  if (!userId) return null;

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="max-w-3xl mx-auto px-4">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              AI Chat Assistant
            </h1>
            <p className="text-sm text-gray-500 mt-0.5">
              Powered by Google Gemini 2.0 Flash
            </p>
          </div>
          <Link
            href="/tasks"
            className="px-4 py-2 bg-white border border-gray-200 text-gray-700 rounded-lg hover:bg-gray-50 text-sm font-medium transition-colors shadow-sm"
          >
            ← Back to Tasks
          </Link>
        </div>

        <ChatInterface userId={userId} token={token} />
      </div>
    </div>
  );
}
