import React, { useState } from 'react'
import axios from 'axios'
import './App.css'

const API_BASE_URL = 'http://localhost:8000'

// Configure axios defaults
axios.defaults.headers.common['Content-Type'] = 'application/json'
axios.defaults.headers.common['Accept'] = 'application/json'

function App() {
  const [url, setUrl] = useState('')
  const [languages, setLanguages] = useState(['en'])
  const [fileFormat, setFileFormat] = useState('txt')
  const [includeTimestamps, setIncludeTimestamps] = useState(true)
  const [preserveFormatting, setPreserveFormatting] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)
  const [availableTranscripts, setAvailableTranscripts] = useState([])
  const [previewData, setPreviewData] = useState(null)

  const handleLanguageChange = (e) => {
    const value = e.target.value
    if (e.target.checked) {
      setLanguages([...languages, value])
    } else {
      setLanguages(languages.filter(lang => lang !== value))
    }
  }

  const handleListTranscripts = async () => {
    if (!url.trim()) {
      setError('กรุณากรอก YouTube URL หรือ Video ID')
      return
    }

    setLoading(true)
    setError(null)
    setSuccess(null)

    try {
      const response = await axios.post(`${API_BASE_URL}/api/transcripts/list`, {
        url: url.trim()
      })

      setAvailableTranscripts(response.data.transcripts || [])
      setSuccess(`พบ ${response.data.transcripts.length} transcript(s)`)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'เกิดข้อผิดพลาด')
      setAvailableTranscripts([])
    } finally {
      setLoading(false)
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
      const response = await axios.post(`${API_BASE_URL}/api/transcripts/preview`, {
        url: url.trim(),
        languages: languages.length > 0 ? languages : ['en'],
        preserve_formatting: preserveFormatting
      })

      setPreviewData(response.data)
      setSuccess('ดึงข้อมูลสำเร็จ!')
    } catch (err) {
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

    if (languages.length === 0) {
      setError('กรุณาเลือกภาษาอย่างน้อย 1 ภาษา')
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
          languages: languages,
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
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'เกิดข้อผิดพลาด')
    } finally {
      setLoading(false)
    }
  }

  const commonLanguages = [
    { code: 'en', name: 'English' },
    { code: 'th', name: 'Thai' },
    { code: 'zh', name: 'Chinese' },
    { code: 'ja', name: 'Japanese' },
    { code: 'ko', name: 'Korean' },
    { code: 'es', name: 'Spanish' },
    { code: 'fr', name: 'French' },
    { code: 'de', name: 'German' },
    { code: 'pt', name: 'Portuguese' },
    { code: 'ru', name: 'Russian' },
    { code: 'vi', name: 'Vietnamese' },
    { code: 'id', name: 'Indonesian' }
  ]

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>🎬 YouTube Transcript Downloader</h1>
          <p>ดึง transcript จาก YouTube และแปลงเป็นไฟล์ต่างๆ</p>
        </header>

        <div className="card">
          <div className="form-group">
            <label htmlFor="url">YouTube URL หรือ Video ID *</label>
            <input
              id="url"
              type="text"
              placeholder="https://www.youtube.com/watch?v=VIDEO_ID หรือ VIDEO_ID"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              disabled={loading}
            />
            <small>ตัวอย่าง: https://www.youtube.com/watch?v=dQw4w9WgXcQ</small>
          </div>

          <div className="form-group">
            <label>ภาษา (เลือกได้หลายภาษา)</label>
            <div className="language-grid">
              {commonLanguages.map((lang) => (
                <label key={lang.code} className="checkbox-label">
                  <input
                    type="checkbox"
                    value={lang.code}
                    checked={languages.includes(lang.code)}
                    onChange={handleLanguageChange}
                    disabled={loading}
                  />
                  <span>{lang.name} ({lang.code})</span>
                </label>
              ))}
            </div>
            <small>ระบบจะลองภาษาแรกก่อน ถ้าไม่มีจะใช้ภาษาถัดไป</small>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="fileFormat">รูปแบบไฟล์</label>
              <select
                id="fileFormat"
                value={fileFormat}
                onChange={(e) => setFileFormat(e.target.value)}
                disabled={loading}
              >
                <option value="txt">TXT (Text File)</option>
                <option value="pdf">PDF (Portable Document Format)</option>
                <option value="docx">DOCX (Microsoft Word)</option>
              </select>
            </div>

            <div className="form-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={includeTimestamps}
                  onChange={(e) => setIncludeTimestamps(e.target.checked)}
                  disabled={loading}
                />
                <span>รวม Timestamps</span>
              </label>
            </div>

            <div className="form-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={preserveFormatting}
                  onChange={(e) => setPreserveFormatting(e.target.checked)}
                  disabled={loading}
                />
                <span>เก็บ HTML Formatting</span>
              </label>
            </div>
          </div>

          {error && (
            <div className="alert alert-error">
              <strong>❌ ข้อผิดพลาด:</strong> {error}
            </div>
          )}

          {success && (
            <div className="alert alert-success">
              <strong>✅ สำเร็จ:</strong> {success}
            </div>
          )}

          <div className="button-group">
            <button
              type="button"
              onClick={handleListTranscripts}
              disabled={loading || !url.trim()}
              className="btn btn-secondary"
            >
              {loading ? 'กำลังโหลด...' : '📋 ดูรายการ Transcript'}
            </button>

            <button
              type="button"
              onClick={handlePreview}
              disabled={loading || !url.trim()}
              className="btn btn-secondary"
            >
              {loading ? 'กำลังโหลด...' : '👁️ Preview'}
            </button>

            <button
              type="button"
              onClick={handleDownload}
              disabled={loading || !url.trim() || languages.length === 0}
              className="btn btn-primary"
            >
              {loading ? 'กำลังดาวน์โหลด...' : `⬇️ ดาวน์โหลด (.${fileFormat.toUpperCase()})`}
            </button>
          </div>
        </div>

        {availableTranscripts.length > 0 && (
          <div className="card">
            <h2>📋 รายการ Transcript ที่มีให้</h2>
            <div className="transcript-list">
              {availableTranscripts.map((transcript, index) => (
                <div key={index} className="transcript-item">
                  <div className="transcript-header">
                    <strong>{transcript.language} ({transcript.language_code})</strong>
                    <span className={`badge ${transcript.is_generated ? 'badge-auto' : 'badge-manual'}`}>
                      {transcript.is_generated ? '🤖 สร้างอัตโนมัติ' : '✍️ สร้างด้วยมือ'}
                    </span>
                  </div>
                  {transcript.is_translatable && (
                    <small>สามารถแปลเป็น {transcript.translation_languages.length} ภาษา</small>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {previewData && (
          <div className="card">
            <h2>👁️ Preview Transcript</h2>
            <div className="preview-info">
              <p><strong>Video ID:</strong> {previewData.video_id}</p>
              <p><strong>ภาษา:</strong> {previewData.language} ({previewData.language_code})</p>
              <p><strong>จำนวน Snippets:</strong> {previewData.total_snippets}</p>
              <p><strong>สร้างอัตโนมัติ:</strong> {previewData.is_generated ? 'ใช่' : 'ไม่ใช่'}</p>
            </div>
            <div className="preview-content">
              <h3>เนื้อหา (แสดง 50 snippets แรก):</h3>
              {previewData.snippets.map((snippet, index) => (
                <div key={index} className="snippet">
                  <span className="timestamp">
                    [{Math.floor(snippet.start / 60)}:{(Math.floor(snippet.start % 60)).toString().padStart(2, '0')}]
                  </span>
                  <span className="text">{snippet.text}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App

