# Simple Application Suite

This project contains 5 simple web applications, each with their own FastAPI backend and HTML/CSS/JavaScript frontend.

## Project Structure

```
applications/
├── app1/
│   ├── main.py (FastAPI server - Port 5001)
│   ├── requirements.txt
│   └── static/
│       ├── index.html
│       ├── style.css
│       └── script.js
├── app2/ (Port 5002)
├── app3/ (Port 5003)
├── app4/ (Port 5004)
├── app5/ (Port 5005)
├── nginx-app1.conf
├── nginx-app2.conf
├── nginx-app3.conf
├── nginx-app4.conf
├── nginx-app5.conf
├── setup-all-apps.ps1
└── README.md
```

## Quick Start

### 1. Install Dependencies
```bash
# For each application, run:
cd app1
pip install -r requirements.txt

cd ../app2
pip install -r requirements.txt

# ... and so on for all apps
```

### 2. Run Applications Directly
```bash
# Application 1 (Port 5001)
cd app1
python main.py

# Application 2 (Port 5002)
cd app2
python main.py

# ... and so on
```

### 3. Setup with Nginx (LAN Access)

Each application has its own nginx configuration file:
- `nginx-app1.conf` - Application 1 (Backend: 5001, Nginx: 8081)
- `nginx-app2.conf` - Application 2 (Backend: 5002, Nginx: 8082)
- `nginx-app3.conf` - Application 3 (Backend: 5003, Nginx: 8083)
- `nginx-app4.conf` - Application 4 (Backend: 5004, Nginx: 8084)
- `nginx-app5.conf` - Application 5 (Backend: 5005, Nginx: 8085)

#### To setup nginx:
1. Copy the nginx configuration files to your nginx config directory
2. Include them in your main nginx.conf or use them separately
3. Restart nginx
4. Access applications via:
   - http://localhost:8081 (App 1)
   - http://localhost:8082 (App 2)
   - http://localhost:8083 (App 3)
   - http://localhost:8084 (App 4)
   - http://localhost:8085 (App 5)

## Application Features

Each application includes:
- **Frontend**: HTML, CSS, JavaScript with responsive design
- **Backend**: FastAPI server with API endpoint
- **Unique Design**: Different color schemes and styling
- **API Testing**: Built-in API test functionality
- **Auto-refresh**: Dynamic content loading

## Application Details

| App | Port | Nginx Port | Color Scheme | 
|-----|------|------------|--------------|
| App 1 | 5001 | 8081 | Blue/Purple Gradient |
| App 2 | 5002 | 8082 | Green Gradient |
| App 3 | 5003 | 8083 | Red/Purple Gradient |
| App 4 | 5004 | 8084 | Pink/Red Gradient |
| App 5 | 5005 | 8085 | Blue/Cyan Gradient |

## API Endpoints

Each application provides:
- `GET /` - Serve the frontend
- `GET /api/app-info` - Returns application information

## Development

To modify an application:
1. Edit the `main.py` for backend changes
2. Edit files in `static/` folder for frontend changes
3. Restart the application to see changes

## Notes

- All applications are independent and can run simultaneously
- Each has its own dependencies and configuration
- Nginx configurations include LAN access setup
- Applications show their number prominently on the frontend
- Each application has unique styling and colors