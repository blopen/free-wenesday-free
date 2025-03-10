
class ModelIframeProxy {
  constructor() {
    console.log("ModelIframeProxy initialisiert");
    this.iframes = {};
    this.responseCallbacks = {};
    this.requestCounter = 0;
    
    // Liste von vertrauenswürdigen Ursprüngen für Cross-Origin-Kommunikation
    this.trustedOrigins = [
      window.location.origin,
      "https://corsproxy.io",
      "https://cors-anywhere.herokuapp.com",
      "https://api.allorigins.win",
      "https://proxy.cors.sh"
    ];
    
    // CORS-Proxy-URLs in einer Prioritätsliste
    this.corsProxies = [
      "https://corsproxy.io/?",
      "https://proxy.cors.sh/",
      "https://cors-anywhere.herokuapp.com/",
      "https://api.allorigins.win/raw?url="
    ];
    
    // Modell-Endpunkte
    this.modelEndpoints = {
      "claude-free": "https://api.anthropic.com/v1/complete",
      "claude-instant": "https://api.anthropic.com/v1/complete",
      "gpt-3.5-turbo": "https://api.openai.com/v1/chat/completions",
      "gemini-pro": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
      "pi": "https://api.inflection.ai/v1/chat/completions",
      "deepseek-chat": "https://api.deepseek.com/v1/chat/completions",
      "deepseek-coder": "https://api.deepseek.com/v1/coder/completions"
    };
    
    this.defaultModel = "claude-free";
    
    // Event-Listener für Nachrichten von iframes
    window.addEventListener('message', this.handleMessage.bind(this));
    
    // Globale Instanz, um Mehrfach-Initialisierungen zu vermeiden
    if (!window.proxyInstance) {
      window.proxyInstance = this;
      console.log("ModelIframeProxy-Instanz bereit");
    }
    
    // Prüfen, ob wir online sind
    this.checkNetworkStatus();
  }
  
  // Prüft, ob eine Internetverbindung besteht
  checkNetworkStatus() {
    this.isOnline = navigator.onLine;
    
    // Event-Listener für Online/Offline-Status
    window.addEventListener('online', () => {
      this.isOnline = true;
      console.log("Internetverbindung wiederhergestellt");
    });
    
    window.addEventListener('offline', () => {
      this.isOnline = false;
      console.log("Keine Internetverbindung");
    });
  }
  
  // Überprüft, ob der Origin vertrauenswürdig ist
  isTrustedOrigin(origin) {
    return this.trustedOrigins.some(trusted => origin.includes(trusted));
  }
  
  // Hauptmethode für Modellanfragen
  requestModelResponse(model, message, callback) {
    try {
      if (!model) model = this.defaultModel;
      
      if (!this.isOnline) {
        this.useOfflineFallback({model, message}, callback);
        return;
      }
      
      const requestId = `req_${Date.now()}_${this.requestCounter++}`;
      this.responseCallbacks[requestId] = callback;
      
      // Entscheiden, ob wir ein iframe oder direkten CORS-Proxy verwenden
      const endpoint = this.modelEndpoints[model];
      if (endpoint) {
        // Direkter API-Zugriff über CORS-Proxy
        this.makeProxyRequest(endpoint, {
          model: model,
          prompt: `\n\nHuman: ${message}\n\nAssistant:`,
          messages: [{role: "user", content: message}],
          max_tokens: 1000,
          temperature: 0.7
        }, callback);
      } else {
        // Fallback auf iframe-Methode
        this.createModelFrame(model, message, requestId);
      }
    } catch (error) {
      console.error("Fehler bei requestModelResponse:", error);
      callback(`Entschuldigung, es gab einen Fehler bei der Verarbeitung Ihrer Anfrage: ${error.message}`);
    }
  }
  
  // Erstellt einen unsichtbaren iframe für die Kommunikation
  createModelFrame(model, message, requestId) {
    // iframe erstellen
    const iframe = document.createElement('iframe');
    iframe.style.display = 'none';
    document.body.appendChild(iframe);
    
    // Iframe-Inhalt setzen
    const iframeContent = `
      <!DOCTYPE html>
      <html>
      <head>
        <script>
          // Funktion zum Senden des Ergebnisses an das Elternfenster
          function sendResponse(response) {
            window.parent.postMessage({
              type: 'model_response',
              requestId: '${requestId}',
              response: response
            }, '*');
          }
          
          // Versuch, eine Antwort zu generieren
          async function generateResponse() {
            try {
              // Simuliert einen erfolgreichen API-Aufruf
              // In einer realen Implementierung würde hier ein API-Aufruf stehen
              await new Promise(resolve => setTimeout(resolve, 1000));
              
              sendResponse("Diese Anfrage wurde durch den iframe-Proxy bearbeitet: ${model} Antwort auf: ${message}");
            } catch (error) {
              sendResponse("Fehler bei der Generierung: " + error.message);
            }
          }
          
          // Starte die Generierung, sobald die Seite geladen ist
          window.onload = generateResponse;
        </script>
      </head>
      <body>
        <div>Verarbeitung von Modell ${model}...</div>
      </body>
      </html>
    `;
    
    // Speichern des iframes für spätere Referenz
    this.iframes[requestId] = iframe;
    
    // Inhalt in den iframe schreiben
    iframe.srcdoc = iframeContent;
    
    // Timeout für den Fall, dass keine Antwort kommt
    const timeoutId = setTimeout(() => {
      this.cleanupFrame(requestId);
      if (this.responseCallbacks[requestId]) {
        this.responseCallbacks[requestId]("Zeitüberschreitung bei der Anfrage an das Modell.");
        delete this.responseCallbacks[requestId];
      }
    }, 15000); // 15 Sekunden Timeout
    
    // Timeout-ID speichern
    this.iframes[requestId].timeoutId = timeoutId;
  }
  
  // Bereinigt den iframe und Callback nach Abschluss
  cleanupFrame(requestId) {
    if (this.iframes[requestId]) {
      // Timeout aufheben
      if (this.iframes[requestId].timeoutId) {
        clearTimeout(this.iframes[requestId].timeoutId);
      }
      
      // iframe entfernen
      this.iframes[requestId].remove();
      delete this.iframes[requestId];
    }
    
    // Callback entfernen
    delete this.responseCallbacks[requestId];
  }
  
  // Event-Handler für Nachrichten von iframes
  handleMessage(event) {
    try {
      // Sicherheits-Check für Origin
      if (this.isTrustedOrigin(event.origin)) {
        try {
          // Verbesserte Fehlerbehandlung bei der Datenverarbeitung
          let data;
          if (typeof event.data === 'string') {
            try {
              data = JSON.parse(event.data);
            } catch (parseError) {
              console.warn("Konnte die Nachricht nicht als JSON parsen:", event.data.substring(0, 100));
              return; // Nicht-JSON-Nachrichten ignorieren
            }
          } else {
            data = event.data;
          }
          
          // Prüfen ob alle erwarteten Felder vorhanden sind
          if (!data || typeof data !== 'object') {
            console.warn("Unerwartetes Nachrichtenformat:", data);
            return;
          }
          
          if (data.type === 'model_response' && data.requestId && this.responseCallbacks[data.requestId]) {
            console.log("Antwort vom iframe erhalten:", data.requestId);
            // Callback mit der Antwort aufrufen
            this.responseCallbacks[data.requestId](data.response || "Keine Antwort erhalten");
            // Callback und iframe aufräumen
            this.cleanupFrame(data.requestId);
          }
        } catch (error) {
          console.error("Fehler beim Verarbeiten der iframe-Nachricht:", error);
        }
      } else {
        console.warn("Nachricht von nicht vertrauenswürdigem Ursprung ignoriert:", event.origin);
      }
    } catch (error) {
      console.error("Fehler bei handleMessage:", error);
    }
  }
  
  // Führt Web-API-Anfragen über CORS-Proxy aus
  makeProxyRequest(endpoint, payload, callback) {
    if (!this.isOnline) {
      this.useOfflineFallback(payload, callback);
      return;
    }
    
    // Aktuelle CORS-Proxy-URL wählen
    const corsProxy = this.corsProxies[0]; // Primärer Proxy
    const proxyUrl = corsProxy + encodeURIComponent(endpoint);
    
    // API-spezifische Header und Payloads erstellen
    let headers = {
      'Content-Type': 'application/json'
    };
    
    // Modell aus dem Payload extrahieren
    const model = payload.model || this.defaultModel;
    
    // Die tatsächliche Anfrage vorbereiten
    let requestData = {};
    
    // Unterschiedliche Formate für verschiedene APIs
    if (model.includes('claude')) {
      // Format für Claude API
      requestData = {
        model: model,
        prompt: payload.prompt || `\n\nHuman: ${payload.message || ''}\n\nAssistant:`,
        max_tokens_to_sample: payload.max_tokens || 1000,
        temperature: payload.temperature || 0.7,
        stop_sequences: ["\n\nHuman:"],
        stream: false
      };
    } else if (model.includes('gpt')) {
      // Format für OpenAI API
      requestData = {
        model: model,
        messages: payload.messages || [{role: "user", content: payload.message || ''}],
        max_tokens: payload.max_tokens || 1000,
        temperature: payload.temperature || 0.7,
        stream: false
      };
    } else {
      // Generisches Format für andere APIs
      requestData = payload;
    }
    
    // Timeout für die gesamte Anfrage
    const timeoutId = setTimeout(() => {
      controller.abort();
      callback("Zeitüberschreitung bei der Web-API-Anfrage. Versuche einen alternativen Proxy...");
      this.tryAlternativeProxy(endpoint, payload, callback, 1); // 1 = erster alternativer Proxy
    }, 8000); // 8 Sekunden Timeout
    
    // AbortController für Fetch-Timeout
    const controller = new AbortController();
    
    console.log(`Verwende CORS-Proxy: ${corsProxy} für Anfrage an ${model}`);
    
    // Fetch-Anfrage über CORS-Proxy
    fetch(proxyUrl, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(requestData),
      signal: controller.signal
    })
    .then(response => {
      clearTimeout(timeoutId); // Timeout aufheben
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      // Extrahiere die Antwort basierend auf dem API-Format
      let modelResponse = "";
      
      if (model.includes('claude')) {
        modelResponse = data.completion || data.content || JSON.stringify(data);
      } else if (model.includes('gpt')) {
        modelResponse = data.choices?.[0]?.message?.content || JSON.stringify(data);
      } else {
        modelResponse = data.response || data.choices?.[0]?.text || JSON.stringify(data);
      }
      
      callback(modelResponse);
    })
    .catch(error => {
      clearTimeout(timeoutId);
      console.error("Fehler bei der Web-API-Anfrage:", error);
      callback(`Fehler bei der Web-API-Anfrage: ${error.message}. Versuche alternativen Zugriff...`);
      this.tryAlternativeProxy(endpoint, payload, callback, 1);
    });
  }
  
  // Versucht es mit einem alternativen CORS-Proxy
  tryAlternativeProxy(endpoint, payload, callback, proxyIndex) {
    if (proxyIndex >= this.corsProxies.length) {
      // Alle Proxies ausprobiert, Fallback auf iframe-Methode
      this.fallbackToIframeMethod(endpoint, payload, callback);
      return;
    }
    
    const corsProxy = this.corsProxies[proxyIndex];
    const proxyUrl = corsProxy + encodeURIComponent(endpoint);
    
    console.log(`Versuche alternativen CORS-Proxy: ${corsProxy}`);
    
    // Timeout für die alternative Anfrage
    const timeoutId = setTimeout(() => {
      controller.abort();
      this.tryAlternativeProxy(endpoint, payload, callback, proxyIndex + 1);
    }, 6000); // Kürzerer Timeout für alternative Proxies
    
    // AbortController für Fetch-Timeout
    const controller = new AbortController();
    
    // Angepasste Headers für bestimmte Proxies
    let headers = {
      'Content-Type': 'application/json'
    };
    
    // Spezielle Header für cors-anywhere
    if (corsProxy.includes('cors-anywhere')) {
      headers['X-Requested-With'] = 'XMLHttpRequest';
    }
    
    // Format für die Anfrage bestimmen (wie in makeProxyRequest)
    const model = payload.model || this.defaultModel;
    let requestData = this.formatRequestData(model, payload);
    
    // Fetch-Anfrage über alternativen CORS-Proxy
    fetch(proxyUrl, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(requestData),
      signal: controller.signal
    })
    .then(response => {
      clearTimeout(timeoutId);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      let modelResponse = this.extractModelResponse(model, data);
      callback(modelResponse);
    })
    .catch(error => {
      clearTimeout(timeoutId);
      console.warn(`Fehler mit Proxy ${corsProxy}:`, error.message);
      
      // Nächsten Proxy versuchen
      this.tryAlternativeProxy(endpoint, payload, callback, proxyIndex + 1);
    });
  }
  
  // Hilfsmethode zur Formatierung der Anfragedaten je nach Modell
  formatRequestData(model, payload) {
    if (model.includes('claude')) {
      return {
        model: model,
        prompt: payload.prompt || `\n\nHuman: ${payload.message || ''}\n\nAssistant:`,
        max_tokens_to_sample: payload.max_tokens || 1000,
        temperature: payload.temperature || 0.7,
        stop_sequences: ["\n\nHuman:"],
        stream: false
      };
    } else if (model.includes('gpt')) {
      return {
        model: model,
        messages: payload.messages || [{role: "user", content: payload.message || ''}],
        max_tokens: payload.max_tokens || 1000,
        temperature: payload.temperature || 0.7,
        stream: false
      };
    } else {
      return payload;
    }
  }
  
  // Hilfsmethode zur Extraktion der Modellantwort je nach API-Format
  extractModelResponse(model, data) {
    if (model.includes('claude')) {
      return data.completion || data.content || JSON.stringify(data);
    } else if (model.includes('gpt')) {
      return data.choices?.[0]?.message?.content || JSON.stringify(data);
    } else {
      return data.response || data.choices?.[0]?.text || JSON.stringify(data);
    }
  }
  
  // Fallback auf iframe-Methode, wenn direkte API fehlschlägt
  fallbackToIframeMethod(endpoint, payload, callback) {
    const model = payload.model || this.defaultModel;
    const message = payload.message || payload.prompt || 
                  (payload.messages ? JSON.stringify(payload.messages) : "Keine Nachricht");
    
    console.log("Fallback auf iframe-Methode für", model);
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
      callback(`Konnte das Offline-Modell nicht erreichen: ${error.message}. Bitte überprüfen Sie Ihre Verbindung.`);
    });
  }
}

// Stellen sicher, dass wir nur eine globale Instanz haben
if (typeof window !== 'undefined' && !window.ModelIframeProxy) {
  window.ModelIframeProxy = ModelIframeProxy;
}
