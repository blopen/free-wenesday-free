
document.addEventListener('DOMContentLoaded', function() {
    // Stelle sicher, dass alle DOM-Elemente initialisiert werden, wenn sie verfügbar sind
    let chatMessages, messageInput, sendMessageBtn;
    
    // DOM elements
    const modelItems = document.querySelectorAll('.model-item');
    const apiServiceSelect = document.getElementById('api-service');
    const apiKeyInput = document.getElementById('api-key-input');
    
    // Verzögertes Abrufen der Chat-Elemente, um sicherzustellen, dass sie geladen sind
    setTimeout(() => {
        chatMessages = document.getElementById('chat-messages');
        messageInput = document.getElementById('message-input');
        sendMessageBtn = document.getElementById('send-message');
        
        // Initialisiere Chat nach erfolgreicher Elementbindung
        if (chatMessages && messageInput && sendMessageBtn) {
            initializeChat();
            setupChatEventListeners();
        }
    }, 500);
    
    const adminLoginBtn = document.getElementById('admin-login-btn');
    const themeToggle = document.getElementById('theme-toggle-checkbox');

    // Theme toggle functionality
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        if (themeToggle) themeToggle.checked = true;
    }

    if (themeToggle) {
        themeToggle.addEventListener('change', function() {
            if (this.checked) {
                document.body.classList.add('dark-theme');
                localStorage.setItem('theme', 'dark');
            } else {
                document.body.classList.remove('dark-theme');
                localStorage.setItem('theme', 'light');
            }
        });
    }

    // Admin Login Funktionalität
    if (adminLoginBtn) {
        adminLoginBtn.addEventListener('click', function() {
            // Passwort-Popup anzeigen
            const password = prompt('Bitte geben Sie das Admin-Passwort ein:');

            // Wenn Cancel gedrückt wurde oder leeres Passwort
            if (password === null || password === '') {
                return;
            }

            // Admin-Login mit Passwort
            fetch('/admin/login_as_admin', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ password: password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    addSystemMessage('Als Admin angemeldet! Sie werden zur Admin-Seite weitergeleitet...');
                    setTimeout(() => {
                        window.location.href = '/admin';
                    }, 1500);
                } else {
                    addSystemMessage(`Fehler beim Login: ${data.error || 'Falsches Passwort'}`);
                }
            })
            .catch(error => {
                console.error('Fehler:', error);
                addSystemMessage('Fehler bei der Kommunikation mit dem Server.');
            });
        });
    }

    // Current model and chat state
    let activeModel = document.querySelector('.model-item.active')?.dataset.model || 'claude-free';
    let isProcessing = false;

    // API-Key-Speichern-Button sicher abrufen
    const saveApiKeyBtn = document.getElementById('save-api-key');
    if (saveApiKeyBtn) {
        saveApiKeyBtn.addEventListener('click', saveApiKey);
    }

    // Initialize chat history from session if available
    if (chatMessages) {
        initializeChat();
    }

    // Event listeners for model selection
    modelItems.forEach(item => {
        item.addEventListener('click', function() {
            if (isProcessing) return; // Prevent changing model during processing

            // Remove active class from current model
            document.querySelector('.model-item.active')?.classList.remove('active');

            // Activate new model
            this.classList.add('active');
            activeModel = this.dataset.model;

            // Send AJAX request to set active model
            fetch('/set_active_model', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `model=${activeModel}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    addSystemMessage(`Modell gewechselt zu ${activeModel}`);
                } else {
                    addSystemMessage(`Fehler beim Wechseln des Modells: ${data.error}`);
                }
            })
            .catch(error => {
                console.error('Fehler:', error);
                addSystemMessage('Fehler bei der Kommunikation mit dem Server.');
            });
        });
    });

    // Function to save API key
    function saveApiKey() {
        const service = apiServiceSelect.value;
        const apiKey = apiKeyInput.value;

        if (!apiKey) {
            addSystemMessage('Bitte geben Sie einen API-Schlüssel ein.');
            return;
        }

        // Send AJAX request to save API key
        fetch('/save_api_key', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `service=${service}&api_key=${apiKey}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                addSystemMessage(`API-Schlüssel für ${service} erfolgreich gespeichert!`);
                apiKeyInput.value = '';

                // Update displayed keys without page reload
                const savedKeysList = document.querySelector('.saved-api-keys ul');
                if (savedKeysList) {
                    let keyExists = false;

                    // Check if service already exists in list
                    const listItems = savedKeysList.querySelectorAll('li');
                    listItems.forEach(item => {
                        if (item.textContent.startsWith(service)) {
                            keyExists = true;
                        }
                    });

                    // Add service to list if not present
                    if (!keyExists) {
                        const newKeyItem = document.createElement('li');
                        newKeyItem.textContent = `${service}: ********`;
                        savedKeysList.appendChild(newKeyItem);
                    }
                }
            } else {
                addSystemMessage('Fehler beim Speichern des API-Schlüssels.');
            }
        })
        .catch(error => {
            console.error('Fehler:', error);
            addSystemMessage('Fehler bei der Kommunikation mit dem Server.');
        });
    }

    // Erstellen der iframe-Proxy-Instanz und stellen sicher, dass es nur eine gibt
    let iframeProxy;

    // Stellen sicher, dass das Proxy-Script geladen wurde
    function ensureProxyLoaded() {
        return new Promise((resolve) => {
            if (typeof window.ModelIframeProxy !== 'undefined') {
                resolve();
                return;
            }

            // Wenn der Proxy noch nicht geladen ist, laden wir ihn asynchron
            const script = document.createElement('script');
            script.src = '/static/iframe_proxy.js?v=' + Date.now(); // Cache-Busting
            script.onload = () => {
                setTimeout(() => resolve(), 100); // Kurze Verzögerung für Skriptinitialisierung
            };
            script.onerror = () => {
                console.error("Konnte iframe_proxy.js nicht laden");
                resolve(); // Trotzdem fortfahren
            };
            document.head.appendChild(script);
        });
    }

    // Initialisieren des Proxys nach der Sicherstellung, dass er geladen ist
    ensureProxyLoaded().then(() => {
        try {
            // Die neue Implementierung sorgt selbst für Singleton-Verhalten
            if (typeof window.ModelIframeProxy !== 'undefined') {
                iframeProxy = new window.ModelIframeProxy();
                console.log("ModelIframeProxy-Instanz bereit");
            } else {
                console.warn("ModelIframeProxy nicht verfügbar, verwende Fallback");
                iframeProxy = createFallbackProxy();
            }
        } catch (e) {
            console.error("Fehler beim Erstellen des ModelIframeProxy:", e);
            iframeProxy = createFallbackProxy();
        }
    });

    // Fallback-Proxy erstellen, falls etwas schiefgeht
    function createFallbackProxy() {
        return {
            requestModelResponse: function(model, message, callback) {
                sendMessageToServer(message);
            },
            makeProxyRequest: function(endpoint, payload, callback) {
                sendMessageToServer(payload.message || payload.prompt || 
                    (payload.messages ? payload.messages[0].content : "Keine Nachricht"));
            }
        };
    }

    // Prüfen ob ein Modell kostenlos ist
    function isFreeModel(model) {
        const freeModels = [
            'claude-free', 
            'claude-instant',
            'gpt-3.5-turbo', 
            'gemini-pro', 
            'llama2-70b', 
            'pi',
            'deepseek-chat',
            'deepseek-coder'
        ];
        return freeModels.includes(model);
    }

    // Öffentliche APIs für verschiedene Modelle
    const publicEndpoints = {
        'claude-free': 'https://api.anthropic.com/v1/complete',
        'claude-instant': 'https://api.anthropic.com/v1/complete',
        'gpt-3.5-turbo': 'https://api.openai.com/v1/chat/completions',
        'gemini-pro': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
        'pi': 'https://api.inflection.ai/v1/chat/completions',
        'deepseek-chat': 'https://api.deepseek.com/v1/chat/completions',
        'deepseek-coder': 'https://api.deepseek.com/v1/coder/completions'
    };

    // Send message function
    function sendMessage() {
        const message = messageInput.value.trim();

        if (!message || isProcessing) return;

        // Set processing state
        isProcessing = true;

        // Display user message
        addMessage(message, 'user');

        // Clear input field
        messageInput.value = '';

        // Show typing indicator
        showTypingIndicator();

        // Verwende den verbesserten Web-Proxy für freie Modelle
        if (isFreeModel(activeModel)) {
            console.log(`Verwende Web-Proxy für ${activeModel}`);

            // Stellen sicher, dass der Proxy verfügbar ist
            if (!iframeProxy) {
                console.log("Proxy noch nicht verfügbar, warte kurz...");
                setTimeout(() => {
                    if (window.proxyInstance) {
                        iframeProxy = window.proxyInstance;
                        continueWithProxy(message);
                    } else {
                        addSystemMessage("Proxy-Modul nicht verfügbar. Nutze Server-API direkt.");
                        sendMessageToServer(message);
                    }
                }, 500);
                return;
            }

            continueWithProxy(message);
        } else {
            // Premium-Modelle verwenden weiterhin die Server-API
            sendMessageToServer(message);
        }
    }

    // Maximale Versuche und Versuchszähler
    let proxyAttemptCounter = 0;
    const MAX_PROXY_ATTEMPTS = 2;

    // Fortsetzung der Nachrichtenverarbeitung mit dem Proxy
    function continueWithProxy(message) {
        // Prüfen, ob zu viele Versuche gemacht wurden
        if (proxyAttemptCounter >= MAX_PROXY_ATTEMPTS) {
            addSystemMessage("Web-Proxy nach mehreren Versuchen fehlgeschlagen, verwende direkt die Server-API...");
            sendMessageToServer(message);
            proxyAttemptCounter = 0; // Zurücksetzen für nächste Nachricht
            return;
        }

        proxyAttemptCounter++;

        // Bereite Payload für die API-Anfrage vor
        let payload = {};
        const endpoint = publicEndpoints[activeModel];

        if (activeModel.includes('claude')) {
            payload = {
                model: activeModel,
                prompt: `\n\nHuman: ${message}\n\nAssistant:`,
                max_tokens_to_sample: 1000,
                temperature: 0.7,
                stream: false // Streaming deaktivieren für bessere Stabilität
            };
        } else if (activeModel.includes('gpt')) {
            payload = {
                model: activeModel,
                messages: [{ role: "user", content: message }],
                max_tokens: 1000,
                temperature: 0.7,
                stream: false
            };
        } else {
            // Generisches Format für andere Modelle
            payload = {
                model: activeModel,
                message: message,
                max_tokens: 1000,
                stream: false
            };
        }

        // Timeout für den gesamten Proxy-Versuch
        const proxyTimeout = setTimeout(() => {
            // Wenn dieser Timeout ausgelöst wird, wurde die Antwort nicht rechtzeitig empfangen
            if (isProcessing) {
                handleProxyResponse(`Timeout beim Warten auf Antwort vom ${activeModel}-Proxy.`);
            }
        }, 12000); // 12 Sekunden Gesamttimeout

        // Versuche direkte Web-API-Anfrage über CORS-Proxy
        if (endpoint) {
            addSystemMessage(`Versuche direkte Anfrage an ${activeModel} über Web-Proxy (Versuch ${proxyAttemptCounter})...`);
            iframeProxy.makeProxyRequest(endpoint, payload, (response) => {
                clearTimeout(proxyTimeout);
                handleProxyResponse(response);
            });
        } else {
            // Fallback auf iframe-Methode, wenn kein Endpunkt konfiguriert ist
            addSystemMessage(`Verwende iframe-Proxy für ${activeModel} (Versuch ${proxyAttemptCounter})...`);
            iframeProxy.requestModelResponse(activeModel, message, (response) => {
                clearTimeout(proxyTimeout);
                handleProxyResponse(response);
            });
        }
    }

    // Handler für Proxy-Antworten
    function handleProxyResponse(response) {
        // Hide typing indicator
        hideTypingIndicator();

        if (response.includes("Fehler") || response.includes("Timeout") || response.includes("keine Antwort")) {
            // Bei Proxy-Fehler: entweder noch einmal versuchen oder an Server weiterleiten
            if (proxyAttemptCounter < MAX_PROXY_ATTEMPTS) {
                addSystemMessage(`Web-Proxy fehlgeschlagen, versuche alternativen Proxy (Versuch ${proxyAttemptCounter + 1})...`);
                continueWithProxy(messageInput.value.trim() || getLastUserMessage());
            } else {
                addSystemMessage("Web-Proxy nach mehreren Versuchen fehlgeschlagen, verwende Server-API...");
                sendMessageToServer(messageInput.value.trim() || getLastUserMessage());
                proxyAttemptCounter = 0; // Zurücksetzen für nächste Nachricht
            }
        } else {
            // Display bot response from proxy
            addMessage(response, 'bot');
            isProcessing = false;
            proxyAttemptCounter = 0; // Erfolgreicher Versuch - Counter zurücksetzen
        }
    }

    // Hilfsfunktion, um die letzte Benutzeranfrage zu erhalten
    function getLastUserMessage() {
        if (!chatMessages) return "";
        const userMessages = chatMessages.querySelectorAll('.message-user .message-content');
        if (userMessages.length > 0) {
            return userMessages[userMessages.length - 1].textContent;
        }
        return "";
    }

    // Funktion zum Senden der Nachricht an den Server (für Premium-Modelle oder Fallback)
    function sendMessageToServer(message) {
        // AJAX request to send message
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `message=${encodeURIComponent(message)}`
        })
        .then(response => response.json())
        .then(data => {
            // Hide typing indicator
            hideTypingIndicator();

            if (data.success) {
                // Display bot response
                addMessage(data.response, 'bot');
            } else {
                // Display error message
                addSystemMessage(`Fehler: ${data.error}`);
            }

            // Reset processing state
            isProcessing = false;
        })
        .catch(error => {
            console.error('Fehler:', error);
            hideTypingIndicator();
            addSystemMessage('Fehler bei der Kommunikation mit dem Server.');
            isProcessing = false;
        });
    }

    // Add message to chat
    function addMessage(content, sender) {
        if (!chatMessages) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message message-${sender}`;

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';

        // Basic markdown formatting for code
        const formattedContent = formatMessage(content);
        messageContent.innerHTML = formattedContent;

        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);

        // Scroll to latest messages
        scrollToBottom();
    }

    // Add system message (notifications, errors, etc.)
    function addSystemMessage(content) {
        if (!chatMessages) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'system-message';
        messageDiv.textContent = content;

        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }

    // Format message with basic markdown
    function formatMessage(content) {
        // Format code blocks
        let formatted = content.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');

        // Format inline code
        formatted = formatted.replace(/`([^`]+)`/g, '<code>$1</code>');

        // Format links
        formatted = formatted.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');

        // Format line breaks
        formatted = formatted.replace(/\n/g, '<br>');

        return formatted;
    }

    // Show typing indicator
    function showTypingIndicator() {
        if (!chatMessages) return;
        
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message message-bot';
        typingDiv.id = 'typing-indicator';

        const typingContent = document.createElement('div');
        typingContent.className = 'message-content typing-indicator';
        typingContent.innerHTML = '<span></span><span></span><span></span>';

        typingDiv.appendChild(typingContent);
        chatMessages.appendChild(typingDiv);
        scrollToBottom();
    }

    // Hide typing indicator
    function hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    // Scroll chat to bottom
    function scrollToBottom() {
        if (!chatMessages) return;
        chatMessages.scrollTop = chatMessages.scrollHeight;
        // Stelle sicher, dass das Scroll-Verhalten auch auf Mobilgeräten funktioniert
        setTimeout(() => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 100);
        
        // Sicherstellen, dass das Eingabefeld immer sichtbar ist
        document.querySelector('.chat-input').style.display = 'flex';
    }

    // Initialize chat with welcome message
    function initializeChat() {
        if (!chatMessages) return;
        
        // Nur initialisieren, wenn der Chat leer ist
        if (chatMessages.children.length === 0) {
            addMessage('Hallo! Wie kann ich Ihnen helfen?', 'bot');
        }
    }

    // Funktion zur Einrichtung von Chat-Event-Listenern
    function setupChatEventListeners() {
        // Event listeners for message sending
        if (sendMessageBtn) {
            sendMessageBtn.addEventListener('click', sendMessage);
        }
    
        // Event listener for Enter key (with Shift+Enter for new line)
        if (messageInput) {
            messageInput.addEventListener('keydown', function(event) {
                if (event.key === 'Enter' && !event.shiftKey) {
                    event.preventDefault();
                    sendMessage();
                }
            });
    
            // Adjust textarea height as content grows
            messageInput.addEventListener('input', function() {
                this.style.height = 'auto';
                const maxHeight = 150; // Maximum height in pixels
    
                if (this.scrollHeight <= maxHeight) {
                    this.style.height = this.scrollHeight + 'px';
                } else {
                    this.style.height = maxHeight + 'px';
                }
            });
        }
    }
    
    // Initiale Einrichtung der Event-Listener versuchen
    if (sendMessageBtn && messageInput) {
        setupChatEventListeners();
    }

    // Handle connection errors
    window.addEventListener('online', function() {
        addSystemMessage('Wieder online. Verbindung wiederhergestellt.');
    });

    window.addEventListener('offline', function() {
        addSystemMessage('Keine Internetverbindung. Bitte überprüfen Sie Ihre Verbindung.');
    });

    // API-Schlüssel sicher speichern
    document.getElementById('save-api-key-btn')?.addEventListener('click', function() {
        const service = document.getElementById('service-selector')?.value;
        const apiKey = document.getElementById('api-key-input')?.value;

        if (!apiKey) {
            alert('Bitte geben Sie einen API-Schlüssel ein.');
            return;
        }

        fetch('/save_api_key', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `service=${encodeURIComponent(service)}&api_key=${encodeURIComponent(apiKey)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Aktualisiere die Liste der gespeicherten Schlüssel
                const savedKeysList = document.getElementById('saved-keys-list');
                if (savedKeysList) {
                    // Prüfe, ob der Schlüssel bereits in der Liste ist
                    let keyExists = false;
                    for (const li of savedKeysList.children) {
                        if (li.textContent.startsWith(service + ':')) {
                            keyExists = true;
                            break;
                        }
                    }

                    if (!keyExists) {
                        const newKey = document.createElement('li');
                        newKey.textContent = `${service}: ********`;
                        savedKeysList.appendChild(newKey);
                    }
                }

                // Eingabefeld zurücksetzen
                if (document.getElementById('api-key-input')) {
                    document.getElementById('api-key-input').value = '';
                }

                alert('API-Schlüssel gespeichert!');
            } else if (data.error) {
                alert(data.error);
                if (data.error.includes('angemeldet')) {
                    setTimeout(() => {
                        window.location.href = '/auth/login';
                    }, 2000);
                }
            }
        })
        .catch(error => {
            console.error('Fehler beim Speichern des API-Schlüssels:', error);
            alert('Fehler beim Speichern des API-Schlüssels');
        });
    });
});
