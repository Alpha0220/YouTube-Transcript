#!/usr/bin/env python3
"""
Script สำหรับรัน backend พร้อม tunnel (ngrok หรือ cloudflare)
ทำให้ frontend บน Vercel สามารถเข้าถึง backend ที่รันบนเครื่อง local ได้
"""

import subprocess
import sys
import time
import signal
import os
import json
import requests
from threading import Thread

# สีสำหรับ output
class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_colored(text, color=Colors.NC):
    print(f"{color}{text}{Colors.NC}")

def check_command(command):
    """ตรวจสอบว่าคำสั่งมีอยู่หรือไม่"""
    try:
        subprocess.run(['which', command], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def start_backend(port=8000):
    """เริ่ม backend server"""
    print_colored(f"📦 Starting FastAPI backend on port {port}...", Colors.GREEN)
    
    # เปลี่ยนไปที่ directory ของ script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # เริ่ม uvicorn
    process = subprocess.Popen(
        [sys.executable, '-m', 'uvicorn', 'main:app', '--host', '0.0.0.0', '--port', str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # รอให้ backend เริ่มทำงาน
    time.sleep(3)
    
    # ตรวจสอบว่า process ยังทำงานอยู่
    if process.poll() is not None:
        stdout, stderr = process.communicate()
        print_colored("❌ Backend ไม่สามารถเริ่มทำงานได้", Colors.RED)
        print(stderr.decode())
        return None
    
    print_colored(f"✅ Backend started (PID: {process.pid})", Colors.GREEN)
    return process

def start_ngrok(port=8000):
    """เริ่ม ngrok tunnel"""
    if not check_command('ngrok'):
        print_colored("❌ ngrok ไม่ได้ติดตั้ง", Colors.RED)
        print_colored("ติดตั้ง: brew install ngrok/ngrok/ngrok (macOS) หรือดูที่ https://ngrok.com/download", Colors.YELLOW)
        return None, None
    
    print_colored("🌐 Starting ngrok tunnel...", Colors.GREEN)
    
    # เริ่ม ngrok
    process = subprocess.Popen(
        ['ngrok', 'http', str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # รอให้ ngrok เริ่มทำงาน
    time.sleep(3)
    
    # ดึง public URL จาก ngrok API
    try:
        response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
        data = response.json()
        tunnels = data.get('tunnels', [])
        if tunnels:
            public_url = tunnels[0].get('public_url')
            if public_url:
                return process, public_url
    except Exception as e:
        print_colored(f"⚠️  ไม่สามารถดึง ngrok URL ได้: {e}", Colors.YELLOW)
        print_colored("ลองเปิด http://localhost:4040 เพื่อดู URL", Colors.YELLOW)
    
    return process, None

def start_cloudflare(port=8000):
    """เริ่ม Cloudflare Tunnel"""
    if not check_command('cloudflared'):
        print_colored("❌ cloudflared ไม่ได้ติดตั้ง", Colors.RED)
        print_colored("ติดตั้ง: brew install cloudflare/cloudflare/cloudflared (macOS)", Colors.YELLOW)
        print_colored("หรือดูที่: https://github.com/cloudflare/cloudflared/releases", Colors.YELLOW)
        return None, None
    
    print_colored("🌐 Starting Cloudflare Tunnel...", Colors.GREEN)
    
    # เริ่ม cloudflared
    process = subprocess.Popen(
        ['cloudflared', 'tunnel', '--url', f'http://localhost:{port}'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    
    # รอให้ tunnel เริ่มทำงาน
    time.sleep(5)
    
    # อ่าน output เพื่อหา URL
    try:
        # อ่าน output จาก process
        output_lines = []
        for _ in range(20):  # อ่าน 20 บรรทัดแรก
            line = process.stdout.readline()
            if not line:
                break
            output_lines.append(line.decode('utf-8', errors='ignore'))
        
        output = ''.join(output_lines)
        
        # หา URL จาก output
        import re
        url_match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', output)
        if url_match:
            return process, url_match.group(0)
    except Exception as e:
        print_colored(f"⚠️  ไม่สามารถดึง Cloudflare URL ได้: {e}", Colors.YELLOW)
    
    return process, None

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Start backend with tunnel')
    parser.add_argument('--tunnel', choices=['ngrok', 'cloudflare'], default='cloudflare',
                       help='เลือก tunnel service (default: cloudflare)')
    parser.add_argument('--port', type=int, default=8000,
                       help='Port สำหรับ backend (default: 8000)')
    
    args = parser.parse_args()
    
    print_colored("🚀 Starting Backend with Tunnel", Colors.GREEN)
    print_colored("═══════════════════════════════════════════════════════", Colors.GREEN)
    print()
    
    # เริ่ม backend
    backend_process = start_backend(args.port)
    if not backend_process:
        sys.exit(1)
    
    # เริ่ม tunnel
    tunnel_process = None
    tunnel_url = None
    
    if args.tunnel == 'ngrok':
        tunnel_process, tunnel_url = start_ngrok(args.port)
    else:
        tunnel_process, tunnel_url = start_cloudflare(args.port)
    
    if not tunnel_process:
        print_colored("❌ ไม่สามารถเริ่ม tunnel ได้", Colors.RED)
        backend_process.terminate()
        sys.exit(1)
    
    if not tunnel_url:
        print_colored("⚠️  ไม่สามารถดึง tunnel URL ได้", Colors.YELLOW)
        print_colored("ลองตรวจสอบ tunnel process หรือดู log", Colors.YELLOW)
        tunnel_url = "ไม่ทราบ URL"
    
    # แสดงผลลัพธ์
    print()
    print_colored("═══════════════════════════════════════════════════════", Colors.GREEN)
    print_colored("✅ Tunnel พร้อมใช้งาน!", Colors.GREEN)
    print()
    print_colored(f"🌐 Public URL: {tunnel_url}", Colors.YELLOW)
    print()
    print_colored("📝 ตั้งค่าใน Frontend:", Colors.YELLOW)
    print_colored(f"   BACKEND_URL={tunnel_url}", Colors.BLUE)
    print()
    print_colored("📋 API Endpoints:", Colors.YELLOW)
    print_colored(f"   - Health Check: {tunnel_url}/api/health", Colors.BLUE)
    print_colored(f"   - API Docs: {tunnel_url}/docs", Colors.BLUE)
    print()
    print_colored("🛑 กด Ctrl+C เพื่อหยุด", Colors.YELLOW)
    print_colored("═══════════════════════════════════════════════════════", Colors.GREEN)
    print()
    
    # Function สำหรับ cleanup
    def cleanup(signum, frame):
        print()
        print_colored("🛑 กำลังหยุด services...", Colors.YELLOW)
        backend_process.terminate()
        tunnel_process.terminate()
        print_colored("✅ หยุดเรียบร้อย", Colors.GREEN)
        sys.exit(0)
    
    # จับ signal
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    
    # รอให้ user กด Ctrl+C
    try:
        backend_process.wait()
    except KeyboardInterrupt:
        cleanup(None, None)

if __name__ == '__main__':
    main()

