# 🎬 YouTube Transcript API - Backend & Frontend Project

โปรเจกต์นี้ประกอบด้วย Backend Service (FastAPI) และ Frontend (React) สำหรับดึง transcript จาก YouTube และแปลงเป็นไฟล์ต่างๆ

## 📋 สารบัญ

1. [Tech Stack](#tech-stack)
2. [โครงสร้างโปรเจกต์](#โครงสร้างโปรเจกต์)
3. [การติดตั้งและใช้งาน](#การติดตั้งและใช้งาน)
4. [API Documentation](#api-documentation)
5. [Frontend Features](#frontend-features)

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework สำหรับ Python
- **Uvicorn** - ASGI server สำหรับรัน FastAPI
- **youtube-transcript-api** - Library สำหรับดึง transcript จาก YouTube
- **reportlab** - สร้างไฟล์ PDF
- **python-docx** - สร้างไฟล์ DOCX
- **Pydantic** - Data validation

### Frontend
- **React 18** - UI library
- **Vite** - Build tool และ dev server
- **Axios** - HTTP client สำหรับเรียก API
- **CSS3** - Styling (ไม่มี CSS framework)

---

## 📁 โครงสร้างโปรเจกต์

```
youtupe-transcrtip/
├── backend/
│   ├── main.py                    # FastAPI application
│   ├── requirements.txt            # Python dependencies
│   └── services/
│       ├── __init__.py
│       ├── transcript_service.py   # Service สำหรับดึง transcript
│       └── file_converter.py      # Service สำหรับแปลงไฟล์
│
├── frontend/
│   ├── package.json                # Node.js dependencies
│   ├── vite.config.js              # Vite configuration
│   ├── index.html
│   └── src/
│       ├── main.jsx                # React entry point
│       ├── App.jsx                 # Main component
│       ├── App.css                 # Styles
│       └── index.css               # Global styles
│
└── README_BACKEND_FRONTEND.md      # คู่มือนี้
```

---

## 🚀 การติดตั้งและใช้งาน

### ขั้นตอนที่ 1: ติดตั้ง Backend

```bash
# เข้าไปในโฟลเดอร์ backend
cd backend

# สร้าง virtual environment (แนะนำ)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# หรือ
venv\Scripts\activate     # Windows

# ติดตั้ง dependencies
pip install -r requirements.txt
```

### ขั้นตอนที่ 2: รัน Backend Server

```bash
# รัน server
python main.py

# หรือใช้ uvicorn โดยตรง
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend จะรันที่: **http://localhost:8000**

API Documentation (Swagger UI): **http://localhost:8000/docs**

### ขั้นตอนที่ 3: ติดตั้ง Frontend

```bash
# เข้าไปในโฟลเดอร์ frontend
cd frontend

# ติดตั้ง dependencies
npm install
```

### ขั้นตอนที่ 4: รัน Frontend

```bash
# รัน development server
npm run dev
```

Frontend จะรันที่: **http://localhost:3000**

### ขั้นตอนที่ 5: Build Frontend สำหรับ Production

```bash
npm run build
```

ไฟล์ที่ build จะอยู่ในโฟลเดอร์ `dist/`

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. GET `/`
ข้อมูล API

**Response:**
```json
{
  "message": "YouTube Transcript API Backend",
  "version": "1.0.0",
  "endpoints": {...}
}
```

#### 2. GET `/api/health`
Health check

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00"
}
```

#### 3. POST `/api/transcripts/list`
ดูรายการ transcript ที่มีให้

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response:**
```json
{
  "success": true,
  "video_id": "VIDEO_ID",
  "transcripts": [
    {
      "language": "English",
      "language_code": "en",
      "is_generated": false,
      "is_translatable": true,
      "translation_languages": ["th", "zh", ...]
    }
  ]
}
```

#### 4. POST `/api/transcripts/preview`
Preview transcript (ส่งกลับเป็น JSON)

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "languages": ["en"],
  "preserve_formatting": false
}
```

**Response:**
```json
{
  "success": true,
  "video_id": "VIDEO_ID",
  "language": "English",
  "language_code": "en",
  "is_generated": false,
  "total_snippets": 100,
  "snippets": [
    {
      "text": "Hello world",
      "start": 0.0,
      "duration": 2.5
    }
  ]
}
```

#### 5. POST `/api/transcripts/download`
ดาวน์โหลด transcript เป็นไฟล์

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "languages": ["en", "th"],
  "preserve_formatting": false,
  "file_format": "pdf",
  "include_timestamps": true
}
```

**Response:**
- File download (binary)
- Content-Type ตาม file_format:
  - `txt`: `text/plain`
  - `pdf`: `application/pdf`
  - `docx`: `application/vnd.openxmlformats-officedocument.wordprocessingml.document`

**Parameters:**
- `url` (required): YouTube URL หรือ Video ID
- `languages` (optional): รายการภาษา (default: `["en"]`)
- `preserve_formatting` (optional): เก็บ HTML formatting (default: `false`)
- `file_format` (optional): `txt`, `pdf`, หรือ `docx` (default: `txt`)
- `include_timestamps` (optional): รวม timestamps (default: `true`)

---

## 🎨 Frontend Features

### ฟีเจอร์หลัก

1. **กรอก YouTube URL หรือ Video ID**
   - รองรับ URL แบบเต็มและ Short URL
   - รองรับ Video ID โดยตรง

2. **เลือกภาษา**
   - เลือกได้หลายภาษา
   - ระบบจะลองภาษาแรกก่อน ถ้าไม่มีจะใช้ภาษาถัดไป

3. **เลือกรูปแบบไฟล์**
   - TXT (Text File)
   - PDF (Portable Document Format)
   - DOCX (Microsoft Word)

4. **Options เพิ่มเติม**
   - รวม Timestamps
   - เก็บ HTML Formatting

5. **ฟีเจอร์พิเศษ**
   - ดูรายการ Transcript ที่มีให้
   - Preview Transcript ก่อนดาวน์โหลด
   - Download ไฟล์

### UI/UX Features

- Responsive Design (รองรับ mobile)
- Loading states
- Error handling
- Success messages
- Modern gradient design

---

## 🔧 Configuration

### Backend Port
แก้ไขใน `backend/main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Frontend Port
แก้ไขใน `frontend/vite.config.js`:
```javascript
server: {
  port: 3000,
  ...
}
```

### CORS Settings
แก้ไขใน `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    ...
)
```

---

## 🐛 Troubleshooting

### Backend ไม่สามารถรันได้

**ปัญหา:** `ModuleNotFoundError`

**วิธีแก้:**
```bash
# ตรวจสอบว่าเปิดใช้งาน virtual environment แล้ว
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# ติดตั้ง dependencies อีกครั้ง
pip install -r requirements.txt
```

### Frontend ไม่สามารถเรียก API ได้

**ปัญหา:** CORS error

**วิธีแก้:**
- ตรวจสอบว่า backend รันอยู่ที่ port 8000
- ตรวจสอบ CORS settings ใน `backend/main.py`
- ตรวจสอบว่า frontend เรียก API ที่ URL ถูกต้อง

### ไม่สามารถดาวน์โหลดไฟล์ได้

**ปัญหา:** ไฟล์ไม่ถูกสร้างหรือไม่ถูกส่งกลับ

**วิธีแก้:**
- ตรวจสอบ logs ของ backend
- ตรวจสอบว่า video มี transcript หรือไม่
- ลองใช้ endpoint `/api/transcripts/list` เพื่อดู transcript ที่มีให้

---

## 📝 ตัวอย่างการใช้งาน

### ตัวอย่างที่ 1: ดาวน์โหลด Transcript เป็น PDF

1. เปิด Frontend ที่ http://localhost:3000
2. กรอก YouTube URL
3. เลือกภาษา (เช่น English)
4. เลือกรูปแบบไฟล์: PDF
5. คลิก "ดาวน์โหลด"

### ตัวอย่างที่ 2: ใช้ API โดยตรง

```bash
# ดูรายการ transcript
curl -X POST http://localhost:8000/api/transcripts/list \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=VIDEO_ID"}'

# ดาวน์โหลดเป็น PDF
curl -X POST http://localhost:8000/api/transcripts/download \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "languages": ["en"],
    "file_format": "pdf"
  }' \
  --output transcript.pdf
```

---

## 🚀 Deployment

### Backend (Production)

```bash
# Build
cd backend
pip install -r requirements.txt

# Run with gunicorn (recommended)
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend (Production)

```bash
# Build
cd frontend
npm run build

# Serve static files (ใช้ nginx หรือ serve)
npm install -g serve
serve -s dist -l 3000
```

---

## 📚 เอกสารเพิ่มเติม

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [youtube-transcript-api Documentation](https://github.com/jdepoix/youtube-transcript-api)

---

## ✅ Checklist

- [x] Backend API พร้อมใช้งาน
- [x] รองรับการแปลงไฟล์เป็น TXT, PDF, DOCX
- [x] Frontend UI สมบูรณ์
- [x] Error handling
- [x] CORS configuration
- [x] API documentation

---

**ขอให้สนุกกับการใช้งาน! 🎉**

