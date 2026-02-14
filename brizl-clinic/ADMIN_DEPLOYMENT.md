# Admin Panel Deployment Guide

## Overview

The admin panel is now integrated into the main `docker-compose.yml` for the Rasa project. This ensures the admin panel can connect to the PostgreSQL database.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     dokploy-network                          │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  postgres   │  │    rasa     │  │    brizl-admin      │  │
│  │   :5432     │  │   :3001     │  │      :3002          │  │
│  │             │  │             │  │                     │  │
│  │  Database   │  │  Chatbot    │  │  Admin Panel        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│        ▲                                    │                │
│        │                                    │                │
│        └────────────────────────────────────┘                │
│                   Shared Database                            │
└─────────────────────────────────────────────────────────────┘
```

## Quick Deploy

```bash
# On your server
cd /path/to/rasa-brizl

# Pull latest changes
git pull

# Rebuild and restart all services
docker-compose down
docker-compose up -d --build

# Check logs
docker-compose logs -f brizl-admin
```

## Services

| Service | Port | URL |
|---------|------|-----|
| PostgreSQL | 5432 | Internal only |
| Rasa Chatbot | 3001 | https://brizl.baysart.com |
| Admin Panel | 3002 | https://admin-brizl.baysart.com |
| Action Server | 5055 | Internal only |
| Social Media Webhook | 5000 | https://selmedia.net/webhooks |

## Environment Variables

The admin panel uses these environment variables (set in docker-compose.yml):

```env
DB_HOST=postgres
DB_PORT=5432
DB_NAME=briz-l
DB_USER=postgres
DB_PASSWORD=herahera
NEXT_PUBLIC_RASA_URL=https://brizl.baysart.com
```

## Database Migration

After deployment, run migrations to create tables:

1. Go to **Settings** page: `https://admin-brizl.baysart.com/admin/settings`
2. Click **"Run Database Migrations"**
3. Tables will be created automatically:
   - `marketing_leads`
   - `follow_ups`
   - `conversion_events`
   - `marketing_analytics`
   - `ai_config`

## DNS Configuration

Make sure these DNS records are configured:

```
Type: CNAME
Name: admin-brizl
Value: baysart.com (or your server)
```

## Troubleshooting

### Check PostgreSQL Connection
```bash
docker exec -it brizl-postgres psql -U postgres -d briz-l
```

### Check Admin Panel Logs
```bash
docker-compose logs -f brizl-admin
```

### Restart Services
```bash
docker-compose restart brizl-admin
docker-compose restart postgres
```

### Check Network Connectivity
```bash
docker network inspect dokploy-network
```

## Access

- **Admin Panel URL:** https://admin-brizl.baysart.com
- **Default Password:** `brizl2024admin`