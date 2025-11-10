# Docker & Docker Compose: Complete Beginner to Advanced Guide

## Table of Contents
1. [Introduction to Docker](#introduction-to-docker)
2. [Docker Basics](#docker-basics)
3. [Dockerfile Fundamentals](#dockerfile-fundamentals)
4. [Advanced Dockerfile Techniques](#advanced-dockerfile-techniques)
5. [Docker Compose Basics](#docker-compose-basics)
6. [Advanced Docker Compose](#advanced-docker-compose)
7. [Real-World Examples](#real-world-examples)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

---

## Introduction to Docker

### What is Docker? 🐳
Docker is a platform that uses **containerization** technology to package applications and their dependencies into lightweight, portable containers.

### Why Use Docker?
- **Consistency**: "Works on my machine" problem solved
- **Portability**: Run anywhere (development, testing, production)
- **Efficiency**: Lightweight compared to virtual machines
- **Scalability**: Easy to scale applications
- **Isolation**: Applications don't interfere with each other

### Docker vs Virtual Machines
```
Virtual Machine:
[App A] [App B] [App C]
[Guest OS] [Guest OS] [Guest OS]
[Hypervisor]
[Host Operating System]
[Infrastructure]

Docker:
[App A] [App B] [App C]
[Docker Engine]
[Host Operating System]
[Infrastructure]
```

---

## Docker Basics

### Key Concepts
- **Image**: A blueprint/template for creating containers
- **Container**: A running instance of an image
- **Registry**: A storage location for images (Docker Hub)
- **Volume**: Persistent data storage
- **Network**: Communication between containers

### Essential Docker Commands

#### Image Management
```bash
# Pull an image from registry
docker pull nginx:latest

# List all images
docker images

# Remove an image
docker rmi image_name:tag

# Build an image from Dockerfile
docker build -t my-app:v1.0 .

# Push image to registry
docker push username/my-app:v1.0
```

#### Container Management
```bash
# Run a container
docker run -d --name my-container -p 8080:80 nginx

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop a container
docker stop my-container

# Start a stopped container
docker start my-container

# Remove a container
docker rm my-container

# Execute command in running container
docker exec -it my-container bash

# View container logs
docker logs my-container

# Follow logs in real-time
docker logs -f my-container
```

#### System Management
```bash
# View Docker system information
docker info

# Clean up unused resources
docker system prune

# View resource usage
docker stats
```

---

## Dockerfile Fundamentals

### What is a Dockerfile?
A Dockerfile is a text file containing instructions to build a Docker image.

### Basic Dockerfile Structure
```dockerfile
# Base image
FROM ubuntu:20.04

# Metadata
LABEL maintainer="your-email@example.com"
LABEL version="1.0"
LABEL description="My awesome application"

# Environment variables
ENV NODE_VERSION=16.20.0
ENV APP_HOME=/usr/src/app

# Set working directory
WORKDIR $APP_HOME

# Copy files
COPY package*.json ./
COPY . .

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install app dependencies
RUN npm install --production

# Expose port
EXPOSE 3000

# Define entry point
CMD ["npm", "start"]
```

### Essential Dockerfile Instructions

#### FROM - Base Image
```dockerfile
# Use official Node.js image
FROM node:16-alpine

# Use specific version
FROM python:3.9-slim

# Multi-stage build
FROM node:16 AS builder
FROM nginx:alpine AS production
```

#### WORKDIR - Set Working Directory
```dockerfile
# Set working directory
WORKDIR /app

# All subsequent commands run from /app
COPY . .
RUN npm install
```

#### COPY vs ADD
```dockerfile
# COPY - Simple file copying (preferred)
COPY src/ /app/src/
COPY package.json /app/

# ADD - Has additional features (auto-extraction, URL support)
ADD https://example.com/file.tar.gz /app/
ADD archive.tar.gz /app/  # Auto-extracts
```

#### RUN - Execute Commands
```dockerfile
# Single command
RUN npm install

# Multiple commands (inefficient)
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

# Multiple commands (efficient - single layer)
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

#### ENV - Environment Variables
```dockerfile
ENV NODE_ENV=production
ENV PORT=3000
ENV DATABASE_URL=postgresql://localhost:5432/mydb

# Use environment variables
WORKDIR /app
EXPOSE $PORT
```

#### EXPOSE - Document Ports
```dockerfile
# Document that app listens on port 3000
EXPOSE 3000

# Multiple ports
EXPOSE 3000 8080 9000
```

#### VOLUME - Persistent Storage
```dockerfile
# Create a volume mount point
VOLUME ["/data"]

# Multiple volumes
VOLUME ["/data", "/logs", "/config"]
```

#### User Management
```dockerfile
# Create user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Switch to non-root user
USER appuser

# Or use numeric UID
USER 1001
```

#### CMD vs ENTRYPOINT
```dockerfile
# CMD - Default command (can be overridden)
CMD ["npm", "start"]

# ENTRYPOINT - Always executes (cannot be overridden)
ENTRYPOINT ["python", "app.py"]

# Combination - ENTRYPOINT + CMD
ENTRYPOINT ["python", "app.py"]
CMD ["--help"]  # Default argument
```

---

## Advanced Dockerfile Techniques

### Multi-Stage Builds
Perfect for reducing image size by separating build and runtime environments.

```dockerfile
# Build stage
FROM node:16 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Production stage
FROM node:16-alpine AS production
WORKDIR /app

# Copy only production files
COPY --from=builder /app/node_modules ./node_modules
COPY . .

EXPOSE 3000
CMD ["npm", "start"]
```

### Build Arguments
```dockerfile
# Define build arguments
ARG NODE_VERSION=16
ARG APP_ENV=production

# Use in FROM instruction
FROM node:${NODE_VERSION}-alpine

# Use in environment variables
ENV NODE_ENV=${APP_ENV}

# Build with custom arguments
# docker build --build-arg NODE_VERSION=18 --build-arg APP_ENV=development .
```

### Conditional Instructions
```dockerfile
ARG ENVIRONMENT=production

# Install development dependencies only in dev
RUN if [ "$ENVIRONMENT" = "development" ]; then \
        npm install; \
    else \
        npm ci --only=production; \
    fi
```

### Health Checks
```dockerfile
# Add health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Custom health check script
COPY healthcheck.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/healthcheck.sh
HEALTHCHECK CMD /usr/local/bin/healthcheck.sh
```

### Optimizing Docker Images

#### Layer Caching
```dockerfile
# ❌ Bad - Changes in source code invalidate npm install layer
COPY . .
RUN npm install

# ✅ Good - package.json changes rarely, better caching
COPY package*.json ./
RUN npm install
COPY . .
```

#### Reducing Image Size
```dockerfile
# Use alpine images
FROM node:16-alpine

# Multi-stage builds
FROM node:16 AS builder
# ... build steps ...
FROM node:16-alpine AS production
COPY --from=builder /app/dist ./dist

# Remove unnecessary files
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Use .dockerignore file
```

#### .dockerignore File
```dockerignore
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.nyc_output
coverage
.DS_Store
*.log
```

---

## Docker Compose Basics

### What is Docker Compose?
Docker Compose is a tool for defining and running multi-container Docker applications using a YAML file.

### Basic docker-compose.yml Structure
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    depends_on:
      - database
    volumes:
      - .:/app
      - /app/node_modules

  database:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - db_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  db_data:
```

### Essential Docker Compose Commands
```bash
# Start services in detached mode
docker-compose up -d

# Start specific service
docker-compose up web

# Build and start
docker-compose up --build

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# View logs
docker-compose logs

# Follow logs for specific service
docker-compose logs -f web

# Execute command in service
docker-compose exec web bash

# Scale services
docker-compose up --scale web=3

# View running services
docker-compose ps
```

### Service Configuration Options

#### Build Configuration
```yaml
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile.prod
      args:
        - NODE_VERSION=16
        - APP_ENV=production
      target: production  # For multi-stage builds
```

#### Environment Variables
```yaml
services:
  web:
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
    
    # Or use environment file
    env_file:
      - .env
      - .env.local
```

#### Volumes
```yaml
services:
  web:
    volumes:
      # Bind mount
      - ./src:/app/src
      
      # Named volume
      - app_data:/app/data
      
      # Anonymous volume
      - /app/node_modules
      
      # Read-only mount
      - ./config:/app/config:ro

volumes:
  app_data:
```

#### Networks
```yaml
services:
  web:
    networks:
      - frontend
      - backend
  
  database:
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
```

#### Port Mapping
```yaml
services:
  web:
    ports:
      # Host:Container
      - "3000:3000"
      - "8080:80"
      
      # Multiple ports
      - "3000-3005:3000-3005"
      
      # Bind to specific interface
      - "127.0.0.1:3000:3000"
```

---

## Advanced Docker Compose

### Environment-Specific Configurations

#### Using Multiple Compose Files
```yaml
# docker-compose.yml (base)
version: '3.8'
services:
  web:
    build: .
    ports:
      - "3000:3000"

# docker-compose.override.yml (development)
version: '3.8'
services:
  web:
    environment:
      - NODE_ENV=development
    volumes:
      - .:/app

# docker-compose.prod.yml (production)
version: '3.8'
services:
  web:
    environment:
      - NODE_ENV=production
    restart: unless-stopped
```

```bash
# Use production config
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

#### Environment Variables in Compose
```yaml
services:
  web:
    image: nginx:${NGINX_VERSION:-latest}
    ports:
      - "${WEB_PORT:-80}:80"
    environment:
      - API_URL=${API_URL}
```

```bash
# .env file
NGINX_VERSION=1.21
WEB_PORT=8080
API_URL=https://api.example.com
```

### Service Dependencies
```yaml
services:
  web:
    depends_on:
      database:
        condition: service_healthy
      redis:
        condition: service_started
    
  database:
    image: postgres:13
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Advanced Networking
```yaml
networks:
  frontend:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
  
  backend:
    driver: bridge
    internal: true  # No external access

services:
  web:
    networks:
      frontend:
        ipv4_address: 172.20.0.10
  
  database:
    networks:
      - backend
```

### Resource Limits
```yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
    
    # Alternative syntax
    mem_limit: 512m
    cpus: 0.5
```

### Secrets Management
```yaml
version: '3.8'

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    external: true

services:
  web:
    secrets:
      - db_password
      - api_key
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password
```

---

## Real-World Examples

### Example 1: MEAN Stack Application
```yaml
version: '3.8'

services:
  # Angular Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "4200:4200"
    depends_on:
      - backend
    networks:
      - app-network

  # Node.js Backend
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - MONGODB_URI=mongodb://database:27017/myapp
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      - database
    networks:
      - app-network
    volumes:
      - ./backend:/app
      - /app/node_modules

  # MongoDB Database
  database:
    image: mongo:5
    restart: unless-stopped
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_ROOT_USERNAME=${MONGO_USERNAME}
      - MONGO_INITDB_ROOT_PASSWORD=${MONGO_PASSWORD}
    volumes:
      - mongodb_data:/data/db
    networks:
      - app-network

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    networks:
      - app-network

volumes:
  mongodb_data:

networks:
  app-network:
    driver: bridge
```

### Example 2: Microservices with Load Balancer
```yaml
version: '3.8'

services:
  # Load Balancer
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - user-service
      - order-service
      - product-service

  # User Service
  user-service:
    build: ./services/user-service
    environment:
      - DATABASE_URL=postgresql://postgres:password@user-db:5432/users
    depends_on:
      - user-db
    deploy:
      replicas: 2

  # Order Service
  order-service:
    build: ./services/order-service
    environment:
      - DATABASE_URL=postgresql://postgres:password@order-db:5432/orders
      - REDIS_URL=redis://redis:6379
    depends_on:
      - order-db
      - redis

  # Product Service
  product-service:
    build: ./services/product-service
    environment:
      - DATABASE_URL=postgresql://postgres:password@product-db:5432/products

  # Databases
  user-db:
    image: postgres:13
    environment:
      POSTGRES_DB: users
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - user_data:/var/lib/postgresql/data

  order-db:
    image: postgres:13
    environment:
      POSTGRES_DB: orders
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - order_data:/var/lib/postgresql/data

  product-db:
    image: postgres:13
    environment:
      POSTGRES_DB: products
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - product_data:/var/lib/postgresql/data

  # Redis Cache
  redis:
    image: redis:6-alpine
    volumes:
      - redis_data:/data

volumes:
  user_data:
  order_data:
  product_data:
  redis_data:
```

### Example 3: Development Environment
```yaml
version: '3.8'

services:
  # Web Application
  app:
    build:
      context: .
      target: development
    ports:
      - "3000:3000"
      - "9229:9229"  # Debug port
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://dev:dev@postgres:5432/devdb
      - REDIS_URL=redis://redis:6379
    volumes:
      - .:/app
      - /app/node_modules
    command: npm run dev
    depends_on:
      - postgres
      - redis

  # PostgreSQL Database
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: devdb
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./sql/init.sql:/docker-entrypoint-initdb.d/init.sql

  # Redis Cache
  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  # PgAdmin for database management
  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      - postgres

  # Mailhog for email testing
  mailhog:
    image: mailhog/mailhog
    ports:
      - "1025:1025"  # SMTP
      - "8025:8025"  # Web UI

volumes:
  postgres_data:
  redis_data:
```

---

## Best Practices

### Security Best Practices

#### 1. Use Non-Root Users
```dockerfile
# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set ownership
COPY --chown=appuser:appuser . /app

# Switch to non-root user
USER appuser
```

#### 2. Use Official Base Images
```dockerfile
# ✅ Good - Official image
FROM node:16-alpine

# ❌ Avoid - Unofficial images
FROM some-random-user/node:latest
```

#### 3. Pin Image Versions
```dockerfile
# ✅ Good - Specific version
FROM node:16.20.0-alpine3.17

# ❌ Bad - Latest tag
FROM node:latest
```

#### 4. Minimal Base Images
```dockerfile
# Use minimal base images
FROM node:16-alpine
FROM python:3.9-slim
FROM golang:1.19-alpine
```

#### 5. Scan for Vulnerabilities
```bash
# Scan images for vulnerabilities
docker scan my-app:latest

# Use tools like Trivy
trivy image my-app:latest
```

### Performance Best Practices

#### 1. Optimize Layer Caching
```dockerfile
# Install dependencies first (changes less frequently)
COPY package*.json ./
RUN npm ci --only=production

# Copy source code last (changes frequently)
COPY . .
```

#### 2. Multi-Stage Builds
```dockerfile
FROM node:16 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:16-alpine AS production
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

#### 3. Minimize Layers
```dockerfile
# ❌ Bad - Multiple layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get clean

# ✅ Good - Single layer
RUN apt-get update && \
    apt-get install -y curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### Docker Compose Best Practices

#### 1. Use Environment Files
```bash
# .env
POSTGRES_VERSION=13
NODE_VERSION=16
APP_PORT=3000
```

```yaml
services:
  app:
    image: node:${NODE_VERSION}-alpine
    ports:
      - "${APP_PORT}:3000"
```

#### 2. Health Checks
```yaml
services:
  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

#### 3. Resource Limits
```yaml
services:
  web:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
```

#### 4. Restart Policies
```yaml
services:
  web:
    restart: unless-stopped  # or always, on-failure, no
```

### Logging Best Practices

#### 1. Structured Logging
```dockerfile
# Use JSON logging format
ENV LOG_FORMAT=json
ENV LOG_LEVEL=info
```

#### 2. Log to stdout/stderr
```javascript
// Don't write to files in containers
console.log(JSON.stringify({
  level: 'info',
  message: 'Application started',
  timestamp: new Date().toISOString()
}));
```

#### 3. Configure Log Drivers
```yaml
services:
  web:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Container Exits Immediately
```bash
# Check container logs
docker logs container_name

# Run container interactively
docker run -it image_name /bin/bash

# Override entrypoint
docker run -it --entrypoint /bin/bash image_name
```

#### 2. Port Already in Use
```bash
# Find process using port
netstat -tulpn | grep :3000

# Kill process
kill -9 PID

# Use different port
docker run -p 3001:3000 my-app
```

#### 3. Permission Denied
```dockerfile
# Fix file permissions
RUN chmod +x /app/start.sh

# Use correct user
USER 1000:1000
```

#### 4. Out of Disk Space
```bash
# Clean up unused resources
docker system prune -a

# Remove unused volumes
docker volume prune

# Remove unused images
docker image prune
```

#### 5. Build Cache Issues
```bash
# Force rebuild without cache
docker build --no-cache -t my-app .

# Remove build cache
docker builder prune
```

### Debugging Techniques

#### 1. Interactive Debugging
```bash
# Run container with shell
docker run -it --entrypoint /bin/bash my-app

# Execute shell in running container
docker exec -it container_name /bin/bash

# Debug with specific user
docker exec -it -u root container_name /bin/bash
```

#### 2. Inspect Container Configuration
```bash
# Inspect container details
docker inspect container_name

# View container processes
docker top container_name

# View resource usage
docker stats container_name
```

#### 3. Network Debugging
```bash
# List networks
docker network ls

# Inspect network
docker network inspect network_name

# Test connectivity
docker exec container_name ping other_container
```

#### 4. Volume Debugging
```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect volume_name

# Check volume contents
docker run --rm -v volume_name:/data alpine ls -la /data
```

### Performance Monitoring

#### 1. Container Resource Usage
```bash
# Real-time stats
docker stats

# Historical data with monitoring tools
# Prometheus + Grafana
# ELK Stack
# DataDog
```

#### 2. Image Size Analysis
```bash
# Analyze image layers
docker history my-app:latest

# Use dive tool for detailed analysis
dive my-app:latest
```

### Production Considerations

#### 1. Container Orchestration
- Use Kubernetes for production
- Consider Docker Swarm for simpler setups
- Implement auto-scaling
- Set up health checks

#### 2. Monitoring and Logging
- Centralized logging (ELK, Fluentd)
- Application monitoring (Prometheus, Grafana)
- Error tracking (Sentry)
- Performance monitoring (APM tools)

#### 3. Security
- Regular security scans
- Use distroless images when possible
- Implement network policies
- Use secrets management
- Regular updates

#### 4. Backup and Recovery
- Database backups
- Configuration backups
- Disaster recovery plans
- Test restore procedures

---

## Quick Reference

### Docker Commands Cheat Sheet
```bash
# Images
docker pull image:tag
docker build -t name:tag .
docker images
docker rmi image:tag

# Containers
docker run -d --name container image
docker ps / docker ps -a
docker stop/start/restart container
docker rm container
docker exec -it container bash
docker logs container

# System
docker info
docker system prune
docker stats
```

### Docker Compose Commands Cheat Sheet
```bash
# Basic operations
docker-compose up -d
docker-compose down
docker-compose restart
docker-compose logs -f

# Building
docker-compose build
docker-compose up --build

# Scaling
docker-compose up --scale service=3

# Specific services
docker-compose up service1 service2
docker-compose exec service bash
```

### Dockerfile Instructions Reference
```dockerfile
FROM image:tag
WORKDIR /path
COPY src dest
ADD src dest
RUN command
ENV key=value
EXPOSE port
VOLUME ["/path"]
USER username
CMD ["executable", "param"]
ENTRYPOINT ["executable"]
HEALTHCHECK CMD command
ARG name=default
LABEL key=value
```

---

## Conclusion

Docker and Docker Compose are powerful tools that revolutionize how we develop, deploy, and manage applications. This guide covered:

- **Docker fundamentals** - Understanding containers, images, and basic operations
- **Dockerfile mastery** - From basic instructions to advanced multi-stage builds
- **Docker Compose** - Orchestrating multi-container applications
- **Best practices** - Security, performance, and production considerations
- **Real-world examples** - Practical implementations you can use
- **Troubleshooting** - Common issues and debugging techniques

### Next Steps
1. Practice with the examples provided
2. Build your own Dockerfiles for existing projects
3. Experiment with Docker Compose for multi-service applications
4. Learn about container orchestration (Kubernetes)
5. Explore advanced topics like Docker Swarm, security scanning, and monitoring

Remember: The best way to learn Docker is by doing. Start with simple examples and gradually work your way up to more complex scenarios.

---

*Happy Dockerizing! 🐳*