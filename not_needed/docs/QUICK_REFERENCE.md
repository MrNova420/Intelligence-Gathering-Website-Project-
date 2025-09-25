# 📋 Quick Reference Card - Intelligence Gathering Platform

## **🚀 One-Command Setup (Any Platform)**

```bash
# Universal setup command:
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git && cd Intelligence-Gathering-Website-Project- && ./run.sh
```

---

## **📱 Platform-Specific Quick Start**

### **Android (Termux)**
```bash
pkg update && pkg install git
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-
./run.sh
```

### **Linux (Ubuntu/Debian)**
```bash
sudo apt install git python3 nodejs -y
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-
./run.sh
```

### **macOS**
```bash
brew install python node git
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-
./run.sh
```

### **Windows**
```cmd
REM Install Python, Node.js, Git first
git clone https://github.com/MrNova420/Intelligence-Gathering-Website-Project-.git
cd Intelligence-Gathering-Website-Project-
run.bat
```

---

## **🎮 Essential Commands**

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `./run.sh` | **Complete setup + start** | First time, or simple restart |
| `./easy_start.sh` | **Advanced management** | When you need control |
| `./fix.sh` | **Auto-fix problems** | When something breaks |
| `./status.sh` | **Check what's running** | Anytime you want status |
| `./health_check.sh` | **Full system analysis** | Deep troubleshooting |

---

## **🌐 Access URLs**

After setup, open in your browser:

| Service | URL | What You'll See |
|---------|-----|-----------------|
| **🌍 Website** | http://localhost:3000 | Full Intelligence Platform Interface |
| **⚙️ API** | http://localhost:8000 | JSON API Responses |
| **📖 Docs** | http://localhost:8000/docs | Interactive API Documentation |

---

## **🛠️ Management Commands**

### **Starting**
```bash
./run.sh                # Simple start (recommended)
./easy_start.sh start   # Advanced start
./easy_start.sh         # Full setup + start
```

### **Stopping**
```bash
./easy_start.sh stop    # Clean shutdown
Ctrl+C                  # Force stop current session
```

### **Monitoring**
```bash
./status.sh             # Quick status check
./health_check.sh       # Detailed health analysis
tmux attach -t intel    # View live logs
```

### **Troubleshooting**
```bash
./fix.sh                # Fix everything automatically
./fix.sh deps          # Fix dependencies only
./fix.sh database      # Fix database issues
python verify_fixes.py # Run all tests
```

---

## **🔧 Troubleshooting Quick Fixes**

| Problem | Quick Fix |
|---------|-----------|
| **psycopg2-binary error** | `./termux_quickstart.sh` |
| **Port 3000/8000 in use** | `./easy_start.sh stop` then restart |
| **Dependencies missing** | `./fix.sh deps` |
| **Database won't start** | `./fix.sh database` |
| **Frontend won't load** | `./fix.sh nodejs` |
| **Everything broken** | `./fix.sh all` |

---

## **📊 Health Check Indicators**

| Score | Status | Action |
|-------|--------|--------|
| **90-100%** | 🟢 Excellent | You're good to go! |
| **70-89%** | 🟡 Good | Minor issues, platform works |
| **50-69%** | 🟠 Fair | Some problems, check logs |
| **0-49%** | 🔴 Poor | Run `./fix.sh` immediately |

---

## **💡 Pro Tips**

### **For First-Time Users**
1. Use `./run.sh` - it handles everything
2. Wait for "Platform is running!" message
3. Open http://localhost:3000 in browser
4. Default login: admin@platform.local / admin123

### **For Developers**
1. Use `./easy_start.sh` for more control
2. Use `tmux attach -t intel` to see live logs
3. Frontend auto-reloads on changes
4. Backend needs restart for code changes

### **For Troubleshooting**
1. Run `./health_check.sh` first
2. If <90% health, run `./fix.sh`
3. Check `./status.sh` for service status
4. Use `python verify_fixes.py` for deep testing

---

## **🎯 Success Checklist**

✅ Setup complete when you see:
- [ ] "Platform is running!" message
- [ ] Website loads at http://localhost:3000
- [ ] API responds at http://localhost:8000
- [ ] Health check shows 90%+ score
- [ ] No error messages in terminal

---

## **📞 Getting Help**

### **Built-in Help**
```bash
./easy_start.sh help    # Show all commands
./fix.sh help          # Show fix options
./health_check.sh      # Detailed diagnostics
```

### **Quick Diagnostics**
```bash
# Check if everything is working:
./quick_test.sh

# See what's running:
./status.sh

# Full health analysis:
./health_check.sh
```

---

## **⚡ Emergency Recovery**

If everything is broken:

```bash
# Nuclear option - fix everything:
./fix.sh all

# Or step by step:
./fix.sh processes     # Kill stuck processes
./fix.sh deps         # Reinstall dependencies  
./fix.sh database     # Reset database
./fix.sh env          # Reset configuration
```

Then restart:
```bash
./run.sh
```

---

## **🔄 Common Workflows**

### **Daily Use**
```bash
./run.sh              # Start everything
# Use the platform
./easy_start.sh stop  # Stop when done
```

### **Development**
```bash
./easy_start.sh start      # Start services
tmux attach -t intel       # View logs
# Make changes
./easy_start.sh restart    # Restart after changes
```

### **Troubleshooting**
```bash
./status.sh               # Check status
./health_check.sh         # Full analysis
./fix.sh                  # Auto-fix issues
./run.sh                  # Restart everything
```

---

**🎉 That's it! You now have everything you need to run the Intelligence Gathering Platform on any device or platform.**