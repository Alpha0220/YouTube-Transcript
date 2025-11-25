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

## 🖥️ Deploy Backend ที่ Render

### ขั้นตอนที่ 1: เตรียมไฟล์

สร้างไฟล์ `render.yaml` ในโฟลเดอร์ `backend/`:

```yaml
services:
  - type: web
    name: youtube-transcript-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

### ขั้นตอนที่ 2: Deploy ที่ Render

1. ไปที่ https://render.com
2. Sign up/Login ด้วย GitHub
3. คลิก "New +" → "Web Service"
4. Connect repository
5. ตั้งค่า:
   - **Name:** youtube-transcript-api
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory:** `backend`
6. คลิก "Create Web Service"

### ขั้นตอนที่ 3: ตั้งค่า CORS

แก้ไข `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend.vercel.app"  # เพิ่ม Vercel URL
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)
```

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
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

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

