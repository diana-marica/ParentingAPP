// Enhanced error logging
window.addEventListener('error', function(event) {
    const errorDiv = document.createElement('div');
    errorDiv.style.color = 'red';
    errorDiv.style.backgroundColor = '#ffeeee';
    errorDiv.style.padding = '10px';
    errorDiv.style.position = 'fixed';
    errorDiv.style.top = '0';
    errorDiv.style.left = '0';
    errorDiv.style.width = '100%';
    errorDiv.style.zIndex = '1000';
    errorDiv.innerHTML = `
        <strong>Eroare critică:</strong> 
        ${event.message} 
        la linia ${event.lineno}, coloana ${event.colno}
        <br>Sursă: ${event.filename}
    `;
    document.body.insertBefore(errorDiv, document.body.firstChild);
    console.error('Eroare globală:', event);
});

console.log("✅ script.js loaded");

// DOM Elements
const chatbox = document.getElementById('chatbox');
const userInput = document.getElementById('userInput');
const modelSelector = document.querySelector('.model-selector');
const newChatBtn = document.querySelector('.new-chat-btn');
const navLinks = document.querySelectorAll('.nav-link');
const actionBtns = document.querySelectorAll('.action-btn');
const langBtns = document.querySelectorAll('.lang-btn');

// State
let chatHistory = [];
let isProcessing = false;
let currentLang = 'en'; // Default language

// Language handling
function setLanguage(lang) {
    currentLang = lang;
    document.documentElement.setAttribute('lang', lang);
    
    // Update active state of language buttons
    langBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === lang);
    });
    
    // Update all translatable elements
    document.querySelectorAll('[data-translate]').forEach(element => {
        const key = element.dataset.translate;
        if (element.tagName === 'INPUT') {
            element.placeholder = translations[lang][key];
        } else {
            element.textContent = translations[lang][key];
        }
    });

    // Save language preference
    localStorage.setItem('preferred-language', lang);
}

// Event Listeners
userInput.addEventListener('keypress', async (e) => {
    if (e.key === 'Enter' && !isProcessing) {
        const message = userInput.value.trim();
        if (message) {
            await sendMessage(message);
        }
    }
});

newChatBtn.addEventListener('click', () => {
    resetChat();
});

navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        navLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
    });
});

actionBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
        const action = e.currentTarget.getAttribute('data-action');
        handleAction(action);
    });
});

langBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        setLanguage(btn.dataset.lang);
    });
});

// Functions
async function sendMessage(message) {
    if (isProcessing) return;
    isProcessing = true;

    // Add user message to UI
    appendMessage('user', message);
    userInput.value = '';

    try {
        // Show typing indicator
        const typingIndicator = appendTypingIndicator();

        // Send to backend with language preference
        const response = await fetch('http://localhost:8000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept-Language': currentLang
            },
            body: JSON.stringify({ message })
        });

        if (!response.ok) throw new Error(translations[currentLang].errorMessage);
        
        const data = await response.json();
        
        // Remove typing indicator and add AI response
        typingIndicator.remove();
        appendMessage('ai', data.response);

        // Save to chat history
        chatHistory.push({ role: 'user', content: message });
        chatHistory.push({ role: 'assistant', content: data.response });
    } catch (error) {
        console.error('Error:', error);
        appendErrorMessage(translations[currentLang].errorMessage);
    } finally {
        isProcessing = false;
    }
}

function appendMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;
    
    const iconDiv = document.createElement('div');
    iconDiv.className = 'message-icon';
    iconDiv.innerHTML = role === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Configure marked options for better rendering
    marked.setOptions({
        gfm: true, // GitHub Flavored Markdown
        breaks: true, // Add <br> on single line breaks
        headerIds: false, // Don't add ids to headers
        mangle: false, // Don't escape HTML
        smartLists: true, // Use smarter list behavior
        smartypants: true, // Use smart punctuation
    });
    
    // Use marked to render markdown for AI responses
    if (role === 'assistant') {
        // Clean up the content
        let processedContent = content
            // Ensure proper spacing around emojis
            .replace(/([^\s])([🎉🤝💖🔍🌟])/g, '$1 $2')
            .replace(/([🎉🤝💖🔍🌟])([^\s])/g, '$1 $2')
            // Add proper spacing after list markers
            .replace(/^(\d+\.) (?=\w)/gm, '$1  ')
            .replace(/^- (?=\w)/gm, '-  ')
            // Ensure proper spacing around headers
            .replace(/###(?=\w)/g, '### ')
            // Add proper spacing around strong markers
            .replace(/\*\*(?=\w)/g, '** ')
            .replace(/(?<=\w)\*\*/g, ' **');
        
        // Render markdown
        contentDiv.innerHTML = marked.parse(processedContent);
        
        // Add target="_blank" to all links
        contentDiv.querySelectorAll('a').forEach(link => {
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
        });

        // Process emojis
        contentDiv.innerHTML = contentDiv.innerHTML.replace(
            /([🎉🤝💖🔍🌟])/g,
            '<span class="emoji">$1</span>'
        );
    } else {
        contentDiv.textContent = content;
    }
    
    messageDiv.appendChild(iconDiv);
    messageDiv.appendChild(contentDiv);
    chatbox.appendChild(messageDiv);
    
    // Scroll to bottom
    chatbox.scrollTop = chatbox.scrollHeight;
    
    // Highlight code blocks if any
    if (role === 'assistant') {
        contentDiv.querySelectorAll('pre code').forEach(block => {
            block.classList.add('highlight');
        });
    }
}

function appendTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'message ai-message typing';
    indicator.innerHTML = `
        <div class="message-icon">
            <i class="fas fa-robot"></i>
        </div>
        <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;
    chatbox.appendChild(indicator);
    chatbox.scrollTop = chatbox.scrollHeight;
    return indicator;
}

function appendErrorMessage(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'message error-message';
    errorDiv.textContent = message;
    chatbox.appendChild(errorDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function resetChat() {
    chatHistory = [];
    chatbox.innerHTML = '';
    userInput.value = '';
    
    // Add welcome message in current language
    const welcomeMessage = translations[currentLang].welcomeMessage;
    appendMessage('ai', welcomeMessage);
}

function handleAction(action) {
    switch(action) {
        case 'search':
            // Implement web search
            break;
        case 'deep-research':
            // Implement deep research
            break;
        case 'upload':
            // Implement file upload
            break;
        default:
            console.log('Unknown action:', action);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Load preferred language from localStorage or use browser language
    const savedLang = localStorage.getItem('preferred-language');
    const browserLang = navigator.language.startsWith('ro') ? 'ro' : 'en';
    setLanguage(savedLang || browserLang);
    
    resetChat();
});

// Global error logging
window.onerror = function(message, source, lineno, colno, error) {
    console.error('Global error:', {
        message, 
        source, 
        lineno, 
        colno, 
        error
    });
    return false;
};