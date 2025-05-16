# Use the official uv image with Python 3.11
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# Set working directory
WORKDIR /app

# Copy the rest of the application
COPY . .

# Install dependencies in a separate layer
RUN uv sync


# Expose the port the app runs on
EXPOSE 8080

# Run the web service
CMD ["uv", "run", "adk", "api_server"]
