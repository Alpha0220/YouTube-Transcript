"""
YouTube Transcript API - โปรแกรมดึง transcript จาก YouTube
ตัวอย่างการใช้งาน youtube-transcript-api
"""

from youtube_transcript_api import YouTubeTranscriptApi


def get_video_id_from_url(url):
    """
    แยก video ID จาก YouTube URL
    รองรับรูปแบบ:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - VIDEO_ID (ถ้าใส่ ID โดยตรง)
    """
    if 'watch?v=' in url:
        return url.split('watch?v=')[1].split('&')[0]
    elif 'youtu.be/' in url:
        return url.split('youtu.be/')[1].split('?')[0]
    else:
        # ถ้าใส่ ID โดยตรง
        return url


def fetch_transcript(video_id, languages=None, preserve_formatting=False):
    """
    ดึง transcript จาก YouTube video
    
    Args:
        video_id: YouTube video ID
        languages: รายการภาษา (เช่น ['th', 'en']) หรือ None สำหรับ default (อังกฤษ)
        preserve_formatting: เก็บ HTML formatting หรือไม่
    
    Returns:
        FetchedTranscript object
    """
    try:
        ytt_api = YouTubeTranscriptApi()
        
        if languages:
            transcript = ytt_api.fetch(video_id, languages=languages, preserve_formatting=preserve_formatting)
        else:
            transcript = ytt_api.fetch(video_id, preserve_formatting=preserve_formatting)
        
        return transcript
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
        return None


def list_available_transcripts(video_id):
    """
    แสดงรายการ transcript ที่มีให้สำหรับ video นี้
    """
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.list(video_id)
        
        print(f"\n📋 รายการ transcript ที่มีให้สำหรับ video: {video_id}")
        print("=" * 60)
        
        for transcript in transcript_list:
            transcript_type = "🤖 สร้างอัตโนมัติ" if transcript.is_generated else "✍️ สร้างด้วยมือ"
            print(f"ภาษา: {transcript.language} ({transcript.language_code}) - {transcript_type}")
            if transcript.is_translatable:
                print(f"  สามารถแปลเป็น: {len(transcript.translation_languages)} ภาษา")
        
        return transcript_list
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
        return None


def save_transcript_to_file(transcript, filename="transcript.txt"):
    """
    บันทึก transcript ลงไฟล์
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Video ID: {transcript.video_id}\n")
            f.write(f"ภาษา: {transcript.language} ({transcript.language_code})\n")
            f.write(f"สร้างอัตโนมัติ: {'ใช่' if transcript.is_generated else 'ไม่ใช่'}\n")
            f.write("=" * 60 + "\n\n")
            
            for snippet in transcript:
                f.write(f"[{snippet.start:.2f}s - {snippet.start + snippet.duration:.2f}s]\n")
                f.write(f"{snippet.text}\n\n")
        
        print(f"✅ บันทึก transcript ลงไฟล์: {filename}")
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการบันทึกไฟล์: {e}")


def main():
    """
    ฟังก์ชันหลัก - ตัวอย่างการใช้งาน
    """
    print("=" * 60)
    print("🎬 YouTube Transcript API - โปรแกรมดึง transcript")
    print("=" * 60)
    
    # ตัวอย่าง 1: ดึง transcript แบบง่าย (ภาษาอังกฤษ)
    print("\n📌 ตัวอย่างที่ 1: ดึง transcript ภาษาอังกฤษ")
    print("-" * 60)
    
    # ใช้ video ID ตัวอย่าง (คุณสามารถเปลี่ยนเป็น video ID จริงได้)
    example_video_id = "dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up
    
    # แสดงรายการ transcript ที่มีให้
    transcript_list = list_available_transcripts(example_video_id)
    
    if transcript_list:
        # ดึง transcript ภาษาอังกฤษ
        print(f"\n📥 กำลังดึง transcript สำหรับ video: {example_video_id}")
        transcript = fetch_transcript(example_video_id, languages=['en'])
        
        if transcript:
            print(f"\n✅ ดึง transcript สำเร็จ!")
            print(f"   ภาษา: {transcript.language} ({transcript.language_code})")
            print(f"   จำนวน snippets: {len(transcript)}")
            print(f"   สร้างอัตโนมัติ: {'ใช่' if transcript.is_generated else 'ไม่ใช่'}")
            
            # แสดงตัวอย่าง 5 snippets แรก
            print(f"\n📝 ตัวอย่างเนื้อหา (5 snippets แรก):")
            print("-" * 60)
            for i, snippet in enumerate(transcript[:5]):
                print(f"{i+1}. [{snippet.start:.2f}s] {snippet.text}")
            
            # บันทึกลงไฟล์
            save_transcript_to_file(transcript, "transcript_en.txt")
    
    # ตัวอย่าง 2: ดึง transcript ภาษาไทย (ถ้ามี)
    print("\n\n📌 ตัวอย่างที่ 2: พยายามดึง transcript ภาษาไทย")
    print("-" * 60)
    
    # คุณสามารถเปลี่ยน video ID เป็น video ที่มี subtitle ภาษาไทย
    thai_video_id = example_video_id  # เปลี่ยนเป็น video ID ที่มี subtitle ไทย
    
    transcript_thai = fetch_transcript(thai_video_id, languages=['th', 'en'])
    
    if transcript_thai:
        print(f"\n✅ ดึง transcript สำเร็จ!")
        print(f"   ภาษา: {transcript_thai.language} ({transcript_thai.language_code})")
        save_transcript_to_file(transcript_thai, "transcript_th.txt")
    
    # ตัวอย่าง 3: แสดงวิธีใช้กับ URL
    print("\n\n📌 ตัวอย่างที่ 3: การใช้งานกับ YouTube URL")
    print("-" * 60)
    print("คุณสามารถใช้ URL แทน video ID ได้:")
    print("""
    # ตัวอย่าง:
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    video_id = get_video_id_from_url(url)
    transcript = fetch_transcript(video_id)
    """)


if __name__ == "__main__":
    # คุณสามารถแก้ไขส่วนนี้เพื่อรับ input จากผู้ใช้
    import sys
    
    if len(sys.argv) > 1:
        # ถ้ามี argument ให้ใช้เป็น video ID หรือ URL
        video_input = sys.argv[1]
        video_id = get_video_id_from_url(video_input)
        
        print(f"🎬 กำลังดึง transcript สำหรับ: {video_id}")
        
        # แสดงรายการ transcript ที่มีให้
        transcript_list = list_available_transcripts(video_id)
        
        # ดึง transcript (ลองภาษาไทยก่อน แล้วค่อยอังกฤษ)
        transcript = fetch_transcript(video_id, languages=['th', 'en'])
        
        if transcript:
            print(f"\n✅ ดึง transcript สำเร็จ!")
            print(f"   ภาษา: {transcript.language} ({transcript.language_code})")
            print(f"   จำนวน snippets: {len(transcript)}")
            
            # แสดงเนื้อหาทั้งหมด
            print(f"\n📝 เนื้อหา transcript:")
            print("=" * 60)
            for snippet in transcript:
                print(f"[{snippet.start:.2f}s] {snippet.text}")
            
            # บันทึกลงไฟล์
            filename = f"transcript_{video_id}.txt"
            save_transcript_to_file(transcript, filename)
    else:
        # ถ้าไม่มี argument ให้รันตัวอย่าง
        main()

