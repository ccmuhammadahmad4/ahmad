# Configuration Limits Reference

## File Upload Limits

### Current Settings:
- **Maximum Upload Size**: **100MB** per file
- **Nginx Setting**: `client_max_body_size 100M;`
- **Location**: Line 13 in `nginx-config.conf`

### To Change Upload Limit:

1. **Edit Nginx Configuration**:
   ```bash
   sudo nano /etc/nginx/sites-available/default
   ```
   
2. **Update the limit**:
   ```nginx
   client_max_body_size 100M;  # Change this value
   ```

3. **Restart Nginx**:
   ```bash
   sudo systemctl reload nginx
   ```

### Common Size Values:
- `10M` = 10 megabytes
- `50M` = 50 megabytes  
- `100M` = 100 megabytes
- `500M` = 500 megabytes
- `1G` = 1 gigabyte

### Flask Application Side:
The Flask app should also validate file sizes. Check `app.py` for any additional limits:

```python
# Example Flask file size validation
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB in bytes

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and len(file.read()) <= MAX_FILE_SIZE:
        # Process file
        pass
    else:
        return "File too large", 413
```

## Security Considerations

- Large file uploads can consume server resources
- Consider implementing file type validation
- Monitor disk space in upload directory
- Set appropriate timeout values for large uploads

## Monitoring Upload Directory

```bash
# Check upload directory size
du -sh /home/abdulrehman/threat_analyzer_web/threat_analyzer_web/uploads/

# Check available disk space  
df -h

# Monitor large files
find /uploads/ -size +50M -ls
```