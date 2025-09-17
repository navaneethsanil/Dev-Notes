# 1. Launch an EC2 Instance
'''* Log into the AWS Console → EC2 → Launch Instance.
* Choose an OS (Ubuntu 22.04 LTS is a safe bet).
* Pick an instance type (t2.micro is free-tier).
* Configure security group:
    * Allow SSH (port 22) from your IP.
    * Allow HTTP (port 80).
    * Allow HTTPS (port 443) if you plan on SSL.
    * If you want to test directly with FastAPI/Uvicorn, allow custom TCP port 8000.
* Launch and download the key pair (.pem file).'''

# 2. SSH Into the Instance
```bash
ssh -i your-key.pem ubuntu@your-ec2-public-dns
```

# 3. Install Dependencies
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv git -y
```

# 4. Clone Your App
```bash
git clone https://github.com/your-username/your-fastapi-app.git
cd your-fastapi-app
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

# 5. Run With Uvicorn (quick test)
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
'''Visit http://<ec2-public-dns>:8000/docs to confirm it’s alive.
(Only works if port 8000 is open in your security group.)'''

# 6. Production Setup with Gunicorn + Uvicorn Workers
# Install:
```bash
pip install gunicorn uvicorn
```

# Start
```bash
gunicorn -k uvicorn.workers.UvicornWorker app.main:app -b 0.0.0.0:8000
```

# 7. Use Systemd to Keep It Running
# Create a service file:
```bash
sudo nano /etc/systemd/system/fastapi.service
```

'''Example content:
[Unit]
Description=FastAPI app
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/your-fastapi-app
ExecStart=/home/ubuntu/your-fastapi-app/venv/bin/gunicorn -k uvicorn.workers.UvicornWorker app.main:app -b 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
'''

# Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable fastapi
sudo systemctl start fastapi
```

# 8. Set Up a Reverse Proxy (Nginx)
```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/fastapi
```
# Config:
'''
server {
    listen 80;
    server_name your-domain-or-ec2-public-dns;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
'''
# Enable:
```bash
sudo ln -s /etc/nginx/sites-available/fastapi /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

# Now your app is available on port 80 (no need for :8000).

# 9. (Optional) SSL with Let’s Encrypt

# If you have a domain pointing to the EC2 instance:
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
```

# That’s the clean baseline: EC2 → Gunicorn/Uvicorn → Systemd → Nginx → (Optional) SSL.
# It scales decently, and you can later add load balancers, autoscaling groups, or Docker if you want to get fancy.




