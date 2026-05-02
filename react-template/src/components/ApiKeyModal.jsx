import React, { useState } from 'react'

const PROVIDERS = [
  { id: 'openai',    label: 'OpenAI',    placeholder: 'sk-...',    link: 'https://platform.openai.com/api-keys' },
  { id: 'anthropic', label: 'Anthropic', placeholder: 'sk-ant-...', link: 'https://console.anthropic.com/settings/keys' },
  { id: 'groq',      label: 'Groq',      placeholder: 'gsk_...',   link: 'https://console.groq.com/keys' },
]

export default function ApiKeyModal({ apiKeys, onSave, onClose }) {
  const [draft, setDraft] = useState({ ...apiKeys })
  const [show, setShow] = useState({})

  const toggleShow = (id) => setShow((s) => ({ ...s, [id]: !s[id] }))

  const handleSave = () => {
    onSave(draft)
    onClose()
  }

  return (
    <div className="modal-overlay" onClick={(e) => e.target === e.currentTarget && onClose()}>
      <div className="modal">
        <div className="modal__header">
          <h2 className="modal__title">⚙ Settings — API Keys</h2>
          <button className="icon-btn modal__close" onClick={onClose}>✕</button>
        </div>

        <p className="modal__desc">
          Keys are stored in your browser's localStorage and never sent to any server except the provider's own API.
        </p>

        <div className="modal__fields">
          {PROVIDERS.map(({ id, label, placeholder, link }) => (
            <div key={id} className="modal__field">
              <label className="modal__label">
                {label}
                <a className="modal__link" href={link} target="_blank" rel="noreferrer">
                  Get key ↗
                </a>
              </label>
              <div className="modal__input-wrap">
                <input
                  className="modal__input"
                  type={show[id] ? 'text' : 'password'}
                  placeholder={placeholder}
                  value={draft[id] ?? ''}
                  onChange={(e) => setDraft((d) => ({ ...d, [id]: e.target.value }))}
                />
                <button className="icon-btn modal__show-btn" onClick={() => toggleShow(id)}>
                  {show[id] ? '🙈' : '👁'}
                </button>
                {draft[id] && (
                  <button className="icon-btn modal__clear-btn" onClick={() => setDraft((d) => ({ ...d, [id]: '' }))}>
                    ✕
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="modal__actions">
          <button className="btn btn--ghost" onClick={onClose}>Cancel</button>
          <button className="btn btn--primary" onClick={handleSave}>Save</button>
        </div>
      </div>
    </div>
  )
}
