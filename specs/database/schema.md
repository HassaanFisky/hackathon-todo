# Database Schema

## Users Table (Managed by Better Auth)

- `id`: Text (Primary Key)
- `name`: Text
- `email`: Text (Unique)
- `emailVerified`: Boolean
- `image`: Text
- `createdAt`: Timestamp
- `updatedAt`: Timestamp

## Sessions Table (Managed by Better Auth)

- `id`: Text (Primary Key)
- `expiresAt`: Timestamp
- `ipAddress`: Text
- `userAgent`: Text
- `userId`: Text (Foreign Key)

## Accounts Table (Managed by Better Auth)

- Accounts for credentials and providers...

## Tasks Table

- `id`: Integer (Primary Key, Auto-increment)
- `user_id`: Text (Foreign Key to users.id)
- `title`: Varchar(200) (Not Null)
- `description`: Varchar(1000) (Nullable)
- `completed`: Boolean (Default: False)
- `created_at`: Timestamp (Default: Now)
- `updated_at`: Timestamp
