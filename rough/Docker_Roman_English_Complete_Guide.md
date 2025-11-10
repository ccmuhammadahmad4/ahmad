# Docker aur Docker Compose: Complete Beginner se Advanced tak Guide

## Table of Contents
1. [Docker ka Introduction](#docker-ka-introduction)
2. [Docker ki Basics](#docker-ki-basics)
3. [Dockerfile ki Fundamentals](#dockerfile-ki-fundamentals)
4. [Advanced Dockerfile Techniques](#advanced-dockerfile-techniques)
5. [Docker Compose ki Basics](#docker-compose-ki-basics)
6. [Advanced Docker Compose](#advanced-docker-compose)
7. [Real-World Examples](#real-world-examples)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

---

## Docker ka Introduction

### Docker kya hai? 🐳
Docker ek aisa platform hai jo **containerization** technology use karta hai applications aur unki dependencies ko lightweight, portable containers mein package karne ke liye.

### Docker kyun use karein?
- **Consistency**: "Mere machine pe to chal raha hai" problem solve ho jata hai
- **Portability**: Kahin bhi run kar sakte hain (development, testing, production)
- **Efficiency**: Virtual machines ke comparison mein bahut light weight hai
- **Scalability**: Applications ko easily scale kar sakte hain
- **Isolation**: Applications ek dusre ko interfere nahi karti

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

## Docker ki Basics

### Key Concepts
- **Image**: Containers banane ke liye ek blueprint/template
- **Container**: Image ka running instance
- **Registry**: Images store karne ki jagah (Docker Hub)
- **Volume**: Persistent data storage
- **Network**: Containers ke beech communication

### Essential Docker Commands

#### Image Management
```bash
# Registry se image pull karna
docker pull nginx:latest

# Saari images list karna
docker images

# Image remove karna
docker rmi image_name:tag

# Dockerfile se image build karna
docker build -t my-app:v1.0 .

# Registry mein image push karna
docker push username/my-app:v1.0
```

#### Container Management
```bash
# Container run karna
docker run -d --name my-container -p 8080:80 nginx

# Running containers list karna
docker ps

# Saare containers list karna (stopped bhi)
docker ps -a

# Container stop karna
docker stop my-container

# Stopped container start karna
docker start my-container

# Container remove karna
docker rm my-container

# Running container mein command execute karna
docker exec -it my-container bash

# Container logs dekhna
docker logs my-container

# Real-time logs follow karna
docker logs -f my-container
```

#### System Management
```bash
# Docker system information dekhna
docker info

# Unused resources clean up karna
docker system prune

# Resource usage dekhna
docker stats
```

---

## Dockerfile ki Fundamentals

### Dockerfile kya hai?
Dockerfile ek text file hai jismein Docker image build karne ke instructions hote hain.

### Basic Dockerfile Structure
```dockerfile
# Base image
FROM ubuntu:20.04

# Metadata
LABEL maintainer="your-email@example.com"
LABEL version="1.0"
LABEL description="Meri awesome application"

# Environment variables
ENV NODE_VERSION=16.20.0
ENV APP_HOME=/usr/src/app

# Working directory set karna
WORKDIR $APP_HOME

# Files copy karna
COPY package*.json ./
COPY . .

# Dependencies install karna
RUN apt-get update && apt-get install -y \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# App dependencies install karna
RUN npm install --production

# Port expose karna
EXPOSE 3000

# Entry point define karna
CMD ["npm", "start"]
```

### Essential Dockerfile Instructions

#### FROM - Base Image
```dockerfile
# Official Node.js image use karna
FROM node:16-alpine

# Specific version use karna
FROM python:3.9-slim

# Multi-stage build
FROM node:16 AS builder
FROM nginx:alpine AS production
```

#### WORKDIR - Working Directory Set karna
```dockerfile
# Working directory set karna
WORKDIR /app

# Aage ke saare commands /app se run honge
COPY . .
RUN npm install
```

#### COPY vs ADD
```dockerfile
# COPY - Simple file copying (prefer karna)
COPY src/ /app/src/
COPY package.json /app/

# ADD - Extra features ke saath (auto-extraction, URL support)
ADD https://example.com/file.tar.gz /app/
ADD archive.tar.gz /app/  # Auto-extract ho jaata hai
```

#### RUN - Commands Execute karna
```dockerfile
# Single command
RUN npm install

# Multiple commands (inefficient tarika)
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

# Multiple commands (efficient tarika - single layer)
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

# Environment variables use karna
WORKDIR /app
EXPOSE $PORT
```

#### EXPOSE - Ports Document karna
```dockerfile
# Document karna ke app port 3000 pe listen karta hai
EXPOSE 3000

# Multiple ports
EXPOSE 3000 8080 9000
```

#### VOLUME - Persistent Storage
```dockerfile
# Volume mount point banana
VOLUME ["/data"]

# Multiple volumes
VOLUME ["/data", "/logs", "/config"]
```

#### User Management
```dockerfile
# Security ke liye user banana
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Non-root user pe switch karna
USER appuser

# Ya numeric UID use karna
USER 1001
```

#### CMD vs ENTRYPOINT
```dockerfile
# CMD - Default command (override ho sakta hai)
CMD ["npm", "start"]

# ENTRYPOINT - Hamesha execute hota hai (override nahi ho sakta)
ENTRYPOINT ["python", "app.py"]

# Combination - ENTRYPOINT + CMD
ENTRYPOINT ["python", "app.py"]
CMD ["--help"]  # Default argument
```

---

## Advanced Dockerfile Techniques

### Multi-Stage Builds
Image size kam karne ke liye perfect hai build aur runtime environments ko separate kar ke.

```dockerfile
# Build stage
FROM node:16 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Production stage
FROM node:16-alpine AS production
WORKDIR /app

# Sirf production files copy karna
COPY --from=builder /app/node_modules ./node_modules
COPY . .

EXPOSE 3000
CMD ["npm", "start"]
```

### Build Arguments
```dockerfile
# Build arguments define karna
ARG NODE_VERSION=16
ARG APP_ENV=production

# FROM instruction mein use karna
FROM node:${NODE_VERSION}-alpine

# Environment variables mein use karna
ENV NODE_ENV=${APP_ENV}

# Custom arguments ke saath build karna
# docker build --build-arg NODE_VERSION=18 --build-arg APP_ENV=development .
```

### Conditional Instructions
```dockerfile
ARG ENVIRONMENT=production

# Development dependencies sirf dev mein install karna
RUN if [ "$ENVIRONMENT" = "development" ]; then \
        npm install; \
    else \
        npm ci --only=production; \
    fi
```

### Health Checks
```dockerfile
# Health check add karna
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Custom health check script
COPY healthcheck.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/healthcheck.sh
HEALTHCHECK CMD /usr/local/bin/healthcheck.sh
```

### Docker Images Optimize karna

#### Layer Caching
```dockerfile
# ❌ Galat - Source code changes mein npm install layer invalidate ho jaata hai
COPY . .
RUN npm install

# ✅ Sahi - package.json rarely change hota hai, better caching
COPY package*.json ./
RUN npm install
COPY . .
```

#### Image Size Kam karna
```dockerfile
# Alpine images use karna
FROM node:16-alpine

# Multi-stage builds
FROM node:16 AS builder
# ... build steps ...
FROM node:16-alpine AS production
COPY --from=builder /app/dist ./dist

# Unnecessary files remove karna
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# .dockerignore file use karna
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

## Docker Compose ki Basics

### Docker Compose kya hai?
Docker Compose ek tool hai jo YAML file use kar ke multi-container Docker applications define aur run karne ke liye use hota hai.

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
# Services ko detached mode mein start karna
docker-compose up -d

# Specific service start karna
docker-compose up web

# Build aur start
docker-compose up --build

# Services stop karna
docker-compose down

# Stop aur volumes remove karna
docker-compose down -v

# Logs dekhna
docker-compose logs

# Specific service ke logs follow karna
docker-compose logs -f web

# Service mein command execute karna
docker-compose exec web bash

# Services scale karna
docker-compose up --scale web=3

# Running services dekhna
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
      target: production  # Multi-stage builds ke liye
```

#### Environment Variables
```yaml
services:
  web:
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
    
    # Ya environment file use karna
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
      
      # Specific interface pe bind karna
      - "127.0.0.1:3000:3000"
```

---

## Advanced Docker Compose

### Environment-Specific Configurations

#### Multiple Compose Files Use karna
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
# Production config use karna
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
    internal: true  # External access nahi

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

  # Database management ke liye PgAdmin
  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      - postgres

  # Email testing ke liye Mailhog
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

#### 1. Non-Root Users Use karna
```dockerfile
# Non-root user banana
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Ownership set karna
COPY --chown=appuser:appuser . /app

# Non-root user pe switch karna
USER appuser
```

#### 2. Official Base Images Use karna
```dockerfile
# ✅ Sahi - Official image
FROM node:16-alpine

# ❌ Avoid karna - Unofficial images
FROM some-random-user/node:latest
```

#### 3. Image Versions Pin karna
```dockerfile
# ✅ Sahi - Specific version
FROM node:16.20.0-alpine3.17

# ❌ Galat - Latest tag
FROM node:latest
```

#### 4. Minimal Base Images
```dockerfile
# Minimal base images use karna
FROM node:16-alpine
FROM python:3.9-slim
FROM golang:1.19-alpine
```

#### 5. Vulnerabilities ke liye Scan karna
```bash
# Images ko vulnerabilities ke liye scan karna
docker scan my-app:latest

# Tools jaise Trivy use karna
trivy image my-app:latest
```

### Performance Best Practices

#### 1. Layer Caching Optimize karna
```dockerfile
# Dependencies pehle install karna (kam change hoti hai)
COPY package*.json ./
RUN npm ci --only=production

# Source code last mein copy karna (frequently change hota hai)
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

#### 3. Layers Minimize karna
```dockerfile
# ❌ Galat - Multiple layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get clean

# ✅ Sahi - Single layer
RUN apt-get update && \
    apt-get install -y curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### Docker Compose Best Practices

#### 1. Environment Files Use karna
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
    restart: unless-stopped  # ya always, on-failure, no
```

### Logging Best Practices

#### 1. Structured Logging
```dockerfile
# JSON logging format use karna
ENV LOG_FORMAT=json
ENV LOG_LEVEL=info
```

#### 2. stdout/stderr mein Log karna
```javascript
// Containers mein files mein write na karna
console.log(JSON.stringify({
  level: 'info',
  message: 'Application start ho gaya',
  timestamp: new Date().toISOString()
}));
```

#### 3. Log Drivers Configure karna
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

### Common Issues aur Solutions

#### 1. Container Immediately Exit ho jaata hai
```bash
# Container logs check karna
docker logs container_name

# Container ko interactively run karna
docker run -it image_name /bin/bash

# Entrypoint override karna
docker run -it --entrypoint /bin/bash image_name
```

#### 2. Port Already in Use
```bash
# Port use karne wala process find karna
netstat -tulpn | grep :3000

# Process kill karna
kill -9 PID

# Different port use karna
docker run -p 3001:3000 my-app
```

#### 3. Permission Denied
```dockerfile
# File permissions fix karna
RUN chmod +x /app/start.sh

# Correct user use karna
USER 1000:1000
```

#### 4. Disk Space Khatam
```bash
# Unused resources clean up karna
docker system prune -a

# Unused volumes remove karna
docker volume prune

# Unused images remove karna
docker image prune
```

#### 5. Build Cache Issues
```bash
# Cache ke bina force rebuild karna
docker build --no-cache -t my-app .

# Build cache remove karna
docker builder prune
```

### Debugging Techniques

#### 1. Interactive Debugging
```bash
# Container ko shell ke saath run karna
docker run -it --entrypoint /bin/bash my-app

# Running container mein shell execute karna
docker exec -it container_name /bin/bash

# Specific user ke saath debug karna
docker exec -it -u root container_name /bin/bash
```

#### 2. Container Configuration Inspect karna
```bash
# Container details inspect karna
docker inspect container_name

# Container processes dekhna
docker top container_name

# Resource usage dekhna
docker stats container_name
```

#### 3. Network Debugging
```bash
# Networks list karna
docker network ls

# Network inspect karna
docker network inspect network_name

# Connectivity test karna
docker exec container_name ping other_container
```

#### 4. Volume Debugging
```bash
# Volumes list karna
docker volume ls

# Volume inspect karna
docker volume inspect volume_name

# Volume contents check karna
docker run --rm -v volume_name:/data alpine ls -la /data
```

### Performance Monitoring

#### 1. Container Resource Usage
```bash
# Real-time stats
docker stats

# Historical data monitoring tools ke saath
# Prometheus + Grafana
# ELK Stack
# DataDog
```

#### 2. Image Size Analysis
```bash
# Image layers analyze karna
docker history my-app:latest

# Detailed analysis ke liye dive tool use karna
dive my-app:latest
```

### Production Considerations

#### 1. Container Orchestration
- Production ke liye Kubernetes use karna
- Simple setups ke liye Docker Swarm consider karna
- Auto-scaling implement karna
- Health checks set up karna

#### 2. Monitoring aur Logging
- Centralized logging (ELK, Fluentd)
- Application monitoring (Prometheus, Grafana)
- Error tracking (Sentry)
- Performance monitoring (APM tools)

#### 3. Security
- Regular security scans
- Jab possible ho distroless images use karna
- Network policies implement karna
- Secrets management use karna
- Regular updates

#### 4. Backup aur Recovery
- Database backups
- Configuration backups
- Disaster recovery plans
- Restore procedures test karna

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

Docker aur Docker Compose powerful tools hain jo revolutionize karte hain ki hum kaise applications develop, deploy, aur manage karte hain. Is guide mein cover kiya:

- **Docker fundamentals** - Containers, images, aur basic operations samajhna
- **Dockerfile mastery** - Basic instructions se advanced multi-stage builds tak
- **Docker Compose** - Multi-container applications orchestrate karna
- **Best practices** - Security, performance, aur production considerations
- **Real-world examples** - Practical implementations jo aap use kar sakte hain
- **Troubleshooting** - Common issues aur debugging techniques

### Agle Steps
1. Provided examples ke saath practice karna
2. Existing projects ke liye apni Dockerfiles banana
3. Multi-service applications ke liye Docker Compose experiment karna
4. Container orchestration (Kubernetes) ke bare mein seekhna
5. Advanced topics explore karna jaise Docker Swarm, security scanning, aur monitoring

Yaad rakhiye: Docker seekhne ka best tarika practice kar ke hai. Simple examples se start kariye aur gradually complex scenarios ki taraf badhiye.

---

*Happy Dockerizing! 🐳*