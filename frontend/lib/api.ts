import axios from "axios";

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
});

// The JWT token is managed differently based on setup.
// If better-auth uses an HTTP Only cookie, the backend would verify it.
// However, the prompt specifically requires the token to be sent in the `Authorization` header.
// Better auth client stores session token or we can obtain it from `useSession` or `getSession()`.
// Since lib/api.ts isn't necessarily within a react scope, we will export a function to configure the token.
// Or attach interceptors here if token is saved in localStorage by betterAuth custom setup. Wait! better auth uses cookies natively.
// If we must pass the authorization header explicitly, we can set it per request in the components.

export const setAuthToken = (token: string | null) => {
  if (token) {
    api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common["Authorization"];
  }
};
