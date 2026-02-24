# Use node LTS
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci

# Copy full application
COPY . .

# Build application
RUN npm run build

EXPOSE 3000

ENV PORT 3000

# Start application server
CMD ["npm", "start"]
