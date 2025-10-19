# 🚀 Deploying FastAPI on AWS EC2

This guide walks you through hosting a **FastAPI** application on an **AWS EC2 instance** in production using **Gunicorn + Uvicorn**, **Systemd**, and **Nginx**.

---

## 1. Launch an EC2 Instance
- Log into the **AWS Console → EC2 → Launch Instance**.
- Choose **Ubuntu 22.04 LTS** (recommended).
- Pick an instance type (e.g., `t2.micro` for free-tier).
- Configure the **security group**:
  - Allow **SSH (22)** from your IP.
  - Allow **HTTP (80)**.
  - Allow **HTTPS (443)** if using SSL.
  - (Optional) Allow **custom TCP 8000** for direct FastAPI testing.
- Launch and download the **key pair (`.pem` file)**.

---

## 2. SSH Into the Instance
```bash
ssh -i your-key.pem ubuntu@your-ec2-public-dns
```

---

## 3. Install Dependencies
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv git -y
```

---

## 4. Clone Your App
```bash
git clone https://github.com/your-username/your-fastapi-app.git
cd your-fastapi-app

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

---

## 5. Run With Uvicorn (Quick Test)
*Before starting the server, ensure your environment variables are properly configured in a .env file. You can create or edit it using: nano .env)*
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Visit:  
`http://<ec2-public-dns>:8000/docs` to confirm it works.  
*(Ensure port `8000` is open in your security group.)*

---

## 6. Production Setup With Gunicorn + Uvicorn Workers

### Install
```bash
pip install gunicorn uvicorn
```

### Start
```bash
gunicorn -k uvicorn.workers.UvicornWorker app.main:app -b 0.0.0.0:8000
```

---

## 7. Keep App Running With Systemd

### Create a service file
```bash
sudo nano /etc/systemd/system/fastapi.service
```

**Example content:**
```ini
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
```

### Enable and start
```bash
sudo systemctl daemon-reload
sudo systemctl enable fastapi
sudo systemctl start fastapi
```

---

## 8. Set Up Nginx Reverse Proxy
```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/fastapi
```

**Config:**
```nginx
server {
    listen 80;
    server_name your-domain-or-ec2-public-dns;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/fastapi /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

Now your app is live at `http://<ec2-public-dns>` (no `:8000` needed).

---

## 9. (Optional) Enable SSL with Let’s Encrypt
If you have a domain pointing to your EC2 instance:
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
```

---

## ✅ Architecture
```
EC2 → Gunicorn/Uvicorn → Systemd → Nginx → (Optional) SSL
```

This setup is **production-ready** and can later scale with **load balancers, auto-scaling groups, or Docker/Kubernetes** if needed.
