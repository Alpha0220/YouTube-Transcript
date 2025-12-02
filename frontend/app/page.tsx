'use client'

import { useState } from 'react'
import axios from 'axios'

// รองรับ environment variable สำหรับ production
// ลบ trailing slash เพื่อหลีกเลี่ยง double slash ใน URL
const API_BASE_URL = (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000').replace(/\/+$/, '')

// Configure axios defaults
axios.defaults.headers.common['Content-Type'] = 'application/json'
axios.defaults.headers.common['Accept'] = 'application/json'

interface Transcript {
  language: string
  language_code: string
  is_generated: boolean
}

interface PreviewData {
  language: string
  total_snippets: number
  snippets: Array<{
    start: number
    text: string
  }>
}

export default function Home() {
  const [url, setUrl] = useState('')
  const [selectedLanguage, setSelectedLanguage] = useState('en')
  const [fileFormat, setFileFormat] = useState('txt')
  const [includeTimestamps, setIncludeTimestamps] = useState(true)
  const [preserveFormatting, setPreserveFormatting] = useState(false)
  const [loading, setLoading] = useState(false)
  const [loadingLanguages, setLoadingLanguages] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [availableLanguages, setAvailableLanguages] = useState<Transcript[]>([])
  const [previewData, setPreviewData] = useState<PreviewData | null>(null)

  // ดึงรายการ transcript เมื่อ URL เปลี่ยนและเปิด dropdown
  const fetchAvailableLanguages = async () => {
    if (!url.trim()) {
      setError('กรุณากรอก YouTube URL หรือ Video ID ก่อน')
      return
    }

    setLoadingLanguages(true)
    setError(null)

    try {
      const response = await axios.post<{ transcripts: Transcript[] }>(`${API_BASE_URL}/api/transcripts/list`, {
        url: url.trim()
      })

      const transcripts = response.data.transcripts || []
      setAvailableLanguages(transcripts)
      
      // ถ้ายังไม่มี selectedLanguage หรือ selectedLanguage ไม่มีในรายการ ให้เลือกภาษาแรก
      if (transcripts.length > 0) {
        const hasSelected = transcripts.some(t => t.language_code === selectedLanguage)
        if (!hasSelected) {
          setSelectedLanguage(transcripts[0].language_code)
        }
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'ไม่สามารถดึงรายการ transcript ได้')
      setAvailableLanguages([])
    } finally {
      setLoadingLanguages(false)
    }
  }

  const handleLanguageDropdownFocus = () => {
    if (url.trim() && availableLanguages.length === 0) {
      fetchAvailableLanguages()
    }
  }

  const handlePreview = async () => {
    if (!url.trim()) {
      setError('กรุณากรอก YouTube URL หรือ Video ID')
      return
    }

    setLoading(true)
    setError(null)
    setSuccess(null)

    try {
      const response = await axios.post<PreviewData>(`${API_BASE_URL}/api/transcripts/preview`, {
        url: url.trim(),
        languages: [selectedLanguage],
        preserve_formatting: preserveFormatting
      })

      setPreviewData(response.data)
      setSuccess('ดึงข้อมูลสำเร็จ!')
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'เกิดข้อผิดพลาด')
      setPreviewData(null)
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = async () => {
    if (!url.trim()) {
      setError('กรุณากรอก YouTube URL หรือ Video ID')
      return
    }

    setLoading(true)
    setError(null)
    setSuccess(null)

    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/transcripts/download`,
        {
          url: url.trim(),
          languages: [selectedLanguage],
          preserve_formatting: preserveFormatting,
          file_format: fileFormat,
          include_timestamps: includeTimestamps
        },
        {
          responseType: 'blob'
        }
      )

      // สร้าง download link
      const blob = new Blob([response.data])
      const downloadUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = downloadUrl
      
      // ดึง filename จาก Content-Disposition header
      const contentDisposition = response.headers['content-disposition']
      let filename = `transcript.${fileFormat}`
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/i)
        if (filenameMatch) {
          filename = filenameMatch[1]
        }
      }
      
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(downloadUrl)

      setSuccess(`ดาวน์โหลดไฟล์ ${filename} สำเร็จ!`)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'เกิดข้อผิดพลาด')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background py-10 px-5">
      <div className="max-w-7xl mx-auto">
        {/* <header className="text-center text-foreground mb-10">
          <h1 className="text-4xl font-semibold tracking-tight">Limitless Knowledge Getter</h1>
          <p className="text-muted-foreground mt-2">Download YouTube video transcripts</p>
        </header> */}

        <div className="bg-card text-card-foreground rounded-xl border border-border p-10 mb-5 shadow-sm">
          <div className="mb-6">
            <label htmlFor="url" className="block mb-2 font-medium text-foreground text-sm">
              YouTube URL
            </label>
            <input
              id="url"
              type="text"
              placeholder="https://www.youtube.com/watch?v=..."
              value={url}
              onChange={(e) => {
                setUrl(e.target.value)
                setAvailableLanguages([])
                setPreviewData(null)
              }}
              disabled={loading}
              className="w-full px-4 py-3 border border-border rounded-lg text-base transition-all bg-input text-foreground disabled:bg-muted disabled:cursor-not-allowed disabled:opacity-50 focus:outline-none focus:border-ring focus:ring-2 focus:ring-ring/20"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-6">
            <div>
              <label htmlFor="language" className="block mb-2 font-medium text-foreground text-sm">
                ภาษา
              </label>
              <select
                id="language"
                value={selectedLanguage}
                onChange={(e) => setSelectedLanguage(e.target.value)}
                onFocus={handleLanguageDropdownFocus}
                disabled={loading || loadingLanguages || !url.trim()}
                className="w-full px-4 py-3 border border-border rounded-lg text-base transition-all bg-input text-foreground disabled:bg-muted disabled:cursor-not-allowed disabled:opacity-50 focus:outline-none focus:border-ring focus:ring-2 focus:ring-ring/20"
              >
                {loadingLanguages ? (
                  <option>กำลังโหลด...</option>
                ) : availableLanguages.length > 0 ? (
                  availableLanguages.map((lang) => (
                    <option key={lang.language_code} value={lang.language_code}>
                      {lang.language} {lang.is_generated ? '(Auto)' : ''}
                    </option>
                  ))
                ) : (
                  <option value="en">English</option>
                )}
              </select>
              {availableLanguages.length > 0 && (
                <small className="block mt-1.5 text-muted-foreground text-sm">
                  {availableLanguages.find(l => l.language_code === selectedLanguage)?.is_generated 
                    ? '🤖 สร้างอัตโนมัติ' 
                    : '✍️ สร้างด้วยมือ'}
                </small>
              )}
            </div>

            <div>
              <label htmlFor="fileFormat" className="block mb-2 font-medium text-foreground text-sm">
                รูปแบบไฟล์
              </label>
              <select
                id="fileFormat"
                value={fileFormat}
                onChange={(e) => setFileFormat(e.target.value)}
                disabled={loading}
                className="w-full px-4 py-3 border border-border rounded-lg text-base transition-all bg-input text-foreground disabled:bg-muted disabled:cursor-not-allowed disabled:opacity-50 focus:outline-none focus:border-ring focus:ring-2 focus:ring-ring/20"
              >
                <option value="txt">TXT</option>
                <option value="pdf">PDF</option>
                <option value="docx">DOCX</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-6 p-5 bg-muted rounded-lg border border-border">
            <label className="flex items-center gap-2.5 cursor-pointer text-base font-medium text-foreground p-2 rounded transition-colors hover:bg-white/50">
              <input
                type="checkbox"
                checked={includeTimestamps}
                onChange={(e) => setIncludeTimestamps(e.target.checked)}
                disabled={loading}
                className="w-5 h-5 cursor-pointer accent-primary flex-shrink-0 disabled:cursor-not-allowed disabled:opacity-50"
              />
              <span className="select-none">รวม Timestamps</span>
            </label>

            <label className="flex items-center gap-2.5 cursor-pointer text-base font-medium text-foreground p-2 rounded transition-colors hover:bg-white/50">
              <input
                type="checkbox"
                checked={preserveFormatting}
                onChange={(e) => setPreserveFormatting(e.target.checked)}
                disabled={loading}
                className="w-5 h-5 cursor-pointer accent-primary flex-shrink-0 disabled:cursor-not-allowed disabled:opacity-50"
              />
              <span className="select-none">เก็บ HTML Formatting</span>
            </label>
          </div>

          {error && (
            <div className="px-4 py-3 rounded-lg mb-5 text-sm bg-red-50 text-destructive border border-red-200">
              {error}
            </div>
          )}

          {success && (
            <div className="px-4 py-3 rounded-lg mb-5 text-sm bg-green-50 text-success border border-green-200">
              {success}
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-8">
            <button
              type="button"
              onClick={handlePreview}
              disabled={loading || !url.trim()}
              className="px-6 py-3.5 rounded-lg text-base font-semibold cursor-pointer transition-all bg-secondary text-secondary-foreground border border-border hover:bg-muted hover:border-border disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'กำลังโหลด...' : 'Preview'}
            </button>

            <button
              type="button"
              onClick={handleDownload}
              disabled={loading || !url.trim()}
              className="px-6 py-3.5 rounded-lg text-base font-semibold cursor-pointer transition-all bg-primary text-primary-foreground border border-primary hover:bg-primary-hover hover:border-primary-hover hover:shadow-lg hover:shadow-primary/20 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'กำลังดาวน์โหลด...' : 'Download'}
            </button>
          </div>
        </div>

        {previewData && (
          <div className="bg-card text-card-foreground rounded-xl border border-border p-10 mt-5 shadow-sm">
            <div className="flex justify-between items-center mb-6 pb-4 border-b border-border">
              <h2 className="text-2xl font-semibold text-foreground">Preview</h2>
              <div className="flex gap-2 text-muted-foreground text-sm">
                <span>{previewData.language}</span>
                <span>•</span>
                <span>{previewData.total_snippets} snippets</span>
              </div>
            </div>
            <div className="max-h-[600px] overflow-y-auto pr-2 scrollbar-thin">
              {previewData.snippets.map((snippet, index) => (
                <div key={index} className="mb-4 p-3 bg-muted rounded-lg border-l-4 border-primary flex gap-3">
                  <span className="text-primary text-sm font-semibold min-w-[50px] flex-shrink-0">
                    {Math.floor(snippet.start / 60)}:{(Math.floor(snippet.start % 60)).toString().padStart(2, '0')}
                  </span>
                  <span className="text-foreground leading-relaxed">{snippet.text}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

