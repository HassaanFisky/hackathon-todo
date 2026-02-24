import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: {
    url: process.env.DATABASE_URL!,
    type: "postgres",
  },
  secret: process.env.BETTER_AUTH_SECRET,
  emailAndPassword: {
    enabled: true,
  },
});
