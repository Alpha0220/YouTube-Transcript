#!/bin/bash
# Script สำหรับรัน Backend ด้วย Docker + Cloudflare Tunnel

set -e

# สีสำหรับ output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🐳 Starting Backend with Docker + Cloudflare Tunnel${NC}"
echo ""

# ตรวจสอบว่า Docker ติดตั้งหรือยัง
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker ไม่ได้ติดตั้ง${NC}"
    echo "ติดตั้ง Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# ตรวจสอบว่า Docker daemon กำลังรันอยู่
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker daemon ไม่ได้รัน${NC}"
    echo "รัน: sudo systemctl start docker"
    exit 1
fi

cd "$(dirname "$0")"

# หยุด containers เดิม (ถ้ามี)
echo -e "${YELLOW}🧹 Cleaning up old containers...${NC}"
docker compose down 2>/dev/null || true

# Build และ Start
echo -e "${YELLOW}🔨 Building and starting containers...${NC}"
docker compose up -d --build

# รอให้ services พร้อม
echo -e "${YELLOW}⏳ Waiting for services to be ready...${NC}"
sleep 10

# ตรวจสอบว่า backend ทำงาน
echo -e "${YELLOW}🔍 Checking backend health...${NC}"
if curl -s http://localhost:8000/api/health | grep -q "healthy"; then
    echo -e "${GREEN}✅ Backend is healthy${NC}"
else
    echo -e "${RED}❌ Backend health check failed${NC}"
    echo "ตรวจสอบ log: docker compose logs backend"
    exit 1
fi

# รอให้ cloudflared สร้าง tunnel
echo -e "${YELLOW}🌐 Waiting for Cloudflare Tunnel...${NC}"
sleep 10

# ดึง URL จาก cloudflared logs
CLOUDFLARE_URL=$(docker compose logs cloudflared 2>&1 | grep -o 'https://[^ ]*\.trycloudflare\.com' | head -1)

if [ -z "$CLOUDFLARE_URL" ]; then
    echo -e "${YELLOW}⏳ Tunnel กำลังสร้าง... รอเพิ่มอีก 10 วินาที${NC}"
    sleep 10
    CLOUDFLARE_URL=$(docker compose logs cloudflared 2>&1 | grep -o 'https://[^ ]*\.trycloudflare\.com' | head -1)
fi

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"

if [ -n "$CLOUDFLARE_URL" ]; then
    echo -e "${GREEN}✅ Services พร้อมใช้งาน!${NC}"
    echo ""
    echo -e "${YELLOW}🌐 Public URL:${NC} ${GREEN}$CLOUDFLARE_URL${NC}"
    echo ""
    echo -e "${YELLOW}📝 ตั้งค่าใน Frontend (Vercel):${NC}"
    echo "   NEXT_PUBLIC_API_URL=$CLOUDFLARE_URL"
    echo ""
    echo -e "${YELLOW}📋 API Endpoints:${NC}"
    echo "   - Health Check: $CLOUDFLARE_URL/api/health"
    echo "   - API Docs: $CLOUDFLARE_URL/docs"
    echo "   - Local: http://localhost:8000"
else
    echo -e "${YELLOW}⚠️  ไม่สามารถดึง Tunnel URL ได้อัตโนมัติ${NC}"
    echo "ดู URL ด้วยคำสั่ง:"
    echo "   docker compose logs cloudflared | grep trycloudflare.com"
fi

echo ""
echo -e "${YELLOW}🛑 หยุด services:${NC}"
echo "   docker compose down"
echo ""
echo -e "${YELLOW}📜 ดู logs:${NC}"
echo "   docker compose logs -f"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"

