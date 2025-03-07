
// iframe-Proxy für freie KI-Modell-Antworten
class ModelIframeProxy {
  constructor() {
    this.activeFrames = {};
    this.responseCallbacks = {};
    this.frameCounter = 0;
    
    // Event-Listener für Nachrichten von den iframes
    window.addEventListener('message', (event) => {
      // Sicherheits-Check für Origin
      if (this.isTrustedOrigin(event.origin)) {
        try {
          const data = typeof event.data === 'string' ? JSON.parse(event.data) : event.data;
          if (data.type === 'model_response' && data.requestId && this.responseCallbacks[data.requestId]) {
            // Callback mit der Antwort aufrufen
            this.responseCallbacks[data.requestId](data.response);
            // Callback und iframe aufräumen
            this.cleanupFrame(data.requestId);
          }
        } catch (e) {
          console.error('Fehler beim Verarbeiten der iframe-Nachricht:', e);
        }
      }
    });
  }
  
  // Überprüfen, ob die Nachricht von einer vertrauenswürdigen Quelle kommt
  isTrustedOrigin(origin) {
    const trustedOrigins = [
      'https://claude.ai',
      'https://chat.openai.com',
      'https://gemini.google.com',
      'https://pi.ai'
      // Weitere vertrauenswürdige Quellen hier hinzufügen
    ];
    return trustedOrigins.includes(origin);
  }
  
  // Modell-Anfrage über iframe
  requestModelResponse(modelType, prompt, callback) {
    const requestId = `req_${Date.now()}_${this.frameCounter++}`;
    this.responseCallbacks[requestId] = callback;
    
    // iframe erstellen und zur Seite hinzufügen
    const iframe = document.createElement('iframe');
    iframe.style.width = '0';
    iframe.style.height = '0';
    iframe.style.border = 'none';
    iframe.style.position = 'absolute';
    iframe.style.left = '-9999px';
    
    // URL basierend auf dem Modell-Typ
    let iframeUrl;
    switch(modelType) {
      case 'claude-free':
        iframeUrl = `https://proxy-api.claudeai.service/chat?requestId=${requestId}&prompt=${encodeURIComponent(prompt)}`;
        break;
      case 'gpt-3.5-turbo':
        iframeUrl = `https://proxy-api.openai.service/chat?requestId=${requestId}&prompt=${encodeURIComponent(prompt)}`;
        break;
      case 'gemini-pro':
        iframeUrl = `https://proxy-api.gemini.service/chat?requestId=${requestId}&prompt=${encodeURIComponent(prompt)}`;
        break;
      // Weitere Modelle hier hinzufügen
      default:
        callback(`Keine öffentliche API für Modell ${modelType} verfügbar.`);
        return;
    }
    
    iframe.src = iframeUrl;
    document.body.appendChild(iframe);
    this.activeFrames[requestId] = iframe;
    
    // Timeout für den Fall, dass keine Antwort kommt
    setTimeout(() => {
      if (this.responseCallbacks[requestId]) {
        callback(`Keine Antwort von ${modelType} erhalten (Timeout). Fällt zurück auf simulierte Antwort.`);
        this.cleanupFrame(requestId);
      }
    }, 20000); // 20 Sekunden Timeout
  }
  
  // iframe und Callback aufräumen
  cleanupFrame(requestId) {
    if (this.activeFrames[requestId]) {
      document.body.removeChild(this.activeFrames[requestId]);
      delete this.activeFrames[requestId];
    }
    delete this.responseCallbacks[requestId];
  }
}

// Exportiere die Klasse für die Verwendung in script.js
window.ModelIframeProxy = ModelIframeProxy;
