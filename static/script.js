const input = document.getElementById("message-input");
const chatBox = document.getElementById("chat-box");

async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, "user");
    input.value = "";
    showTyping();

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message})
        });

        const data = await response.json();
        removeTyping();

        addMessage(
            data.success ? data.response : "Sorry, something went wrong.",
            "bot",
            data.timestamp
        );
    } catch (error) {
        removeTyping();
        addMessage("Unable to connect to the server. Please try again.", "bot");
        console.error(error);
    }
}

function sendQuickMessage(message) {
    input.value = message;
    sendMessage();
}

function addMessage(message, sender, time = null) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}-message`;

    const avatar = sender === "bot" ? "♥" : "You";
    const senderName = sender === "bot" ? "Elder Care Assistant" : "You";
    const messageTime = time || new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });

    messageDiv.innerHTML = `
        <div class="avatar">${avatar}</div>
        <div class="message-content">
            <div class="sender">${senderName}</div>
            <div class="bubble">${escapeHTML(message)}</div>
            <div class="time">${messageTime}</div>
        </div>
    `;

    chatBox.appendChild(messageDiv);
    scrollToBottom();
}

function showTyping() {
    const typing = document.createElement("div");
    typing.id = "typing-indicator";
    typing.className = "message bot-message";
    typing.innerHTML = `
        <div class="avatar">♥</div>
        <div class="message-content">
            <div class="sender">Elder Care Assistant</div>
            <div class="bubble">Typing...</div>
        </div>
    `;
    chatBox.appendChild(typing);
    scrollToBottom();
}

function removeTyping() {
    const typing = document.getElementById("typing-indicator");
    if (typing) typing.remove();
}

function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
}

function escapeHTML(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

input.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});
s
