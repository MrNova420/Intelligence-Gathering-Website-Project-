# 🚀 Complete Platform Guide - Intelligence Gathering Platform

## **Universal Setup for All Devices & Platforms**

This comprehensive guide provides step-by-step instructions for running the Intelligence Gathering Platform on any device or operating system.

---

## 📱 **Android (Termux)**

### **Method 1: Super Easy (Recommended)**
```bash
# Install Termux from F-Droid: https://f-droid.org/packages/com.termux/
# Open Termux and run:

pkg update && pkg upgrade
pkg install git
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-

# ONE COMMAND SETUP:
./run.sh

# Access points:
# Website: http://localhost:3000
# API: http://localhost:8000
```

### **Method 2: Step-by-Step**
```bash
# Step 1: Install system packages
pkg install python nodejs git tmux sqlite

# Step 2: Clone and setup
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-

# Step 3: Install dependencies (SQLite-only)
pip install -r backend/requirements-lite.txt

# Step 4: Setup database
python backend/app/db/setup_standalone.py

# Step 5: Install frontend dependencies
cd frontend && npm install && cd ..

# Step 6: Start services
./easy_start.sh start
```

### **Troubleshooting Android/Termux:**
```bash
# If psycopg2-binary errors:
./termux_quickstart.sh

# If any issues:
./fix.sh

# Check health:
./health_check.sh
```

---

## 🐧 **Linux (Ubuntu/Debian/CentOS/Arch)**

### **Method 1: Automatic Setup**
```bash
# Install git first:
sudo apt update && sudo apt install git  # Ubuntu/Debian
# OR
sudo yum install git                     # CentOS/RHEL
# OR  
sudo pacman -S git                       # Arch

# Clone and run:
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-

# ONE COMMAND SETUP:
./run.sh
```

### **Method 2: Manual Control**
```bash
# Install dependencies:
sudo apt install python3 python3-pip nodejs npm tmux sqlite3  # Ubuntu/Debian
# OR
sudo yum install python3 python3-pip nodejs npm tmux sqlite   # CentOS
# OR
sudo pacman -S python python-pip nodejs npm tmux sqlite       # Arch

# Setup project:
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-

# Choose installation type:
./install.sh                    # Full automated
./easy_start.sh setup          # With progress display
pip install -r backend/requirements-lite.txt  # Manual
```

### **Service Management Linux:**
```bash
# Start everything:
./easy_start.sh start

# Monitor with tmux:
tmux attach -t intel

# Status dashboard:
./status.sh

# Stop everything:
./easy_start.sh stop
```

---

## 🍎 **macOS**

### **Method 1: Homebrew (Recommended)**
```bash
# Install Homebrew if not installed:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies:
brew install python node git tmux sqlite

# Setup project:
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-

# ONE COMMAND SETUP:
./run.sh
```

### **Method 2: Manual macOS Setup**
```bash
# Download Python from python.org and Node.js from nodejs.org
# Install git from developer tools:
xcode-select --install

# Setup project:
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-

# Install dependencies:
pip3 install -r backend/requirements-lite.txt
cd frontend && npm install && cd ..

# Start platform:
./easy_start.sh
```

---

## 🪟 **Windows**

### **Method 1: Windows Native (Batch Script)**
```cmd
REM Install Python from python.org
REM Install Node.js from nodejs.org  
REM Install Git from git-scm.com

REM Clone and setup:
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-

REM ONE COMMAND SETUP:
run.bat
```

### **Method 2: WSL (Windows Subsystem for Linux)**
```bash
# Enable WSL and install Ubuntu
# Then follow Linux Ubuntu instructions:

wsl --install
# Restart computer, then:

wsl
sudo apt update && sudo apt install git python3 python3-pip nodejs npm

git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-

./run.sh
```

### **Method 3: PowerShell**
```powershell
# Install Chocolatey package manager:
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Install dependencies:
choco install python nodejs git

# Setup project:
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-

# Use Windows batch file:
.\run.bat
```

---

## 🐳 **Docker (Any Platform)**

### **Quick Docker Setup**
```bash
# Clone repository:
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-

# Start with Docker:
./start_with_docker.sh

# OR use docker-compose:
docker-compose up -d

# Access:
# Website: http://localhost:3000
# API: http://localhost:8000
```

---

## ☁️ **Cloud Platforms**

### **AWS/Google Cloud/Azure**
```bash
# Create VM instance with Ubuntu/Debian
# SSH into instance:
ssh user@your-instance-ip

# Install dependencies:
sudo apt update && sudo apt install git python3 python3-pip nodejs npm

# Setup project:
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-

# Run setup:
./install.sh

# Start services:
./easy_start.sh start

# Configure firewall to allow ports 3000 and 8000
```

### **Raspberry Pi**
```bash
# Same as Linux, but may need longer timeouts:
sudo apt update && sudo apt install git python3 python3-pip nodejs npm

git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-

# Use slower installation:
./install.sh

# Start with single worker:
./easy_start.sh start
```

---

## 🛠️ **Command Reference by Platform**

### **Universal Commands (Work Everywhere)**
```bash
./run.sh              # Complete setup + start (easiest)
./easy_start.sh        # Advanced management
./fix.sh              # Fix any problems
./status.sh           # Check what's running
./health_check.sh     # Full system analysis
./quick_test.sh       # Fast validation
```

### **Platform-Specific Commands**
```bash
# Termux only:
./start_termux.sh     # Termux-optimized setup
./termux_quickstart.sh # Quick psycopg2 fix

# Windows only:
run.bat               # Windows batch script

# Docker:
./start_with_docker.sh # Docker deployment
docker-compose up     # Standard Docker Compose
```

---

## 🌐 **Access Points (All Platforms)**

After successful setup, access these URLs:

| Service | URL | Description |
|---------|-----|-------------|
| **Website** | http://localhost:3000 | Full React frontend |
| **API** | http://localhost:8000 | FastAPI backend |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |
| **Health Check** | http://localhost:8000/health | Service health status |

---

## 🔧 **Management Commands**

### **Starting Services**
```bash
./run.sh                    # Simple start (first time)
./easy_start.sh start      # Advanced start
./easy_start.sh            # Full setup + start
```

### **Stopping Services**
```bash
./easy_start.sh stop       # Stop all services
Ctrl+C                     # Stop current session
tmux kill-session -t intel # Kill tmux session
```

### **Monitoring**
```bash
./status.sh               # Real-time status
./health_check.sh         # Health analysis
tmux attach -t intel      # Attach to services
```

### **Troubleshooting**
```bash
./fix.sh                  # Auto-fix common issues
./fix.sh deps            # Fix dependencies only
./fix.sh database        # Fix database only
python verify_fixes.py   # Run verification tests
```

---

## 📊 **System Requirements**

### **Minimum Requirements**
- **RAM**: 2GB (4GB recommended)
- **Storage**: 2GB free space
- **CPU**: Any modern processor
- **Network**: Internet connection for setup

### **Supported Versions**
- **Python**: 3.8+ (3.10+ recommended)
- **Node.js**: 16+ (18+ recommended)
- **Git**: Any recent version
- **OS**: Any Linux, macOS 10.15+, Windows 10+, Android (Termux)

---

## ⚡ **Quick Start Cheat Sheet**

| Platform | Quick Command |
|----------|---------------|
| **Termux** | `pkg install git && git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git && cd Intelligence-Gathering-Website-Project- && ./run.sh` |
| **Linux** | `git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git && cd Intelligence-Gathering-Website-Project- && ./run.sh` |
| **macOS** | `git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git && cd Intelligence-Gathering-Website-Project- && ./run.sh` |
| **Windows** | `git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git && cd Intelligence-Gathering-Website-Project- && run.bat` |

---

## 🆘 **Getting Help**

### **Built-in Help**
```bash
./easy_start.sh help      # Show all commands
./fix.sh help            # Show fix options
./status.sh              # Check system status
```

### **Common Issues & Solutions**

| Problem | Solution |
|---------|----------|
| psycopg2-binary fails | Use `./termux_quickstart.sh` or `requirements-lite.txt` |
| Port already in use | Run `./easy_start.sh stop` then restart |
| Permission denied | Run `chmod +x *.sh` |
| Dependencies missing | Run `./fix.sh deps` |
| Database errors | Run `./fix.sh database` |
| Node.js issues | Run `./fix.sh nodejs` |

### **Diagnostic Commands**
```bash
./health_check.sh        # Full system health (aim for 90%+)
./quick_test.sh          # Fast functionality test
python verify_fixes.py   # Comprehensive verification
./status.sh              # Current service status
```

---

## 🎯 **Success Indicators**

✅ **Setup Successful When:**
- Health check shows 90%+ score
- All verification tests pass
- Website loads at http://localhost:3000
- API responds at http://localhost:8000
- No error messages in startup logs

🎉 **You're Ready!** Start exploring the Intelligence Gathering Platform!