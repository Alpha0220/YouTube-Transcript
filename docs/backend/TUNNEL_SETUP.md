# 🌐 คู่มือการ Setup Tunnel สำหรับ Expose Backend ให้ Frontend บน Vercel

คู่มือนี้จะช่วยให้คุณ expose backend ที่รันบนเครื่อง local ให้ frontend บน Vercel สามารถเข้าถึงได้

## 📋 วิธีที่แนะนำ

### วิธีที่ 1: Cloudflare Tunnel (แนะนำ - ฟรีและเสถียร)

#### ขั้นตอนการติดตั้ง:

1. **ติดตั้ง cloudflared:**
   ```bash
   # Linux
   wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
   sudo dpkg -i cloudflared-linux-amd64.deb
   
   # macOS
   brew install cloudflare/cloudflare/cloudflared
   
   # หรือดาวน์โหลดจาก: https://github.com/cloudflare/cloudflared/releases
   ```

2. **รัน backend พร้อม tunnel:**
   ```bash
   cd backend
   chmod +x start_with_cloudflare.sh
   ./start_with_cloudflare.sh
   ```

3. **คัดลอก URL ที่ได้** (จะแสดงใน terminal) และใช้เป็น `BACKEND_URL` ใน frontend

#### ข้อดี:
- ✅ ฟรี 100%
- ✅ ไม่ต้องสมัครบัญชี (สำหรับ quick tunnel)
- ✅ ใช้งานง่าย
- ✅ เสถียร

#### ข้อเสีย:
- ⚠️ URL จะเปลี่ยนทุกครั้งที่รันใหม่ (ถ้าใช้ quick tunnel)
- ⚠️ ถ้าต้องการ URL คงที่ ต้อง setup named tunnel (ฟรีเหมือนกัน)

---

### วิธีที่ 2: ngrok (ง่ายและเร็ว)

#### ขั้นตอนการติดตั้ง:

1. **สมัครบัญชี ngrok (ฟรี):**
   - ไปที่ https://dashboard.ngrok.com
   - สมัครบัญชีฟรี

2. **ติดตั้ง ngrok:**
   ```bash
   # Linux
   curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
   echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
   sudo apt update && sudo apt install ngrok
   
   # macOS
   brew install ngrok/ngrok/ngrok
   ```

3. **ตั้งค่า authtoken:**
   ```bash
   ngrok config add-authtoken YOUR_AUTHTOKEN
   ```
   (หา authtoken จาก https://dashboard.ngrok.com/get-started/your-authtoken)

4. **รัน backend พร้อม tunnel:**
   ```bash
   cd backend
   chmod +x start_with_ngrok.sh
   ./start_with_ngrok.sh
   ```

5. **คัดลอก URL ที่ได้** และใช้เป็น `BACKEND_URL` ใน frontend

#### ข้อดี:
- ✅ ใช้งานง่าย
- ✅ มี dashboard สำหรับดู traffic
- ✅ URL คงที่ (ถ้าใช้ paid plan)

#### ข้อเสีย:
- ⚠️ ต้องสมัครบัญชี
- ⚠️ Free plan: URL เปลี่ยนทุกครั้ง, มี session time limit

---

## 🔧 การตั้งค่า Frontend

หลังจากได้ tunnel URL แล้ว ให้ตั้งค่าใน frontend:

### สำหรับ Vercel:

1. **ตั้งค่า Environment Variable ใน Vercel:**
   - ไปที่ Vercel Dashboard → Project → Settings → Environment Variables
   - เพิ่ม:
     ```
     NEXT_PUBLIC_BACKEND_URL=https://your-tunnel-url.com
     ```
   - หรือถ้าใช้ React/Vite:
     ```
     VITE_BACKEND_URL=https://your-tunnel-url.com
     ```

2. **อัพเดท CORS ใน Backend:**
   - แก้ไขไฟล์ `.env`:
     ```bash
     ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-tunnel-url.com
     ```
   - หรือถ้าใช้ tunnel URL:
     ```bash
     ALLOWED_ORIGINS=*
     ```

### สำหรับ Local Development:

ในไฟล์ `.env.local` หรือ `.env` ของ frontend:
```bash
BACKEND_URL=https://your-tunnel-url.com
```

---

## 🎯 ตัวอย่างการใช้งาน

### 1. เริ่ม Backend พร้อม Cloudflare Tunnel:
```bash
cd backend
./start_with_cloudflare.sh
```

Output จะเป็น:
```
🌐 Public URL: https://abc123.trycloudflare.com
```

### 2. ตั้งค่าใน Frontend:
```javascript
// ใน frontend code
const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://abc123.trycloudflare.com';

// เรียก API
fetch(`${BACKEND_URL}/api/transcripts/list`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ url: 'https://youtube.com/watch?v=...' })
});
```

### 3. Deploy Frontend บน Vercel:
- เพิ่ม Environment Variable: `NEXT_PUBLIC_BACKEND_URL=https://abc123.trycloudflare.com`
- Deploy

---

## ⚠️ ข้อควรระวัง

1. **URL จะเปลี่ยนทุกครั้งที่รันใหม่** (ถ้าใช้ quick tunnel/free ngrok)
   - ต้องอัพเดท `BACKEND_URL` ใน frontend ทุกครั้ง
   - หรือใช้ named tunnel/paid ngrok สำหรับ URL คงที่

2. **Security:**
   - Tunnel URL เป็น public - ใครก็เข้าถึงได้
   - ควรเพิ่ม authentication ถ้าต้องการความปลอดภัย

3. **Performance:**
   - Tunnel จะเพิ่ม latency เล็กน้อย
   - ควรใช้เฉพาะตอน development หรือ testing

4. **CORS:**
   - ตรวจสอบว่า backend ตั้งค่า CORS ถูกต้อง
   - ควรเพิ่ม tunnel URL และ Vercel URL ใน `ALLOWED_ORIGINS`

---

## 🚀 สำหรับ Production

สำหรับ production จริง ควร:
1. Deploy backend บน cloud service (Render, Railway, AWS, etc.)
2. ใช้ domain จริง
3. ตั้งค่า SSL certificate
4. ตั้งค่า CORS ให้เฉพาะ domain ที่ต้องการ

---

## 📞 Troubleshooting

### Tunnel ไม่ทำงาน:
- ตรวจสอบว่า backend รันอยู่: `curl http://localhost:8000/api/health`
- ตรวจสอบ log: `cat /tmp/cloudflared.log` หรือ `cat /tmp/ngrok.log`

### Frontend ไม่สามารถเรียก API ได้:
- ตรวจสอบ CORS settings ใน backend
- ตรวจสอบว่า tunnel URL ถูกต้อง
- ตรวจสอบ Network tab ใน browser console

### URL เปลี่ยนบ่อย:
- ใช้ Cloudflare Named Tunnel หรือ ngrok paid plan
- หรือใช้ script ที่ auto-update URL

---

## 📚 เอกสารเพิ่มเติม

- [Cloudflare Tunnel Docs](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)
- [ngrok Docs](https://ngrok.com/docs)
- [Vercel Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)

