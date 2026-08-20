import { W_SYSTEM_PROMPT } from '../../wenesday/@w.js'

export { W_SYSTEM_PROMPT }

export const MODELS = [
  { id: 'gpt-3.5-turbo',              name: 'GPT-3.5 Turbo',       provider: 'openai',    free: true  },
  { id: 'gpt-4o-mini',                name: 'GPT-4o Mini',          provider: 'openai',    free: false },
  { id: 'gpt-4o',                     name: 'GPT-4o',               provider: 'openai',    free: false },
  { id: 'gpt-4',                      name: 'GPT-4',                provider: 'openai',    free: false },
  { id: 'claude-haiku-4-5',           name: 'Claude Haiku 4.5',     provider: 'anthropic', free: false },
  { id: 'claude-sonnet-4-5',          name: 'Claude Sonnet 4.5',    provider: 'anthropic', free: false },
  { id: 'claude-opus-4-5',            name: 'Claude Opus 4.5',      provider: 'anthropic', free: false },
  { id: 'llama-3.3-70b-versatile',    name: 'Llama 3.3 70B',        provider: 'groq',      free: true  },
  { id: 'mixtral-8x7b-32768',         name: 'Mixtral 8x7B',         provider: 'groq',      free: true  },
  { id: 'gemma2-9b-it',               name: 'Gemma 2 9B',           provider: 'groq',      free: true  },
]

export function getProvider(modelId) {
  return MODELS.find((m) => m.id === modelId)?.provider ?? 'openai'
}

async function callOpenAI(messages, modelId, apiKey) {
  const res = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({ model: modelId, messages }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err?.error?.message ?? `OpenAI error ${res.status}`)
  }
  const data = await res.json()
  return data.choices[0].message.content
}

async function callAnthropic(messages, modelId, apiKey) {
  const system = messages.find((m) => m.role === 'system')?.content
  const conversation = messages.filter((m) => m.role !== 'system')

  const body = {
    model: modelId,
    max_tokens: 4096,
    messages: conversation,
    ...(system ? { system } : {}),
  }

  const res = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
      'anthropic-dangerous-direct-browser-access': 'true',
    },
    body: JSON.stringify(body),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err?.error?.message ?? `Anthropic error ${res.status}`)
  }
  const data = await res.json()
  return data.content[0].text
}

async function callGroq(messages, modelId, apiKey) {
  const res = await fetch('https://api.groq.com/openai/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({ model: modelId, messages }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err?.error?.message ?? `Groq error ${res.status}`)
  }
  const data = await res.json()
  return data.choices[0].message.content
}

/** Prepend @w system prompt if not already present */
function withWSystem(messages) {
  if (messages[0]?.role === 'system') return messages
  return [{ role: 'system', content: W_SYSTEM_PROMPT }, ...messages]
}

export async function sendMessage(messages, modelId, apiKeys) {
  messages = withWSystem(messages)
  const provider = getProvider(modelId)
  const key = apiKeys[provider]

  if (!key) {
    throw new Error(
      `No API key for ${provider}. Open Settings (⚙) and add your ${provider} key.`
    )
  }

  switch (provider) {
    case 'openai':    return callOpenAI(messages, modelId, key)
    case 'anthropic': return callAnthropic(messages, modelId, key)
    case 'groq':      return callGroq(messages, modelId, key)
    default:          throw new Error(`Unknown provider: ${provider}`)
  }
}
