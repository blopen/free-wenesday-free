import React, { useRef, useEffect } from 'react'

export default function ChatInput({ onSend, loading, disabled }) {
  const ref = useRef(null)

  useEffect(() => {
    if (ref.current) {
      ref.current.style.height = 'auto'
      ref.current.style.height = Math.min(ref.current.scrollHeight, 200) + 'px'
    }
  })

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      submit()
    }
  }

  const submit = () => {
    const text = ref.current?.value.trim()
    if (!text || loading) return
    onSend(text)
    ref.current.value = ''
    ref.current.style.height = 'auto'
  }

  return (
    <div className="chat-input">
      <textarea
        ref={ref}
        className="chat-input__textarea"
        placeholder="Message Wenesday… (Enter to send, Shift+Enter for newline)"
        onKeyDown={handleKeyDown}
        disabled={disabled || loading}
        rows={1}
      />
      <button
        className={`btn btn--primary chat-input__send ${loading ? 'btn--loading' : ''}`}
        onClick={submit}
        disabled={disabled || loading}
        title="Send (Enter)"
      >
        {loading ? (
          <span className="spinner" />
        ) : (
          <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
            <path d="M2 21l21-9L2 3v7l15 2-15 2z" />
          </svg>
        )}
      </button>
    </div>
  )
}
