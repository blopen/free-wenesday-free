import React, { useEffect, useRef } from 'react'
import MessageBubble from './MessageBubble.jsx'

function TypingIndicator() {
  return (
    <div className="message message--assistant">
      <div className="message__avatar">W</div>
      <div className="message__body">
        <div className="typing-indicator">
          <span /><span /><span />
        </div>
      </div>
    </div>
  )
}

function WelcomeScreen({ modelName }) {
  return (
    <div className="welcome">
      <div className="welcome__logo">W</div>
      <h1 className="welcome__title">Wenesday</h1>
      <p className="welcome__subtitle">Free community AI chat — open source</p>
      <p className="welcome__model">Active model: <strong>{modelName}</strong></p>
      <div className="welcome__hints">
        <div className="welcome__hint">💡 Ask anything</div>
        <div className="welcome__hint">📝 Write code</div>
        <div className="welcome__hint">🔍 Research topics</div>
        <div className="welcome__hint">🌐 Translate text</div>
      </div>
    </div>
  )
}

export default function ChatWindow({ messages, loading, error, modelName }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  return (
    <div className="chat-window">
      {messages.length === 0 && !loading ? (
        <WelcomeScreen modelName={modelName} />
      ) : (
        <div className="chat-window__messages">
          {messages.map((m) => (
            <MessageBubble key={m.id} message={m} />
          ))}
          {loading && <TypingIndicator />}
          {error && (
            <div className="chat-window__error">
              ⚠ {error}
            </div>
          )}
          <div ref={bottomRef} />
        </div>
      )}
    </div>
  )
}
