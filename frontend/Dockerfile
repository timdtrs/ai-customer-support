FROM node:18-slim

WORKDIR /app

# Copy only manifest files first to leverage Docker layer caching
COPY package*.json ./

# Install all dependencies (including optional platform-specific ones like Rollup)
# Use npm ci to respect the lockfile and ensure clean installs in CI/containers
RUN npm ci

# Copy the rest of the app sources
COPY . .

EXPOSE 5173

# Startbefehl
CMD ["npm", "run", "dev", "--", "--host"]
