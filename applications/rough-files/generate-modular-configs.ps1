# MODULAR NGINX SETUP GENERATOR
# Creates separate routing files for each application

# App configurations
$apps = @(
    @{Number=3; Port=5003; Theme="Purple"},
    @{Number=4; Port=5004; Theme="Orange"},
    @{Number=5; Port=5005; Theme="Red"}
)

foreach ($app in $apps) {
    $appNumber = $app.Number
    $port = $app.Port
    $theme = $app.Theme
    
    $content = @"
# APP$appNumber ROUTING CONFIGURATION
# $theme theme FastAPI application
# Port: $port

# Static files for app$appNumber (CSS, JS, images)
location ~ ^/app$appNumber/static/(.*)$ {
    proxy_pass http://127.0.0.1:$port/static/$1;
    proxy_set_header Host $host;
}

# App $appNumber main routing - $theme theme
location /app$appNumber/ {
    rewrite ^/app$appNumber/(.*)$ /$1 break;
    proxy_pass http://127.0.0.1:$port;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
}
"@

    $filename = "app$appNumber-routing.conf"
    $content | Out-File -FilePath $filename -Encoding UTF8
    Write-Host "Created: $filename"
}

Write-Host "`nAll app routing files created successfully!"
Write-Host "Next steps:"
Write-Host "1. Copy all app*-routing.conf files to C:\nginx\conf\apps\"
Write-Host "2. Copy nginx-port80-base.conf to C:\nginx\conf\apps\"
Write-Host "3. Update nginx.conf to include nginx-port80-base.conf"
Write-Host "4. Restart nginx"