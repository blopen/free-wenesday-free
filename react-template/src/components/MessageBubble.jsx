import React, { useState, useEffect } from 'react'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

marked.setOptions({ breaks: true, gfm: true })

function formatTime(iso) {
  try {
    return new Date(iso).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } catch {
    return ''
  }
}

export default function MessageBubble({ message }) {
  const { role, content, ts, model } = message
  const isUser = role === 'user'
  const [copied, setCopied] = useState(false)

  const html = DOMPurify.sanitize(marked.parse(content || ''))

  const copy = () => {
    navigator.clipboard.writeText(content).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 1500)
    })
  }

  return (
    <div className={`message message--${role}`}>
      <div className="message__avatar">{isUser ? '🧑' : 'W'}</div>
      <div className="message__body">
        <div className="message__meta">
          <span className="message__author">{isUser ? 'You' : model ?? 'Wenesday'}</span>
          <span className="message__time">{formatTime(ts)}</span>
        </div>
        <div
          className="message__content"
          dangerouslySetInnerHTML={{ __html: html }}
        />
        <button className="message__copy-btn" onClick={copy} title="Copy">
          {copied ? '✓ Copied' : '⎘ Copy'}
        </button>
      </div>
    </div>
  )
}
