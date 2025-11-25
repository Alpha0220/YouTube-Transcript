import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

const API_BASE_URL = 'http://localhost:8000'

// Configure axios defaults
axios.defaults.headers.common['Content-Type'] = 'application/json'
axios.defaults.headers.common['Accept'] = 'application/json'

function App() {
  const [url, setUrl] = useState('')
  const [selectedLanguage, setSelectedLanguage] = useState('en')
  const [fileFormat, setFileFormat] = useState('txt')
  const [includeTimestamps, setIncludeTimestamps] = useState(true)
  const [preserveFormatting, setPreserveFormatting] = useState(false)
  const [loading, setLoading] = useState(false)
  const [loadingLanguages, setLoadingLanguages] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)
  const [availableLanguages, setAvailableLanguages] = useState([])
  const [previewData, setPreviewData] = useState(null)

  // ดึงรายการ transcript เมื่อ URL เปลี่ยนและเปิด dropdown
  const fetchAvailableLanguages = async () => {
    if (!url.trim()) {
      setError('กรุณากรอก YouTube URL หรือ Video ID ก่อน')
      return
    }

    setLoadingLanguages(true)
    setError(null)

    try {
      const response = await axios.post(`${API_BASE_URL}/api/transcripts/list`, {
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
    } catch (err) {
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
      const response = await axios.post(`${API_BASE_URL}/api/transcripts/preview`, {
        url: url.trim(),
        languages: [selectedLanguage],
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
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'เกิดข้อผิดพลาด')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>YouTube Transcript</h1>
        </header>

        <div className="card">
          <div className="form-group">
            <label htmlFor="url">YouTube URL</label>
            <input
              id="url"
              type="text"
              placeholder="https://www.youtube.com/watch?v=..."
              value={url}
              onChange={(e) => {
                setUrl(e.target.value)
                setAvailableLanguages([]) // Reset เมื่อ URL เปลี่ยน
                setPreviewData(null)
              }}
              disabled={loading}
              className="input-url"
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="language">ภาษา</label>
              <select
                id="language"
                value={selectedLanguage}
                onChange={(e) => setSelectedLanguage(e.target.value)}
                onFocus={handleLanguageDropdownFocus}
                disabled={loading || loadingLanguages || !url.trim()}
                className="select-language"
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
                <small className="hint">
                  {availableLanguages.find(l => l.language_code === selectedLanguage)?.is_generated 
                    ? '🤖 สร้างอัตโนมัติ' 
                    : '✍️ สร้างด้วยมือ'}
                </small>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="fileFormat">รูปแบบไฟล์</label>
              <select
                id="fileFormat"
                value={fileFormat}
                onChange={(e) => setFileFormat(e.target.value)}
                disabled={loading}
                className="select-format"
              >
                <option value="txt">TXT</option>
                <option value="pdf">PDF</option>
                <option value="docx">DOCX</option>
              </select>
            </div>
          </div>

          <div className="options-row">
            <label className="checkbox-option">
              <input
                type="checkbox"
                checked={includeTimestamps}
                onChange={(e) => setIncludeTimestamps(e.target.checked)}
                disabled={loading}
              />
              <span>รวม Timestamps</span>
            </label>

            <label className="checkbox-option">
              <input
                type="checkbox"
                checked={preserveFormatting}
                onChange={(e) => setPreserveFormatting(e.target.checked)}
                disabled={loading}
              />
              <span>เก็บ HTML Formatting</span>
            </label>
          </div>

          {error && (
            <div className="alert alert-error">
              {error}
            </div>
          )}

          {success && (
            <div className="alert alert-success">
              {success}
            </div>
          )}

          <div className="button-group">
            <button
              type="button"
              onClick={handlePreview}
              disabled={loading || !url.trim()}
              className="btn btn-preview"
            >
              {loading ? 'กำลังโหลด...' : 'Preview'}
            </button>

            <button
              type="button"
              onClick={handleDownload}
              disabled={loading || !url.trim()}
              className="btn btn-download"
            >
              {loading ? 'กำลังดาวน์โหลด...' : 'Download'}
            </button>
          </div>
        </div>

        {previewData && (
          <div className="card preview-card">
            <div className="preview-header">
              <h2>Preview</h2>
              <div className="preview-meta">
                <span>{previewData.language}</span>
                <span>•</span>
                <span>{previewData.total_snippets} snippets</span>
              </div>
            </div>
            <div className="preview-content">
              {previewData.snippets.map((snippet, index) => (
                <div key={index} className="snippet">
                  <span className="timestamp">
                    {Math.floor(snippet.start / 60)}:{(Math.floor(snippet.start % 60)).toString().padStart(2, '0')}
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
