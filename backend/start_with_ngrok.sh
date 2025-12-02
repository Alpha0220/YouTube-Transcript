#!/bin/bash
# สคริปต์สำหรับรัน backend พร้อม ngrok tunnel
# ทำให้ frontend บน Vercel สามารถเข้าถึง backend ที่รันบนเครื่อง local ได้

set -e

# สีสำหรับ output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Backend with ngrok Tunnel${NC}"
echo ""

# ตรวจสอบว่า ngrok ติดตั้งหรือยัง
if ! command -v ngrok &> /dev/null; then
    echo -e "${RED}❌ ngrok ไม่ได้ติดตั้ง${NC}"
    echo ""
    echo "วิธีติดตั้ง ngrok:"
    echo "1. ดาวน์โหลดจาก https://ngrok.com/download"
    echo "2. หรือใช้: curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo \"deb https://ngrok-agent.s3.amazonaws.com buster main\" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok"
    echo "3. หรือใช้: brew install ngrok/ngrok/ngrok (macOS)"
    echo ""
    echo "หลังจากติดตั้งแล้ว ต้อง:"
    echo "1. สมัครบัญชีที่ https://dashboard.ngrok.com (ฟรี)"
    echo "2. คัดลอก authtoken จาก dashboard"
    echo "3. รัน: ngrok config add-authtoken YOUR_TOKEN"
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

# เริ่ม ngrok tunnel
echo -e "${GREEN}🌐 Starting ngrok tunnel...${NC}"
ngrok http $BACKEND_PORT > /tmp/ngrok.log 2>&1 &
NGROK_PID=$!

# รอให้ ngrok เริ่มทำงาน
sleep 3

# ดึง public URL จาก ngrok API
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"https://[^"]*' | head -1 | cut -d'"' -f4)

if [ -z "$NGROK_URL" ]; then
    echo -e "${RED}❌ ไม่สามารถดึง ngrok URL ได้${NC}"
    echo "ตรวจสอบ log: cat /tmp/ngrok.log"
    kill $BACKEND_PID $NGROK_PID 2>/dev/null || true
    exit 1
fi

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Tunnel พร้อมใช้งาน!${NC}"
echo ""
echo -e "${YELLOW}🌐 Public URL:${NC} ${GREEN}$NGROK_URL${NC}"
echo ""
echo -e "${YELLOW}📝 ตั้งค่าใน Frontend:${NC}"
echo "   ใช้ URL นี้เป็น BACKEND_URL ใน frontend"
echo "   ตัวอย่าง: BACKEND_URL=$NGROK_URL"
echo ""
echo -e "${YELLOW}📋 API Endpoints:${NC}"
echo "   - Health Check: $NGROK_URL/api/health"
echo "   - API Docs: $NGROK_URL/docs"
echo ""
echo -e "${YELLOW}⚠️  หมายเหตุ:${NC}"
echo "   - URL นี้จะเปลี่ยนทุกครั้งที่รันใหม่ (เว้นแต่ใช้ ngrok paid plan)"
echo "   - ต้องอัพเดท BACKEND_URL ใน frontend ทุกครั้งที่ URL เปลี่ยน"
echo ""
echo -e "${YELLOW}🛑 กด Ctrl+C เพื่อหยุด tunnel และ backend${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo ""

# Function สำหรับ cleanup
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 กำลังหยุด services...${NC}"
    kill $BACKEND_PID $NGROK_PID 2>/dev/null || true
    echo -e "${GREEN}✅ หยุดเรียบร้อย${NC}"
    exit 0
}

# จับ signal สำหรับ cleanup
trap cleanup SIGINT SIGTERM

# รอให้ user กด Ctrl+C
wait

