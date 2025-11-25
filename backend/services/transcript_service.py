"""
Transcript Service - บริการสำหรับดึง transcript จาก YouTube
"""

from youtube_transcript_api import YouTubeTranscriptApi
from typing import List, Optional


class TranscriptService:
    """Service สำหรับจัดการ transcript"""
    
    def __init__(self):
        self.api = YouTubeTranscriptApi()
    
    def extract_video_id(self, url_or_id: str) -> str:
        """
        แยก video ID จาก YouTube URL หรือรับ ID โดยตรง
        
        Args:
            url_or_id: YouTube URL หรือ Video ID
        
        Returns:
            Video ID
        """
        url = url_or_id.strip()
        
        # ถ้าเป็น URL แบบ watch?v=
        if 'watch?v=' in url:
            return url.split('watch?v=')[1].split('&')[0]
        # ถ้าเป็น Short URL
        elif 'youtu.be/' in url:
            return url.split('youtu.be/')[1].split('?')[0]
        # ถ้าเป็น embed URL
        elif 'embed/' in url:
            return url.split('embed/')[1].split('?')[0]
        # ถ้าใส่ ID โดยตรง
        else:
            return url
    
    def fetch_transcript(
        self,
        video_id: str,
        languages: Optional[List[str]] = None,
        preserve_formatting: bool = False
    ):
        """
        ดึง transcript จาก YouTube video
        
        Args:
            video_id: YouTube video ID
            languages: รายการภาษา (เช่น ['th', 'en'])
            preserve_formatting: เก็บ HTML formatting หรือไม่
        
        Returns:
            FetchedTranscript object หรือ None ถ้าเกิดข้อผิดพลาด
        """
        try:
            if languages:
                return self.api.fetch(
                    video_id,
                    languages=languages,
                    preserve_formatting=preserve_formatting
                )
            else:
                return self.api.fetch(
                    video_id,
                    preserve_formatting=preserve_formatting
                )
        except Exception as e:
            raise Exception(f"ไม่สามารถดึง transcript ได้: {str(e)}")
    
    def list_transcripts(self, video_id: str):
        """
        แสดงรายการ transcript ที่มีให้สำหรับ video
        
        Args:
            video_id: YouTube video ID
        
        Returns:
            TranscriptList object
        """
        try:
            return self.api.list(video_id)
        except Exception as e:
            raise Exception(f"ไม่สามารถดึงรายการ transcript ได้: {str(e)}")

