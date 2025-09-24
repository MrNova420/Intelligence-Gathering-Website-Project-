# 🚀 Termux Setup Guide - Intelligence Gathering Platform

## **Complete Termux/Android Deployment Guide**

This guide provides step-by-step instructions for running the Intelligence Gathering Platform on Android devices using Termux.

---

## 📱 **Prerequisites for Termux**

### **1. Install Termux**
- Download from F-Droid (recommended): https://f-droid.org/packages/com.termux/
- Or GitHub releases: https://github.com/termux/termux-app/releases

### **2. Basic Termux Setup**
```bash
# Update package lists
pkg update && pkg upgrade

# Install essential packages
pkg install python git nodejs-lts redis

# Install Python package manager
pkg install python-pip

# Optional: Install text editor
pkg install nano vim
```

---

## 🔧 **Platform Installation**

### **Step 1: Clone Repository**
```bash
# Clone the project
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git

# Navigate to project directory
cd Intelligence-Gathering-Website-Project-
```

### **Step 2: Install Python Dependencies**
```bash
# Install lightweight dependencies (SQLite only - recommended for Termux)
pip install -r backend/requirements-lite.txt

# If you encounter build errors with requirements-lite.txt, try minimal install:
pip install fastapi uvicorn sqlalchemy pydantic dnspython phonenumbers python-dotenv requests passlib[bcrypt] cryptography

# Alternative for problematic packages (install one by one):
pip install --no-cache-dir fastapi uvicorn sqlalchemy pydantic requests

# If psycopg2-binary fails (common on Termux):
# Skip it - SQLite will be used instead of PostgreSQL
```

### **Step 3: Configure Environment**
```bash
# Copy environment template
cp .env.example .env

# Edit configuration (use nano or vim)
nano .env

# Basic Termux configuration:
DATABASE_URL=sqlite:///./intelligence_platform.db
REDIS_URL=redis://localhost:6379/0
DEBUG=true
ENVIRONMENT=termux
```

### **Step 4: Initialize Database**
```bash
# Setup SQLite database
python backend/app/db/setup_standalone.py

# Should output: ✅ Database setup completed successfully
```

### **Step 5: Start Redis (Optional)**
```bash
# Start Redis server in background
redis-server --daemonize yes

# Or use in-memory fallback (no Redis required)
export USE_REDIS_FALLBACK=true
```

---

## 🚀 **Running the Platform**

### **Start the Server**
```bash
# Run the standalone server
python backend/run_standalone.py

# You should see:
# 🚀 Intelligence Gathering Platform - Standalone Mode
# 📱 Termux Compatible: YES
# 🌐 Access Points:
#    • API Server: http://localhost:8000
#    • API Docs: http://localhost:8000/docs
```

### **Test the Platform**
```bash
# In a new Termux session, run validation tests
python backend/run_validation.py

# Run comprehensive enhancement tests
python backend/comprehensive_enhancement_test.py

# Expected output: ✅ All tests passed
```

### **Access the Platform**
- **API Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Admin Panel**: http://localhost:8000/admin

---

## 🌐 **Network Access from Other Devices**

### **Find Your Device IP**
```bash
# Get your device's IP address
ip addr show wlan0 | grep inet

# Or use:
ifconfig wlan0 | grep inet
```

### **Access from Other Devices**
If your Termux device IP is `192.168.1.100`, other devices on the same network can access:
- **API**: http://192.168.1.100:8000
- **Docs**: http://192.168.1.100:8000/docs

---

## 🔧 **Advanced Configuration**

### **Performance Optimization**
```bash
# Add to .env file for better performance
export UVICORN_WORKERS=1
export DATABASE_POOL_SIZE=5
export REDIS_MAX_CONNECTIONS=10
```

### **Security Configuration**
```bash
# Generate secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Add to .env file:
SECRET_KEY=your-generated-key-here
```

### **Memory Optimization**
```bash
# For low-memory devices, add to .env:
USE_MINIMAL_SCANNERS=true
CACHE_SIZE_LIMIT=50MB
WORKER_MEMORY_LIMIT=256MB
```

---

## 🧪 **Testing & Validation**

### **Run All Tests**
```bash
# Basic validation
python backend/run_validation.py

# Comprehensive tests
python backend/comprehensive_enhancement_test.py

# Security tests
python backend/tests/test_security.py

# Scanner tests
python backend/tests/test_scanners.py
```

### **API Testing**
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test API documentation
curl http://localhost:8000/docs

# Test scanner endpoint
curl -X POST http://localhost:8000/api/v1/scanners/email \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'
```

---

## 🛠️ **Troubleshooting**

### **Common Issues & Solutions**

#### **1. Permission Denied Errors**
```bash
# Fix file permissions
chmod +x backend/run_standalone.py
chmod +x backend/app/db/setup_standalone.py
```

#### **2. Package Installation Failures**
```bash
# Common solution: Use lightweight requirements
pip install -r backend/requirements-lite.txt

# If psycopg2-binary fails (common in Termux):
# Skip it - SQLite will be used instead

# Update pip first
pip install --upgrade pip

# Install build essentials if needed
pkg install build-essential clang

# For cryptography issues:
pkg install openssl-dev libffi-dev

# Install minimal packages individually:
pip install fastapi uvicorn sqlalchemy pydantic dnspython phonenumbers

# Platform will use fallback implementations for missing packages
```

#### **3. Database Connection Issues**
```bash
# Remove existing database and recreate
rm backend/intelligence_platform.db
python backend/app/db/setup_standalone.py
```

#### **4. Port Already in Use**
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 PID

# Or use different port
python backend/run_standalone.py --port 8080
```

#### **5. Memory Issues**
```bash
# Check available memory
free -h

# Restart Termux if needed
exit
# Reopen Termux app
```

### **Redis Issues**
```bash
# If Redis fails to start
redis-server --help

# Use fallback mode
export USE_REDIS_FALLBACK=true
python backend/run_standalone.py
```

---

## 📊 **Performance Monitoring**

### **Monitor Resource Usage**
```bash
# Check CPU and memory usage
top

# Check disk usage
df -h

# Monitor Python processes
ps aux | grep python
```

### **Platform Health Monitoring**
```bash
# Check platform health
curl http://localhost:8000/health

# View logs
tail -f backend/logs/platform.log
```

---

## 🔐 **Security Considerations**

### **Termux Security**
- Keep Termux and packages updated
- Use strong passwords for admin account
- Don't expose on public networks without authentication
- Consider VPN for remote access

### **Network Security**
```bash
# Only allow local connections (default)
export UVICORN_HOST=127.0.0.1

# Allow network access (be cautious)
export UVICORN_HOST=0.0.0.0
```

---

## 🎯 **Usage Examples**

### **Basic Email Scan**
```python
import requests

# Submit email scan
response = requests.post('http://localhost:8000/api/v1/queries/', 
    json={
        'query_type': 'email',
        'query_value': 'test@example.com',
        'scan_options': {'basic_scan': True}
    }
)

print(f"Query ID: {response.json()['id']}")
```

### **Phone Number Analysis**
```python
import requests

# Submit phone scan  
response = requests.post('http://localhost:8000/api/v1/queries/',
    json={
        'query_type': 'phone',
        'query_value': '+1234567890',
        'scan_options': {'include_location': True}
    }
)

print(f"Scan submitted: {response.json()}")
```

---

## 📱 **Termux-Specific Features**

### **Storage Access**
```bash
# Access Android storage
termux-setup-storage

# Platform data location
ls ~/storage/shared/IntelligencePlatform/
```

### **Notifications**
```bash
# Install termux-api for notifications
pkg install termux-api

# Send completion notification
termux-notification -t "Scan Complete" -c "Intelligence gathering finished"
```

### **Background Operation**
```bash
# Keep running in background
nohup python backend/run_standalone.py > platform.log 2>&1 &

# Check if running
ps aux | grep python
```

---

## 🆘 **Support & Resources**

### **Termux Documentation**
- Official Wiki: https://wiki.termux.com/
- Package Repository: https://packages.termux.org/
- Community Forum: https://www.reddit.com/r/termux/

### **Platform Support**
- GitHub Issues: https://github.com/MrNova420/Intelligence-Gathering-Website-Project-/issues
- Validation Tool: `python backend/run_validation.py`
- Test Suite: `python backend/comprehensive_enhancement_test.py`

### **Quick Commands Reference**
```bash
# Start platform
python backend/run_standalone.py

# Run tests
python backend/run_validation.py

# Check health
curl http://localhost:8000/health

# View logs
tail -f platform.log

# Stop server
pkill -f run_standalone.py
```

---

## ✅ **Success Checklist**

After setup, verify these work:

- [ ] ✅ Termux packages installed
- [ ] ✅ Python dependencies installed  
- [ ] ✅ Database initialized successfully
- [ ] ✅ Server starts without errors
- [ ] ✅ Health check returns 200 OK
- [ ] ✅ API documentation accessible
- [ ] ✅ Validation tests pass
- [ ] ✅ Sample queries work
- [ ] ✅ Can access from other devices (optional)

**If all items are checked, your Intelligence Gathering Platform is fully operational on Termux! 🎉**

---

## 🎉 **What's Next?**

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Run Sample Queries**: Test email and phone scanning
3. **Access Admin Panel**: Use admin@platform.local / admin123
4. **Customize Configuration**: Edit .env for your needs
5. **Set up Remote Access**: Configure for network access if needed

**Your platform is now ready for intelligence gathering operations on Android! 📱🔍**