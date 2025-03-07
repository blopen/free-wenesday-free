document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const modelItems = document.querySelectorAll('.model-item');
    const saveApiKeyBtn = document.getElementById('save-api-key');
    const apiServiceSelect = document.getElementById('api-service');
    const apiKeyInput = document.getElementById('api-key-input');
    const chatMessages = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendMessageBtn = document.getElementById('send-message');
    const adminLoginBtn = document.getElementById('admin-login-btn');

    // Admin Login Funktionalität
    if (adminLoginBtn) {
        adminLoginBtn.addEventListener('click', function() {
            // Simuliere Admin-Login
            fetch('/admin/login_as_admin', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    addSystemMessage('Als Admin angemeldet! Sie werden zur Admin-Seite weitergeleitet...');
                    setTimeout(() => {
                        window.location.href = '/admin';
                    }, 1500);
                } else {
                    addSystemMessage(`Fehler beim Login: ${data.error}`);
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

    // Initialize chat history from session if available
    initializeChat();

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

    // Event listener for API key saving
    saveApiKeyBtn.addEventListener('click', function() {
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
            } else {
                addSystemMessage('Fehler beim Speichern des API-Schlüssels.');
            }
        })
        .catch(error => {
            console.error('Fehler:', error);
            addSystemMessage('Fehler bei der Kommunikation mit dem Server.');
        });
    });

    // Erstellen der iframe-Proxy-Instanz und stellen sicher, dass es nur eine gibt
    let iframeProxy; 
    try {
        // Prüfen, ob bereits eine Instanz existiert
        if (!window.proxyInstance) {
            window.proxyInstance = new ModelIframeProxy();
            console.log("Neue ModelIframeProxy-Instanz erstellt");
        }
        iframeProxy = window.proxyInstance;
    } catch (e) {
        console.error("Fehler beim Erstellen des ModelIframeProxy:", e);
        // Fallback-Objekt erstellen, falls die Klasse nicht verfügbar ist
        iframeProxy = {
            requestModelResponse: function(model, message, callback) {
                callback("Proxy-Modul nicht verfügbar. Versuche Server-Anfrage...");
            },
            makeProxyRequest: function(endpoint, payload, callback) {
                callback("Proxy-Modul nicht verfügbar. Versuche Server-Anfrage...");
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
            
            // Bereite Payload für die API-Anfrage vor
            let payload = {};
            const endpoint = publicEndpoints[activeModel];
            
            if (activeModel.includes('claude')) {
                payload = {
                    model: activeModel,
                    prompt: `\n\nHuman: ${message}\n\nAssistant:`,
                    max_tokens_to_sample: 1000,
                    temperature: 0.7
                };
            } else if (activeModel.includes('gpt')) {
                payload = {
                    model: activeModel,
                    messages: [{ role: "user", content: message }],
                    max_tokens: 1000,
                    temperature: 0.7
                };
            } else {
                // Generisches Format für andere Modelle
                payload = {
                    model: activeModel,
                    message: message,
                    max_tokens: 1000
                };
            }
            
            // Versuche direkte Web-API-Anfrage über CORS-Proxy
            if (endpoint) {
                addSystemMessage(`Versuche direkte Anfrage an ${activeModel} über Web-Proxy...`);
                iframeProxy.makeProxyRequest(endpoint, payload, handleProxyResponse);
            } else {
                // Fallback auf iframe-Methode, wenn kein Endpunkt konfiguriert ist
                addSystemMessage(`Verwende iframe-Proxy für ${activeModel}...`);
                iframeProxy.requestModelResponse(activeModel, message, handleProxyResponse);
            }
        } else {
            // Premium-Modelle verwenden weiterhin die Server-API
            sendMessageToServer(message);
        }
    }
    
    // Handler für Proxy-Antworten
    function handleProxyResponse(response) {
        // Hide typing indicator
        hideTypingIndicator();
        
        if (response.includes("Fehler") || response.includes("Timeout") || response.includes("simulierte Antwort")) {
            // Wenn der Proxy fehlschlägt, Fallback auf Server-Anfrage
            addSystemMessage("Web-Proxy fehlgeschlagen, verwende Server-API...");
            sendMessageToServer(messageInput.value.trim() || getLastUserMessage());
        } else {
            // Display bot response from proxy
            addMessage(response, 'bot');
            isProcessing = false;
        }
    }
    
    // Hilfsfunktion, um die letzte Benutzeranfrage zu erhalten
    function getLastUserMessage() {
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
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Initialize chat with welcome message
    function initializeChat() {
        addMessage('Hallo! Wie kann ich Ihnen helfen?', 'bot');
    }

    // Event listeners for message sending
    sendMessageBtn.addEventListener('click', sendMessage);

    // Event listener for Enter key (with Shift+Enter for new line)
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

    // Handle connection errors
    window.addEventListener('online', function() {
        addSystemMessage('Wieder online. Verbindung wiederhergestellt.');
    });

    window.addEventListener('offline', function() {
        addSystemMessage('Keine Internetverbindung. Bitte überprüfen Sie Ihre Verbindung.');
    });
});