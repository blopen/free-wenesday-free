
document.addEventListener('DOMContentLoaded', function() {
    // DOM-Elemente
    const modelItems = document.querySelectorAll('.model-item');
    const saveApiKeyBtn = document.getElementById('save-api-key');
    const apiServiceSelect = document.getElementById('api-service');
    const apiKeyInput = document.getElementById('api-key-input');
    const chatMessages = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendMessageBtn = document.getElementById('send-message');
    
    // Aktuelles Modell auswählen
    let activeModel = document.querySelector('.model-item.active').dataset.model;
    
    // Event-Listener für Modellauswahl
    modelItems.forEach(item => {
        item.addEventListener('click', function() {
            // Aktives Modell entfernen
            document.querySelector('.model-item.active').classList.remove('active');
            // Neues Modell aktivieren
            this.classList.add('active');
            activeModel = this.dataset.model;
            
            // AJAX-Anfrage zum Setzen des aktiven Modells
            fetch('/set_active_model', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `model=${activeModel}`
            })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    alert('Fehler beim Setzen des Modells: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Fehler:', error);
            });
        });
    });
    
    // Event-Listener für API-Schlüssel speichern
    saveApiKeyBtn.addEventListener('click', function() {
        const service = apiServiceSelect.value;
        const apiKey = apiKeyInput.value;
        
        if (!apiKey) {
            alert('Bitte geben Sie einen API-Schlüssel ein.');
            return;
        }
        
        // AJAX-Anfrage zum Speichern des API-Schlüssels
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
                alert('API-Schlüssel erfolgreich gespeichert!');
                apiKeyInput.value = '';
                
                // Aktualisieren der angezeigten Schlüssel ohne Seitenneuladen
                const savedKeysList = document.querySelector('.saved-api-keys ul');
                let keyExists = false;
                
                // Überprüfen, ob der Dienst bereits in der Liste vorhanden ist
                const listItems = savedKeysList.querySelectorAll('li');
                listItems.forEach(item => {
                    if (item.textContent.startsWith(service)) {
                        keyExists = true;
                    }
                });
                
                // Wenn der Dienst nicht vorhanden ist, fügen wir ihn hinzu
                if (!keyExists) {
                    const newKeyItem = document.createElement('li');
                    newKeyItem.textContent = `${service}: ********`;
                    savedKeysList.appendChild(newKeyItem);
                }
            } else {
                alert('Fehler beim Speichern des API-Schlüssels.');
            }
        })
        .catch(error => {
            console.error('Fehler:', error);
        });
    });
    
    // Nachricht senden
    function sendMessage() {
        const message = messageInput.value.trim();
        
        if (!message) return;
        
        // Benutzernachricht anzeigen
        addMessage(message, 'user');
        
        // Textfeld leeren
        messageInput.value = '';
        
        // AJAX-Anfrage zum Senden der Nachricht
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `message=${encodeURIComponent(message)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Bot-Antwort anzeigen
                addMessage(data.response, 'bot');
            } else {
                // Fehlermeldung anzeigen
                addMessage('Fehler: ' + data.error, 'bot error');
            }
        })
        .catch(error => {
            console.error('Fehler:', error);
            addMessage('Fehler bei der Kommunikation mit dem Server.', 'bot error');
        });
    }
    
    // Nachricht zum Chat hinzufügen
    function addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message message-${sender}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;
        
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // Zum neuesten Nachrichten scrollen
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Event-Listener für Senden-Button
    sendMessageBtn.addEventListener('click', sendMessage);
    
    // Event-Listener für Enter-Taste (mit Shift+Enter für neue Zeile)
    messageInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });
    
    // Füge eine Begrüßungsnachricht hinzu
    addMessage('Hallo! Wie kann ich Ihnen helfen?', 'bot');
});
// Funktion zum Laden und Initialisieren der Chat-UI
document.addEventListener('DOMContentLoaded', function() {
    // Model-Auswahl-Event-Listener
    const modelButtons = document.querySelectorAll('.model-button');
    modelButtons.forEach(button => {
        button.addEventListener('click', function() {
            const model = this.getAttribute('data-model');
            fetch('/set_active_model', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `model=${model}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Aktives Modell hervorheben
                    modelButtons.forEach(btn => btn.classList.remove('active'));
                    this.classList.add('active');

                    // Wenn es Claude-free ist, zeige einen Hinweis an
                    const messageArea = document.getElementById('chat-messages');
                    if (model === 'claude-free') {
                        const infoMessage = document.createElement('div');
                        infoMessage.className = 'system-message';
                        infoMessage.innerHTML = '<p>Du nutzt jetzt Claude ohne API-Schlüssel! Diese Version hat eingeschränkte Funktionalität.</p>';
                        messageArea.appendChild(infoMessage);
                        messageArea.scrollTop = messageArea.scrollHeight;
                    }
                }
            });
        });
    });

    // API-Schlüssel-Speicher-Event-Listener
    document.getElementById('save-api-key').addEventListener('click', function() {
        const service = document.getElementById('api-service').value;
        const apiKey = document.getElementById('api-key-input').value;
        
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
                alert('API-Schlüssel gespeichert!');
                location.reload();
            }
        });
    });

    // Chat-Formular-Event-Listener
    document.getElementById('chat-form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const messageInput = document.getElementById('message-input');
        const message = messageInput.value.trim();
        
        if (message) {
            addMessageToChat('user', message);
            messageInput.value = '';
            
            // Lade-Animation anzeigen
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'loading-message';
            loadingDiv.innerHTML = '<p>AI denkt nach...</p>';
            document.getElementById('chat-messages').appendChild(loadingDiv);
            
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `message=${encodeURIComponent(message)}`
            })
            .then(response => response.json())
            .then(data => {
                // Lade-Animation entfernen
                document.querySelector('.loading-message').remove();
                
                if (data.success) {
                    addMessageToChat('assistant', data.response);
                } else {
                    addMessageToChat('system', `Fehler: ${data.error}`);
                }
            });
        }
    });
    
    // Funktion zum Hinzufügen von Nachrichten zur Chat-UI
    function addMessageToChat(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `${role}-message`;
        
        // Einfache Markdown-Unterstützung für Code-Blöcke
        content = content.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
        
        messageDiv.innerHTML = `<p>${content}</p>`;
        document.getElementById('chat-messages').appendChild(messageDiv);
        
        // Zum Ende scrollen
        const chatMessages = document.getElementById('chat-messages');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
