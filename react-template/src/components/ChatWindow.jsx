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

const WD_HINTS = [
  { icon: '💡', de: 'Frag mich alles',    en: 'Ask me anything' },
  { icon: '📝', de: 'Code schreiben',     en: 'Write code' },
  { icon: '🔍', de: 'Themen recherchieren', en: 'Research topics' },
  { icon: '🌐', de: 'Text übersetzen',    en: 'Translate text' },
  { icon: '⚡', de: 'Scripts generieren', en: 'Generate scripts' },
  { icon: '🖼', de: 'Bild-Prompt erstellen', en: 'Create image prompt' },
]

function WelcomeScreen({ modelName }) {
  return (
    <div className="welcome">
      <div className="welcome__logo">@w</div>
      <h1 className="welcome__title">Wenesday</h1>
      <p className="welcome__subtitle">Free community AI — open source · lopez.codes</p>
      <p className="welcome__model">Aktives Modell / Active model: <strong>{modelName}</strong></p>
      <p className="welcome__wd-hint">Tippe <code>@w</code> um die Wenesday-Persona zu aktivieren</p>
      <div className="welcome__hints">
        {WD_HINTS.map((h) => (
          <div key={h.en} className="welcome__hint">
            {h.icon} {h.de} / {h.en}
          </div>
        ))}
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
