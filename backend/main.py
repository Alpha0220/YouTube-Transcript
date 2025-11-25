"""
YouTube Transcript API Backend Service
FastAPI backend สำหรับดึง transcript และแปลงเป็นไฟล์ต่างๆ
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import tempfile
from datetime import datetime

from services.transcript_service import TranscriptService
from services.file_converter import FileConverter

app = FastAPI(
    title="YouTube Transcript API",
    description="API สำหรับดึง transcript จาก YouTube และแปลงเป็นไฟล์ต่างๆ",
    version="1.0.0"
)

# CORS middleware เพื่อให้ frontend เรียกใช้ได้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # อนุญาตทุก origin (สำหรับ development)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Initialize services
transcript_service = TranscriptService()
file_converter = FileConverter()


class TranscriptRequest(BaseModel):
    """Request model สำหรับดึง transcript"""
    url: str = Field(..., description="YouTube URL หรือ Video ID")
    languages: Optional[List[str]] = Field(default=["en"], description="รายการภาษา (เช่น ['th', 'en'])")
    preserve_formatting: bool = Field(default=False, description="เก็บ HTML formatting หรือไม่")
    file_format: str = Field(default="txt", description="รูปแบบไฟล์ (txt, pdf, doc)")
    include_timestamps: bool = Field(default=True, description="รวม timestamps หรือไม่")


class ListTranscriptsRequest(BaseModel):
    """Request model สำหรับดูรายการ transcript"""
    url: str = Field(..., description="YouTube URL หรือ Video ID")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "YouTube Transcript API Backend",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "API information",
            "POST /api/transcripts/list": "List available transcripts",
            "POST /api/transcripts/download": "Download transcript as file"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.options("/api/transcripts/{path:path}")
async def options_handler(path: str):
    """Handle OPTIONS requests for CORS"""
    return {"message": "OK"}


@app.post("/api/transcripts/list")
async def list_transcripts(request: ListTranscriptsRequest):
    """
    แสดงรายการ transcript ที่มีให้สำหรับ video
    """
    try:
        if not request.url or not request.url.strip():
            raise HTTPException(status_code=400, detail="กรุณากรอก YouTube URL หรือ Video ID")
        
        video_id = transcript_service.extract_video_id(request.url.strip())
        transcripts = transcript_service.list_transcripts(video_id)
        
        result = []
        for transcript in transcripts:
            result.append({
                "language": transcript.language,
                "language_code": transcript.language_code,
                "is_generated": transcript.is_generated,
                "is_translatable": transcript.is_translatable,
                "translation_languages": transcript.translation_languages if hasattr(transcript, 'translation_languages') else []
            })
        
        return {
            "success": True,
            "video_id": video_id,
            "transcripts": result
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"ไม่สามารถดึงรายการ transcript ได้: {str(e)}")


@app.post("/api/transcripts/download")
async def download_transcript(request: TranscriptRequest):
    """
    ดึง transcript และแปลงเป็นไฟล์ตามรูปแบบที่เลือก
    """
    try:
        if not request.url or not request.url.strip():
            raise HTTPException(status_code=400, detail="กรุณากรอก YouTube URL หรือ Video ID")
        
        # Extract video ID
        video_id = transcript_service.extract_video_id(request.url.strip())
        
        # ตรวจสอบ languages
        languages = request.languages if request.languages else ["en"]
        
        # Fetch transcript
        transcript = transcript_service.fetch_transcript(
            video_id=video_id,
            languages=languages,
            preserve_formatting=request.preserve_formatting
        )
        
        if not transcript:
            raise HTTPException(status_code=404, detail="ไม่พบ transcript สำหรับ video นี้")
        
        # Convert to file
        file_format = request.file_format.lower() if request.file_format else "txt"
        
        if file_format == "txt":
            file_path = file_converter.to_txt(
                transcript=transcript,
                include_timestamps=request.include_timestamps
            )
            media_type = "text/plain"
        elif file_format == "pdf":
            file_path = file_converter.to_pdf(
                transcript=transcript,
                include_timestamps=request.include_timestamps
            )
            media_type = "application/pdf"
        elif file_format == "doc" or file_format == "docx":
            file_path = file_converter.to_docx(
                transcript=transcript,
                include_timestamps=request.include_timestamps
            )
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        else:
            raise HTTPException(status_code=400, detail=f"รูปแบบไฟล์ไม่รองรับ: {file_format}")
        
        # Generate filename
        filename = f"transcript_{video_id}_{transcript.language_code}.{file_format}"
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type=media_type,
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"เกิดข้อผิดพลาด: {str(e)}")


@app.post("/api/transcripts/preview")
async def preview_transcript(request: TranscriptRequest):
    """
    ดึง transcript และส่งกลับเป็น JSON (สำหรับ preview)
    """
    try:
        if not request.url or not request.url.strip():
            raise HTTPException(status_code=400, detail="กรุณากรอก YouTube URL หรือ Video ID")
        
        video_id = transcript_service.extract_video_id(request.url.strip())
        
        # ตรวจสอบ languages
        languages = request.languages if request.languages else ["en"]
        
        transcript = transcript_service.fetch_transcript(
            video_id=video_id,
            languages=languages,
            preserve_formatting=request.preserve_formatting
        )
        
        if not transcript:
            raise HTTPException(status_code=404, detail="ไม่พบ transcript สำหรับ video นี้")
        
        snippets = []
        for snippet in transcript:
            snippets.append({
                "text": snippet.text,
                "start": snippet.start,
                "duration": snippet.duration
            })
        
        return {
            "success": True,
            "video_id": transcript.video_id,
            "language": transcript.language,
            "language_code": transcript.language_code,
            "is_generated": transcript.is_generated,
            "total_snippets": len(transcript),
            "snippets": snippets[:50]  # แสดงแค่ 50 snippets แรกสำหรับ preview
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"เกิดข้อผิดพลาด: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

