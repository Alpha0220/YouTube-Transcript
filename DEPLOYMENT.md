# 🚀 คู่มือการ Deploy - YouTube Transcript API

## 📋 สารบัญ

1. [Backend Deployment Options](#backend-deployment-options)
2. [Frontend Deployment Options](#frontend-deployment-options)
3. [Deploy Frontend ที่ Vercel](#deploy-frontend-ที่-vercel)
4. [Deploy Backend ที่ Render/Railway](#deploy-backend-ที่-renderrailway)
5. [Configuration](#configuration)

---

## 🖥️ Backend Deployment Options

### 1. **Render** (แนะนำ - ฟรี)
- ✅ ฟรี tier พร้อมใช้งาน
- ✅ Auto-deploy จาก GitHub
- ✅ HTTPS อัตโนมัติ
- ✅ Environment variables

**URL:** https://render.com

### 2. **Railway**
- ✅ ฟรี $5 credit/เดือน
- ✅ Auto-deploy จาก GitHub
- ✅ ง่ายต่อการใช้งาน

**URL:** https://railway.app

### 3. **Fly.io**
- ✅ ฟรี tier
- ✅ Global edge deployment
- ✅ Docker-based

**URL:** https://fly.io

### 4. **Heroku**
- ⚠️ ไม่มีฟรี tier แล้ว (ต้องจ่าย)
- ✅ ง่ายต่อการใช้งาน

**URL:** https://heroku.com

### 5. **DigitalOcean App Platform**
- ⚠️ ต้องจ่าย (เริ่มต้น $5/เดือน)
- ✅ Stable และ reliable

**URL:** https://www.digitalocean.com/products/app-platform

### 6. **AWS/GCP/Azure**
- ⚠️ ซับซ้อนกว่า แต่ flexible
- ✅ สำหรับ production scale

---

## 🎨 Frontend Deployment Options

### 1. **Vercel** (แนะนำ - ฟรี)
- ✅ ฟรี tier พร้อมใช้งาน
- ✅ Auto-deploy จาก GitHub
- ✅ CDN global
- ✅ HTTPS อัตโนมัติ
- ✅ Perfect สำหรับ React/Vite

**URL:** https://vercel.com

### 2. **Netlify**
- ✅ ฟรี tier
- ✅ Auto-deploy จาก GitHub
- ✅ Form handling, Functions

**URL:** https://netlify.com

### 3. **GitHub Pages**
- ✅ ฟรี
- ✅ ง่าย
- ⚠️ ต้อง build เอง

**URL:** https://pages.github.com

### 4. **Cloudflare Pages**
- ✅ ฟรี
- ✅ Fast CDN
- ✅ Auto-deploy

**URL:** https://pages.cloudflare.com

---

## 🎯 Deploy Frontend ที่ Vercel

### ขั้นตอนที่ 1: เตรียมไฟล์

สร้างไฟล์ `vercel.json` ในโฟลเดอร์ `frontend/`:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "vite"
}
```

### ขั้นตอนที่ 2: อัปเดต Environment Variables

แก้ไข `frontend/src/App.jsx` ให้รองรับ environment variable:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
```

### ขั้นตอนที่ 3: Deploy ที่ Vercel

#### วิธีที่ 1: ผ่าน Vercel Dashboard

1. ไปที่ https://vercel.com
2. Sign up/Login ด้วย GitHub
3. คลิก "Add New Project"
4. Import repository จาก GitHub
5. ตั้งค่า:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Install Command:** `npm install`
6. เพิ่ม Environment Variable:
   - `VITE_API_URL` = URL ของ backend (เช่น `https://your-backend.onrender.com`)
7. คลิก "Deploy"

#### วิธีที่ 2: ผ่าน Vercel CLI

```bash
cd frontend
npm install -g vercel
vercel login
vercel
```

### ขั้นตอนที่ 4: ตั้งค่า Environment Variables

ใน Vercel Dashboard:
1. ไปที่ Project Settings
2. Environment Variables
3. เพิ่ม:
   - `VITE_API_URL` = `https://your-backend.onrender.com`

---

## 🖥️ Deploy Backend ที่ Render (คู่มือละเอียด)

### 📌 ภาพรวม

Render เป็น platform ที่ให้บริการฟรีสำหรับ deploy web services โดยมีคุณสมบัติ:
- ✅ Free tier พร้อมใช้งาน (มีข้อจำกัดบางอย่าง)
- ✅ Auto-deploy จาก GitHub (deploy อัตโนมัติเมื่อ push code)
- ✅ HTTPS อัตโนมัติ
- ✅ Environment variables management
- ✅ Logs และ monitoring
- ✅ Auto-sleep หลังจาก idle 15 นาที (free tier)

---

### 📋 ขั้นตอนที่ 1: เตรียมไฟล์ในโปรเจค

#### 1.1 ตรวจสอบไฟล์ `backend/render.yaml`

ไฟล์นี้ควรมีอยู่แล้วในโปรเจค และมีเนื้อหาดังนี้:

```yaml
services:
  - type: web
    name: youtube-transcript-api
    env: python
    buildCommand: pip install -r backend/requirements.txt
    startCommand: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

**คำอธิบาย:**
- `type: web` - บอกว่าเป็น web service
- `name` - ชื่อของ service
- `env: python` - ใช้ Python environment
- `buildCommand` - คำสั่งที่ใช้ติดตั้ง dependencies (ต้องระบุ path `backend/requirements.txt` เพราะ Render จะรันจาก root directory)
- `startCommand` - คำสั่งที่ใช้เริ่ม server (ต้อง `cd backend` ก่อนเพราะไฟล์ main.py อยู่ใน backend folder)
- `PYTHON_VERSION` - ระบุเวอร์ชัน Python ที่ต้องการ

#### 1.2 ตรวจสอบไฟล์ `backend/requirements.txt`

ไฟล์นี้ควรมี dependencies ทั้งหมดที่จำเป็น:

```
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
python-multipart>=0.0.6
youtube-transcript-api>=1.2.3
reportlab>=4.0.7
python-docx>=1.1.0
pydantic>=2.5.0
aiofiles>=23.2.1
```

#### 1.3 ตรวจสอบโครงสร้างไฟล์

ให้แน่ใจว่าโครงสร้างโปรเจคเป็นแบบนี้:

```
youtupe-transcrtip/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── render.yaml
│   └── services/
│       ├── transcript_service.py
│       └── file_converter.py
└── frontend/
    └── ...
```

#### 1.4 Commit และ Push ไป GitHub

```bash
# ตรวจสอบสถานะไฟล์
git status

# เพิ่มไฟล์ที่เปลี่ยนแปลง
git add backend/render.yaml
git add backend/requirements.txt

# Commit
git commit -m "Prepare for Render deployment"

# Push ไป GitHub
git push origin main
```

**สำคัญ:** ต้องแน่ใจว่าโค้ดทั้งหมดถูก push ไป GitHub แล้ว เพราะ Render จะ clone จาก GitHub

---

### 📋 ขั้นตอนที่ 2: สร้างบัญชี Render

#### 2.1 ไปที่เว็บไซต์ Render

เปิดเบราว์เซอร์และไปที่: **https://render.com**

#### 2.2 สมัครสมาชิก

1. คลิกปุ่ม **"Get Started for Free"** หรือ **"Sign Up"**
2. เลือก **"Sign up with GitHub"** (แนะนำเพราะจะเชื่อมต่อกับ GitHub repository ได้ง่าย)
3. อนุญาต Render เข้าถึง GitHub account ของคุณ
4. กรอกข้อมูลเพิ่มเติมถ้าจำเป็น

#### 2.3 ยืนยันอีเมล (ถ้าจำเป็น)

Render อาจส่งอีเมลยืนยันมาให้ คลิกลิงก์ในอีเมลเพื่อยืนยันบัญชี

---

### 📋 ขั้นตอนที่ 3: สร้าง Web Service ใหม่

#### 3.1 เข้าสู่ Dashboard

หลังจาก login แล้ว คุณจะเห็น Dashboard ของ Render

#### 3.2 สร้าง Web Service

1. คลิกปุ่ม **"New +"** ที่มุมบนขวา
2. เลือก **"Web Service"** จากเมนูที่ปรากฏ

#### 3.3 เชื่อมต่อ GitHub Repository

1. Render จะแสดงรายการ GitHub repositories ของคุณ
2. **ค้นหาและเลือก repository** ที่มีโค้ด backend ของคุณ (เช่น `YouTube-Transcript`)
3. คลิก **"Connect"** เพื่อเชื่อมต่อ

**หมายเหตุ:** ถ้าไม่เห็น repository ให้คลิก **"Configure account"** เพื่อให้สิทธิ์ Render เข้าถึง repositories

---

### 📋 ขั้นตอนที่ 4: ตั้งค่า Web Service

หลังจากเชื่อมต่อ repository แล้ว Render จะแสดงหน้าตั้งค่า:

#### 4.1 ตั้งค่าพื้นฐาน

**Name:**
- ใส่ชื่อ service เช่น `youtube-transcript-api`
- ชื่อนี้จะใช้เป็นส่วนหนึ่งของ URL (เช่น `youtube-transcript-api.onrender.com`)

**Region:**
- เลือก region ที่ใกล้ที่สุด (เช่น Singapore, Oregon)
- สำหรับประเทศไทย แนะนำ **Singapore** หรือ **Oregon**

**Branch:**
- เลือก branch ที่ต้องการ deploy (ปกติคือ `main` หรือ `master`)

**Root Directory:**
- **เว้นว่างไว้** หรือใส่ `backend` (แต่ใน render.yaml เราได้ตั้งค่า buildCommand ให้ใช้ path `backend/requirements.txt` แล้ว)

#### 4.2 ตั้งค่า Environment และ Runtime

**Environment:**
- เลือก **"Python 3"**

**Python Version:**
- เลือก **"3.11.0"** หรือเวอร์ชันที่ระบุใน render.yaml

#### 4.3 ตั้งค่า Build และ Start Commands

**Build Command:**
```
pip install -r backend/requirements.txt
```

**Start Command:**
```
cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

**คำอธิบาย:**
- `$PORT` เป็น environment variable ที่ Render จะกำหนดให้อัตโนมัติ
- ต้องใช้ `cd backend` เพราะไฟล์ `main.py` อยู่ใน backend folder

#### 4.4 ตั้งค่า Instance Type (Free Tier)

**Instance Type:**
- เลือก **"Free"** (มีข้อจำกัด: จะ sleep หลังจาก idle 15 นาที)

**Auto-Deploy:**
- เปิดใช้งาน **"Yes"** เพื่อให้ deploy อัตโนมัติเมื่อ push code ใหม่

---

### 📋 ขั้นตอนที่ 5: ตั้งค่า Environment Variables (ถ้าจำเป็น)

#### 5.1 เพิ่ม Environment Variables

ในส่วน **"Environment Variables"** คุณสามารถเพิ่มตัวแปรได้ เช่น:

**ALLOWED_ORIGINS:**
- Key: `ALLOWED_ORIGINS`
- Value: `http://localhost:3000,https://your-frontend.vercel.app`
- ใช้สำหรับตั้งค่า CORS

**FRONTEND_URL:**
- Key: `FRONTEND_URL`
- Value: `https://your-frontend.vercel.app`
- URL ของ frontend ที่จะเรียกใช้ API

**หมายเหตุ:** สำหรับโปรเจคนี้ อาจไม่จำเป็นต้องตั้งค่า environment variables เพิ่มเติม เพราะโค้ดรองรับ CORS แบบ wildcard (`*`) ในโหมด development

---

### 📋 ขั้นตอนที่ 6: Deploy Service

#### 6.1 เริ่ม Deploy

1. ตรวจสอบการตั้งค่าทั้งหมดอีกครั้ง
2. คลิกปุ่ม **"Create Web Service"** ที่ด้านล่าง

#### 6.2 รอ Build และ Deploy

Render จะเริ่มกระบวนการ:
1. **Cloning repository** - ดึงโค้ดจาก GitHub
2. **Installing dependencies** - รัน build command (`pip install -r backend/requirements.txt`)
3. **Starting service** - รัน start command (`uvicorn main:app ...`)

**เวลาในการ deploy:** ประมาณ 2-5 นาที (ขึ้นอยู่กับขนาดของ dependencies)

#### 6.3 ตรวจสอบ Logs

ขณะที่ deploy อยู่ คุณสามารถดู **Logs** ได้แบบ real-time:

1. คลิกแท็บ **"Logs"** ในหน้า service
2. ดู output จาก build และ start commands
3. ถ้ามี error จะแสดงใน logs

**ตัวอย่าง Logs ที่ควรเห็น:**
```
==> Cloning from https://github.com/your-username/YouTube-Transcript
==> Checking out commit abc123...
==> Installing Python version 3.11.0...
==> Running build command 'pip install -r backend/requirements.txt'...
Collecting fastapi>=0.104.1
...
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 ...
==> Starting service with 'cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT'
INFO:     Started server process [123]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:10000 (Press CTRL+C to quit)
```

---

### 📋 ขั้นตอนที่ 7: ตรวจสอบการ Deploy

#### 7.1 ตรวจสอบสถานะ

เมื่อ deploy สำเร็จ คุณจะเห็น:
- ✅ **Status:** "Live"
- ✅ **URL:** `https://youtube-transcript-api.onrender.com`

#### 7.2 ทดสอบ API

1. เปิด URL ที่ Render ให้มาในเบราว์เซอร์
2. เพิ่ม `/docs` ที่ท้าย URL เพื่อดู API documentation:
   ```
   https://youtube-transcript-api.onrender.com/docs
   ```
3. คุณควรเห็น Swagger UI ที่แสดง endpoints ทั้งหมด

#### 7.3 ทดสอบ Endpoint

ลองเรียกใช้ endpoint เพื่อทดสอบ:

**Health Check:**
```
GET https://youtube-transcript-api.onrender.com/
```

**API Documentation:**
```
GET https://youtube-transcript-api.onrender.com/docs
```

**Test Transcript Endpoint:**
```
POST https://youtube-transcript-api.onrender.com/api/transcript
Content-Type: application/json

{
  "video_id": "dQw4w9WgXcQ"
}
```

---

### 📋 ขั้นตอนที่ 8: ตั้งค่า CORS (ถ้ายังไม่ได้ตั้ง)

#### 8.1 ตรวจสอบไฟล์ `backend/main.py`

เปิดไฟล์ `backend/main.py` และตรวจสอบส่วน CORS:

```python
# CORS middleware เพื่อให้ frontend เรียกใช้ได้
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
if allowed_origins == ["*"]:
    # Development mode - อนุญาตทุก origin
    cors_origins = ["*"]
else:
    # Production mode - อนุญาตเฉพาะ origins ที่ระบุ
    cors_origins = allowed_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)
```

#### 8.2 เพิ่ม Frontend URL (ถ้าต้องการจำกัด CORS)

ถ้าต้องการจำกัด CORS ให้เฉพาะ frontend URL ของคุณ:

1. ไปที่ Render Dashboard → Service → Environment
2. เพิ่ม Environment Variable:
   - Key: `ALLOWED_ORIGINS`
   - Value: `https://your-frontend.vercel.app,http://localhost:3000`
3. Save และรอให้ service restart อัตโนมัติ

---

### 📋 ขั้นตอนที่ 9: Auto-Deploy Setup

#### 9.1 ตรวจสอบ Auto-Deploy

Render จะ auto-deploy เมื่อ:
- ✅ Push code ใหม่ไปยัง branch ที่เชื่อมต่อ (เช่น `main`)
- ✅ Merge pull request
- ✅ Manual trigger จาก Dashboard

#### 9.2 ทดสอบ Auto-Deploy

1. แก้ไขโค้ดเล็กน้อย (เช่น เพิ่ม comment)
2. Commit และ push:
   ```bash
   git add .
   git commit -m "Test auto-deploy"
   git push origin main
   ```
3. กลับไปที่ Render Dashboard
4. คุณจะเห็น deployment ใหม่เริ่มขึ้นอัตโนมัติ

---

### 🐛 Troubleshooting (แก้ไขปัญหา)

#### ❌ ปัญหา: Build Failed - requirements.txt not found

**อาการ:**
```
ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'
```

**วิธีแก้:**
1. ตรวจสอบว่า `render.yaml` ใช้ `buildCommand: pip install -r backend/requirements.txt` (มี `backend/` นำหน้า)
2. ตรวจสอบว่าไฟล์ `backend/requirements.txt` มีอยู่จริงใน repository
3. Push ไฟล์ไป GitHub อีกครั้ง

#### ❌ ปัญหา: Module not found

**อาการ:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**วิธีแก้:**
1. ตรวจสอบว่า `requirements.txt` มี dependencies ทั้งหมด
2. ตรวจสอบ build logs ว่า dependencies ติดตั้งสำเร็จหรือไม่
3. ลองเพิ่ม `--upgrade` ใน build command:
   ```
   pip install --upgrade -r backend/requirements.txt
   ```

#### ❌ ปัญหา: Port already in use

**อาการ:**
```
ERROR: [Errno 98] Address already in use
```

**วิธีแก้:**
- ใช้ `$PORT` environment variable (Render จะกำหนดให้อัตโนมัติ)
- ตรวจสอบว่า start command ใช้ `--port $PORT`

#### ❌ ปัญหา: Service keeps crashing

**อาการ:**
- Service deploy สำเร็จแต่ crash ทันที
- Logs แสดง error

**วิธีแก้:**
1. ดู Logs ใน Render Dashboard
2. ตรวจสอบว่า:
   - `main.py` มีอยู่และถูกต้อง
   - Import statements ถูกต้อง
   - Dependencies ทั้งหมดติดตั้งแล้ว
3. ทดสอบรัน local ก่อน:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

#### ❌ ปัญหา: CORS Error

**อาการ:**
- Frontend ไม่สามารถเรียก API ได้
- Browser console แสดง CORS error

**วิธีแก้:**
1. ตรวจสอบ CORS settings ใน `main.py`
2. เพิ่ม frontend URL ใน `ALLOWED_ORIGINS` environment variable
3. หรือใช้ `*` สำหรับ development (ไม่แนะนำสำหรับ production)

#### ❌ ปัญหา: Service sleeps after 15 minutes (Free Tier)

**อาการ:**
- Service ไม่ตอบสนองหลังจาก idle 15 นาที
- Request แรกหลังจาก sleep จะช้ามาก (cold start)

**วิธีแก้:**
- **Free tier limitation** - ไม่สามารถแก้ไขได้
- ทางเลือก:
  1. ใช้ paid plan ($7/เดือน)
  2. ใช้ external service เพื่อ "ping" service ทุก 10 นาที (เช่น UptimeRobot)
  3. ยอมรับ cold start (request แรกจะช้า ~30 วินาที)

#### ❌ ปัญหา: YouTube Blocking IP (IP Blocked Error)

**อาการ:**
```
ERROR: Could not retrieve a transcript for the video!
YouTube is blocking requests from your IP.
This usually is due to cloud provider IPs being blocked.
```

**สาเหตุ:**
- YouTube บล็อก IPs จาก cloud providers (Render, AWS, GCP, Azure, etc.)
- เป็นปัญหาที่พบบ่อยเมื่อ deploy บน cloud platforms

**วิธีแก้ไข:**

**วิธีที่ 1: ใช้ Cookies (แนะนำ)**

1. **ได้ Cookies จาก Browser:**
   - เปิด YouTube ใน browser (Chrome/Firefox)
   - กด `F12` เพื่อเปิด Developer Tools
   - ไปที่แท็บ **Application** (Chrome) หรือ **Storage** (Firefox)
   - คลิก **Cookies** → `https://www.youtube.com`
   - คัดลอก cookies ที่สำคัญ (เช่น `VISITOR_INFO1_LIVE`, `LOGIN_INFO`, `PREF`)
   - หรือใช้ browser extension เช่น "Get cookies.txt LOCALLY"

2. **ตั้งค่า Environment Variable ใน Render:**
   - ไปที่ Render Dashboard → Service → Environment
   - เพิ่ม Environment Variable:
     - **Key:** `YOUTUBE_COOKIES`
     - **Value:** วาง cookies ที่คัดลอกมา (format: `VISITOR_INFO1_LIVE=xxx; LOGIN_INFO=yyy; PREF=zzz`)
   - Save และรอให้ service restart

3. **รูปแบบ Cookies:**
   ```
   VISITOR_INFO1_LIVE=xxx; LOGIN_INFO=yyy; PREF=zzz; YSC=aaa
   ```
   หรือเป็น JSON array:
   ```json
   [{"name": "VISITOR_INFO1_LIVE", "value": "xxx"}, {"name": "LOGIN_INFO", "value": "yyy"}]
   ```

**วิธีที่ 2: ใช้ Proxy Service**

1. ใช้ proxy service เช่น:
   - ScraperAPI
   - Bright Data
   - ProxyMesh

2. ตั้งค่า proxy ใน environment variable:
   ```
   HTTP_PROXY=http://proxy.example.com:8080
   HTTPS_PROXY=http://proxy.example.com:8080
   ```

**วิธีที่ 3: ลองใหม่ในภายหลัง**

- บางครั้ง YouTube อาจ unblock IP หลังจากผ่านไปสักครู่
- ลองรอ 1-2 ชั่วโมงแล้วลองใหม่

**วิธีที่ 4: ใช้ Residential Proxy**

- ใช้ residential proxy แทน datacenter proxy
- มีค่าใช้จ่าย แต่มีโอกาสถูก block น้อยกว่า

**หมายเหตุ:**
- Cookies จะหมดอายุ ต้องอัปเดตเป็นระยะ
- ใช้ cookies ของตัวเองเท่านั้น (ไม่ใช้ของคนอื่น)
- ถ้าใช้ cookies ของ account ที่ login แล้ว อาจช่วยได้มากกว่า

---

### 📝 Checklist การ Deploy

ใช้ checklist นี้เพื่อให้แน่ใจว่า deploy สำเร็จ:

- [ ] ไฟล์ `backend/render.yaml` มีอยู่และถูกต้อง
- [ ] ไฟล์ `backend/requirements.txt` มี dependencies ทั้งหมด
- [ ] โค้ดทั้งหมดถูก push ไป GitHub
- [ ] สร้างบัญชี Render และเชื่อมต่อ GitHub
- [ ] สร้าง Web Service ใหม่
- [ ] ตั้งค่า Build Command: `pip install -r backend/requirements.txt`
- [ ] ตั้งค่า Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] ตั้งค่า Python Version: `3.11.0`
- [ ] Deploy สำเร็จและ service เป็น "Live"
- [ ] ทดสอบ API ที่ `/docs` endpoint
- [ ] ตั้งค่า CORS (ถ้าจำเป็น)
- [ ] ทดสอบ auto-deploy โดย push code ใหม่

---

### 🔗 URLs หลัง Deploy

หลังจาก deploy สำเร็จ คุณจะได้:

**Backend URL:**
```
https://youtube-transcript-api.onrender.com
```

**API Documentation (Swagger UI):**
```
https://youtube-transcript-api.onrender.com/docs
```

**Alternative API Documentation (ReDoc):**
```
https://youtube-transcript-api.onrender.com/redoc
```

**Health Check:**
```
https://youtube-transcript-api.onrender.com/
```

---

### 💡 Tips และ Best Practices

1. **ใช้ Environment Variables** สำหรับ sensitive data (API keys, secrets)
2. **Monitor Logs** เป็นประจำเพื่อตรวจสอบ errors
3. **ตั้งค่า Auto-Deploy** เพื่อให้ deploy อัตโนมัติเมื่อ push code
4. **ทดสอบ Local ก่อน** deploy เพื่อลดโอกาสเกิด error
5. **ใช้ Git Tags** สำหรับ production deployments
6. **Backup Environment Variables** เก็บไว้ที่อื่นด้วย
7. **ตั้งค่า Alerts** (ถ้าใช้ paid plan) เพื่อรับแจ้งเตือนเมื่อ service down

---

### 📚 เอกสารเพิ่มเติม

- [Render Documentation](https://render.com/docs)
- [Render Python Guide](https://render.com/docs/python-version)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Render Pricing](https://render.com/pricing)

---

**🎉 พร้อม Deploy แล้ว! ขอให้โชคดีกับการ deploy! 🚀**

---

## 🔧 Configuration

### Frontend Configuration

#### 1. สร้างไฟล์ `.env.production` ใน `frontend/`:

```env
VITE_API_URL=https://your-backend.onrender.com
```

#### 2. อัปเดต `vite.config.js`:

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

#### 3. อัปเดต `App.jsx`:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
```

### Backend Configuration

#### 1. สร้างไฟล์ `Procfile` ใน `backend/` (สำหรับ Heroku/Railway):

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### 2. สร้างไฟล์ `runtime.txt` (ถ้าจำเป็น):

```
python-3.11.0
```

#### 3. อัปเดต CORS ใน `main.py`:

```python
# สำหรับ production
allowed_origins = [
    "http://localhost:3000",
    "https://your-frontend.vercel.app",
    os.getenv("FRONTEND_URL", "")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)
```

---

## 📝 ตัวอย่างไฟล์ที่ต้องสร้าง

### `frontend/vercel.json`

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### `backend/render.yaml`

```yaml
services:
  - type: web
    name: youtube-transcript-api
    env: python
    buildCommand: pip install -r backend/requirements.txt
    startCommand: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

**หมายเหตุ:** 
- `buildCommand` ต้องระบุ path `backend/requirements.txt` เพราะ Render จะรันจาก root directory
- `startCommand` ต้องมี `cd backend` เพราะไฟล์ `main.py` อยู่ใน backend folder

### `backend/Procfile`

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## ✅ Checklist การ Deploy

### Frontend (Vercel)
- [ ] สร้าง `vercel.json`
- [ ] อัปเดต `App.jsx` ให้ใช้ environment variable
- [ ] Push code ไป GitHub
- [ ] Connect repository ใน Vercel
- [ ] ตั้งค่า Environment Variable (`VITE_API_URL`)
- [ ] Deploy

### Backend (Render)
- [ ] สร้าง `render.yaml` หรือใช้ Dashboard
- [ ] อัปเดต CORS ให้รองรับ frontend URL
- [ ] Push code ไป GitHub
- [ ] Connect repository ใน Render
- [ ] ตั้งค่า Build/Start commands
- [ ] Deploy

---

## 🔗 URLs หลัง Deploy

### Frontend
```
https://your-project.vercel.app
```

### Backend
```
https://your-backend.onrender.com
```

### API Documentation
```
https://your-backend.onrender.com/docs
```

---

## 🐛 Troubleshooting

### Frontend ไม่สามารถเรียก Backend ได้

**ปัญหา:** CORS error

**วิธีแก้:**
1. ตรวจสอบว่า backend CORS อนุญาต frontend URL แล้ว
2. ตรวจสอบ Environment Variable `VITE_API_URL`
3. ตรวจสอบ Network tab ใน browser console

### Backend ไม่สามารถรันได้

**ปัญหา:** Port error

**วิธีแก้:**
- ใช้ `$PORT` environment variable (Render/Railway)
- หรือใช้ `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Build Failed

**ปัญหา:** Dependencies ไม่พบ

**วิธีแก้:**
- ตรวจสอบ `requirements.txt` (backend)
- ตรวจสอบ `package.json` (frontend)
- ตรวจสอบ build logs

---

## 📚 เอกสารเพิ่มเติม

- [Vercel Documentation](https://vercel.com/docs)
- [Render Documentation](https://render.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

**พร้อม Deploy แล้ว! 🚀**

