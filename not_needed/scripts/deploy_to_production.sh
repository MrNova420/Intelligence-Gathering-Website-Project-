#!/bin/bash
# 🚀 Production Deployment Script - Intelligence Gathering Platform
# Automates deployment to various cloud providers

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo -e "${PURPLE}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  🚀 INTELLIGENCE GATHERING PLATFORM - PRODUCTION DEPLOY      ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

info() { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
error() { echo -e "${RED}✗${NC} $1"; }
step() { echo -e "${BLUE}→${NC} $1"; }

# Check if we're in the right directory
if [[ ! -f "README.md" ]] || [[ ! -d "backend" ]] || [[ ! -d "frontend" ]]; then
    error "Please run this script from the project root directory"
    exit 1
fi

show_menu() {
    echo ""
    echo -e "${BLUE}📋 Choose your deployment option:${NC}"
    echo ""
    echo "1) 🚀 Quick Deploy (Vercel + Railway)     - Fast, automatic, $0-20/month"
    echo "2) 🏗️  DigitalOcean Droplet              - Full control, $12-50/month"
    echo "3) ☁️  AWS Complete Setup                 - Enterprise scale, $50+/month"
    echo "4) 🐳 Docker Production Setup            - Container-based, any provider"
    echo "5) 🛠️  VPS Manual Setup                   - Custom server, any provider"
    echo "6) 📚 Show Detailed Guide                - Open deployment documentation"
    echo "7) ❌ Exit"
    echo ""
    read -p "Select option (1-7): " choice
}

# Quick Deploy (Vercel + Railway)
quick_deploy() {
    step "Setting up Quick Deploy (Vercel + Railway)..."
    
    # Check if railway CLI is installed
    if ! command -v railway &> /dev/null; then
        step "Installing Railway CLI..."
        if command -v npm &> /dev/null; then
            npm install -g @railway/cli
        else
            error "npm not found. Please install Node.js first."
            return 1
        fi
    fi
    
    # Check if vercel CLI is installed
    if ! command -v vercel &> /dev/null; then
        step "Installing Vercel CLI..."
        if command -v npm &> /dev/null; then
            npm install -g vercel
        else
            error "npm not found. Please install Node.js first."
            return 1
        fi
    fi
    
    echo ""
    info "🚀 Quick Deploy Setup Instructions:"
    echo ""
    echo "1. Backend (Railway):"
    echo "   railway login"
    echo "   railway init"
    echo "   railway up"
    echo ""
    echo "2. Frontend (Vercel):"
    echo "   vercel login"
    echo "   vercel"
    echo ""
    echo "3. Set environment variables in Railway dashboard:"
    echo "   DATABASE_URL=postgresql://[Railway provides this]"
    echo "   SECRET_KEY=$(openssl rand -hex 32)"
    echo "   ENVIRONMENT=production"
    echo ""
    echo "4. Set environment variables in Vercel dashboard:"
    echo "   REACT_APP_API_URL=https://[your-railway-app].railway.app"
    echo "   REACT_APP_ENVIRONMENT=production"
    echo ""
    
    read -p "Would you like to start the deployment process? (y/n): " confirm
    if [[ $confirm == "y" || $confirm == "Y" ]]; then
        step "Starting Railway backend deployment..."
        railway login || warn "Please complete Railway login manually"
        railway init || warn "Please complete Railway init manually"
        
        step "Starting Vercel frontend deployment..."  
        vercel login || warn "Please complete Vercel login manually"
        vercel || warn "Please complete Vercel deployment manually"
        
        info "Quick deploy initiated! Check your Railway and Vercel dashboards."
    fi
}

# DigitalOcean Setup
digitalocean_setup() {
    step "Preparing DigitalOcean deployment setup..."
    
    # Generate deployment script
    cat > deploy_digitalocean.sh << 'EOF'
#!/bin/bash
# DigitalOcean Droplet Setup Script

# Update system
apt update && apt upgrade -y

# Install dependencies
apt install nginx postgresql postgresql-contrib redis-server \
    python3 python3-pip nodejs npm git certbot python3-certbot-nginx -y

# Create application user
adduser --system --group intelligence
mkdir -p /var/www/intelligence
chown intelligence:intelligence /var/www/intelligence

# Clone repository (replace with your repo URL)
sudo -u intelligence git clone https://github.com/YourUsername/Intelligence-Gathering-Website-Project-.git /var/www/intelligence

# Install Python dependencies
cd /var/www/intelligence
sudo -u intelligence pip3 install -r backend/requirements.txt

# Install Node.js dependencies and build
cd frontend
sudo -u intelligence npm install
sudo -u intelligence npm run build
cd ..

# Setup environment
sudo -u intelligence cp .env.example .env
echo "Please edit /var/www/intelligence/.env with your production settings"

# Create systemd service
cat > /etc/systemd/system/intelligence-backend.service << 'EOL'
[Unit]
Description=Intelligence Gathering Platform Backend
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=intelligence
WorkingDirectory=/var/www/intelligence/backend
Environment=PATH=/usr/bin
ExecStart=/usr/bin/python3 run_standalone.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOL

# Enable service
systemctl daemon-reload
systemctl enable intelligence-backend

echo "Setup complete! Please:"
echo "1. Configure PostgreSQL database"
echo "2. Edit /var/www/intelligence/.env"
echo "3. Setup Nginx configuration"
echo "4. Start services: systemctl start intelligence-backend"
EOF

    chmod +x deploy_digitalocean.sh
    
    info "DigitalOcean deployment script created: deploy_digitalocean.sh"
    echo ""
    echo "Instructions:"
    echo "1. Create a DigitalOcean droplet (Ubuntu 22.04, $12/month minimum)"
    echo "2. Upload this script to your droplet: scp deploy_digitalocean.sh root@your-ip:~/"
    echo "3. SSH to your droplet: ssh root@your-ip"
    echo "4. Run the script: ./deploy_digitalocean.sh"
    echo "5. Follow the post-setup instructions"
    echo ""
    echo "For detailed instructions, see: PRODUCTION_DEPLOYMENT_GUIDE.md"
}

# AWS Setup
aws_setup() {
    step "Preparing AWS deployment configuration..."
    
    # Generate CloudFormation template
    cat > aws-infrastructure.yaml << 'EOF'
AWSTemplateFormatVersion: '2010-09-09'
Description: Intelligence Gathering Platform Infrastructure

Parameters:
  KeyName:
    Type: AWS::EC2::KeyPair::KeyName
    Description: EC2 Key Pair for SSH access

Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      
  PublicSubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: !Select [0, !GetAZs '']
      MapPublicIpOnLaunch: true
      
  InternetGateway:
    Type: AWS::EC2::InternetGateway
    
  AttachGateway:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref VPC
      InternetGatewayId: !Ref InternetGateway
      
  PublicRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC
      
  PublicRoute:
    Type: AWS::EC2::Route
    DependsOn: AttachGateway
    Properties:
      RouteTableId: !Ref PublicRouteTable
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref InternetGateway
      
  SubnetRouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PublicSubnet
      RouteTableId: !Ref PublicRouteTable
      
  SecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Intelligence Platform Security Group
      VpcId: !Ref VPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
          
  EC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-0c02fb55956c7d316  # Ubuntu 22.04 LTS
      InstanceType: t3.small
      KeyName: !Ref KeyName
      SecurityGroupIds:
        - !Ref SecurityGroup
      SubnetId: !Ref PublicSubnet
      UserData:
        Fn::Base64: !Sub |
          #!/bin/bash
          apt update && apt upgrade -y
          apt install git python3 python3-pip nodejs npm nginx -y
          # Add your deployment commands here
          
Outputs:
  InstancePublicIP:
    Description: Public IP of the EC2 instance
    Value: !GetAtt EC2Instance.PublicIp
EOF

    info "AWS CloudFormation template created: aws-infrastructure.yaml"
    echo ""
    echo "Instructions:"
    echo "1. Install AWS CLI: pip install awscli"
    echo "2. Configure AWS: aws configure"
    echo "3. Deploy stack: aws cloudformation create-stack --stack-name intelligence-platform --template-body file://aws-infrastructure.yaml --parameters ParameterKey=KeyName,ParameterValue=your-key-pair"
    echo "4. Wait for completion: aws cloudformation wait stack-create-complete --stack-name intelligence-platform"
    echo "5. Get instance IP: aws cloudformation describe-stacks --stack-name intelligence-platform"
    echo ""
    echo "For detailed instructions, see: PRODUCTION_DEPLOYMENT_GUIDE.md"
}

# Docker Production Setup
docker_production() {
    step "Setting up Docker production configuration..."
    
    # Generate production docker-compose
    cat > docker-compose.prod.yml << 'EOF'
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: intelligence_platform
      POSTGRES_USER: intelligence
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    
  redis:
    image: redis:7-alpine
    restart: unless-stopped
    
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    environment:
      DATABASE_URL: postgresql://intelligence:${DB_PASSWORD}@db:5432/intelligence_platform
      REDIS_URL: redis://redis:6379/0
      SECRET_KEY: ${SECRET_KEY}
      ENVIRONMENT: production
    depends_on:
      - db
      - redis
    restart: unless-stopped
    
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
      args:
        REACT_APP_API_URL: ${BACKEND_URL}
    restart: unless-stopped
    
  nginx:
    build: ./nginx
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - backend
      - frontend
    volumes:
      - ./ssl:/etc/nginx/ssl
    restart: unless-stopped

volumes:
  postgres_data:
EOF

    # Generate Nginx configuration
    mkdir -p nginx
    cat > nginx/Dockerfile << 'EOF'
FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf
EOF

    cat > nginx/nginx.conf << 'EOF'
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    
    access_log /var/log/nginx/access.log main;
    
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    
    include /etc/nginx/conf.d/*.conf;
}
EOF

    cat > nginx/default.conf << 'EOF'
server {
    listen 80;
    server_name _;
    
    # Frontend
    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Backend API
    location /api/ {
        proxy_pass http://backend:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

    # Generate environment file template
    cat > .env.production << 'EOF'
# Production Environment Variables
DB_PASSWORD=your-secure-database-password
SECRET_KEY=your-64-character-secret-key
BACKEND_URL=https://yourdomain.com

# Optional: External services
CLEARBIT_API_KEY=your-api-key
HUNTER_API_KEY=your-api-key
STRIPE_SECRET_KEY=your-stripe-key
EOF

    info "Docker production setup created!"
    echo ""
    echo "Files created:"
    echo "- docker-compose.prod.yml"
    echo "- nginx/ directory with configuration"
    echo "- .env.production template"
    echo ""
    echo "Usage:"
    echo "1. Edit .env.production with your values"
    echo "2. Deploy: docker-compose -f docker-compose.prod.yml up -d"
    echo "3. Setup SSL certificates in ssl/ directory"
    echo "4. Update nginx config for HTTPS"
    echo ""
}

# VPS Manual Setup
vps_manual() {
    step "Generating VPS manual setup guide..."
    
    cat > vps_setup_guide.txt << 'EOF'
VPS Manual Setup Guide - Intelligence Gathering Platform
=======================================================

Prerequisites:
- VPS with Ubuntu 22.04+ (2GB RAM minimum)
- Root SSH access
- Domain name pointing to VPS IP

Step 1: Connect to VPS
ssh root@your-vps-ip

Step 2: Update system
apt update && apt upgrade -y

Step 3: Install dependencies
apt install nginx postgresql postgresql-contrib redis-server \
    python3 python3-pip nodejs npm git certbot python3-certbot-nginx \
    htop ufw fail2ban -y

Step 4: Setup firewall
ufw allow ssh
ufw allow 'Nginx Full'
ufw enable

Step 5: Create application user
adduser --system --group --shell /bin/bash intelligence
mkdir -p /var/www/intelligence
chown intelligence:intelligence /var/www/intelligence

Step 6: Clone repository
sudo -u intelligence git clone YOUR_REPO_URL /var/www/intelligence

Step 7: Install application dependencies
cd /var/www/intelligence
sudo -u intelligence pip3 install -r backend/requirements.txt
cd frontend && sudo -u intelligence npm install && sudo -u intelligence npm run build

Step 8: Setup PostgreSQL
sudo -u postgres createuser intelligence
sudo -u postgres createdb intelligence_platform -O intelligence
sudo -u postgres psql -c "ALTER USER intelligence PASSWORD 'your-secure-password';"

Step 9: Configure environment
sudo -u intelligence cp .env.example .env
sudo -u intelligence nano .env
# Set your production values

Step 10: Setup systemd service
# See PRODUCTION_DEPLOYMENT_GUIDE.md for complete service configuration

Step 11: Configure Nginx
# See PRODUCTION_DEPLOYMENT_GUIDE.md for complete Nginx configuration

Step 12: Setup SSL
certbot --nginx -d yourdomain.com

Step 13: Start services
systemctl start intelligence-backend
systemctl enable intelligence-backend
systemctl restart nginx

Step 14: Test deployment
curl https://yourdomain.com
curl https://yourdomain.com/api/health

For detailed instructions, see PRODUCTION_DEPLOYMENT_GUIDE.md
EOF

    info "VPS setup guide created: vps_setup_guide.txt"
    echo ""
    echo "This guide provides step-by-step instructions for manual VPS setup."
    echo "For complete details, see: PRODUCTION_DEPLOYMENT_GUIDE.md"
}

# Show detailed guide
show_guide() {
    if command -v xdg-open &> /dev/null; then
        xdg-open PRODUCTION_DEPLOYMENT_GUIDE.md
    elif command -v open &> /dev/null; then
        open PRODUCTION_DEPLOYMENT_GUIDE.md
    else
        step "Opening deployment guide..."
        less PRODUCTION_DEPLOYMENT_GUIDE.md
    fi
}

# Main execution
main() {
    while true; do
        show_menu
        
        case $choice in
            1)
                quick_deploy
                break
                ;;
            2)
                digitalocean_setup
                break
                ;;
            3)
                aws_setup
                break
                ;;
            4)
                docker_production
                break
                ;;
            5)
                vps_manual
                break
                ;;
            6)
                show_guide
                ;;
            7)
                info "Goodbye! Good luck with your deployment! 🚀"
                exit 0
                ;;
            *)
                warn "Invalid option. Please choose 1-7."
                ;;
        esac
        
        echo ""
        read -p "Press Enter to return to menu..."
    done
}

# Run main function
main