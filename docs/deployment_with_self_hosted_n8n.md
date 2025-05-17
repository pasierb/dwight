# Deployment with self-hosted n8n




`docker-compose.yml`

```yml
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    restart: always
    cap_add:
      - SYS_ADMIN
    security_opt:
      - seccomp=unconfined
    ports:
      - 5678:5678
    environment:
      - N8N_HOST=${SUBDOMAIN}.${DOMAIN_NAME}
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - NODE_ENV=production
      - WEBHOOK_URL=https://${SUBDOMAIN}.${DOMAIN_NAME}/
      - GENERIC_TIMEZONE=${GENERIC_TIMEZONE}
    volumes:
      - n8n_data:/home/node/.n8n
      - ${DATA_FOLDER}/local_files:/files
  dwigt:
    # Replace with the actual path to where to cloned Dwight repo
    build: /path/to/repo/dwight
    environment:
      - GOOGLE_GENAI_USE_VERTEXAI=FALSE
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}

      
volumes:
  n8n_data:
    external: true
```

For more details how to deploy n8n see [official n8n docs](https://docs.n8n.io/hosting/installation/docker/)

`Dockerfile` (see full [Dockerfile](../Dockerfile))

```Dockerfile
...

# Expose the port the app runs on
EXPOSE 8080

# Run the web service
CMD ["uv", "run", "adk", "api_server"]
```
