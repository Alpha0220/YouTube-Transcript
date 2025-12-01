'use client'

import Image from "next/image"

export default function Navbar() {
  return (
    <nav className="sticky top-0 z-50 bg-card border-b border-border shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-8">
            <Image src="/assets/limitless-logo.jpg" alt="Limitless Knowledge Getter" width={80} height={80} />
            <h1 className="text-2xl font-bold text-foreground">
              Limitless Knowledge Getter
            </h1>
          </div>
          <div className="flex items-center gap-4">
            {/* สามารถเพิ่มเมนูอื่นๆ ได้ที่นี่ */}
          </div>
        </div>
      </div>
    </nav>
  )
}

