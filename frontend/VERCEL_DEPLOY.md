# 🚀 คู่มือ Deploy Frontend ขึ้น Vercel แบบละเอียด

## 📋 สารบัญ
1. [เตรียมความพร้อม](#เตรียมความพร้อม)
2. [วิธีที่ 1: Deploy ผ่าน Vercel Dashboard (แนะนำ)](#วิธีที่-1-deploy-ผ่าน-vercel-dashboard-แนะนำ)
3. [วิธีที่ 2: Deploy ผ่าน Vercel CLI](#วิธีที่-2-deploy-ผ่าน-vercel-cli)
4. [ตั้งค่า Environment Variables](#ตั้งค่า-environment-variables)
5. [ตรวจสอบการ Deploy](#ตรวจสอบการ-deploy)
6. [แก้ไขปัญหา (Troubleshooting)](#แก้ไขปัญหา-troubleshooting)

---

## 🎯 เตรียมความพร้อม

### 1. ตรวจสอบไฟล์ที่จำเป็น

ตรวจสอบว่ามีไฟล์เหล่านี้อยู่แล้ว:
- ✅ `package.json` - มี scripts สำหรับ build
- ✅ `next.config.js` - Next.js configuration
- ✅ `vercel.json` - Vercel configuration (optional)
- ✅ `.gitignore` - Git ignore file

### 2. ตรวจสอบว่าโค้ดพร้อม Deploy

```bash
cd frontend

# ติดตั้ง dependencies
pnpm install

# ทดสอบ build ในเครื่อง
pnpm run build

# ทดสอบ production build
pnpm start
```

ถ้า build สำเร็จ แสดงว่าโค้ดพร้อม deploy แล้ว ✅

---

## 🌐 วิธีที่ 1: Deploy ผ่าน Vercel Dashboard (แนะนำ)

### ขั้นตอนที่ 1: สร้างบัญชี Vercel

1. ไปที่ [vercel.com](https://vercel.com)
2. คลิก **Sign Up**
3. เลือกวิธี Sign Up:
   - **GitHub** (แนะนำ) - เชื่อมต่อกับ GitHub account
   - **GitLab** - เชื่อมต่อกับ GitLab account
   - **Bitbucket** - เชื่อมต่อกับ Bitbucket account
   - **Email** - สมัครด้วย email

### ขั้นตอนที่ 2: Push โค้ดขึ้น Git Repository

**ถ้ายังไม่มี Git repository:**

```bash
cd frontend

# สร้าง Git repository (ถ้ายังไม่มี)
git init

# เพิ่มไฟล์ทั้งหมด
git add .

# Commit
git commit -m "Initial commit: Next.js + TypeScript + Tailwind"

# สร้าง repository บน GitHub/GitLab/Bitbucket แล้ว push
git remote add origin <YOUR_REPO_URL>
git branch -M main
git push -u origin main
```

**ถ้ามี Git repository อยู่แล้ว:**

```bash
cd frontend
git add .
git commit -m "Ready for Vercel deployment"
git push
```

### ขั้นตอนที่ 3: Import Project ใน Vercel

1. หลังจาก Sign In เข้า Vercel Dashboard
2. คลิก **Add New...** → **Project**
3. เลือก Git Provider (GitHub/GitLab/Bitbucket)
4. Authorize Vercel ให้เข้าถึง repository
5. เลือก repository ที่ต้องการ deploy
6. คลิก **Import**

### ขั้นตอนที่ 4: ตั้งค่า Project

Vercel จะ auto-detect Next.js อัตโนมัติ แต่ตรวจสอบการตั้งค่าดังนี้:

**Project Settings:**
- **Framework Preset:** Next.js (auto-detected)
- **Root Directory:** `frontend` (ถ้า repo อยู่ที่ root) หรือ `.` (ถ้า repo คือ frontend folder)
- **Build Command:** `pnpm run build` (หรือ `npm run build`)
- **Output Directory:** `.next` (auto-detected)
- **Install Command:** `pnpm install` (หรือ `npm install`)

**ถ้าโปรเจกต์อยู่ที่ `/frontend` ใน repo:**
- ตั้งค่า **Root Directory** เป็น `frontend`

### ขั้นตอนที่ 5: ตั้งค่า Environment Variables

1. ในหน้า Project Settings → **Environment Variables**
2. เพิ่มตัวแปรต่อไปนี้:

```
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

**ตัวอย่าง:**
- Development: `http://localhost:8000`
- Production: `https://your-backend-api.vercel.app` หรือ `https://api.yourdomain.com`

3. เลือก **Environment:**
   - ✅ Production
   - ✅ Preview
   - ✅ Development (optional)

4. คลิก **Save**

### ขั้นตอนที่ 6: Deploy

1. คลิก **Deploy**
2. รอให้ build เสร็จ (ประมาณ 1-3 นาที)
3. เมื่อเสร็จแล้ว จะได้ URL เช่น:
   - `https://your-project-name.vercel.app`

### ขั้นตอนที่ 7: ตั้งค่า Custom Domain (Optional)

1. ไปที่ Project → **Settings** → **Domains**
2. เพิ่ม domain ที่ต้องการ
3. ตั้งค่า DNS records ตามที่ Vercel แนะนำ
4. รอให้ DNS propagate (อาจใช้เวลา 24-48 ชั่วโมง)

---

## 💻 วิธีที่ 2: Deploy ผ่าน Vercel CLI

### ขั้นตอนที่ 1: ติดตั้ง Vercel CLI

```bash
# ติดตั้ง Vercel CLI แบบ global
npm install -g vercel

# หรือใช้ pnpm
pnpm add -g vercel
```

### ขั้นตอนที่ 2: Login เข้า Vercel

```bash
vercel login
```

จะเปิด browser ให้ login หรือใช้ email

### ขั้นตอนที่ 3: Deploy

```bash
cd frontend

# Deploy ครั้งแรก (Production)
vercel

# หรือ deploy แบบ production โดยตรง
vercel --prod
```

**คำถามที่ Vercel CLI จะถาม:**
1. **Set up and deploy?** → `Y`
2. **Which scope?** → เลือก account ของคุณ
3. **Link to existing project?** → `N` (ถ้าเป็นครั้งแรก)
4. **What's your project's name?** → พิมพ์ชื่อโปรเจกต์ หรือกด Enter
5. **In which directory is your code located?** → `./` หรือ `frontend`
6. **Want to override the settings?** → `N` (ถ้าใช้ default)

### ขั้นตอนที่ 4: ตั้งค่า Environment Variables

```bash
# เพิ่ม environment variable
vercel env add NEXT_PUBLIC_API_URL

# เลือก environment (Production, Preview, Development)
# ใส่ค่า: https://your-backend-url.com
```

หรือตั้งค่าผ่าน Dashboard ก็ได้ (แนะนำ)

### ขั้นตอนที่ 5: Redeploy

```bash
# Redeploy production
vercel --prod
```

---

## ⚙️ ตั้งค่า Environment Variables

### Environment Variables ที่ต้องตั้งค่า:

| Variable Name | Description | Example |
|--------------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | URL ของ Backend API | `https://api.example.com` |

### วิธีตั้งค่า:

**ผ่าน Dashboard:**
1. Project → **Settings** → **Environment Variables**
2. เพิ่ม variable
3. เลือก Environment (Production, Preview, Development)
4. **Save**

**ผ่าน CLI:**
```bash
vercel env add NEXT_PUBLIC_API_URL
```

**สำคัญ:** ต้อง redeploy หลังจากเพิ่ม environment variables

---

## ✅ ตรวจสอบการ Deploy

### 1. ตรวจสอบ Build Logs

1. ไปที่ Project → **Deployments**
2. คลิกที่ deployment ล่าสุด
3. ดู **Build Logs** ว่ามี error หรือไม่

### 2. ตรวจสอบ Runtime Logs

1. Project → **Deployments** → เลือก deployment
2. ดู **Runtime Logs** สำหรับ runtime errors

### 3. ทดสอบเว็บไซต์

1. เปิด URL ที่ Vercel ให้มา
2. ทดสอบฟีเจอร์ต่างๆ:
   - ✅ หน้าเว็บโหลดได้
   - ✅ Form ทำงานได้
   - ✅ API calls ไปที่ backend ได้
   - ✅ Download ไฟล์ได้

### 4. ตรวจสอบ Network Tab

1. เปิด Browser DevTools → **Network**
2. ตรวจสอบว่า API calls ไปที่ URL ที่ถูกต้อง
3. ตรวจสอบว่าไม่มี CORS errors

---

## 🔧 แก้ไขปัญหา (Troubleshooting)

### ปัญหา 1: Build Failed

**อาการ:** Build error ใน Vercel

**วิธีแก้:**
```bash
# ทดสอบ build ในเครื่องก่อน
cd frontend
pnpm install
pnpm run build

# ถ้ามี error ให้แก้ไขก่อน deploy
```

**สาเหตุที่พบบ่อย:**
- Dependencies ไม่ครบ → ตรวจสอบ `package.json`
- TypeScript errors → แก้ไข type errors
- Environment variables ไม่ครบ → เพิ่มใน Vercel

### ปัญหา 2: 404 Not Found

**อาการ:** หน้าเว็บแสดง 404

**วิธีแก้:**
- ตรวจสอบว่าใช้ Next.js App Router ถูกต้อง
- ตรวจสอบ `next.config.js` ว่าถูกต้อง
- ตรวจสอบ routing ในโค้ด

### ปัญหา 3: API Calls ไม่ทำงาน

**อาการ:** API calls ไปที่ backend ไม่ได้

**วิธีแก้:**
1. ตรวจสอบ `NEXT_PUBLIC_API_URL` ใน Environment Variables
2. ตรวจสอบว่า backend URL ถูกต้องและ accessible
3. ตรวจสอบ CORS settings ใน backend
4. ดู Network tab ใน Browser DevTools

### ปัญหา 4: Environment Variables ไม่ทำงาน

**อาการ:** Environment variables ไม่ถูกใช้

**วิธีแก้:**
1. ตรวจสอบว่า variable name ถูกต้อง (ต้องมี `NEXT_PUBLIC_` prefix)
2. Redeploy หลังจากเพิ่ม environment variables
3. ตรวจสอบใน Runtime Logs

### ปัญหา 5: Images ไม่แสดง

**อาการ:** Logo หรือ images ไม่แสดง

**วิธีแก้:**
1. ตรวจสอบว่าไฟล์อยู่ใน `public/` folder
2. ใช้ Next.js Image component
3. ตรวจสอบ path ของ image

---

## 📝 Checklist ก่อน Deploy

- [ ] ✅ Build สำเร็จในเครื่อง (`pnpm run build`)
- [ ] ✅ Production build ทำงานได้ (`pnpm start`)
- [ ] ✅ Environment variables ตั้งค่าแล้ว
- [ ] ✅ Backend API URL ถูกต้อง
- [ ] ✅ Git repository พร้อมแล้ว
- [ ] ✅ ไม่มี TypeScript errors
- [ ] ✅ ไม่มี console errors

---

## 🎉 หลังจาก Deploy สำเร็จ

### Automatic Deployments

Vercel จะ auto-deploy เมื่อ:
- ✅ Push code ไปที่ `main` branch → Production
- ✅ Push code ไปที่ branch อื่น → Preview
- ✅ สร้าง Pull Request → Preview

### Monitoring

- **Analytics:** Project → **Analytics**
- **Logs:** Project → **Deployments** → เลือก deployment → **Logs**
- **Performance:** Project → **Speed Insights**

---

## 📚 เอกสารเพิ่มเติม

- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)

---

## 💡 Tips

1. **ใช้ Preview Deployments:** ทดสอบก่อน deploy production
2. **ตั้งค่า Custom Domain:** ทำให้ดูเป็นมืออาชีพมากขึ้น
3. **Monitor Performance:** ใช้ Vercel Analytics
4. **ตั้งค่า CI/CD:** Auto-deploy เมื่อ push code
5. **Backup Environment Variables:** บันทึกไว้ที่ปลอดภัย

---

**Happy Deploying! 🚀**

