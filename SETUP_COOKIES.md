# 🍪 คู่มือการตั้งค่า Cookies สำหรับ YouTube Transcript API

## 📋 ภาพรวม

คู่มือนี้จะสอนวิธีตั้งค่า cookies เพื่อแก้ปัญหา YouTube IP blocking เมื่อ deploy บน Render หรือ cloud providers อื่นๆ

---

## 🎯 ขั้นตอนที่ 1: ได้ Cookies จาก Browser

### วิธีที่ 1: ใช้ Chrome Browser (แนะนำ)

1. **เปิด YouTube ใน Chrome**
   - ไปที่ https://www.youtube.com
   - **สำคัญ:** ต้อง login YouTube account ก่อน (จะได้ cookies ที่ดีกว่า)

2. **เปิด Developer Tools**
   - กด `F12` หรือ `Ctrl+Shift+I` (Windows/Linux)
   - หรือ `Cmd+Option+I` (Mac)
   - หรือคลิกขวา → "Inspect"

3. **ไปที่แท็บ Application**
   - คลิกแท็บ **"Application"** ที่ด้านบน
   - (ถ้าไม่เห็น ให้คลิก `>>` เพื่อดูแท็บเพิ่มเติม)

4. **เปิด Cookies**
   - ในแถบซ้าย คลิก **"Cookies"** → `https://www.youtube.com`
   - คุณจะเห็นรายการ cookies ทั้งหมด

5. **คัดลอก Cookies ที่สำคัญ**
   - คลิกขวาที่ cookie → **"Copy"** หรือ **"Copy value"**
   - Cookies ที่ควรคัดลอก:
     - `VISITOR_INFO1_LIVE` ⭐ (สำคัญมาก)
     - `LOGIN_INFO` (ถ้า login แล้ว)
     - `PREF`
     - `YSC`
     - `CONSENT` (ถ้ามี)

### วิธีที่ 2: ใช้ Browser Extension (ง่ายกว่า)

1. **ติดตั้ง Extension**
   - Chrome: [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
   - Firefox: [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)

2. **Export Cookies**
   - เปิด YouTube
   - คลิก extension icon
   - คลิก "Export" หรือ "Copy"
   - จะได้ cookies ในรูปแบบ `cookie1=value1; cookie2=value2`

### วิธีที่ 3: ใช้ Browser Console (สำหรับผู้เชี่ยวชาญ)

1. เปิด YouTube ใน browser
2. กด `F12` → ไปที่แท็บ **Console**
3. พิมพ์คำสั่ง:
   ```javascript
   document.cookie
   ```
4. Copy ผลลัพธ์ทั้งหมด

---

## 📝 ขั้นตอนที่ 2: จัดรูปแบบ Cookies

### รูปแบบที่ 1: String Format (แนะนำ)

```
VISITOR_INFO1_LIVE=xxx; LOGIN_INFO=yyy; PREF=zzz; YSC=aaa
```

**ตัวอย่างจริง:**
```
VISITOR_INFO1_LIVE=CgtRSDZ4WlBvOE1ZRSiA8Z2KBg%3D%3D; LOGIN_INFO=AFmmF2swRQIhAJ...; PREF=f4=4000000&tz=Asia%2FBangkok; YSC=dQw4w9WgXcQ
```

### รูปแบบที่ 2: JSON Array (สำหรับ advanced users)

```json
[
  {"name": "VISITOR_INFO1_LIVE", "value": "xxx"},
  {"name": "LOGIN_INFO", "value": "yyy"},
  {"name": "PREF", "value": "zzz"}
]
```

---

## ⚙️ ขั้นตอนที่ 3: ตั้งค่าใน Render

### วิธีที่ 1: ผ่าน Render Dashboard (แนะนำ)

1. **เข้าสู่ Render Dashboard**
   - ไปที่ https://dashboard.render.com
   - Login เข้าสู่ระบบ

2. **เลือก Service**
   - คลิกที่ service ของคุณ (เช่น `youtube-transcript-api`)

3. **ไปที่ Environment**
   - คลิกแท็บ **"Environment"** ที่ด้านบน

4. **เพิ่ม Environment Variable**
   - คลิกปุ่ม **"Add Environment Variable"** หรือ **"Add Variable"**
   - ตั้งค่าดังนี้:
     - **Key:** `YOUTUBE_COOKIES`
     - **Value:** วาง cookies ที่คัดลอกมา (รูปแบบ string)
     - **Example:**
       ```
       VISITOR_INFO1_LIVE=CgtRSDZ4WlBvOE1ZRSiA8Z2KBg%3D%3D; LOGIN_INFO=AFmmF2swRQIhAJ...; PREF=f4=4000000&tz=Asia%2FBangkok
       ```

5. **Save**
   - คลิก **"Save Changes"** หรือ **"Save"**
   - Render จะ restart service อัตโนมัติ

6. **รอ Deploy**
   - รอให้ service restart เสร็จ (ประมาณ 1-2 นาที)
   - ตรวจสอบ logs ว่าไม่มี error

### วิธีที่ 2: ผ่าน render.yaml (สำหรับ advanced users)

แก้ไขไฟล์ `backend/render.yaml`:

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
      - key: YOUTUBE_COOKIES
        value: "VISITOR_INFO1_LIVE=xxx; LOGIN_INFO=yyy; PREF=zzz"
```

**หมายเหตุ:** ไม่แนะนำวิธีนี้เพราะ cookies จะถูก commit ไปที่ Git (ไม่ปลอดภัย)

---

## ✅ ขั้นตอนที่ 4: ทดสอบ

### 1. ตรวจสอบว่า Cookies ถูกตั้งค่าแล้ว

ดู Logs ใน Render:
- ไปที่ Render Dashboard → Service → Logs
- ตรวจสอบว่าไม่มี error เกี่ยวกับ cookies

### 2. ทดสอบ API

ลองเรียก API อีกครั้ง:
```bash
curl -X POST https://your-backend.onrender.com/api/transcripts/list \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

หรือทดสอบผ่าน Frontend:
- เปิด frontend
- ลองดึง transcript จาก video
- ควรทำงานได้แล้ว!

---

## 🔍 Troubleshooting

### ❌ ปัญหา: Cookies ไม่ทำงาน

**อาการ:**
- ยังคงได้ error "IP blocked"

**วิธีแก้:**
1. ตรวจสอบว่า cookies ไม่หมดอายุ (ลองได้ใหม่)
2. ตรวจสอบว่า format ถูกต้อง (ต้องมี `;` คั่นระหว่าง cookies)
3. ลอง login YouTube ก่อนแล้วคัดลอก cookies ใหม่
4. ตรวจสอบว่า environment variable ชื่อ `YOUTUBE_COOKIES` ถูกต้อง

### ❌ ปัญหา: Cookies หมดอายุ

**อาการ:**
- ทำงานได้สักพักแล้วหยุดทำงาน

**วิธีแก้:**
- Cookies มักหมดอายุใน 1-2 สัปดาห์
- ต้องคัดลอก cookies ใหม่และอัปเดตใน Render

### ❌ ปัญหา: Format ไม่ถูกต้อง

**อาการ:**
- Error เมื่อ start service

**วิธีแก้:**
- ตรวจสอบว่าไม่มี newline หรือ special characters
- ใช้ string format: `cookie1=value1; cookie2=value2`
- ไม่ต้องใส่ quotes (`"`) ใน Render Dashboard

---

## 💡 Tips และ Best Practices

### 1. ใช้ Account ที่ Login แล้ว
- Cookies จาก account ที่ login แล้วจะทำงานได้ดีกว่า
- มีโอกาสถูก block น้อยกว่า

### 2. หมั่นอัปเดต Cookies
- Cookies หมดอายุประมาณ 1-2 สัปดาห์
- ตั้ง reminder เพื่ออัปเดตเป็นระยะ

### 3. เก็บ Cookies ไว้ที่ปลอดภัย
- **อย่า** commit cookies ไปที่ Git
- ใช้ Environment Variables เท่านั้น
- เก็บ backup ไว้ที่อื่น (password manager)

### 4. ใช้หลาย Cookies (ถ้าจำเป็น)
- ถ้ามีหลาย YouTube accounts
- สามารถ rotate cookies ได้

### 5. Monitor Logs
- ตรวจสอบ logs เป็นประจำ
- ถ้าเห็น error เกี่ยวกับ cookies ให้อัปเดตทันที

---

## 📸 Screenshots Guide

### ขั้นตอนที่ 1: เปิด Developer Tools
```
1. เปิด YouTube
2. กด F12
3. คลิกแท็บ "Application"
```

### ขั้นตอนที่ 2: คัดลอก Cookies
```
1. คลิก Cookies → https://www.youtube.com
2. คลิกขวาที่ cookie → Copy value
3. คัดลอก cookies ที่สำคัญ
```

### ขั้นตอนที่ 3: ตั้งค่าใน Render
```
1. Render Dashboard → Service → Environment
2. Add Environment Variable
3. Key: YOUTUBE_COOKIES
4. Value: (วาง cookies ที่คัดลอกมา)
5. Save
```

---

## 🔐 Security Notes

⚠️ **สำคัญ:**
- Cookies อาจมีข้อมูลส่วนตัว (เช่น login session)
- **อย่า** แชร์ cookies กับคนอื่น
- **อย่า** commit cookies ไปที่ Git repository
- ใช้ Environment Variables เท่านั้น
- ถ้า cookies ถูก compromise ให้ revoke session ทันที

---

## 📚 เอกสารเพิ่มเติม

- [youtube-transcript-api Documentation](https://github.com/jdepoix/youtube-transcript-api)
- [Render Environment Variables](https://render.com/docs/environment-variables)
- [Chrome Developer Tools](https://developer.chrome.com/docs/devtools/)

---

## ✅ Checklist

ใช้ checklist นี้เพื่อให้แน่ใจว่าตั้งค่าถูกต้อง:

- [ ] ได้ cookies จาก browser (ใช้ Chrome/Firefox)
- [ ] Login YouTube account ก่อนคัดลอก cookies
- [ ] คัดลอก cookies ที่สำคัญ (VISITOR_INFO1_LIVE, LOGIN_INFO, etc.)
- [ ] จัดรูปแบบ cookies เป็น string format
- [ ] เพิ่ม Environment Variable `YOUTUBE_COOKIES` ใน Render
- [ ] วาง cookies ใน Value field
- [ ] Save และรอให้ service restart
- [ ] ทดสอบ API ว่าทำงานได้แล้ว
- [ ] ตรวจสอบ logs ว่าไม่มี error

---

**🎉 พร้อมใช้งานแล้ว!**

หลังจากตั้งค่า cookies แล้ว YouTube จะไม่ block IP ของคุณอีกต่อไป!

