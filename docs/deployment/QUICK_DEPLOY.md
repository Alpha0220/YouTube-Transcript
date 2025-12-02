# ⚡ Quick Deploy Guide - YouTube Transcript API

## 🎯 Frontend ที่ Vercel (ฟรี)

### ✅ ได้! Vercel รองรับ React + Vite อย่างสมบูรณ์

### ขั้นตอน:

1. **Push code ไป GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push
   ```

2. **ไปที่ Vercel**
   - เปิด https://vercel.com
   - Sign up/Login ด้วย GitHub
   - คลิก "Add New Project"
   - เลือก repository

3. **ตั้งค่า Project**
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build` (default)
   - **Output Directory:** `dist` (default)

4. **เพิ่ม Environment Variable**
   - `VITE_API_URL` = URL ของ backend
     - เช่น: `https://your-backend.onrender.com`
     - หรือ: `https://your-backend.railway.app`

5. **Deploy!**
   - คลิก "Deploy"
   - รอสักครู่
   - ได้ URL: `https://your-project.vercel.app`

---

## 🖥️ Backend ที่ Render (ฟรี)

### ขั้นตอน:

1. **Push code ไป GitHub**

2. **ไปที่ Render**
   - เปิด https://render.com
   - Sign up/Login ด้วย GitHub
   - คลิก "New +" → "Web Service"
   - Connect repository

3. **ตั้งค่า Service**
   - **Name:** youtube-transcript-api
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory:** `backend`

4. **Deploy!**
   - คลิก "Create Web Service"
   - รอ build และ deploy
   - ได้ URL: `https://your-backend.onrender.com`

5. **อัปเดต Frontend**
   - ไปที่ Vercel Dashboard
   - เพิ่ม/แก้ไข Environment Variable:
     - `VITE_API_URL` = `https://your-backend.onrender.com`
   - Redeploy

---

## 🚀 Backend ที่ Railway (ฟรี $5/เดือน)

### ขั้นตอน:

1. **Push code ไป GitHub**

2. **ไปที่ Railway**
   - เปิด https://railway.app
   - Sign up/Login ด้วย GitHub
   - คลิก "New Project"
   - เลือก "Deploy from GitHub repo"

3. **ตั้งค่า**
   - เลือก repository
   - Railway จะ detect Python อัตโนมัติ
   - ตั้งค่า:
     - **Root Directory:** `backend`
     - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Deploy!**
   - Railway จะ deploy อัตโนมัติ
   - ได้ URL: `https://your-backend.railway.app`

---

## 📋 สรุป Platform ที่แนะนำ

### Frontend
| Platform | ฟรี | ง่าย | แนะนำ |
|----------|-----|------|-------|
| **Vercel** | ✅ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Netlify | ✅ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| GitHub Pages | ✅ | ⭐⭐⭐ | ⭐⭐⭐ |

### Backend
| Platform | ฟรี | ง่าย | แนะนำ |
|----------|-----|------|-------|
| **Render** | ✅ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Railway** | ✅ ($5/เดือน) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Fly.io | ✅ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Heroku | ❌ | ⭐⭐⭐⭐ | ⭐⭐ |

---

## 🔧 Configuration ที่ต้องทำ

### 1. Frontend (`frontend/src/App.jsx`)
✅ **ทำแล้ว!** - ใช้ `import.meta.env.VITE_API_URL`

### 2. Backend CORS (`backend/main.py`)
✅ **ทำแล้ว!** - รองรับ environment variable `ALLOWED_ORIGINS`

### 3. Environment Variables

**Vercel (Frontend):**
```
VITE_API_URL=https://your-backend.onrender.com
```

**Render/Railway (Backend):**
```
ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
```

---

## ✅ Checklist

### Frontend (Vercel)
- [x] สร้าง `vercel.json`
- [x] อัปเดต `App.jsx` ให้ใช้ environment variable
- [ ] Push code ไป GitHub
- [ ] Connect repository ใน Vercel
- [ ] ตั้งค่า `VITE_API_URL`
- [ ] Deploy

### Backend (Render/Railway)
- [x] สร้าง `render.yaml` / `Procfile`
- [x] อัปเดต CORS
- [ ] Push code ไป GitHub
- [ ] Connect repository
- [ ] ตั้งค่า `ALLOWED_ORIGINS` (ถ้าต้องการ)
- [ ] Deploy

---

## 🎉 พร้อม Deploy!

**Frontend:** https://vercel.com  
**Backend:** https://render.com หรือ https://railway.app

**อ่านรายละเอียดเพิ่มเติม:** `DEPLOYMENT.md`

