// Application 4 JavaScript Functions
document.addEventListener('DOMContentLoaded', function() {
    loadAppInfo();
});

async function loadAppInfo() {
    try {
        const response = await fetch('./api/app-info');
        const data = await response.json();
        
        document.getElementById('app-number').textContent = data.app_number;
        document.getElementById('app-message').textContent = data.message;
        document.getElementById('app-port').textContent = data.port;
        document.getElementById('app-status').textContent = 'Active';
        
        console.log('App info loaded:', data);
    } catch (error) {
        console.error('Error loading app info:', error);
        document.getElementById('app-message').textContent = 'Error loading application info';
        document.getElementById('app-status').textContent = 'Error';
    }
}

async function refreshInfo() {
    const button = event.target;
    button.textContent = 'Refreshing...';
    button.disabled = true;
    
    try {
        await loadAppInfo();
        showNotification('Application info refreshed successfully!', 'success');
    } catch (error) {
        showNotification('Error refreshing app info', 'error');
    } finally {
        button.textContent = 'Refresh Info';
        button.disabled = false;
    }
}

async function testAPI() {
    const button = event.target;
    button.textContent = 'Testing...';
    button.disabled = true;
    
    try {
        const response = await fetch('./api/app-info');
        if (response.ok) {
            const data = await response.json();
            showNotification(`API Test Success! App ${data.app_number} is responding.`, 'success');
        } else {
            showNotification('API Test Failed!', 'error');
        }
    } catch (error) {
        console.error('API test error:', error);
        showNotification('API connection error!', 'error');
    } finally {
        button.textContent = 'Test API';
        button.disabled = false;
    }
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 5px;
        color: white;
        font-weight: 600;
        z-index: 1000;
        transition: all 0.3s ease;
        max-width: 300px;
    `;
    
    switch(type) {
        case 'success':
            notification.style.backgroundColor = '#48bb78';
            break;
        case 'error':
            notification.style.backgroundColor = '#f56565';
            break;
        default:
            notification.style.backgroundColor = '#f5576c';
    }
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
        notification.style.opacity = '1';
    }, 10);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        notification.style.opacity = '0';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}