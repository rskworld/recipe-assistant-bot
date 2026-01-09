/**
 * Recipe Assistant Bot - Chat JavaScript
 * Author: RSK World (https://rskworld.in)
 * Founder: Molla Samser
 * Designer & Tester: Rima Khatun
 * Contact: help@rskworld.in, +91 93305 39277
 * Year: 2026
 */

class RecipeChatBot {
    constructor() {
        this.chatContainer = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.quickSuggestions = document.querySelectorAll('.quick-suggestion');
        this.isListening = false;
        this.recognition = null;
        
        this.init();
    }
    
    init() {
        // Event listeners
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        // Quick suggestion buttons
        this.quickSuggestions.forEach(button => {
            button.addEventListener('click', () => {
                const message = button.getAttribute('data-message');
                this.messageInput.value = message;
                this.sendMessage();
            });
        });
        
        // Initialize voice input if supported
        this.initVoiceInput();
        
        // Focus on input
        this.messageInput.focus();
    }
    
    initVoiceInput() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';
            
            this.recognition.onstart = () => {
                this.isListening = true;
                this.updateVoiceButton();
            };
            
            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                this.messageInput.value = transcript;
                this.isListening = false;
                this.updateVoiceButton();
            };
            
            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.isListening = false;
                this.updateVoiceButton();
                this.showError('Voice recognition failed. Please try again.');
            };
            
            this.recognition.onend = () => {
                this.isListening = false;
                this.updateVoiceButton();
            };
            
            // Add voice button to input group
            this.addVoiceButton();
        }
    }
    
    addVoiceButton() {
        const voiceButton = document.createElement('button');
        voiceButton.className = 'btn btn-outline-secondary';
        voiceButton.type = 'button';
        voiceButton.id = 'voiceButton';
        voiceButton.innerHTML = '<i class="fas fa-microphone"></i>';
        voiceButton.title = 'Voice Input (Click to speak)';
        
        voiceButton.addEventListener('click', () => this.toggleVoiceInput());
        
        const inputGroup = this.messageInput.parentElement;
        inputGroup.insertBefore(voiceButton, this.sendButton);
    }
    
    toggleVoiceInput() {
        if (!this.recognition) {
            this.showError('Voice input is not supported in your browser.');
            return;
        }
        
        if (this.isListening) {
            this.recognition.stop();
        } else {
            this.recognition.start();
        }
    }
    
    updateVoiceButton() {
        const voiceButton = document.getElementById('voiceButton');
        if (voiceButton) {
            if (this.isListening) {
                voiceButton.innerHTML = '<i class="fas fa-microphone-slash"></i>';
                voiceButton.className = 'btn btn-danger';
                voiceButton.title = 'Stop Recording';
            } else {
                voiceButton.innerHTML = '<i class="fas fa-microphone"></i>';
                voiceButton.className = 'btn btn-outline-secondary';
                voiceButton.title = 'Voice Input (Click to speak)';
            }
        }
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message) {
            this.showError('Please enter a message');
            return;
        }
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input
        this.messageInput.value = '';
        
        // Show loading indicator
        this.showLoading();
        
        try {
            // Send message to backend
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            
            // Remove loading indicator
            this.removeLoading();
            
            if (data.status === 'success') {
                this.addMessage(data.response, 'bot');
            } else {
                this.showError(data.error || 'An error occurred');
            }
            
        } catch (error) {
            this.removeLoading();
            this.showError('Network error. Please try again.');
            console.error('Chat error:', error);
        }
    }
    
    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const senderLabel = sender === 'bot' ? 'Recipe Bot:' : 'You:';
        messageContent.innerHTML = `<strong>${senderLabel}</strong> ${this.formatMessage(content)}`;
        
        messageDiv.appendChild(messageContent);
        this.chatContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        this.scrollToBottom();
    }
    
    formatMessage(content) {
        // Convert newlines to <br>
        let formatted = content.replace(/\n/g, '<br>');
        
        // Convert bullet points to proper HTML lists
        formatted = formatted.replace(/•\s([^•\n]+)/g, '<li>$1</li>');
        formatted = formatted.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
        
        // Convert numbered lists
        formatted = formatted.replace(/(\d+\.\s)/g, '<br>$1');
        
        return formatted;
    }
    
    showLoading() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message bot-message loading-message';
        loadingDiv.innerHTML = `
            <div class="message-content">
                <strong>Recipe Bot:</strong> 
                <span class="loading-spinner"></span> Thinking...
            </div>
        `;
        this.chatContainer.appendChild(loadingDiv);
        this.scrollToBottom();
    }
    
    removeLoading() {
        const loadingMessage = this.chatContainer.querySelector('.loading-message');
        if (loadingMessage) {
            loadingMessage.remove();
        }
    }
    
    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'message bot-message error-message';
        errorDiv.style.backgroundColor = '#f8d7da';
        errorDiv.style.borderLeftColor = '#dc3545';
        errorDiv.innerHTML = `
            <div class="message-content">
                <strong>Recipe Bot:</strong> 
                <span style="color: #721c24;">${message}</span>
            </div>
        `;
        this.chatContainer.appendChild(errorDiv);
        this.scrollToBottom();
    }
    
    scrollToBottom() {
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }
}

// Additional utility functions
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 1050; max-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.recipeChatBot = new RecipeChatBot();
    
    // Add some helpful keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + K to focus input
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            document.getElementById('messageInput').focus();
        }
        
        // Escape to clear input
        if (e.key === 'Escape') {
            document.getElementById('messageInput').value = '';
        }
    });
    
    // Show welcome notification
    setTimeout(() => {
        showNotification('Welcome to Recipe Assistant Bot! Ask me about recipes, ingredients, or cooking tips.', 'success');
    }, 1000);
});

// Error handling for network issues
window.addEventListener('online', () => {
    showNotification('Connection restored!', 'success');
});

window.addEventListener('offline', () => {
    showNotification('Connection lost. Some features may not work.', 'warning');
});
