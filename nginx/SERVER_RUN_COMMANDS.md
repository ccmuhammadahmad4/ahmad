# 🚀 SERVER PAR RUN KARNE KE COMMANDS 🚀

## 📋 PART 1: INITIAL SETUP (Ek baar karna hai)

### 1.1 Server par login
```bash
ssh abdulrehman@YOUR_SERVER_IP
```

### 1.2 System packages install 
```bash
sudo apt update
sudo apt install nginx python3-pip python3-venv -y
```

### 1.3 Working directory banao
```bash
mkdir -p ~/deployment-files
cd ~/deployment-files
```

---

## 📋 PART 2: FILES CREATE KARO (Copy-Paste)

### 2.1 Nginx Configuration
```bash
nano nginx-config.conf
```
**Content copy-paste karo from nginx-config.conf file**

### 2.2 Gunicorn Configuration  
```bash
nano gunicorn-config.py
```
**Content copy-paste karo from gunicorn-config.py file**

### 2.3 Service File
```bash
nano threat-analyzer.service
```
**Content copy-paste karo from threat-analyzer.service file**

### 2.4 Server IP update karo
```bash
nano nginx-config.conf
```
**Line 3 mein `YOUR_SERVER_IP` ko replace karo actual IP se**

---

## 📋 PART 3: DEPLOYMENT COMMANDS (Sequence mein run karo)

### 3.1 Log directory banao
```bash
sudo mkdir -p /var/log/gunicorn
sudo chown abdulrehman:abdulrehman /var/log/gunicorn
```

### 3.2 Nginx configuration copy
```bash
sudo cp nginx-config.conf /etc/nginx/sites-available/threat_analyzer_web
sudo ln -sf /etc/nginx/sites-available/threat_analyzer_web /etc/nginx/sites-enabled/
```

### 3.3 Default nginx site remove karo
```bash
sudo rm -f /etc/nginx/sites-enabled/default
```

### 3.4 Service file copy
```bash
sudo cp threat-analyzer.service /etc/systemd/system/
```

### 3.5 Gunicorn config copy
```bash
cp gunicorn-config.py /home/abdulrehman/threat_analyzer_web/threat_analyzer_web/
```

### 3.6 Nginx configuration test
```bash
sudo nginx -t
```
**✅ Output: "syntax is ok" aur "test is successful"**

### 3.7 Services start karo
```bash
sudo systemctl daemon-reload
sudo systemctl enable threat-analyzer.service  
sudo systemctl restart nginx
sudo systemctl start threat-analyzer.service
```

---

## 📋 PART 4: VERIFICATION COMMANDS

### 4.1 Service status check
```bash
sudo systemctl status threat-analyzer.service
sudo systemctl status nginx
```
**✅ Dono "active (running)" show karna chahiye**

### 4.2 Port listening check
```bash
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :5000
```
**✅ Port 80 (nginx) aur 5000 (gunicorn) listening hona chahiye**

### 4.3 Application test
```bash
curl http://localhost
curl http://YOUR_SERVER_IP
```
**✅ Flask app response milna chahiye**

---

## 📋 PART 5: DAILY OPERATIONS (Regular use ke liye)

### 5.1 Application restart
```bash
sudo systemctl restart threat-analyzer.service
```

### 5.2 Nginx restart  
```bash
sudo systemctl restart nginx
```

### 5.3 Check logs
```bash
# Application logs
sudo journalctl -u threat-analyzer.service -f

# Nginx error logs  
sudo tail -f /var/log/nginx/error.log

# Gunicorn logs
sudo tail -f /var/log/gunicorn/threat_analyzer_error.log
```

### 5.4 Stop services
```bash
sudo systemctl stop threat-analyzer.service
sudo systemctl stop nginx
```

### 5.5 Start services
```bash
sudo systemctl start nginx
sudo systemctl start threat-analyzer.service
```

---

## 🛠️ TROUBLESHOOTING COMMANDS

### Agar application nahi chal rahi:

#### 1. Check if virtual environment exists
```bash
ls -la /home/abdulrehman/threat_analyzer_web/venv/bin/python3
```

#### 2. Check if wsgi.py exists
```bash
ls -la /home/abdulrehman/threat_analyzer_web/threat_analyzer_web/wsgi.py
```

#### 3. Manually test gunicorn
```bash
cd /home/abdulrehman/threat_analyzer_web/threat_analyzer_web
source ../venv/bin/activate
gunicorn --bind 127.0.0.1:5000 wsgi:application
```

#### 4. Check permissions
```bash
sudo chown -R abdulrehman:abdulrehman /home/abdulrehman/threat_analyzer_web/
```

#### 5. Check if port is free
```bash
sudo lsof -i :5000
sudo kill -9 PID_NUMBER  # Replace PID_NUMBER with actual PID
```

---

## ✅ SUCCESS INDICATORS

### Application working properly ka signs:

1. **Service Status:**
   ```bash
   sudo systemctl status threat-analyzer.service
   # Output: "Active: active (running)"
   ```

2. **Port Listening:**
   ```bash
   sudo netstat -tlnp | grep :80
   sudo netstat -tlnp | grep :5000
   # Both ports should show LISTEN
   ```

3. **Browser Access:**
   ```
   http://YOUR_SERVER_IP
   # Should load your Flask application
   ```

4. **No Errors in Logs:**
   ```bash
   sudo journalctl -u threat-analyzer.service --no-pager
   # Should not show any ERROR messages
   ```

---

## 🎯 FINAL ACCESS

**Your application will be available at:**
```
http://YOUR_SERVER_IP
```

**Example: If your server IP is 192.168.1.100:**
```
http://192.168.1.100
```