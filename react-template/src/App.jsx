import React, { useState, useCallback } from 'react'
import Sidebar from './components/Sidebar.jsx'
import ChatWindow from './components/ChatWindow.jsx'
import ChatInput from './components/ChatInput.jsx'
import ApiKeyModal from './components/ApiKeyModal.jsx'
import { useLocalStorage } from './hooks/useLocalStorage.js'
import { useChat } from './hooks/useChat.js'
import { MODELS } from './services/api.js'

let idCounter = 0
function uid() {
  return `${Date.now()}-${++idCounter}`
}

function deriveTitle(text) {
  return text.slice(0, 42) + (text.length > 42 ? '…' : '')
}

function newConversation(title = '') {
  return { id: uid(), title, messages: [], createdAt: new Date().toISOString() }
}

export default function App() {
  const [theme, setTheme]             = useLocalStorage('wd_theme', 'dark')
  const [apiKeys, setApiKeys]         = useLocalStorage('wd_api_keys', {})
  const [activeModel, setActiveModel] = useLocalStorage('wd_model', 'gpt-3.5-turbo')
  const [conversations, setConvs]     = useLocalStorage('wd_conversations', [])
  const [activeId, setActiveId]       = useLocalStorage('wd_active_id', null)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [showSettings, setShowSettings] = useState(false)

  const { loading, error, send, clearError } = useChat(activeModel, apiKeys)

  const activeConv = conversations.find((c) => c.id === activeId) ?? null

  const updateConv = useCallback((id, patch) => {
    setConvs((prev) => prev.map((c) => (c.id === id ? { ...c, ...patch } : c)))
  }, [setConvs])

  const handleNew = useCallback(() => {
    const conv = newConversation()
    setConvs((prev) => [conv, ...prev])
    setActiveId(conv.id)
    setSidebarOpen(false)
    clearError()
  }, [setConvs, setActiveId, clearError])

  const handleSelect = useCallback((id) => {
    setActiveId(id)
    setSidebarOpen(false)
    clearError()
  }, [setActiveId, clearError])

  const handleSend = useCallback(async (text) => {
    let convId = activeId
    let baseMessages = activeConv?.messages ?? []

    if (!convId) {
      const conv = newConversation(deriveTitle(text))
      setConvs((prev) => [conv, ...prev])
      setActiveId(conv.id)
      convId = conv.id
      baseMessages = []
    }

    const userMsg = { id: uid(), role: 'user', content: text, ts: new Date().toISOString() }
    const updatedWithUser = [...baseMessages, userMsg]

    updateConv(convId, {
      messages: updatedWithUser,
      title: activeConv?.title || deriveTitle(text),
    })

    const apiHistory = updatedWithUser.map(({ role, content }) => ({ role, content }))

    await send(apiHistory, (reply) => {
      const assistantMsg = {
        id: uid(),
        role: 'assistant',
        content: reply,
        ts: new Date().toISOString(),
        model: activeModel,
      }
      setConvs((prev) =>
        prev.map((c) =>
          c.id === convId
            ? { ...c, messages: [...updatedWithUser, assistantMsg] }
            : c
        )
      )
    })
  }, [activeId, activeConv, activeModel, send, setConvs, setActiveId, updateConv])

  const handleClearConv = useCallback(() => {
    if (!activeId) return
    updateConv(activeId, { messages: [], title: '' })
    clearError()
  }, [activeId, updateConv, clearError])

  const handleDeleteConv = useCallback(() => {
    setConvs((prev) => prev.filter((c) => c.id !== activeId))
    setActiveId(null)
    clearError()
  }, [activeId, setConvs, setActiveId, clearError])

  const currentModelName = MODELS.find((m) => m.id === activeModel)?.name ?? activeModel

  return (
    <div className={`app app--${theme}`} data-theme={theme}>
      <button
        className="hamburger"
        onClick={() => setSidebarOpen((o) => !o)}
        aria-label="Toggle sidebar"
      >
        ☰
      </button>

      {sidebarOpen && (
        <div className="sidebar-overlay" onClick={() => setSidebarOpen(false)} />
      )}

      <Sidebar
        conversations={conversations}
        activeId={activeId}
        onSelect={handleSelect}
        onNew={handleNew}
        activeModel={activeModel}
        onModelChange={setActiveModel}
        onSettings={() => setShowSettings(true)}
        onClear={handleDeleteConv}
        theme={theme}
        onThemeToggle={() => setTheme((t) => (t === 'dark' ? 'light' : 'dark'))}
        open={sidebarOpen}
      />

      <main className="main">
        <header className="main__header">
          <button
            className="hamburger hamburger--inline"
            onClick={() => setSidebarOpen((o) => !o)}
            aria-label="Toggle sidebar"
          >
            ☰
          </button>
          <span className="main__logo-text">Wenesday</span>
          <span className="main__model-badge">{currentModelName}</span>
          <button
            className="icon-btn main__settings-btn"
            onClick={() => setShowSettings(true)}
            title="Settings"
          >
            ⚙
          </button>
        </header>

        <ChatWindow
          messages={activeConv?.messages ?? []}
          loading={loading}
          error={error}
          modelName={currentModelName}
        />

        <div className="main__input-area">
          <ChatInput
            onSend={handleSend}
            loading={loading}
          />
          <p className="main__disclaimer">
            Wenesday · open-source · AI can make mistakes — verify important info.
          </p>
        </div>
      </main>

      {showSettings && (
        <ApiKeyModal
          apiKeys={apiKeys}
          onSave={setApiKeys}
          onClose={() => setShowSettings(false)}
        />
      )}
    </div>
  )
}
