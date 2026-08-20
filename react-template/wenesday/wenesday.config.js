/**
 * wenesday.config.js — internal installation registry
 * New install location: react-template/  (Vite + React)
 * Previous location:    / (Flask/Python monolith) — in maintenance
 *
 * lopez.codes · it.lopez-be.ch · blopen/free-wenesday-free
 */

import { W_SYSTEM_PROMPT, W_VERSION, W_PROVIDER } from './@w.js'

const config = {
  app: {
    name: 'Wenesday',
    slug: 'free-wenesday-free',
    version: W_VERSION,
    provider: W_PROVIDER,
    repo: 'https://github.com/blopen/free-wenesday-free',
    branch: 'claude/react-chat-template-lHK73',
  },

  install: {
    type: 'react-vite',
    root: 'react-template/',
    entry: 'react-template/src/main.jsx',
    devCmd: 'npm run dev',
    buildCmd: 'npm run build',
    port: 3000,
  },

  /**
   * Previous (Flask) install is in maintenance — same repo root.
   * Will be restored; use this React template in the meantime.
   */
  legacy: {
    type: 'flask-python',
    entry: 'app.py',
    status: 'maintenance',
  },

  w: {
    command: '@w',
    systemPrompt: W_SYSTEM_PROMPT,
    wdFormat: {
      userPrefix: '//',
      fileExtension: '.wd',
      exampleFiles: ['index.wd', 'front/Wensday.wd'],
    },
  },

  models: {
    default: 'gpt-3.5-turbo',
    free: ['gpt-3.5-turbo', 'llama-3.3-70b-versatile', 'mixtral-8x7b-32768', 'gemma2-9b-it'],
  },
}

export default config
