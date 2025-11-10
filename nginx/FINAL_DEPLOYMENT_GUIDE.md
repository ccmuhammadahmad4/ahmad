# 🚀 FINAL ERROR-FREE DEPLOYMENT GUIDE 🚀

## ✅ PRE-REQUISITES CHECK

### Server Information Required:
- Server IP Address: ________________
- Username: abdulrehman
- Application Path: /home/abdulrehman/threat_analyzer_web/threat_analyzer_web

---

## 📋 STEP 1: SERVER PAR LOGIN KARO

```bash
ssh abdulrehman@YOUR_SERVER_IP
```

## 📋 STEP 2: WORKING DIRECTORY BANAO

```bash
mkdir -p ~/deployment-files
cd ~/deployment-files
```

## 📋 STEP 3: FILES CREATE KARO (Copy-Paste Content)

### 3.1 Nginx Configuration File
```bash
nano nginx-config.conf
```

**COPY-PASTE THIS EXACT CONTENT:**
```nginx
server {
    listen 80;
    server_name YOUR_SERVER_IP;
    
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    
    client_max_body_size 100M;
    root /var/www/html;
    
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;
    
    location /static/ {
        alias /home/abdulrehman/threat_analyzer_web/threat_analyzer_web/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
    
    location /uploads/ {
        alias /home/abdulrehman/threat_analyzer_web/threat_analyzer_web/uploads/;
        expires 1d;
        add_header Cache-Control "public";
        access_log off;
    }
    
    location = /favicon.ico {
        alias /home/abdulrehman/threat_analyzer_web/threat_analyzer_web/static/favicon.ico;
        access_log off;
        log_not_found off;
    }
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        proxy_buffering on;
        proxy_buffer_size 128k;
        proxy_buffers 4 256k;
        proxy_busy_buffers_size 256k;
    }
    
    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
    
    location = /404.html {
        root /var/www/html;
        internal;
    }
    
    location = /50x.html {
        root /var/www/html;
        internal;
    }
    
    location ~ /\. {
        deny all;
    }
    
    location ~ ~$ {
        deny all;
    }
}
```

**Save karne ke liye:** `Ctrl+X` → `Y` → `Enter`

### 3.2 Gunicorn Configuration File
```bash
nano gunicorn-config.py
```

**COPY-PASTE THIS EXACT CONTENT:**
```python
import multiprocessing

bind = "127.0.0.1:5000"
backlog = 2048

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

max_requests = 1000
max_requests_jitter = 50

accesslog = "/var/log/gunicorn/threat_analyzer_access.log"
errorlog = "/var/log/gunicorn/threat_analyzer_error.log"
loglevel = "info"

proc_name = "threat_analyzer_web"
daemon = False
user = "abdulrehman"
group = "abdulrehman"
preload_app = True
graceful_timeout = 30
```

**Save karne ke liye:** `Ctrl+X` → `Y` → `Enter`

### 3.3 Service File
```bash
nano threat-analyzer.service
```

**COPY-PASTE THIS EXACT CONTENT:**
```ini
[Unit]
Description=Threat Analyzer Web Application
After=network.target

[Service]
Type=exec
User=abdulrehman
Group=abdulrehman
WorkingDirectory=/home/abdulrehman/threat_analyzer_web/threat_analyzer_web
Environment=PATH=/home/abdulrehman/threat_analyzer_web/venv/bin
ExecStart=/home/abdulrehman/threat_analyzer_web/venv/bin/gunicorn --config gunicorn-config.py wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure
RestartSec=5
KillMode=mixed
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target
```

**Save karne ke liye:** `Ctrl+X` → `Y` → `Enter`

---

## 📋 STEP 4: IMPORTANT - UPDATE YOUR SERVER IP

```bash
nano nginx-config.conf
```

**Line 3 mein** `YOUR_SERVER_IP` ko replace karo apne actual server IP se:
```nginx
server_name 192.168.1.100;  # Example: Replace with your IP
```

---

## 📋 STEP 5: SYSTEM PACKAGES INSTALL

```bash
sudo apt update
sudo apt install nginx python3-pip python3-venv -y
```

---

## 📋 STEP 6: DEPLOYMENT COMMANDS (Ek ek kar ke run karo)

### 6.1 Log Directory
```bash
sudo mkdir -p /var/log/gunicorn
sudo chown abdulrehman:abdulrehman /var/log/gunicorn
```

### 6.2 Nginx Configuration
```bash
sudo cp nginx-config.conf /etc/nginx/sites-available/threat_analyzer_web
sudo ln -sf /etc/nginx/sites-available/threat_analyzer_web /etc/nginx/sites-enabled/
```

### 6.3 Remove Default Nginx Site
```bash
sudo rm -f /etc/nginx/sites-enabled/default
```

### 6.4 Service Configuration
```bash
sudo cp threat-analyzer.service /etc/systemd/system/
```

### 6.5 Gunicorn Configuration
```bash
cp gunicorn-config.py /home/abdulrehman/threat_analyzer_web/threat_analyzer_web/
```

### 6.6 Test Nginx Configuration
```bash
sudo nginx -t
```
**✅ Yeh command "syntax is ok" aur "test is successful" show karna chahiye**

### 6.7 Start Services
```bash
sudo systemctl daemon-reload
sudo systemctl enable threat-analyzer.service
sudo systemctl restart nginx
sudo systemctl start threat-analyzer.service
```

---

## 📋 STEP 7: VERIFICATION (Check karo sab kuch working hai)

### 7.1 Service Status Check
```bash
sudo systemctl status threat-analyzer.service
sudo systemctl status nginx
```
**✅ Dono "active (running)" show karna chahiye**

### 7.2 Port Check
```bash
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :5000
```
**✅ Port 80 (nginx) aur 5000 (gunicorn) listening hona chahiye**

### 7.3 Application Test
```bash
curl http://localhost
```
**✅ Yeh aapka Flask app ka response dena chahiye**

---

## 📋 STEP 8: ACCESS YOUR APPLICATION

**Browser mein jao:**
```
http://YOUR_SERVER_IP
```

---

## 🛠️ TROUBLESHOOTING COMMANDS

### Agar koi error aaye to:

#### Check Logs
```bash
# Service logs
sudo journalctl -u threat-analyzer.service -f

# Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Gunicorn logs
sudo tail -f /var/log/gunicorn/threat_analyzer_error.log
```

#### Restart Services
```bash
sudo systemctl restart threat-analyzer.service
sudo systemctl restart nginx
```

#### Check if Virtual Environment exists
```bash
ls -la /home/abdulrehman/threat_analyzer_web/venv/bin/
```

#### Check if wsgi.py exists
```bash
ls -la /home/abdulrehman/threat_analyzer_web/threat_analyzer_web/wsgi.py
```

---

## ✅ SUCCESS CHECKLIST

- [ ] Server par login successful
- [ ] Files create aur copy paste successful
- [ ] Server IP updated in nginx config
- [ ] nginx -t command successful
- [ ] Services start successful
- [ ] Port 80 aur 5000 listening
- [ ] Browser mein application accessible

---

## 🎯 FINAL RESULT

Aapka application is URL par available hoga:
**http://YOUR_SERVER_IP**

## 📞 SUPPORT

Agar koi step mein problem aaye to specific error message share karo, main help karunga.
```