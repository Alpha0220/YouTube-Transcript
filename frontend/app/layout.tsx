import type { Metadata } from 'next'
import './globals.css'
import Navbar from '@/components/Navbar'

export const metadata: Metadata = {
  title: 'Limitless Knowledge Getter',
  description: 'Download YouTube video transcripts',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="th">
      <body>
        <Navbar />
        {children}
      </body>
    </html>
  )
}

