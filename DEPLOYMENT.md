# IndicSahayak Deployment Guide

This guide covers different deployment options for IndicSahayak AI Assistant.

## Table of Contents

1. [Local Development](#local-development)
2. [Hugging Face Spaces](#hugging-face-spaces)
3. [Streamlit Cloud](#streamlit-cloud)
4. [Docker Deployment](#docker-deployment)
5. [Cloud Platforms](#cloud-platforms)
6. [Self-Hosting](#self-hosting)

## Local Development

### Prerequisites
- Python 3.8+
- pip or conda
- Git

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/indic-sahayak.git
cd indic-sahayak

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r chatbot/requirements.txt

# Run the application
streamlit run chatbot/indic_sahayak.py
```

## Hugging Face Spaces

### Creating a Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose "Streamlit" as the SDK
4. Set visibility to "Public"

### Space Configuration

Create `README.md` in your Space:
```markdown
---
title: IndicSahayak
emoji: 🇮🇳
colorFrom: blue
colorTo: red
sdk: streamlit
sdk_version: 1.28.0
app_file: chatbot/indic_sahayak.py
pinned: false
license: mit
short_description: AI Assistant for Hindi and Telugu languages
---
```

### Requirements File
Create `requirements.txt`:
```
streamlit>=1.28.0
requests>=2.31.0
pandas>=2.0.0
huggingface-hub>=0.16.0
transformers>=4.30.0
torch>=2.0.0
numpy>=1.24.0
python-dotenv>=1.0.0
```

### Environment Variables
Set in Space settings:
- `HUGGINGFACE_API_KEY`: Your Hugging Face API key
- `DIFY_API_KEY`: Your Dify API key (optional)

## Streamlit Cloud

### Deployment Steps

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Click "New app"
4. Connect your GitHub repository
5. Set the main file path: `chatbot/indic_sahayak.py`
6. Add environment variables if needed

### Configuration
```yaml
# .streamlit/config.toml
[server]
port = 8501
enableCORS = false
enableXsrfProtection = false

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

## Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY chatbot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY chatbot/ .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
CMD ["streamlit", "run", "indic_sahayak.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  indic-sahayak:
    build: .
    ports:
      - "8501:8501"
    environment:
      - HUGGINGFACE_API_KEY=${HUGGINGFACE_API_KEY}
      - DIFY_API_KEY=${DIFY_API_KEY}
    volumes:
      - ./chatbot:/app
    restart: unless-stopped
```

### Build and Run
```bash
# Build the image
docker build -t indic-sahayak .

# Run the container
docker run -p 8501:8501 -e HUGGINGFACE_API_KEY=your_key indic-sahayak

# Or use docker-compose
docker-compose up -d
```

## Cloud Platforms

### Google Cloud Platform

#### App Engine
```yaml
# app.yaml
runtime: python39

env_variables:
  HUGGINGFACE_API_KEY: "your_api_key"
  DIFY_API_KEY: "your_dify_key"

handlers:
- url: /.*
  script: auto
```

#### Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT-ID/indic-sahayak
gcloud run deploy --image gcr.io/PROJECT-ID/indic-sahayak --platform managed
```

### AWS

#### Elastic Beanstalk
```yaml
# .ebextensions/python.config
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: chatbot/indic_sahayak.py
  aws:elasticbeanstalk:application:environment:
    HUGGINGFACE_API_KEY: "your_api_key"
```

#### Lambda (with Serverless)
```yaml
# serverless.yml
service: indic-sahayak

provider:
  name: aws
  runtime: python3.9
  environment:
    HUGGINGFACE_API_KEY: ${env:HUGGINGFACE_API_KEY}

functions:
  app:
    handler: chatbot/indic_sahayak.handler
    events:
      - http:
          path: /
          method: any
```

### Azure

#### Container Instances
```bash
# Build and push to Azure Container Registry
az acr build --registry myregistry --image indic-sahayak .

# Deploy to Container Instances
az container create \
  --resource-group myResourceGroup \
  --name indic-sahayak \
  --image myregistry.azurecr.io/indic-sahayak \
  --ports 8501 \
  --environment-variables HUGGINGFACE_API_KEY=your_key
```

## Self-Hosting

### VPS Deployment

#### Using Nginx as Reverse Proxy
```nginx
# /etc/nginx/sites-available/indic-sahayak
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

#### Systemd Service
```ini
# /etc/systemd/system/indic-sahayak.service
[Unit]
Description=IndicSahayak AI Assistant
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/indic-sahayak
Environment=PATH=/opt/indic-sahayak/venv/bin
ExecStart=/opt/indic-sahayak/venv/bin/streamlit run chatbot/indic_sahayak.py --server.port=8501
Restart=always

[Install]
WantedBy=multi-user.target
```

### Raspberry Pi

#### Setup Script
```bash
#!/bin/bash
# setup-raspberry-pi.sh

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv git -y

# Clone repository
git clone https://github.com/yourusername/indic-sahayak.git
cd indic-sahayak

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r chatbot/requirements.txt

# Create systemd service
sudo cp scripts/indic-sahayak.service /etc/systemd/system/
sudo systemctl enable indic-sahayak
sudo systemctl start indic-sahayak
```

## Environment Variables

### Required
- `HUGGINGFACE_API_KEY`: Your Hugging Face API key for model access

### Optional
- `DIFY_API_KEY`: Your Dify.ai API key
- `STREAMLIT_SERVER_PORT`: Port for Streamlit server (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Server address (default: localhost)
- `LOG_LEVEL`: Logging level (default: INFO)

## Monitoring and Maintenance

### Health Checks
```python
# health_check.py
import requests
import sys

def check_health():
    try:
        response = requests.get("http://localhost:8501/_stcore/health", timeout=5)
        if response.status_code == 200:
            print("✅ Service is healthy")
            return True
        else:
            print("❌ Service is unhealthy")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    sys.exit(0 if check_health() else 1)
```

### Logging Configuration
```python
# logging_config.py
import logging
import os

def setup_logging():
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('indic_sahayak.log'),
            logging.StreamHandler()
        ]
    )
```

## Security Considerations

### API Key Management
- Use environment variables for API keys
- Never commit API keys to version control
- Rotate API keys regularly
- Use least-privilege access

### Network Security
- Use HTTPS in production
- Implement rate limiting
- Set up proper firewall rules
- Use reverse proxy for additional security

### Data Privacy
- Implement data retention policies
- Encrypt sensitive data
- Follow GDPR/privacy regulations
- Regular security audits

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find process using port 8501
   lsof -i :8501
   # Kill the process
   kill -9 <PID>
   ```

2. **API Key Issues**
   ```bash
   # Check environment variables
   echo $HUGGINGFACE_API_KEY
   # Test API connection
   python -c "import requests; print(requests.get('https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium', headers={'Authorization': f'Bearer {os.getenv(\"HUGGINGFACE_API_KEY\")}'}).status_code)"
   ```

3. **Memory Issues**
   ```bash
   # Monitor memory usage
   htop
   # Increase swap if needed
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

### Performance Optimization

1. **Caching**
   - Implement response caching
   - Use Redis for session storage
   - Cache model responses

2. **Load Balancing**
   - Use multiple instances
   - Implement health checks
   - Use CDN for static assets

3. **Database Optimization**
   - Use connection pooling
   - Implement query optimization
   - Regular maintenance

## Support

For deployment issues:
- 📧 Email: support@indicsahayak.ai
- 💬 Discord: [Join our community](https://discord.gg/indicsahayak)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/indic-sahayak/issues)
- 📖 Documentation: [Wiki](https://github.com/yourusername/indic-sahayak/wiki)
