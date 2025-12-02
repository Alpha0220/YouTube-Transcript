#!/bin/bash
# Script สำหรับหยุด Backend และ Cloudflare Tunnel

# สีสำหรับ output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🛑 Stopping YouTube Transcript Backend Services${NC}"
echo ""

# หยุด Cloudflare Tunnel
if pgrep -x "cloudflared" > /dev/null; then
    echo -e "${YELLOW}Stopping Cloudflare Tunnel...${NC}"
    pkill cloudflared
    echo -e "${GREEN}✅ Cloudflare Tunnel stopped${NC}"
else
    echo -e "${YELLOW}ℹ️  Cloudflare Tunnel is not running${NC}"
fi

# หยุด Backend (uvicorn)
if pgrep -f "uvicorn main:app" > /dev/null; then
    echo -e "${YELLOW}Stopping Backend (uvicorn)...${NC}"
    pkill -f "uvicorn main:app"
    echo -e "${GREEN}✅ Backend stopped${NC}"
else
    echo -e "${YELLOW}ℹ️  Backend is not running${NC}"
fi

# หยุด Docker containers (ถ้ามี)
if docker ps -q --filter "name=youtube-transcript" 2>/dev/null | grep -q .; then
    echo -e "${YELLOW}Stopping Docker containers...${NC}"
    docker compose down 2>/dev/null || docker-compose down 2>/dev/null
    echo -e "${GREEN}✅ Docker containers stopped${NC}"
fi

echo ""
echo -e "${GREEN}✅ All services stopped!${NC}"

