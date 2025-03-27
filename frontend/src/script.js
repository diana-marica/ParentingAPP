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

async function sendMessage() {
    try {
        const userInputElement = document.getElementById("userInput");
        if (!userInputElement) {
            throw new Error("Nu s-a găsit elementul de input!");
        }

        const userInput = userInputElement.value.trim();
        if (!userInput) return;

        const chatbox = document.getElementById("chatbox");
        if (!chatbox) {
            throw new Error("Nu s-a găsit caseta de chat!");
        }

        // User message
        const userMessage = document.createElement("div");
        userMessage.classList.add("message", "user-message");
        userMessage.textContent = `Tu: ${userInput}`;
        chatbox.appendChild(userMessage);

        // Clear input
        userInputElement.value = "";

        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query: userInput })
        });

        if (!response.ok) {
            throw new Error(`Eroare HTTP! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("✅ AI Response:", data);

        const reply = data.response || "⚠️ Mimi nu a răspuns.";
        const aiMessage = document.createElement("div");
        aiMessage.classList.add("message", "ai-message");
        aiMessage.innerHTML = `Mimi: ${reply}`;
        chatbox.appendChild(aiMessage);

        // Scroll to bottom
        chatbox.scrollTop = chatbox.scrollHeight;

    } catch (error) {
        console.error("❌ Eroare completă:", error);
        
        const errorDiv = document.createElement('div');
        errorDiv.style.color = 'red';
        errorDiv.classList.add("message", "ai-message");
        errorDiv.innerHTML = `<strong>Eroare:</strong> ${error.message}`;
        
        const chatbox = document.getElementById("chatbox");
        if (chatbox) {
            chatbox.appendChild(errorDiv);
        } else {
            document.body.appendChild(errorDiv);
        }
    }
}

// Ensure DOM is fully loaded before adding event listeners
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM fully loaded and parsed");
    
    const userInputElement = document.getElementById("userInput");
    if (userInputElement) {
        userInputElement.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                sendMessage();
            }
        });
    } else {
        console.error("Nu s-a găsit elementul de input!");
    }
});

async function resetMemory() {
    try {
        const response = await fetch("http://127.0.0.1:8000/reset", {
            method: "GET"
        });

        if (!response.ok) {
            throw new Error(`Eroare HTTP! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Reset response:", data);

        const chatbox = document.getElementById("chatbox");
        if (chatbox) {
            chatbox.innerHTML = `<div class="message ai-message">Mimi: ${data.message}</div>`;
        }
    } catch (error) {
        console.error("Eroare la resetare:", error);
        const chatbox = document.getElementById("chatbox");
        if (chatbox) {
            chatbox.innerHTML = `<div class="message ai-message" style="color:red;">Eroare la resetare: ${error.message}</div>`;
        }
    }
}

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