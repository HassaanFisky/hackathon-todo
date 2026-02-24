# Frontend Development Context

## Overview

Next.js React frontend built with `app` router. Connects to `FastAPI` via `axios`.
Authentication uses `better-auth`.

## Setup

```bash
npm install
# Or via uv, but Next.js usually uses npm/pnpm
```

## Running

```bash
npm run dev
```

## Environment Variables

- `NEXT_PUBLIC_API_URL`
- `BETTER_AUTH_SECRET`
- `DATABASE_URL`
- `NEXT_PUBLIC_BETTER_AUTH_URL`

## Structure

- `app/api/auth/[...all]` - Better Auth endpoints
- `lib/api.ts` - Axios configuration
- `lib/auth.ts` - Better Auth configuration

## Tailwind CSS

Configured with `@tailwindcss/postcss` per new Next.js 15+ defaults. Ensure CSS imports correctly.
