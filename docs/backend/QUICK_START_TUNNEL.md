# 🚀 Quick Start: Expose Backend ให้ Frontend บน Vercel

## วิธีที่ 1: Cloudflare Tunnel (แนะนำ - ฟรี)

```bash
# 1. ติดตั้ง cloudflared (ครั้งเดียว)
# Linux:
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# macOS:
brew install cloudflare/cloudflare/cloudflared

# 2. รัน backend พร้อม tunnel
cd backend
./start_with_cloudflare.sh

# หรือใช้ Python script:
python start_tunnel.py --tunnel cloudflare
```

**คัดลอก URL ที่ได้** และตั้งค่าใน Vercel:
- Environment Variable: `NEXT_PUBLIC_BACKEND_URL=https://xxx.trycloudflare.com`

---

## วิธีที่ 2: ngrok

```bash
# 1. สมัครบัญชีที่ https://dashboard.ngrok.com (ฟรี)
# 2. ติดตั้ง ngrok
# Linux:
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok

# macOS:
brew install ngrok/ngrok/ngrok

# 3. ตั้งค่า authtoken
ngrok config add-authtoken YOUR_TOKEN

# 4. รัน backend พร้อม tunnel
cd backend
./start_with_ngrok.sh

# หรือใช้ Python script:
python start_tunnel.py --tunnel ngrok
```

**คัดลอก URL ที่ได้** และตั้งค่าใน Vercel

---

## วิธีที่ 3: Python Script (ง่ายที่สุด)

```bash
cd backend
python start_tunnel.py --tunnel cloudflare  # หรือ ngrok
```

---

## ⚙️ ตั้งค่าใน Vercel

1. ไปที่ Vercel Dashboard → Project → Settings → Environment Variables
2. เพิ่ม:
   ```
   NEXT_PUBLIC_BACKEND_URL=https://your-tunnel-url.com
   ```
3. Redeploy frontend

---

## ⚠️ หมายเหตุ

- URL จะเปลี่ยนทุกครั้งที่รันใหม่ (ถ้าใช้ free plan)
- ต้องอัพเดท `NEXT_PUBLIC_BACKEND_URL` ใน Vercel ทุกครั้งที่ URL เปลี่ยน
- สำหรับ URL คงที่ ดูที่ `TUNNEL_SETUP.md`

---

## 📚 ดูรายละเอียดเพิ่มเติม

ดูที่ `TUNNEL_SETUP.md` สำหรับคู่มือแบบละเอียด

