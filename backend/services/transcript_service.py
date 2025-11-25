"""
Transcript Service - บริการสำหรับดึง transcript จาก YouTube
"""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
    YouTubeRequestFailed,
    RequestBlocked,
    IpBlocked,
    CouldNotRetrieveTranscript
)
from typing import List, Optional
import os


class TranscriptService:
    """Service สำหรับจัดการ transcript"""
    
    def __init__(self):
        # รองรับ cookies จาก environment variable (ถ้ามี)
        # วิธีได้ cookies: เปิด YouTube ใน browser → F12 → Application → Cookies → คัดลอก cookies
        cookies = os.getenv("YOUTUBE_COOKIES", None)
        if cookies:
            # cookies ควรเป็น list ของ dict หรือ string
            self.api = YouTubeTranscriptApi(cookies=cookies)
        else:
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
            FetchedTranscript object
        
        Raises:
            Exception: ถ้าเกิดข้อผิดพลาดในการดึง transcript
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
        except TranscriptsDisabled:
            raise Exception("Video นี้ปิดการใช้งาน transcripts")
        except NoTranscriptFound:
            raise Exception("ไม่พบ transcript สำหรับ video นี้")
        except VideoUnavailable:
            raise Exception("Video ไม่พร้อมใช้งานหรือถูกลบ")
        except (RequestBlocked, IpBlocked) as e:
            error_msg = str(e)
            raise Exception(
                "YouTube กำลังบล็อกการเข้าถึงจาก IP นี้ (มักเกิดจาก cloud provider)\n"
                "วิธีแก้ไข:\n"
                "1. ใช้ cookies จาก browser (ตั้งค่า YOUTUBE_COOKIES environment variable)\n"
                "2. ใช้ proxy service\n"
                "3. ลองใหม่ในภายหลัง\n"
                f"รายละเอียด: {error_msg}"
            )
        except YouTubeRequestFailed as e:
            error_msg = str(e)
            if "IP" in error_msg or "blocked" in error_msg.lower():
                raise Exception(
                    "YouTube กำลังบล็อกการเข้าถึงจาก IP นี้ (มักเกิดจาก cloud provider)\n"
                    "วิธีแก้ไข:\n"
                    "1. ใช้ cookies จาก browser (ตั้งค่า YOUTUBE_COOKIES environment variable)\n"
                    "2. ใช้ proxy service\n"
                    "3. ลองใหม่ในภายหลัง\n"
                    f"รายละเอียด: {error_msg}"
                )
            raise Exception(f"ไม่สามารถดึง transcript ได้: {error_msg}")
        except Exception as e:
            error_msg = str(e)
            if "IP" in error_msg or "blocked" in error_msg.lower():
                raise Exception(
                    "YouTube กำลังบล็อกการเข้าถึงจาก IP นี้\n"
                    "นี่เป็นปัญหาที่พบบ่อยเมื่อ deploy บน cloud providers (Render, AWS, GCP, etc.)\n"
                    "วิธีแก้ไข:\n"
                    "1. เพิ่ม YOUTUBE_COOKIES environment variable ใน Render\n"
                    "2. ใช้ proxy service\n"
                    "3. ลองใหม่ในภายหลัง\n"
                    f"รายละเอียด: {error_msg}"
                )
            raise Exception(f"ไม่สามารถดึง transcript ได้: {error_msg}")
    
    def list_transcripts(self, video_id: str):
        """
        แสดงรายการ transcript ที่มีให้สำหรับ video
        
        Args:
            video_id: YouTube video ID
        
        Returns:
            TranscriptList object
        
        Raises:
            Exception: ถ้าเกิดข้อผิดพลาดในการดึงรายการ transcript
        """
        try:
            return self.api.list(video_id)
        except TranscriptsDisabled:
            raise Exception("Video นี้ปิดการใช้งาน transcripts")
        except VideoUnavailable:
            raise Exception("Video ไม่พร้อมใช้งานหรือถูกลบ")
        except (RequestBlocked, IpBlocked) as e:
            error_msg = str(e)
            raise Exception(
                "YouTube กำลังบล็อกการเข้าถึงจาก IP นี้ (มักเกิดจาก cloud provider)\n"
                "วิธีแก้ไข:\n"
                "1. ใช้ cookies จาก browser (ตั้งค่า YOUTUBE_COOKIES environment variable)\n"
                "2. ใช้ proxy service\n"
                "3. ลองใหม่ในภายหลัง\n"
                f"รายละเอียด: {error_msg}"
            )
        except YouTubeRequestFailed as e:
            error_msg = str(e)
            if "IP" in error_msg or "blocked" in error_msg.lower():
                raise Exception(
                    "YouTube กำลังบล็อกการเข้าถึงจาก IP นี้ (มักเกิดจาก cloud provider)\n"
                    "วิธีแก้ไข:\n"
                    "1. ใช้ cookies จาก browser (ตั้งค่า YOUTUBE_COOKIES environment variable)\n"
                    "2. ใช้ proxy service\n"
                    "3. ลองใหม่ในภายหลัง\n"
                    f"รายละเอียด: {error_msg}"
                )
            raise Exception(f"ไม่สามารถดึงรายการ transcript ได้: {error_msg}")
        except Exception as e:
            error_msg = str(e)
            if "IP" in error_msg or "blocked" in error_msg.lower():
                raise Exception(
                    "YouTube กำลังบล็อกการเข้าถึงจาก IP นี้\n"
                    "นี่เป็นปัญหาที่พบบ่อยเมื่อ deploy บน cloud providers (Render, AWS, GCP, etc.)\n"
                    "วิธีแก้ไข:\n"
                    "1. เพิ่ม YOUTUBE_COOKIES environment variable ใน Render\n"
                    "2. ใช้ proxy service\n"
                    "3. ลองใหม่ในภายหลัง\n"
                    f"รายละเอียด: {error_msg}"
                )
            raise Exception(f"ไม่สามารถดึงรายการ transcript ได้: {error_msg}")

