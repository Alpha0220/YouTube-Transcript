"""
ตัวอย่างการใช้งานแบบง่าย - YouTube Transcript API
เหมาะสำหรับผู้เริ่มต้น
"""

from youtube_transcript_api import YouTubeTranscriptApi


def simple_example():
    """
    ตัวอย่างง่ายๆ: ดึง transcript จาก YouTube video
    """
    # สร้าง instance
    ytt_api = YouTubeTranscriptApi()
    
    # Video ID ที่ต้องการดึง transcript
    # เปลี่ยนเป็น video ID ที่คุณต้องการ
    video_id = "dQw4w9WgXcQ"
    
    try:
        # ดึง transcript (ภาษาอังกฤษ)
        print(f"กำลังดึง transcript สำหรับ video: {video_id}")
        transcript = ytt_api.fetch(video_id)
        
        # แสดงข้อมูล
        print(f"\n✅ สำเร็จ!")
        print(f"ภาษา: {transcript.language}")
        print(f"จำนวน snippets: {len(transcript)}")
        
        # แสดงเนื้อหา
        print("\n📝 เนื้อหา transcript:")
        print("-" * 50)
        for snippet in transcript:
            print(f"[{snippet.start:.2f}s] {snippet.text}")
            
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")


def thai_example():
    """
    ตัวอย่าง: ดึง transcript ภาษาไทย
    """
    ytt_api = YouTubeTranscriptApi()
    
    # Video ID ที่มี subtitle ภาษาไทย
    video_id = "YOUR_VIDEO_ID_HERE"  # เปลี่ยนเป็น video ID ที่มี subtitle ไทย
    
    try:
        # ลองดึงภาษาไทยก่อน ถ้าไม่มีจะใช้ภาษาอังกฤษ
        transcript = ytt_api.fetch(video_id, languages=['th', 'en'])
        
        print(f"ภาษา: {transcript.language} ({transcript.language_code})")
        
        # แสดงเนื้อหา
        for snippet in transcript:
            print(snippet.text)
            
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")


def list_transcripts_example():
    """
    ตัวอย่าง: แสดงรายการ transcript ที่มีให้
    """
    ytt_api = YouTubeTranscriptApi()
    video_id = "dQw4w9WgXcQ"
    
    try:
        transcript_list = ytt_api.list(video_id)
        
        print(f"รายการ transcript ที่มีให้สำหรับ video: {video_id}")
        print("-" * 50)
        
        for transcript in transcript_list:
            transcript_type = "สร้างอัตโนมัติ" if transcript.is_generated else "สร้างด้วยมือ"
            print(f"• {transcript.language} ({transcript.language_code}) - {transcript_type}")
            
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")


if __name__ == "__main__":
    print("=" * 50)
    print("YouTube Transcript API - ตัวอย่างการใช้งาน")
    print("=" * 50)
    
    # รันตัวอย่าง
    simple_example()
    
    # ถ้าต้องการดูรายการ transcript ที่มีให้
    # list_transcripts_example()

