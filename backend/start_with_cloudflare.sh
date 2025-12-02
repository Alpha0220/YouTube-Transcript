#!/bin/bash
# สคริปต์สำหรับรัน backend พร้อม Cloudflare Tunnel
# ทำให้ frontend บน Vercel สามารถเข้าถึง backend ที่รันบนเครื่อง local ได้
# ฟรีและ URL ไม่เปลี่ยน (ถ้าใช้ subdomain เดิม)

set -e

# สีสำหรับ output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Backend with Cloudflare Tunnel${NC}"
echo ""

# ตรวจสอบว่า cloudflared ติดตั้งหรือยัง
if ! command -v cloudflared &> /dev/null; then
    echo -e "${RED}❌ cloudflared ไม่ได้ติดตั้ง${NC}"
    echo ""
    echo "วิธีติดตั้ง cloudflared:"
    echo ""
    echo "Linux:"
    echo "  wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb"
    echo "  sudo dpkg -i cloudflared-linux-amd64.deb"
    echo ""
    echo "macOS:"
    echo "  brew install cloudflare/cloudflare/cloudflared"
    echo ""
    echo "หรือดาวน์โหลดจาก: https://github.com/cloudflare/cloudflared/releases"
    exit 1
fi

# ตรวจสอบว่า backend port ถูกใช้หรือยัง
BACKEND_PORT=${PORT:-8000}
if lsof -Pi :$BACKEND_PORT -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${YELLOW}⚠️  Port $BACKEND_PORT กำลังถูกใช้งาน${NC}"
    echo "กำลังปิด process ที่ใช้ port นี้..."
    lsof -ti:$BACKEND_PORT | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# เริ่ม backend ใน background
echo -e "${GREEN}📦 Starting FastAPI backend on port $BACKEND_PORT...${NC}"
cd "$(dirname "$0")"
python -m uvicorn main:app --host 0.0.0.0 --port $BACKEND_PORT > /tmp/backend.log 2>&1 &
BACKEND_PID=$!

# รอให้ backend เริ่มทำงาน
echo "รอให้ backend เริ่มทำงาน..."
sleep 3

# ตรวจสอบว่า backend ทำงานหรือไม่
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}❌ Backend ไม่สามารถเริ่มทำงานได้${NC}"
    echo "ตรวจสอบ log: cat /tmp/backend.log"
    exit 1
fi

echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"
echo ""

# เริ่ม Cloudflare Tunnel
echo -e "${GREEN}🌐 Starting Cloudflare Tunnel...${NC}"
echo -e "${BLUE}💡 Tip: ถ้ายังไม่ได้ login ให้รัน 'cloudflared tunnel login' ก่อน${NC}"
echo ""

# ใช้ quick tunnel (ฟรี, URL จะเปลี่ยนทุกครั้ง)
# หรือใช้ named tunnel (ฟรี, URL คงที่ - ต้อง setup ก่อน)
TUNNEL_MODE=${TUNNEL_MODE:-quick}

if [ "$TUNNEL_MODE" = "named" ]; then
    # Named tunnel (URL คงที่)
    TUNNEL_NAME=${TUNNEL_NAME:-youtube-transcript-backend}
    echo -e "${YELLOW}📝 ใช้ Named Tunnel: $TUNNEL_NAME${NC}"
    echo "   (URL จะคงที่ แต่ต้อง setup ก่อน)"
    cloudflared tunnel --protocol http2 --url http://localhost:$BACKEND_PORT > /tmp/cloudflared.log 2>&1 &
    CLOUDFLARED_PID=$!
else
    # Quick tunnel (URL เปลี่ยนทุกครั้ง แต่ setup ง่าย)
    echo -e "${YELLOW}📝 ใช้ Quick Tunnel${NC}"
    echo "   (URL จะเปลี่ยนทุกครั้งที่รันใหม่)"
    cloudflared tunnel --protocol http2 --url http://localhost:$BACKEND_PORT > /tmp/cloudflared.log 2>&1 &
    CLOUDFLARED_PID=$!
fi

# รอให้ tunnel เริ่มทำงาน (ต้องรอนานพอให้ได้ URL)
sleep 15

# ดึง public URL จาก log
CLOUDFLARE_URL=$(grep -o 'https://[^ ]*\.trycloudflare\.com' /tmp/cloudflared.log | head -1)

if [ -z "$CLOUDFLARE_URL" ]; then
    echo -e "${RED}❌ ไม่สามารถดึง Cloudflare Tunnel URL ได้${NC}"
    echo "ตรวจสอบ log: cat /tmp/cloudflared.log"
    kill $BACKEND_PID $CLOUDFLARED_PID 2>/dev/null || true
    exit 1
fi

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Tunnel พร้อมใช้งาน!${NC}"
echo ""
echo -e "${YELLOW}🌐 Public URL:${NC} ${GREEN}$CLOUDFLARE_URL${NC}"
echo ""
echo -e "${YELLOW}📝 ตั้งค่าใน Frontend:${NC}"
echo "   ใช้ URL นี้เป็น BACKEND_URL ใน frontend"
echo "   ตัวอย่าง: BACKEND_URL=$CLOUDFLARE_URL"
echo ""
echo -e "${YELLOW}📋 API Endpoints:${NC}"
echo "   - Health Check: $CLOUDFLARE_URL/api/health"
echo "   - API Docs: $CLOUDFLARE_URL/docs"
echo ""
echo -e "${YELLOW}💡 สำหรับ URL คงที่:${NC}"
echo "   1. สมัคร Cloudflare Zero Trust (ฟรี)"
echo "   2. สร้าง named tunnel"
echo "   3. ตั้งค่า subdomain"
echo "   4. ใช้ TUNNEL_MODE=named TUNNEL_NAME=your-tunnel-name"
echo ""
echo -e "${YELLOW}🛑 กด Ctrl+C เพื่อหยุด tunnel และ backend${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo ""

# Function สำหรับ cleanup
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 กำลังหยุด services...${NC}"
    kill $BACKEND_PID $CLOUDFLARED_PID 2>/dev/null || true
    echo -e "${GREEN}✅ หยุดเรียบร้อย${NC}"
    exit 0
}

# จับ signal สำหรับ cleanup
trap cleanup SIGINT SIGTERM

# รอให้ user กด Ctrl+C
wait

