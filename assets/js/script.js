class UniQuestChatbot {
    constructor() {
        this.apiUrl = 'http://localhost:5000';
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.typingIndicator = document.getElementById('typingIndicator');
        
        this.initializeEventListeners();
        this.showWelcomeMessage();
    }

    initializeEventListeners() {
        // Send message on button click
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        // Send message on Enter key press
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Quick action buttons
        document.querySelectorAll('.quick-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const query = btn.getAttribute('data-query');
                this.messageInput.value = query;
                this.sendMessage();
            });
        });

        // Auto-resize input
        this.messageInput.addEventListener('input', () => {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = this.messageInput.scrollHeight + 'px';
        });
    }

    showWelcomeMessage() {
        // Welcome message is already in HTML, so we just need to scroll to bottom
        this.scrollToBottom();
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;

        // Disable input while processing
        this.setInputState(false);
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input
        this.messageInput.value = '';
        this.messageInput.style.height = 'auto';
        
        // Show typing indicator
        this.showTypingIndicator();

        try {
            // Send request to backend
            const response = await this.callAPI(message);
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            // Add bot response to chat
            this.addMessage(response, 'bot');
            
        } catch (error) {
            // Hide typing indicator
            this.hideTypingIndicator();
            
            // Show error message
            this.addMessage(
                "Sorry, I'm having trouble connecting to my brain right now 🤖💭. Please make sure the backend server is running and try again!",
                'bot'
            );
            
            console.error('Error:', error);
        }

        // Re-enable input
        this.setInputState(true);
        this.messageInput.focus();
    }

    async callAPI(message) {
        const response = await fetch(`${this.apiUrl}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }

        return data.response;
    }

    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        if (sender === 'bot') {
            // Convert markdown-like formatting to HTML
            let formattedContent = content
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\n/g, '<br>')
                .replace(/(\d+)\.\s/g, '<br><strong>$1.</strong> ')
                .replace(/(📍|⭐|💰|🏫|📅|💼|🎭|🌏|🚀|🔬|⚽|🎉|👩‍🎓|🏢|🧑‍💻|🎓|📊)/g, '<span style="font-size: 1.1em;">$1</span>');
            
            messageContent.innerHTML = formattedContent;
        } else {
            messageContent.textContent = content;
        }
        
        messageDiv.appendChild(messageContent);
        this.chatMessages.appendChild(messageDiv);
        
        this.scrollToBottom();
    }

    showTypingIndicator() {
        this.typingIndicator.style.display = 'block';
    }

    hideTypingIndicator() {
        this.typingIndicator.style.display = 'none';
    }

    setInputState(enabled) {
        this.messageInput.disabled = !enabled;
        this.sendButton.disabled = !enabled;
        
        if (enabled) {
            this.sendButton.innerHTML = '<span class="send-text">Send</span><span class="send-icon">📤</span>';
        } else {
            this.sendButton.innerHTML = '<span class="send-text">Thinking...</span><span class="send-icon">🤔</span>';
        }
    }

    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }
}

// Sample responses for offline mode
const sampleResponses = {
    "Which college is the best?": "🎓 Based on ratings, the best college is National Institute of Technology Rourkela with a rating of 3.12/5.0.\n\n📍 Location: Rourkela, Odisha\n💰 Average Fees: ₹3.51 lakhs\n🏫 Type: Public/Government\n📅 Established: 2007",
    
    "What are the top 5 colleges?": "🏆 Here are the top 5 engineering colleges:\n\n1. **National Institute of Technology Rourkela** ⭐ 3.12\n2. **BMS College of Engineering** ⭐ 3.83\n3. **Institute of Chemical Technology** ⭐ 3.77\n4. **Jawaharlal Nehru University** ⭐ 3.77\n5. **University of Hyderabad** ⭐ 3.72",
    
    "Which college has less fee?": "💸 Most affordable colleges:\n\n1. **LD College of Engineering** - ₹0.10 lakhs\n2. **Jawaharlal Nehru University** - ₹0.18 lakhs\n3. **University of Calcutta** - ₹0.24 lakhs"
};

// Fallback function for offline mode
function handleOfflineMode(message) {
    return sampleResponses[message] || "I'm currently offline. Please start the backend server by running 'python backend/chatbot.py' and refresh the page.";
}

// Initialize the chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new UniQuestChatbot();
    
    // Add some interactive effects
    addInteractiveEffects();
});

function addInteractiveEffects() {
    // Add hover effects to messages
    document.addEventListener('mouseover', (e) => {
        if (e.target.closest('.message')) {
            e.target.closest('.message').style.transform = 'scale(1.02)';
        }
    });
    
    document.addEventListener('mouseout', (e) => {
        if (e.target.closest('.message')) {
            e.target.closest('.message').style.transform = 'scale(1)';
        }
    });
    
    // Add loading animation to send button
    const sendButton = document.getElementById('sendButton');
    sendButton.addEventListener('mousedown', () => {
        sendButton.style.transform = 'scale(0.95)';
    });
    
    sendButton.addEventListener('mouseup', () => {
        sendButton.style.transform = 'scale(1)';
    });
}

// Add some utility functions
function formatResponse(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>')
        .replace(/(📍|⭐|💰|🏫|📅)/g, '<span class="emoji">$1</span>');
}

// Console welcome message
console.log(`
🎓 UniQuest College Search Chatbot
=================================
Frontend loaded successfully!
Backend API: http://localhost:5000
Made with ❤️ for helping students find their perfect college
`);