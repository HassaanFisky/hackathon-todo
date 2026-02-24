# Authentication Spec

## Flow

- Uses Better Auth for full authentication stack.
- Login via email/password.
- Sign up via Name, Email, Password.

## Security

- API secures endpoints checking JWT tokens using `python-jose`.
- All endpoints must include an `Authorization: Bearer <token>` header, sourced from the `better-auth` session.
- Passwords are hashed by Better Auth and stored in the PostgreSQL database.
- A shared `BETTER_AUTH_SECRET` is used between FastAPI and Next.js to encode and decode the token if using JWT plugins. If strictly session-based, verify the session securely against the database or JWT depending on the setup.

## Environment Variables

- `BETTER_AUTH_SECRET` (Must be at least 32 characters long)
- `DATABASE_URL`
- `NEXT_PUBLIC_API_URL`
- `NEXT_PUBLIC_BETTER_AUTH_URL`
