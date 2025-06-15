#!/bin/bash

# AI Platform Deployment Script
set -e

echo "🚀 AI Platform Deployment Script"
echo "================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from template...${NC}"
    cp .env.example .env
    
    # Generate secure keys
    echo "🔑 Generating secure keys..."
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    JWT_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    MASTER_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    DB_PASSWORD=$(python3 -c "import secrets; print(secrets.token_urlsafe(16))")
    REDIS_PASSWORD=$(python3 -c "import secrets; print(secrets.token_urlsafe(16))")
    
    # Update .env with generated keys
    sed -i "s/your-secret-key-here-change-in-production/$SECRET_KEY/" .env
    sed -i "s/your-jwt-secret-key-here-change-in-production/$JWT_SECRET_KEY/" .env
    sed -i "s/your-master-encryption-key-here-change-in-production/$MASTER_KEY/" .env
    sed -i "s/change-this-strong-password/$DB_PASSWORD/" .env
    sed -i "s/change-this-redis-password/$REDIS_PASSWORD/" .env
    
    echo -e "${GREEN}✅ .env file created with secure keys${NC}"
    echo -e "${YELLOW}⚠️  Please review and update .env file with your specific settings${NC}"
fi

# Create required directories
echo "📁 Creating required directories..."
mkdir -p logs uploads static

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build and start services
echo "🏗️  Building and starting services..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check if services are running
echo "🔍 Checking service status..."
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}✅ Services are running${NC}"
else
    echo -e "${RED}❌ Some services failed to start${NC}"
    docker-compose logs --tail=20
    exit 1
fi

# Initialize database
echo "🗄️  Initializing database..."
if docker-compose exec -T app python database_setup.py init; then
    echo -e "${GREEN}✅ Database initialized${NC}"
else
    echo -e "${RED}❌ Database initialization failed${NC}"
    exit 1
fi

# Create admin user
echo "👤 Creating admin user..."
echo "Please enter admin credentials:"
read -p "Admin email: " ADMIN_EMAIL
read -s -p "Admin password: " ADMIN_PASSWORD
echo

if docker-compose exec -T app python -c "
from src.auth.authentication import create_user
try:
    user = create_user('$ADMIN_EMAIL', '$ADMIN_PASSWORD', is_admin=True)
    print('Admin user created successfully')
except Exception as e:
    print(f'Error: {e}')
"; then
    echo -e "${GREEN}✅ Admin user created${NC}"
else
    echo -e "${YELLOW}⚠️  Admin user creation failed (may already exist)${NC}"
fi

# Run health check
echo "🏥 Running health check..."
sleep 10
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Health check passed${NC}"
else
    echo -e "${YELLOW}⚠️  Health check failed - check logs${NC}"
fi

# Display deployment information
echo ""
echo "🎉 Deployment Complete!"
echo "======================"
echo -e "Main Application: ${GREEN}http://localhost${NC}"
echo -e "Admin Dashboard: ${GREEN}http://localhost/admin-enhanced${NC}"
echo -e "User Dashboard: ${GREEN}http://localhost/dashboard${NC}"
echo -e "Integration Setup: ${GREEN}http://localhost/integration-quickstart${NC}"
echo ""
echo -e "Admin Email: ${GREEN}$ADMIN_EMAIL${NC}"
echo ""
echo "📋 Next Steps:"
echo "1. Update your domain in nginx.conf for production"
echo "2. Configure SSL certificates for HTTPS"
echo "3. Set up email settings in .env for notifications"
echo "4. Review security settings in .env"
echo "5. Set up monitoring and backups"
echo ""
echo "📚 Documentation: README_DEPLOYMENT.md"
echo "🛠️  Management: Use docker-compose commands"
echo ""
echo -e "${GREEN}Happy hosting! 🚀${NC}"