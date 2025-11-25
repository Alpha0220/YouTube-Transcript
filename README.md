# 🎬 YouTube Transcript API Project

โปรเจกต์สำหรับดึง transcript (คำบรรยาย) จาก YouTube videos โดยใช้ library `youtube-transcript-api`

## 📋 สารบัญ

1. [การติดตั้ง (Installation)](#การติดตั้ง-installation)
2. [การใช้งาน (Usage)](#การใช้งาน-usage)
3. [ตัวอย่างโค้ด (Examples)](#ตัวอย่างโค้ด-examples)
4. [API Reference](#api-reference)
5. [FAQ](#faq)

---

## 🚀 การติดตั้ง (Installation)

### ขั้นตอนที่ 1: ติดตั้ง Python

ตรวจสอบว่าคุณมี Python ติดตั้งแล้วหรือไม่:

```bash
python3 --version
```

ควรเป็น Python 3.8 หรือสูงกว่า (แต่ต่ำกว่า 3.15)

### ขั้นตอนที่ 2: สร้าง Virtual Environment (แนะนำ)

```bash
# สร้าง virtual environment
python3 -m venv venv

# เปิดใช้งาน virtual environment
# บน Linux/Mac:
source venv/bin/activate
# บน Windows:
# venv\Scripts\activate
```

### ขั้นตอนที่ 3: ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

หรือติดตั้งโดยตรง:

```bash
pip install youtube-transcript-api
```

---

## 💻 การใช้งาน (Usage)

### วิธีที่ 1: ใช้งานผ่าน Command Line

```bash
# รันโปรแกรมพร้อม video ID หรือ URL
python main.py dQw4w9WgXcQ

# หรือใช้ URL เต็ม
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### วิธีที่ 2: ใช้งานในโค้ด Python

```python
from youtube_transcript_api import YouTubeTranscriptApi

# สร้าง instance
ytt_api = YouTubeTranscriptApi()

# ดึง transcript (ภาษาอังกฤษ)
transcript = ytt_api.fetch('dQw4w9WgXcQ')

# แสดงเนื้อหา
for snippet in transcript:
    print(f"[{snippet.start}s] {snippet.text}")
```

---

## 📝 ตัวอย่างโค้ด (Examples)

### ตัวอย่างที่ 1: ดึง Transcript ภาษาอังกฤษ

```python
from youtube_transcript_api import YouTubeTranscriptApi

ytt_api = YouTubeTranscriptApi()
transcript = ytt_api.fetch('VIDEO_ID')

for snippet in transcript:
    print(f"{snippet.text}")
```

### ตัวอย่างที่ 2: ดึง Transcript ภาษาไทย

```python
from youtube_transcript_api import YouTubeTranscriptApi

ytt_api = YouTubeTranscriptApi()
# ลองภาษาไทยก่อน ถ้าไม่มีจะใช้ภาษาอังกฤษ
transcript = ytt_api.fetch('VIDEO_ID', languages=['th', 'en'])

print(f"ภาษา: {transcript.language}")
for snippet in transcript:
    print(f"[{snippet.start:.2f}s] {snippet.text}")
```

### ตัวอย่างที่ 3: แสดงรายการ Transcript ที่มีให้

```python
from youtube_transcript_api import YouTubeTranscriptApi

ytt_api = YouTubeTranscriptApi()
transcript_list = ytt_api.list('VIDEO_ID')

for transcript in transcript_list:
    print(f"ภาษา: {transcript.language} ({transcript.language_code})")
    print(f"สร้างอัตโนมัติ: {transcript.is_generated}")
```

### ตัวอย่างที่ 4: แปล Transcript

```python
from youtube_transcript_api import YouTubeTranscriptApi

ytt_api = YouTubeTranscriptApi()
transcript_list = ytt_api.list('VIDEO_ID')

# หา transcript ภาษาอังกฤษ
transcript = transcript_list.find_transcript(['en'])

# แปลเป็นภาษาไทย
translated = transcript.translate('th')
translated_data = translated.fetch()

for snippet in translated_data:
    print(snippet.text)
```

### ตัวอย่างที่ 5: บันทึกลงไฟล์

```python
from youtube_transcript_api import YouTubeTranscriptApi

ytt_api = YouTubeTranscriptApi()
transcript = ytt_api.fetch('VIDEO_ID', languages=['en'])

# บันทึกลงไฟล์
with open('transcript.txt', 'w', encoding='utf-8') as f:
    for snippet in transcript:
        f.write(f"[{snippet.start:.2f}s] {snippet.text}\n")
```

---

## 📚 API Reference

### YouTubeTranscriptApi().fetch()

ดึง transcript จาก video

**Parameters:**
- `video_id` (str): YouTube video ID (ไม่ใช่ URL เต็ม)
- `languages` (list, optional): รายการภาษา เช่น `['th', 'en']` (default: `['en']`)
- `preserve_formatting` (bool, optional): เก็บ HTML formatting (default: `False`)

**Returns:**
- `FetchedTranscript` object ที่มี:
  - `snippets`: รายการ transcript snippets
  - `video_id`: video ID
  - `language`: ชื่อภาษา
  - `language_code`: รหัสภาษา
  - `is_generated`: สร้างอัตโนมัติหรือไม่

### YouTubeTranscriptApi().list()

แสดงรายการ transcript ที่มีให้

**Parameters:**
- `video_id` (str): YouTube video ID

**Returns:**
- `TranscriptList` object ที่สามารถ iterate ได้

### FetchedTranscript Object

Object ที่ได้จาก `fetch()` มีคุณสมบัติ:
- `snippets`: รายการ snippets (iterable)
- แต่ละ snippet มี:
  - `text`: ข้อความ
  - `start`: เวลาเริ่มต้น (วินาที)
  - `duration`: ระยะเวลา (วินาที)

---

## ❓ FAQ

### Q: จะหา Video ID ได้อย่างไร?

A: จาก YouTube URL เช่น `https://www.youtube.com/watch?v=VIDEO_ID` 
   Video ID คือส่วนหลัง `v=` (ในตัวอย่างคือ `VIDEO_ID`)

### Q: Video นี้ไม่มี subtitle จะทำอย่างไร?

A: บาง video อาจไม่มี subtitle เลย หรือมีแต่ auto-generated subtitle เท่านั้น
   ลองใช้ `list()` เพื่อดูว่ามี transcript อะไรบ้าง

### Q: จะดึง subtitle ภาษาไทยได้อย่างไร?

A: ใช้ `languages=['th', 'en']` เพื่อลองภาษาไทยก่อน ถ้าไม่มีจะใช้ภาษาอังกฤษ

### Q: ได้ error "No transcripts were found" หมายความว่าอะไร?

A: หมายความว่า video นี้ไม่มี transcript ให้ดึง ลองใช้ `list()` เพื่อตรวจสอบ

### Q: สามารถใช้กับ video ที่มี age restriction ได้ไหม?

A: บาง video ที่มี age restriction อาจต้องใช้ cookie authentication
   ดูรายละเอียดเพิ่มเติมใน [documentation](https://github.com/jdepoix/youtube-transcript-api)

---

## 🔗 Links

- [youtube-transcript-api PyPI](https://pypi.org/project/youtube-transcript-api/)
- [GitHub Repository](https://github.com/jdepoix/youtube-transcript-api)

---

## 📄 License

MIT License

---

## 🙏 Credits

โปรเจกต์นี้ใช้ library [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) 
ที่พัฒนาโดย Jonas Depoix

