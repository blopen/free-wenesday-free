import React from 'react'
import { MODELS } from '../services/api.js'

export default function Sidebar({ conversations, activeId, onSelect, onNew, activeModel, onModelChange, onSettings, onClear, theme, onThemeToggle, open }) {
  const providers = [...new Set(MODELS.map((m) => m.provider))]

  return (
    <aside className={`sidebar ${open ? 'sidebar--open' : ''}`}>
      <div className="sidebar__header">
        <span className="sidebar__logo">W</span>
        <span className="sidebar__title">Wenesday</span>
        <button className="icon-btn sidebar__theme-btn" onClick={onThemeToggle} title="Toggle theme">
          {theme === 'dark' ? '☀️' : '🌙'}
        </button>
      </div>

      <button className="btn btn--primary sidebar__new-btn" onClick={onNew}>
        + New Chat
      </button>

      <nav className="sidebar__conversations">
        <p className="sidebar__section-label">Conversations</p>
        {conversations.length === 0 && (
          <p className="sidebar__empty">No conversations yet.</p>
        )}
        {conversations.map((c) => (
          <button
            key={c.id}
            className={`sidebar__conv-item ${c.id === activeId ? 'sidebar__conv-item--active' : ''}`}
            onClick={() => onSelect(c.id)}
          >
            <span className="sidebar__conv-icon">💬</span>
            <span className="sidebar__conv-name">{c.title || 'New Chat'}</span>
          </button>
        ))}
      </nav>

      <div className="sidebar__model-section">
        <p className="sidebar__section-label">Model</p>
        {providers.map((provider) => (
          <div key={provider} className="sidebar__provider-group">
            <p className="sidebar__provider-label">{provider}</p>
            {MODELS.filter((m) => m.provider === provider).map((m) => (
              <button
                key={m.id}
                className={`sidebar__model-item ${activeModel === m.id ? 'sidebar__model-item--active' : ''}`}
                onClick={() => onModelChange(m.id)}
              >
                <span className="sidebar__model-name">{m.name}</span>
                {m.free && <span className="badge badge--free">free</span>}
              </button>
            ))}
          </div>
        ))}
      </div>

      <div className="sidebar__footer">
        {activeId && (
          <button className="icon-btn sidebar__clear-btn" onClick={onClear} title="Clear conversation">
            🗑 Clear
          </button>
        )}
        <button className="icon-btn sidebar__settings-btn" onClick={onSettings} title="Settings">
          ⚙ Settings
        </button>
      </div>
    </aside>
  )
}
