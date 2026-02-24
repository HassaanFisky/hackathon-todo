"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { authClient } from "../lib/auth-client";

export default function Home() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkSession = async () => {
      try {
        const { data, error } = await authClient.getSession();
        if (data && data.user && !error) {
          router.push("/tasks");
        } else {
          router.push("/auth/signin");
        }
      } catch (err) {
        router.push("/auth/signin");
      } finally {
        setLoading(false);
      }
    };
    checkSession();
  }, [router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-xl font-semibold text-gray-500 animate-pulse">
          Initializing...
        </div>
      </div>
    );
  }

  return null;
}
