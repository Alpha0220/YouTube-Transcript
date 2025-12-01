# 📮 คู่มือการใช้งาน Postman Collection

## 📥 วิธี Import Collection

### วิธีที่ 1: Import จากไฟล์

1. เปิด Postman
2. คลิก **"Import"** ที่มุมบนซ้าย
3. เลือก **"Upload Files"**
4. เลือกไฟล์ `YouTube_Transcript_API.postman_collection.json`
5. คลิก **"Import"**

### วิธีที่ 2: Import จาก URL (ถ้า push ไป GitHub)

1. เปิด Postman
2. คลิก **"Import"**
3. เลือกแท็บ **"Link"**
4. วาง URL ของไฟล์ collection
5. คลิก **"Continue"** → **"Import"**

---

## ⚙️ ตั้งค่า Environment Variables

### สร้าง Environment ใหม่

1. คลิก **"Environments"** ที่แถบซ้าย
2. คลิก **"+"** เพื่อสร้าง environment ใหม่
3. ตั้งชื่อ: `YouTube Transcript API - Local` หรือ `YouTube Transcript API - Production`

### ตั้งค่า Variables

| Variable | Initial Value | Current Value |
|----------|---------------|---------------|
| `base_url` | `http://localhost:8000` | `http://localhost:8000` |

**สำหรับ Production:**
- `base_url` = `https://your-backend.onrender.com`

### ใช้ Environment

1. เลือก environment ที่สร้างไว้จาก dropdown มุมบนขวา
2. Collection จะใช้ `{{base_url}}` จาก environment ที่เลือก

---

## 🚀 วิธีใช้งาน

### 1. Root & Health Endpoints

#### Get API Info
- **Method:** `GET`
- **URL:** `{{base_url}}/`
- **Description:** ดูข้อมูล API และ endpoints ที่มี

#### Health Check
- **Method:** `GET`
- **URL:** `{{base_url}}/api/health`
- **Description:** ตรวจสอบว่า API ทำงานปกติหรือไม่

### 2. Transcript Endpoints

#### List Available Transcripts
- **Method:** `POST`
- **URL:** `{{base_url}}/api/transcripts/list`
- **Body:**
  ```json
  {
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  }
  ```
- **Response:** รายการ transcripts ที่มีให้สำหรับ video

#### Preview Transcript
- **Method:** `POST`
- **URL:** `{{base_url}}/api/transcripts/preview`
- **Body:**
  ```json
  {
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "languages": ["en"],
    "preserve_formatting": false
  }
  ```
- **Response:** Transcript แบบ JSON (แสดง 50 snippets แรก)

#### Download Transcript
- **Method:** `POST`
- **URL:** `{{base_url}}/api/transcripts/download`
- **Body:**
  ```json
  {
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "languages": ["en"],
    "file_format": "txt",
    "include_timestamps": true,
    "preserve_formatting": false
  }
  ```
- **Response:** ไฟล์ transcript (TXT, PDF, หรือ DOCX)

---

## 📝 ตัวอย่าง Request Bodies

### List Transcripts
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

### Preview Transcript (English)
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "languages": ["en"],
  "preserve_formatting": false
}
```

### Preview Transcript (Thai)
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "languages": ["th", "en"],
  "preserve_formatting": false
}
```

### Download TXT
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "languages": ["en"],
  "file_format": "txt",
  "include_timestamps": true,
  "preserve_formatting": false
}
```

### Download PDF
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "languages": ["en"],
  "file_format": "pdf",
  "include_timestamps": true,
  "preserve_formatting": false
}
```

### Download DOCX
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "languages": ["en"],
  "file_format": "docx",
  "include_timestamps": true,
  "preserve_formatting": false
}
```

---

## 🔧 Parameters

### Request Parameters

| Parameter | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `url` | string | ✅ Yes | - | YouTube URL หรือ Video ID |
| `languages` | array | ❌ No | `["en"]` | รายการภาษา (เช่น `["th", "en"]`) |
| `file_format` | string | ❌ No | `"txt"` | รูปแบบไฟล์ (`txt`, `pdf`, `docx`) |
| `include_timestamps` | boolean | ❌ No | `true` | รวม timestamps หรือไม่ |
| `preserve_formatting` | boolean | ❌ No | `false` | เก็บ HTML formatting หรือไม่ |

### URL Formats ที่รองรับ

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `VIDEO_ID` (โดยตรง)

---

## 📊 Response Examples

### List Transcripts Response
```json
{
  "success": true,
  "video_id": "dQw4w9WgXcQ",
  "transcripts": [
    {
      "language": "English",
      "language_code": "en",
      "is_generated": false,
      "is_translatable": true,
      "translation_languages": []
    }
  ]
}
```

### Preview Transcript Response
```json
{
  "success": true,
  "video_id": "dQw4w9WgXcQ",
  "language": "English",
  "language_code": "en",
  "is_generated": false,
  "total_snippets": 150,
  "snippets": [
    {
      "text": "Never gonna give you up",
      "start": 0.0,
      "duration": 3.5
    }
  ]
}
```

---

## ⚠️ Error Responses

### 400 Bad Request
```json
{
  "detail": "กรุณากรอก YouTube URL หรือ Video ID"
}
```

### 404 Not Found
```json
{
  "detail": "ไม่พบ transcript สำหรับ video นี้"
}
```

### 500 Internal Server Error
```json
{
  "detail": "ไม่สามารถดึง transcript ได้: [error message]"
}
```

---

## 💡 Tips

1. **ใช้ Environment Variables:** สร้าง environment แยกสำหรับ local และ production
2. **Save Responses:** คลิกขวาที่ response → "Save Response" เพื่อเก็บตัวอย่าง
3. **Tests:** เพิ่ม tests เพื่อตรวจสอบ response automatically
4. **Pre-request Scripts:** ใช้ pre-request scripts เพื่อ generate dynamic values

---

## 🔗 Links

- [Postman Documentation](https://learning.postman.com/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [API Docs]({{base_url}}/docs) - Swagger UI
- [ReDoc]({{base_url}}/redoc) - Alternative API docs

---

**พร้อมใช้งานแล้ว! 🚀**

