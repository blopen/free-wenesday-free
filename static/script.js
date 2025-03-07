
document.addEventListener('DOMContentLoaded', function() {
    // API-Schlüssel speichern
    const saveKeyButtons = document.querySelectorAll('.save-key');
    saveKeyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const service = this.dataset.service;
            const inputId = `${service}-key`;
            const apiKey = document.getElementById(inputId).value;
            
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
                    alert(`${service.charAt(0).toUpperCase() + service.slice(1)} API-Schlüssel gespeichert!`);
                }
            });
        });
    });
    
    // Modell wechseln
    const modelItems = document.querySelectorAll('.model-item');
    modelItems.forEach(item => {
        item.addEventListener('click', function() {
            const model = this.dataset.model;
            
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
                    // Aktives Modell aktualisieren
                    document.querySelectorAll('.model-item').forEach(m => m.classList.remove('active'));
                    this.classList.add('active');
                    document.getElementById('active-model').textContent = model;
                }
            });
        });
    });
    
    // Chat-Funktionalität
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-message');
    const sendButton = document.getElementById('send-button');
    
    function addMessage(text, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        
        // Benutzer-Nachricht anzeigen
        addMessage(message, true);
        userInput.value = '';
        
        // Nachricht an den Server senden
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
                addMessage(data.response, false);
            } else {
                // Fehlermeldung anzeigen
                addMessage(`Fehler: ${data.error}`, false);
            }
        })
        .catch(error => {
            addMessage('Fehler bei der Kommunikation mit dem Server.', false);
        });
    }
    
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
});
