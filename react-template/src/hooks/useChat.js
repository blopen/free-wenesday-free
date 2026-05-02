import { useState, useCallback } from 'react'
import { sendMessage as apiSend } from '../services/api.js'

export function useChat(model, apiKeys) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const send = useCallback(async (history, onSuccess) => {
    setLoading(true)
    setError(null)
    try {
      const reply = await apiSend(history, model, apiKeys)
      onSuccess(reply)
    } catch (err) {
      setError(err.message ?? 'Request failed.')
    } finally {
      setLoading(false)
    }
  }, [model, apiKeys])

  const clearError = useCallback(() => setError(null), [])

  return { loading, error, send, clearError }
}
