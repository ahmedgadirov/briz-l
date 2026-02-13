# Admin Panel Deployment Guide

## Admin Panel for Briz-L Clinic

The admin panel is accessible at `/admin` route and provides comprehensive management features.

### Features

1. **Dashboard** (`/admin`)
   - Lead statistics overview
   - Today's leads count
   - Hot leads requiring attention
   - Conversion rates

2. **Leads Management** (`/admin/leads`)
   - View all leads with pagination
   - Filter by status (new, cold, warm, hot, converted)
   - Search functionality
   - Update lead status
   - View conversation history

3. **Conversations** (`/admin/conversations`)
   - Browse all conversations
   - View detailed chat history
   - See detected symptoms, surgeries, booking intent
   - Quick WhatsApp contact link

4. **Analytics** (`/admin/analytics`)
   - Conversion funnel visualization
   - Daily leads chart
   - Top surgery inquiries
   - Daily breakdown table
   - Date range filtering (7, 14, 30 days)

5. **AI Configuration** (`/admin/ai-config`)
   - Edit system prompt for Vera AI
   - Manage doctors database
   - Manage surgeries/procedures
   - Adjust lead scoring weights

6. **Settings** (`/admin/settings`)
   - Admin password management
   - Domain configuration info
   - Database connection status

### Domain Setup for admin-brizl.baysart.com

#### Option 1: Subdomain with Reverse Proxy (Recommended)

1. **DNS Configuration:**
   ```
   Type: CNAME
   Name: admin-brizl
   Value: baysart.com (or your server IP)
   TTL: 3600
   ```

2. **Nginx Configuration:**
   ```nginx
   server {
       listen 443 ssl;
       server_name admin-brizl.baysart.com;
       
       ssl_certificate /path/to/ssl/cert.pem;
       ssl_certificate_key /path/to/ssl/key.pem;
       
       location / {
           proxy_pass http://localhost:3000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

#### Option 2: Path-based Routing

If you want the admin panel on the main domain:

1. **Nginx Configuration:**
   ```nginx
   location /admin {
       proxy_pass http://localhost:3000;
       proxy_http_version 1.1;
       proxy_set_header Upgrade $http_upgrade;
       proxy_set_header Connection 'upgrade';
       proxy_set_header Host $host;
   }
   ```

### Environment Variables

Add these to your `.env` or deployment environment:

```env
# Database
DB_HOST=your-postgres-host
DB_PORT=5432
DB_NAME=briz-l
DB_USER=postgres
DB_PASSWORD=your-secure-password

# Admin Authentication
ADMIN_PASSWORD=brizl2024admin

# Optional: OpenAI for AI features
OPENAI_API_KEY=your-openai-api-key
```

### Database Tables Required

The admin panel uses these PostgreSQL tables:

1. **marketing_leads** - Stores all lead information
2. **marketing_analytics** - Daily analytics data
3. **ai_config** - AI configuration storage

These tables are created automatically by the marketing system.

### Security Notes

1. **Change the default password** immediately after deployment
2. The admin panel uses cookie-based authentication
3. All API routes are protected with authentication middleware
4. Consider adding IP whitelisting for additional security

### Building and Running

```bash
# Install dependencies
cd brizl-clinic
npm install

# Build for production
npm run build

# Start production server
npm run start
```

### Docker Deployment

The admin panel is included in the main brizl-clinic Docker image:

```bash
docker build -t brizl-clinic .
docker run -p 3000:3000 \
  -e DB_HOST=postgres \
  -e DB_PASSWORD=your-password \
  brizl-clinic
```

### Access

- **Local:** http://localhost:3000/admin
- **Production:** https://admin-brizl.baysart.com (after DNS setup)

### Default Credentials

- **Password:** `brizl2024admin`

**⚠️ Important:** Change this password in production!