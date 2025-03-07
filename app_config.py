
# Konfigurationsdatei für die App

# URLs für die verschiedenen Modell-Proxies
MODEL_PROXY_URLS = {
    "claude-free": "https://api-proxy.claude.service/chat",
    "gpt-3.5-turbo": "https://api-proxy.openai.service/chat",
    "gemini-pro": "https://api-proxy.gemini.service/chat",
    "llama2-70b": "https://api-proxy.llama2.service/chat",
    "pi": "https://api-proxy.inflection.service/chat"
}

# API-Ratelimits für freie Modelle (Anfragen pro Minute)
FREE_MODEL_RATE_LIMITS = {
    "claude-free": 5,
    "gpt-3.5-turbo": 3, 
    "gemini-pro": 5,
    "llama2-70b": 3,
    "pi": 5
}

# Maximale Token-Länge für freie Modelle
FREE_MODEL_MAX_TOKENS = {
    "claude-free": 1024,
    "gpt-3.5-turbo": 1024,
    "gemini-pro": 1024,
    "llama2-70b": 512,
    "pi": 512
}
