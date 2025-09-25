# 👨‍🏫 Step-by-Step Tutorials - Intelligence Gathering Platform

## **Complete Tutorials for Every Platform**

Detailed, step-by-step instructions with screenshots and troubleshooting for each platform.

---

## 📱 **Tutorial 1: Android (Termux) - Complete Setup**

### **Step 1: Install Termux**
1. Download Termux from **F-Droid** (recommended): https://f-droid.org/packages/com.termux/
2. Or download from GitHub releases: https://github.com/termux/termux-app/releases
3. Install the APK file
4. Open Termux

### **Step 2: Update System**
```bash
# Update package lists and upgrade system
pkg update && pkg upgrade

# When prompted, press 'Y' and Enter
```
**Expected output**: Package updates and upgrades

### **Step 3: Install Git**
```bash
pkg install git

# When prompted, press 'y' and Enter
```
**Expected output**: `git` successfully installed

### **Step 4: Clone Repository**
```bash
# Clone the project
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git

# Navigate to project directory
cd Intelligence-Gathering-Website-Project-

# List files to confirm
ls
```
**Expected output**: You should see files like `README.md`, `run.sh`, `backend/`, `frontend/`

### **Step 5: One-Command Setup**
```bash
# Run the super-easy setup script
./run.sh
```

**What this does automatically:**
- Installs Python, Node.js, and all dependencies
- Sets up SQLite database
- Configures the platform
- Starts both backend and frontend services

**Expected output:**
```
🚀 Starting Intelligence Gathering Platform...
🔧 First time setup detected...
✓ Platform detected: termux
✓ System dependencies installed
✓ Python dependencies installed
✓ Database setup completed
✓ Services started in tmux session
🎉 Platform is running!
```

### **Step 6: Access the Platform**
1. Open a web browser on your Android device
2. Go to: `http://localhost:3000`
3. You should see the Intelligence Gathering Platform interface

**Default login:**
- Email: `admin@platform.local`
- Password: `admin123`

### **Step 7: Verify Everything Works**
```bash
# In a new Termux session (swipe down and tap "New session")
cd Intelligence-Gathering-Website-Project-

# Check status
./status.sh
```

**Expected output**: Green checkmarks showing services are running

### **Termux Troubleshooting:**

**Problem: psycopg2-binary error**
```bash
./termux_quickstart.sh
```

**Problem: Permission denied**
```bash
chmod +x *.sh
./run.sh
```

**Problem: Services not starting**
```bash
./fix.sh
./run.sh
```

---

## 🐧 **Tutorial 2: Linux (Ubuntu) - Complete Setup**

### **Step 1: Open Terminal**
- Press `Ctrl + Alt + T` to open terminal
- Or search for "Terminal" in applications

### **Step 2: Update System**
```bash
sudo apt update && sudo apt upgrade -y
```
**Expected output**: System packages updated

### **Step 3: Install Dependencies**
```bash
# Install all required packages
sudo apt install git python3 python3-pip nodejs npm tmux sqlite3 -y
```
**Expected output**: All packages installed successfully

### **Step 4: Clone Repository**
```bash
# Navigate to home directory
cd ~

# Clone the project
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git

# Enter project directory
cd Intelligence-Gathering-Website-Project-
```

### **Step 5: Run Setup**
```bash
# One command does everything
./run.sh
```

**Expected output:**
```
🚀 Starting Intelligence Gathering Platform...
✓ Platform detected: debian
✓ Installing system dependencies...
✓ Python dependencies installed
✓ Node.js dependencies installed
✓ Database setup completed
🎉 Platform is running!
```

### **Step 6: Access Platform**
1. Open Firefox or any browser
2. Navigate to: `http://localhost:3000`
3. Login with default credentials

### **Step 7: Monitor Services**
```bash
# Check what's running
./status.sh

# View live logs
tmux attach -t intel

# Detach from tmux: Ctrl+B then D
```

### **Linux Management Commands:**
```bash
# Start services
./easy_start.sh start

# Stop services  
./easy_start.sh stop

# Restart everything
./easy_start.sh restart

# Fix any issues
./fix.sh
```

---

## 🍎 **Tutorial 3: macOS - Complete Setup**

### **Step 1: Install Prerequisites**

**Option A: Using Homebrew (Recommended)**
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python node git tmux sqlite
```

**Option B: Manual Installation**
1. Download Python from: https://www.python.org/downloads/
2. Download Node.js from: https://nodejs.org/
3. Install Xcode Command Line Tools: `xcode-select --install`

### **Step 2: Open Terminal**
- Press `Cmd + Space`, type "Terminal", press Enter
- Or go to Applications > Utilities > Terminal

### **Step 3: Clone Repository**
```bash
# Navigate to home directory
cd ~

# Clone project
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git

# Enter directory
cd Intelligence-Gathering-Website-Project-
```

### **Step 4: Run Setup**
```bash
./run.sh
```

**Expected output:**
```
🚀 Starting Intelligence Gathering Platform...
✓ Platform detected: macos
✓ System dependencies found
✓ Python dependencies installed
✓ Node.js dependencies installed
✓ Database initialized
🎉 Platform is running!
```

### **Step 5: Access Platform**
1. Open Safari or Chrome
2. Go to: `http://localhost:3000`
3. Log in with admin credentials

### **macOS-Specific Tips:**
```bash
# If permission issues:
sudo chmod +x *.sh

# If Python issues:
python3 -m pip install --upgrade pip
./fix.sh deps

# Monitor with Activity Monitor or terminal:
./status.sh
```

---

## 🪟 **Tutorial 4: Windows - Complete Setup**

### **Method A: Using Windows Batch Script**

### **Step 1: Install Prerequisites**
1. **Python**: Download from https://www.python.org/downloads/
   - ✅ Check "Add Python to PATH"
   - ✅ Check "Install pip"
2. **Node.js**: Download from https://nodejs.org/
   - Use the LTS version
   - Default settings are fine
3. **Git**: Download from https://git-scm.com/download/win
   - Default settings are fine

### **Step 2: Open Command Prompt**
- Press `Win + R`, type `cmd`, press Enter
- Or search for "Command Prompt" in Start menu

### **Step 3: Clone Repository**
```cmd
REM Navigate to your user directory
cd %USERPROFILE%

REM Clone the project
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git

REM Enter directory
cd Intelligence-Gathering-Website-Project-
```

### **Step 4: Run Windows Setup**
```cmd
REM Use the Windows batch script
run.bat
```

**Expected output:**
```
🚀 Intelligence Gathering Platform - Windows Setup
✅ Python and Node.js found!
📦 Installing Python dependencies...
🔧 Setting up environment...
🗄️ Setting up database...
✅ Services started!
```

### **Step 5: Access Platform**
1. Open Edge, Chrome, or Firefox
2. Navigate to: `http://localhost:3000`
3. Use admin login credentials

### **Method B: Using WSL (Windows Subsystem for Linux)**

### **Step 1: Enable WSL**
```powershell
# Run as Administrator
wsl --install
```
Restart computer when prompted.

### **Step 2: Open WSL**
- Search for "Ubuntu" in Start menu
- Or type `wsl` in Command Prompt

### **Step 3: Follow Linux Instructions**
```bash
# Update WSL Ubuntu
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install git python3 python3-pip nodejs npm -y

# Clone and setup
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-
./run.sh
```

---

## 🐳 **Tutorial 5: Docker (Any Platform)**

### **Step 1: Install Docker**
- **Windows/Mac**: Download Docker Desktop from https://docker.com
- **Linux**: Follow instructions at https://docs.docker.com/engine/install/

### **Step 2: Clone Repository**
```bash
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-
```

### **Step 3: Start with Docker**
```bash
# Option 1: Use our Docker script
./start_with_docker.sh

# Option 2: Use docker-compose directly
docker-compose up -d

# Option 3: Build and run manually
docker build -t intelligence-platform .
docker run -p 3000:3000 -p 8000:8000 intelligence-platform
```

### **Step 4: Access Platform**
- Website: http://localhost:3000
- API: http://localhost:8000

### **Docker Management:**
```bash
# View running containers
docker ps

# Stop containers
docker-compose down

# View logs
docker-compose logs -f

# Rebuild if needed
docker-compose up --build
```

---

## ☁️ **Tutorial 6: Cloud Platforms (AWS/GCP/Azure)**

### **Step 1: Create Virtual Machine**
1. Create Ubuntu 20.04+ instance
2. Allow HTTP traffic (ports 80, 3000, 8000)
3. SSH into the instance

### **Step 2: Setup Environment**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install git python3 python3-pip nodejs npm nginx -y

# Clone repository
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-
```

### **Step 3: Run Setup**
```bash
# Install and start
./install.sh
./easy_start.sh start
```

### **Step 4: Configure Nginx (Optional)**
```bash
# Create nginx config
sudo tee /etc/nginx/sites-available/intelligence-platform << EOF
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
    
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/intelligence-platform /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🆘 **Universal Troubleshooting Guide**

### **Step 1: Run Diagnostics**
```bash
# Check overall health
./health_check.sh

# Quick functionality test
./quick_test.sh

# Detailed status
./status.sh
```

### **Step 2: Auto-Fix Common Issues**
```bash
# Fix everything automatically
./fix.sh

# Or fix specific components:
./fix.sh deps      # Dependencies
./fix.sh database  # Database issues
./fix.sh nodejs    # Frontend issues
./fix.sh env       # Configuration
```

### **Step 3: Manual Troubleshooting**

**Services not starting:**
```bash
# Kill any stuck processes
./fix.sh processes

# Restart everything
./run.sh
```

**Port conflicts:**
```bash
# Stop all services
./easy_start.sh stop

# Wait 10 seconds, then restart
./easy_start.sh start
```

**Permission issues:**
```bash
# Fix file permissions
chmod +x *.sh
./fix.sh perms
```

**Database issues:**
```bash
# Reset database
./fix.sh database

# Or manually:
rm -f backend/intelligence_platform.db
python backend/app/db/setup_standalone.py
```

### **Step 4: Get Help**
```bash
# Show all available commands
./easy_start.sh help

# Show fix options
./fix.sh help

# Run comprehensive verification
python verify_fixes.py
```

---

## 🎯 **Success Verification**

After completing any tutorial, verify success:

### **✅ Checklist:**
- [ ] `./health_check.sh` shows 90%+ score
- [ ] Website loads at http://localhost:3000
- [ ] API responds at http://localhost:8000/docs
- [ ] Login works with admin credentials
- [ ] `./status.sh` shows all services running
- [ ] No error messages in terminal

### **🎉 Congratulations!**
You have successfully deployed the Intelligence Gathering Platform on your chosen platform!