
// iframe-Proxy für freie KI-Modell-Antworten
// Prüfen, ob eine vorherige Definition vorhanden ist
window.ModelIframeProxy = window.ModelIframeProxy || (function() {
  class ModelIframeProxy {
    constructor() {
      if (window._modelProxyInstance) {
        return window._modelProxyInstance;
      }
      
      this.activeFrames = {};
      this.responseCallbacks = {};
      this.frameCounter = 0;
      this.initMessageListener();
      console.log("ModelIframeProxy initialisiert");
      window._modelProxyInstance = this;
    }
    
    initMessageListener() {
      // Event-Listener für Nachrichten von den iframes
      window.addEventListener('message', this.handleMessage.bind(this));
    }
    
    handleMessage(event) {
      // Sicherheits-Check für Origin
      if (this.isTrustedOrigin(event.origin)) {
        try {
          const data = typeof event.data === 'string' ? JSON.parse(event.data) : event.data;
          if (data.type === 'model_response' && data.requestId && this.responseCallbacks[data.requestId]) {
            console.log("Antwort vom iframe erhalten:", data.requestId);
            // Callback mit der Antwort aufrufen
            this.responseCallbacks[data.requestId](data.response);
            // Callback und iframe aufräumen
            this.cleanupFrame(data.requestId);
          }
        } catch (e) {
          console.error('Fehler beim Verarbeiten der iframe-Nachricht:', e);
        }
      } else {
        console.warn("Nachricht von nicht vertrauenswürdiger Quelle:", event.origin);
      }
    }
    
    // Überprüfen, ob die Nachricht von einer vertrauenswürdigen Quelle kommt
    isTrustedOrigin(origin) {
      const trustedOrigins = [
        'https://claude.ai',
        'https://chat.openai.com',
        'https://gemini.google.com',
        'https://bard.google.com',
        'https://pi.ai',
        window.location.origin
      ];
      
      // Check if origin begins with any trusted origin
      return trustedOrigins.some(trusted => origin === trusted || origin.startsWith(trusted));
    }
    
    // Direkte Web-API-Anfrage mit CORS-Proxy
    makeProxyRequest(endpoint, payload, callback) {
      // Wechselnde CORS Proxies für bessere Verfügbarkeit
      const corsProxies = [
        'https://corsproxy.io/?',
        'https://cors-anywhere.herokuapp.com/',
        'https://api.allorigins.win/raw?url='
      ];
      
      // Zufälligen Proxy auswählen
      const corsProxyUrl = corsProxies[Math.floor(Math.random() * corsProxies.length)];
      const apiUrl = corsProxyUrl + encodeURIComponent(endpoint);
      
      console.log("Sende Anfrage an Web-API über CORS-Proxy:", endpoint);
      
      // Prüfen, ob die Internetverbindung verfügbar ist
      if (!navigator.onLine) {
        console.log("Keine Internetverbindung verfügbar, verwende lokalen Fallback");
        this.useOfflineFallback(payload, callback);
        return;
      }
      
      // Timeout für die Fetch-Anfrage
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 Sekunden Timeout
      
      fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest',
          'Origin': window.location.origin
        },
        body: JSON.stringify(payload),
        signal: controller.signal
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log("Antwort von Web-API erhalten");
        callback(data.response || data.choices?.[0]?.text || data.content || JSON.stringify(data));
      })
      .catch(error => {
        console.error("Fehler bei der Web-API-Anfrage:", error);
        callback(`Fehler bei der Web-API-Anfrage: ${error.message}. Versuche alternativen Zugriff...`);
        this.fallbackToIframeMethod(endpoint, payload, callback);
      });
    }
    
    // Fallback auf iframe-Methode, wenn direkte API fehlschlägt
    fallbackToIframeMethod(endpoint, payload, callback) {
      const model = payload.model || 'claude-free';
      const message = payload.message || payload.prompt || 
                    (payload.messages ? JSON.stringify(payload.messages) : "Keine Nachricht");
      
      this.requestModelResponse(model, message, callback);
    }
    
    // Verwende lokales DeepSeek-Modell als Fallback, wenn keine Internetverbindung besteht
    useOfflineFallback(payload, callback) {
      console.log("Verwende lokales DeepSeek-Modell als Fallback");
      
      // Versuche, eine Server-Anfrage für das lokale DeepSeek-Modell zu senden
      fetch('/offline_model_request', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: "deepseek-chat",
          message: payload.message || payload.prompt || 
                  (payload.messages ? JSON.stringify(payload.messages) : "Keine Nachricht")
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          callback(data.response);
        } else {
          callback(`Offline-Modell-Fehler: ${data.error}. Versuche es später erneut.`);
        }
      })
      .catch(error => {
        console.error("Fehler bei der Offline-Modell-Anfrage:", error);
        callback("Lokales Modell nicht verfügbar. Bitte überprüfen Sie Ihre Verbindung oder versuchen Sie es später erneut.");
      });
    }

    // Modell-Anfrage über iframe
    requestModelResponse(modelType, prompt, callback) {
      const requestId = `req_${Date.now()}_${this.frameCounter++}`;
      this.responseCallbacks[requestId] = callback;
      
      console.log(`Erstelle iframe für ${modelType}-Anfrage mit ID: ${requestId}`);
      
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
        case 'claude-instant':
          iframeUrl = `https://api-proxy.claudeai.service/chat?requestId=${requestId}&prompt=${encodeURIComponent(prompt)}`;
          break;
        case 'gpt-3.5-turbo':
          iframeUrl = `https://api-proxy.openai.service/chat?requestId=${requestId}&prompt=${encodeURIComponent(prompt)}`;
          break;
        case 'gemini-pro':
          iframeUrl = `https://api-proxy.gemini.service/chat?requestId=${requestId}&prompt=${encodeURIComponent(prompt)}`;
          break;
        case 'pi':
          iframeUrl = `https://api-proxy.inflection.service/chat?requestId=${requestId}&prompt=${encodeURIComponent(prompt)}`;
          break;
        case 'llama2-70b':
          iframeUrl = `https://api-proxy.llama2.service/chat?requestId=${requestId}&prompt=${encodeURIComponent(prompt)}`;
          break;
        case 'deepseek-chat':
          iframeUrl = `https://api-proxy.deepseek.service/chat?requestId=${requestId}&prompt=${encodeURIComponent(prompt)}`;
          break;
        case 'deepseek-coder':
          iframeUrl = `https://api-proxy.deepseek.service/coder?requestId=${requestId}&prompt=${encodeURIComponent(prompt)}`;
          break;
        default:
          console.warn(`Keine bekannte Proxy-URL für Modell ${modelType}`);
          callback(`Keine öffentliche API für Modell ${modelType} verfügbar.`);
          return;
      }
      
      iframe.src = iframeUrl;
      document.body.appendChild(iframe);
      this.activeFrames[requestId] = iframe;
      
      console.log(`iframe für ${modelType} erstellt und zur Seite hinzugefügt`);
      
      // Timeout für den Fall, dass keine Antwort kommt
      setTimeout(() => {
        if (this.responseCallbacks[requestId]) {
          console.warn(`Timeout für Anfrage ${requestId}`);
          callback(`Keine Antwort von ${modelType} erhalten (Timeout). Versuche direkte Server-Anfrage...`);
          this.cleanupFrame(requestId);
        }
      }, 10000); // 10 Sekunden Timeout (reduziert von 15)
    }
    
    // iframe und Callback aufräumen
    cleanupFrame(requestId) {
      if (this.activeFrames[requestId]) {
        try {
          console.log(`Entferne iframe für Anfrage ${requestId}`);
          document.body.removeChild(this.activeFrames[requestId]);
        } catch (e) {
          console.warn(`Fehler beim Entfernen des iframe für ${requestId}:`, e);
        }
        delete this.activeFrames[requestId];
      }
      delete this.responseCallbacks[requestId];
    }
  }

  return ModelIframeProxy;
})();
