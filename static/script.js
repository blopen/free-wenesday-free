
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
